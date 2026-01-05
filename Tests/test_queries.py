#!/usr/bin/env python3
# Python script to test all PromQL queries against a Prometheus server

import json
import requests
import sys
import urllib.parse
import time
from datetime import datetime
from queries import all_queries

# Load configuration
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    prometheus_url = config['prometheus_url']
    instance_name = config['instance_name']
except Exception as e:
    print(f"Error loading configuration: {e}")
    sys.exit(1)

# Initialize results log
log_file = 'results.log'
with open(log_file, 'w') as f:
    f.write(f"Query Test Results - {datetime.now()}\n\n")

def test_prom_query(name, query, expected_type):
    """Test a single PromQL query against the Prometheus server"""    # Replace instance placeholder
    query = query.replace('$INSTANCE', instance_name)
    query = query.replace('\\"', '"')  # Fix escaped quotes
    
    # URL encode the query
    encoded_query = urllib.parse.quote(query)
    url = f"{prometheus_url}/api/v1/query?query={encoded_query}"
    
    print(f"Testing: {name}")
    print(f"Query: {query}")
    
    try:
        # Make the API call
        response = requests.get(url)
        response_data = response.json()
        
        # Check if successful
        if response_data.get('status') == 'success':
            result_type = response_data.get('data', {}).get('resultType')
            print(f"Success! Result type: {result_type} (Expected: {expected_type})")
              # Check if the result type matches what we expect
            type_matches = result_type == expected_type
            if type_matches:
                result = "PASS"
            else:
                result = f"TYPE MISMATCH (got {result_type}, expected {expected_type})"
              # Check if we got any data
            data_count = 0
            if result_type == 'vector':
                data_count = len(response_data.get('data', {}).get('result', []))
            elif result_type == 'matrix':
                data_count = len(response_data.get('data', {}).get('result', []))
            elif result_type == 'scalar':
                data_count = 1
            
            if data_count == 0:
                # Only alert queries might legitimately return no data
                # These are the specific queries we know might return no data
                is_alert_query = "alert" in name.lower() or query.find(" > ") > 0
                
                if is_alert_query:
                    print("Note: Alert query executed successfully but returned no data")
                    print("This is normal for alert conditions that aren't currently triggered")
                    result = "PASS (ALERT NO DATA)"
                else:
                    print("Warning: Query returned no data - this might indicate an issue")
                    result = "NO DATA"
            else:
                print(f"Data points: {data_count}")
        else:
            error = response_data.get('error', 'Unknown error')
            print(f"Error: {error}")
            result = f"ERROR: {error}"
    except Exception as e:
        print(f"Exception: {e}")
        result = f"EXCEPTION: {str(e)}"
    
    # Log the result
    with open(log_file, 'a') as f:
        f.write(f"{name} - {result}\n")
        f.write(f"Query: {query}\n\n")
    
    print("-" * 40 + "\n")
    return result

# Test prerequisites
print("Testing prerequisites...")

# Check if we can reach the Prometheus server
try:
    test_url = f"{prometheus_url}/-/healthy"
    health_check = requests.get(test_url)
    if health_check.status_code == 200:
        print("✅ Prometheus server is reachable.")
    else:
        print(f"⚠️ Prometheus server returned status code {health_check.status_code}")
except Exception as e:
    print(f"❌ Cannot reach Prometheus server at {prometheus_url}")
    print(f"Error: {e}")
    print("Please check your configuration in config.json")
    sys.exit(1)

# Run tests for all queries
print("\n===== Testing All PromQL Queries =====\n")

results = {
    "passed": 0,
    "failed": 0,
    "total": len(all_queries)
}

for query_info in all_queries:
    result = test_prom_query(
        name=query_info['name'],
        query=query_info['query'],
        expected_type=query_info['expected_type']
    )
      # Consider test passed if it executed without error, even if it returns no data
    if "ERROR" not in result and "EXCEPTION" not in result and "MISMATCH" not in result:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Small delay to avoid overwhelming the server
    time.sleep(0.1)

# Summary
print("===== Test Summary =====")
print(f"Total queries: {results['total']}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
success_rate = round((results['passed'] / results['total']) * 100, 2)
print(f"Success rate: {success_rate}%")

# Log summary
with open(log_file, 'a') as f:
    f.write("===== Test Summary =====\n")
    f.write(f"Total queries: {results['total']}\n")
    f.write(f"Passed: {results['passed']}\n")
    f.write(f"Failed: {results['failed']}\n")
    f.write(f"Success rate: {success_rate}%\n")

print(f"\nResults saved to: {log_file}")
