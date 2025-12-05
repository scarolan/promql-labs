#!/bin/bash
# Histogram Traffic Generator for Lab 9
# This script generates HTTP traffic to Prometheus to create histogram data
# for the prometheus_http_request_duration_seconds metrics

PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
DURATION="${DURATION:-300}"  # Run for 5 minutes by default
REQUESTS_PER_SECOND="${REQUESTS_PER_SECOND:-5}"

echo "🚀 Histogram Traffic Generator"
echo "================================"
echo "Prometheus URL: $PROMETHEUS_URL"
echo "Duration: ${DURATION}s"
echo "Requests/second: $REQUESTS_PER_SECOND"
echo ""
echo "Generating traffic to create histogram data..."
echo "Press Ctrl+C to stop early"
echo ""

# Calculate sleep interval
SLEEP_INTERVAL=$(echo "scale=3; 1/$REQUESTS_PER_SECOND" | bc)

# Various query endpoints to hit (creates varied latency distribution)
ENDPOINTS=(
    "/api/v1/query?query=up"
    "/api/v1/query?query=node_cpu_seconds_total"
    "/api/v1/query?query=prometheus_http_request_duration_seconds_bucket"
    "/api/v1/query?query=sum(rate(node_cpu_seconds_total[5m]))"
    "/api/v1/query?query=histogram_quantile(0.95,sum(rate(prometheus_http_request_duration_seconds_bucket[5m]))by(le))"
    "/api/v1/label/__name__/values"
    "/api/v1/targets"
    "/api/v1/status/config"
    "/api/v1/query_range?query=up&start=$(date -d '1 hour ago' +%s)&end=$(date +%s)&step=60"
    "/-/healthy"
)

START_TIME=$(date +%s)
END_TIME=$((START_TIME + DURATION))
REQUEST_COUNT=0
SUCCESS_COUNT=0
FAIL_COUNT=0

while [ $(date +%s) -lt $END_TIME ]; do
    # Pick a random endpoint
    ENDPOINT=${ENDPOINTS[$RANDOM % ${#ENDPOINTS[@]}]}
    
    # Make the request (suppress output, capture status)
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${PROMETHEUS_URL}${ENDPOINT}" 2>/dev/null)
    
    REQUEST_COUNT=$((REQUEST_COUNT + 1))
    
    if [ "$HTTP_STATUS" = "200" ]; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo -ne "\r✅ Requests: $REQUEST_COUNT | Success: $SUCCESS_COUNT | Failed: $FAIL_COUNT"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo -ne "\r⚠️  Requests: $REQUEST_COUNT | Success: $SUCCESS_COUNT | Failed: $FAIL_COUNT"
    fi
    
    sleep $SLEEP_INTERVAL
done

echo ""
echo ""
echo "================================"
echo "📊 Traffic Generation Complete!"
echo "================================"
echo "Total requests: $REQUEST_COUNT"
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""
echo "You can now run histogram queries in Lab 9!"
echo "Try: histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))"
