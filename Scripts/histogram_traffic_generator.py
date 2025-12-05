#!/usr/bin/env python3
"""
Histogram Traffic Generator for Lab 9

This script generates HTTP traffic to Prometheus to create histogram data
for the prometheus_http_request_duration_seconds metrics.

Usage:
    python histogram_traffic_generator.py [--url URL] [--duration SECONDS] [--rps REQUESTS_PER_SECOND]

Examples:
    python histogram_traffic_generator.py
    python histogram_traffic_generator.py --url http://localhost:9090 --duration 300 --rps 5
"""

import argparse
import random
import time
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote

def main():
    parser = argparse.ArgumentParser(description='Generate HTTP traffic for Prometheus histogram data')
    parser.add_argument('--url', default='http://localhost:9090', help='Prometheus URL (default: http://localhost:9090)')
    parser.add_argument('--duration', type=int, default=300, help='Duration in seconds (default: 300)')
    parser.add_argument('--rps', type=float, default=5, help='Requests per second (default: 5)')
    args = parser.parse_args()

    prometheus_url = args.url.rstrip('/')
    duration = args.duration
    rps = args.rps

    print("🚀 Histogram Traffic Generator")
    print("=" * 40)
    print(f"Prometheus URL: {prometheus_url}")
    print(f"Duration: {duration}s")
    print(f"Requests/second: {rps}")
    print()
    print("Generating traffic to create histogram data...")
    print("Press Ctrl+C to stop early")
    print()

    # Various query endpoints to hit (creates varied latency distribution)
    endpoints = [
        "/api/v1/query?query=up",
        "/api/v1/query?query=node_cpu_seconds_total",
        "/api/v1/query?query=" + quote("sum(rate(node_cpu_seconds_total[5m]))"),
        "/api/v1/query?query=" + quote("prometheus_http_request_duration_seconds_bucket"),
        "/api/v1/query?query=" + quote("histogram_quantile(0.95,sum(rate(prometheus_http_request_duration_seconds_bucket[5m]))by(le))"),
        "/api/v1/label/__name__/values",
        "/api/v1/targets",
        "/api/v1/status/config",
        "/-/healthy",
    ]

    # Add some range queries with different time ranges for varied latency
    now = int(time.time())
    for hours_ago in [1, 2, 6]:
        start = now - (hours_ago * 3600)
        endpoints.append(f"/api/v1/query_range?query=up&start={start}&end={now}&step=60")

    sleep_interval = 1.0 / rps
    start_time = time.time()
    end_time = start_time + duration
    
    request_count = 0
    success_count = 0
    fail_count = 0

    try:
        while time.time() < end_time:
            # Pick a random endpoint
            endpoint = random.choice(endpoints)
            url = f"{prometheus_url}{endpoint}"
            
            try:
                req = Request(url, headers={'User-Agent': 'PromQL-Labs-Traffic-Generator/1.0'})
                with urlopen(req, timeout=10) as response:
                    _ = response.read()  # Consume response
                    success_count += 1
            except (URLError, HTTPError) as e:
                fail_count += 1
            
            request_count += 1
            
            # Update progress
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            status = "✅" if fail_count == 0 else "⚠️"
            sys.stdout.write(f"\r{status} Requests: {request_count} | Success: {success_count} | Failed: {fail_count} | Time remaining: {remaining}s   ")
            sys.stdout.flush()
            
            time.sleep(sleep_interval)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")

    print("\n")
    print("=" * 40)
    print("📊 Traffic Generation Complete!")
    print("=" * 40)
    print(f"Total requests: {request_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    print()
    print("You can now run histogram queries in Lab 9!")
    print("Try: histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))")

if __name__ == "__main__":
    main()
