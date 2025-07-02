#!/usr/bin/env pwsh
# PowerShell script to test all PromQL queries against a Prometheus server

# Add necessary assembly for URL encoding
Add-Type -AssemblyName System.Web

# Import configuration
$config = Get-Content -Path "$PSScriptRoot\config.json" -Raw | ConvertFrom-Json
$prometheusUrl = $config.prometheus_url
$instanceName = $config.instance_name

# Import queries from the queries.ps1 file - this approach doesn't use Export-ModuleMember
# Instead, we'll dot source the file and use the variables directly
. "$PSScriptRoot\queries.ps1"

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
    
    # Replace $instanceName placeholder
    $query = $query.Replace('$instanceName', $instanceName)
    
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
Write-Host "Success rate: $([math]::Round(($results.Passed / $results.Total) * 100, 2))%"

# Log summary
"===== Test Summary =====" | Out-File -FilePath $logFile -Append
"Total queries: $($results.Total)" | Out-File -FilePath $logFile -Append
"Passed: $($results.Passed)" | Out-File -FilePath $logFile -Append
"Failed: $($results.Failed)" | Out-File -FilePath $logFile -Append
"Success rate: $([math]::Round(($results.Passed / $results.Total) * 100, 2))%" | Out-File -FilePath $logFile -Append

Write-Host "`nResults saved to: $logFile"
