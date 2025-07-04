#!/usr/bin/env pwsh
# PowerShell script to test all PromQL queries against a Prometheus server

# Add necessary assembly for URL encoding
Add-Type -AssemblyName System.Web

# Import configuration
$config = Get-Content -Path "$PSScriptRoot\config.json" -Raw | ConvertFrom-Json
$prometheusUrl = $config.prometheus_url
$instanceName = $config.instance_name

# Parse queries from the Python queries.py file instead of using PowerShell queries.ps1
# Use Python directly to parse the queries file and output JSON that PowerShell can read
function Get-PythonQueries {
    param (
        [string]$pythonFilePath
    )
    
    # Create a temporary Python script to convert queries to JSON
    $tempPythonScript = [System.IO.Path]::GetTempFileName() + ".py"
    
    Write-Host "Using Python to parse queries from: $pythonFilePath"
    Write-Host "Temporary script created at: $tempPythonScript"
    
    @'
import json
import sys
import os

# Use raw string for Windows path to avoid escape issues
sys.path.append(r'$PSScriptRoot')

try:
    from queries import *
    
    # Combine all lab queries
    all_queries = []
    lab_vars = [lab0_queries, lab1_queries, lab2_queries, lab3_queries, lab4_queries, 
                lab5_queries, lab6_queries, lab7_queries, lab8_queries, lab9_queries]
    
    for lab_query_list in lab_vars:
        all_queries.extend(lab_query_list)
    
    # Convert to PowerShell-friendly format
    powershell_queries = []
    for query in all_queries:
        # Replace $INSTANCE with $instanceName for PowerShell
        query_text = query["query"].replace("$INSTANCE", "$instanceName")
        
        # Add to PowerShell queries list
        powershell_queries.append({
            "Name": query["name"],
            "Query": query_text,
            "ExpectedType": query["expected_type"]
        })
    
    print(json.dumps(powershell_queries))
except Exception as e:
    print(json.dumps({"error": str(e)}))
'@ | Out-File -FilePath $tempPythonScript -Encoding utf8

    try {
        # Check if Python is available (try py first, then fall back to python)
        $pythonCommand = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } 
                        elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } 
                        else { $null }
        
        if (-not $pythonCommand) {
            throw "Python is not installed or not in your PATH. Please install Python 3.x to run this script."
        }
        
        # Execute the Python script and capture its JSON output
        Write-Host "Executing Python script with '$pythonCommand' to parse queries..."
        $pythonOutput = & $pythonCommand $tempPythonScript 2>&1
        
        # Check if there was an error
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error running Python script:" -ForegroundColor Red
            Write-Host $pythonOutput -ForegroundColor Red
            throw "Python script execution failed. See error above."
        }
        
        Write-Host "Python script executed successfully"
        
        # Convert the JSON output to PowerShell objects
        try {
            $queries = $pythonOutput | ConvertFrom-Json
            
            # Check if we got an error message
            if ($queries.error) {
                Write-Host "Python script returned an error:" -ForegroundColor Red
                Write-Host $queries.error -ForegroundColor Red
                throw "Python script returned an error: $($queries.error)"
            }
            
            Write-Host "Successfully parsed $($queries.Count) queries from Python"
            return $queries
        } catch {
            Write-Host "Error converting Python output to JSON:" -ForegroundColor Red
            Write-Host "Python output was:" -ForegroundColor Red
            Write-Host $pythonOutput -ForegroundColor Yellow
            throw "Failed to parse JSON from Python script output"
        }
    }
    catch {
        Write-Host "Error parsing Python queries: $_" -ForegroundColor Red
        Write-Host "Make sure Python 3.x is installed and available as 'py' or 'python' in your PATH." -ForegroundColor Yellow
        throw $_
    }
    finally {
        # Clean up temporary file
        if (Test-Path $tempPythonScript) {
            Remove-Item $tempPythonScript -Force
        }
    }
}

# Get all queries from the Python file
$allQueries = Get-PythonQueries -pythonFilePath "$PSScriptRoot\queries.py"

# Initialize results log
$logFile = "$PSScriptRoot\results.log"
"Query Test Results - $(Get-Date)" | Out-File -FilePath $logFile

Write-Host "Found $($allQueries.Count) queries to test."
"Found $($allQueries.Count) queries to test." | Out-File -FilePath $logFile -Append

# Function to test a single query
function Test-PromQuery {
    param (
        [string]$name,
        [string]$query,
        [string]$expectedType
    )
    
    # Replace $instanceName placeholder and unescape any escaped characters
    $query = $query.Replace('$instanceName', $instanceName)
    $query = $ExecutionContext.InvokeCommand.ExpandString($query)
    
    # URL encode the query
    $encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)
    $url = "$prometheusUrl/api/v1/query?query=$encodedQuery"
    
    Write-Host "Testing: $name"
    Write-Host "Query: $query"
    
    try {
        # Make the API call
        $response = Invoke-RestMethod -Uri $url -Method Get -ErrorAction Stop
        
        # Check if successful
        if ($response.status -eq "success") {
            $resultType = $response.data.resultType
            Write-Host "Success! Result type: $resultType (Expected: $expectedType)" -ForegroundColor Green
            
            # Check if the result type matches what we expect
            $typeMatches = $resultType -eq $expectedType
            if ($typeMatches) {
                $result = "PASS"
            } else {
                $result = "TYPE MISMATCH (got $resultType, expected $expectedType)"
            }
            
            # Check if we got any data
            $dataCount = 0
            if ($resultType -eq "vector") {
                $dataCount = $response.data.result.Length
            } elseif ($resultType -eq "matrix") {
                $dataCount = $response.data.result.Length
            } elseif ($resultType -eq "scalar") {
                $dataCount = 1
            }
            
            if ($dataCount -eq 0) {
                # Only alert queries might legitimately return no data
                $isAlertQuery = $name.ToLower().Contains("alert") -or $query.Contains(" > ")
                
                if ($isAlertQuery) {
                    Write-Host "Note: Alert query executed successfully but returned no data" -ForegroundColor Cyan
                    Write-Host "This is normal for alert conditions that aren't currently triggered" -ForegroundColor Cyan
                    $result = "PASS (ALERT NO DATA)"
                } else {
                    Write-Host "Warning: Query returned no data - this might indicate an issue" -ForegroundColor Yellow
                    $result = "NO DATA"
                }
            } else {
                Write-Host "Data points: $dataCount" -ForegroundColor Cyan
            }
        } else {
            Write-Host "Error: $($response.error)" -ForegroundColor Red
            $result = "ERROR: $($response.error)"
        }
    } catch {
        Write-Host "Exception: $_" -ForegroundColor Red
        $result = "EXCEPTION: $_"
    }
    
    # Log the result
    "$name - $result" | Out-File -FilePath $logFile -Append
    "Query: $query" | Out-File -FilePath $logFile -Append
    "" | Out-File -FilePath $logFile -Append
    
    return $result
}

# Test prerequisites
Write-Host "Testing prerequisites..."

# Check if we can reach the Prometheus server
try {
    $testUrl = "$prometheusUrl/-/healthy"
    Invoke-RestMethod -Uri $testUrl -Method Get -ErrorAction Stop
    Write-Host "✅ Prometheus server is reachable." -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot reach Prometheus server at $prometheusUrl" -ForegroundColor Red
    Write-Host "Please check your configuration in config.json" -ForegroundColor Yellow
    exit 1
}

# Run tests for all queries
Write-Host "`n===== Testing All PromQL Queries =====`n"

$results = @{
    Passed = 0
    Failed = 0
    Total = $allQueries.Count
}

# Check if we have queries
if ($allQueries.Count -eq 0) {
    Write-Host "No queries found. There might be an issue with parsing queries.py" -ForegroundColor Red
    exit 1
}

foreach ($query in $allQueries) {
    # Small delay to avoid overwhelming the server
    Start-Sleep -Milliseconds 100
    
    $result = Test-PromQuery -name $query.Name -query $query.Query -expectedType $query.ExpectedType
    
    # Consider test passed if it executed without error, even if it returns no data
    if (-not $result.Contains("ERROR") -and -not $result.Contains("EXCEPTION") -and -not $result.Contains("MISMATCH")) {
        $results.Passed++
    } else {
        $results.Failed++
    }
    
    Write-Host "----------------------------------------`n"
}

# Summary
Write-Host "===== Test Summary ====="
Write-Host "Total queries: $($results.Total)"
Write-Host "Passed: $($results.Passed)" -ForegroundColor Green
Write-Host "Failed: $($results.Failed)" -ForegroundColor Red
if ($results.Total -gt 0) {
    $successRate = [math]::Round(($results.Passed / $results.Total) * 100, 2)
    Write-Host "Success rate: $($successRate)%"
    # Log summary
    "===== Test Summary =====" | Out-File -FilePath $logFile -Append
    "Total queries: $($results.Total)" | Out-File -FilePath $logFile -Append
    "Passed: $($results.Passed)" | Out-File -FilePath $logFile -Append
    "Failed: $($results.Failed)" | Out-File -FilePath $logFile -Append
    "Success rate: $($successRate)%" | Out-File -FilePath $logFile -Append
} else {
    Write-Host "Success rate: N/A (no queries tested)" -ForegroundColor Yellow
    # Log summary
    "===== Test Summary =====" | Out-File -FilePath $logFile -Append
    "Total queries: 0" | Out-File -FilePath $logFile -Append
    "Passed: 0" | Out-File -FilePath $logFile -Append
    "Failed: 0" | Out-File -FilePath $logFile -Append
    "Success rate: N/A (no queries tested)" | Out-File -FilePath $logFile -Append
}

Write-Host "`nResults saved to: $logFile"
