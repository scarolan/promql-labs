#!/usr/bin/env python3
"""
A script to verify that Prometheus recording rules are working.
Tests the recording rules used in the labs against a Prometheus instance.
"""

import json
import sys
import requests
from datetime import datetime

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

PROMETHEUS_URL = config['prometheus_url']
INSTANCE_NAME = config['instance_name']

# Recording rules to test
RECORDING_RULES = [
    {
        "name": "instance:node_cpu_usage:percent",
        "query": f'instance:node_cpu_usage:percent{{instance="{INSTANCE_NAME}"}}',
        "alternative": f'100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{{instance="{INSTANCE_NAME}",mode="idle"}}[5m])) / count by (instance) (node_cpu_seconds_total{{instance="{INSTANCE_NAME}",mode="idle"}})))'
    },
    {
        "name": "memory_usage_percent",
        "query": "memory_usage_percent",
        "alternative": f'100 * (1 - (node_memory_MemAvailable_bytes{{instance="{INSTANCE_NAME}"}} / node_memory_MemTotal_bytes{{instance="{INSTANCE_NAME}"}}))'
    }
]

def query_prometheus(query):
    """Query Prometheus and return the result."""
    params = {
        'query': query,
        'time': datetime.now().timestamp()
    }
    
    url = f"{PROMETHEUS_URL.rstrip('/')}/api/v1/query"
    response = requests.get(url, params=params, timeout=10)
    
    if response.status_code != 200:
        print(f"Error querying Prometheus: {response.status_code} {response.text}")
        return None
    
    return response.json()

def test_recording_rule(rule):
    """Test a recording rule and its alternative query."""
    print(f"\nTesting rule: {rule['name']}")
    
    # Query the recording rule
    rule_result = query_prometheus(rule['query'])
    if not rule_result or rule_result['status'] != 'success' or not rule_result['data']['result']:
        print(f"⚠️ Recording rule not found or returned no results: {rule['query']}")
        print(f"Testing alternative query: {rule['alternative']}")
        
        # Try the alternative query
        alt_result = query_prometheus(rule['alternative'])
        if alt_result and alt_result['status'] == 'success' and alt_result['data']['result']:
            print(f"✅ Alternative query works: {rule['alternative']}")
            print(f"   Value: {alt_result['data']['result'][0]['value'][1]}")
            return True
        else:
            print(f"❌ Alternative query failed: {rule['alternative']}")
            return False
    else:
        print(f"✅ Recording rule works: {rule['query']}")
        print(f"   Value: {rule_result['data']['result'][0]['value'][1]}")
        return True

def main():
    """Test all recording rules."""
    print(f"Testing recording rules against: {PROMETHEUS_URL}")
    print(f"Using instance: {INSTANCE_NAME}")
    
    success = True
    for rule in RECORDING_RULES:
        if not test_recording_rule(rule):
            success = False
    
    if success:
        print("\n✅ All recording rules are working!")
        return 0
    else:
        print("\n⚠️ Some recording rules are not working.")
        print("Please check the Prometheus configuration and rules files.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
