# 📊 Lab 9: Histograms and Quantiles

## Objectives
- Understand histogram metrics and their bucket structure
- Learn how to use the histogram_quantile function for percentile analysis
- Analyze latency distributions with bucketing
- Calculate SLO-related metrics
- Create synthetic histograms for metrics that aren't inherently histograms

## Instructions

1. **Explore Histogram Metrics:**
   ```promql
   # Examine the structure of a histogram metric
   prometheus_http_request_duration_seconds_bucket
   ```
   
   > **Explanation:** Histogram metrics have multiple time series with a `le` (less than or equal) label representing bucket boundaries. The value of each time series is the count of observations falling within that bucket. This allows for percentile calculation across the distribution.
   >
   > To understand the structure better, you can also examine the bucket counts and their boundaries:
   > 
   > ```promql
   > # Filter to see specific buckets
   > prometheus_http_request_duration_seconds_bucket{handler="/api/v1/query"}
   > ```

2. **Calculate Percentile Latencies:**
   ```promql
   # Calculate 95th percentile latency
   histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))
   ```
   
   > **Explanation:** The `histogram_quantile` function calculates the specified quantile (0.95 = 95th percentile) from bucket data. This gives you the value below which 95% of observations fall. This query first aggregates request rates across all buckets, then calculates the 95th percentile.
   >
   > **Function Signature:** `histogram_quantile(φ float, b instant-vector)`
   > - `φ` is the quantile to calculate, between 0 and 1 (e.g., 0.5 for median, 0.95 for 95th percentile)
   > - `b` is a vector of bucket counts with the `le` label
   >
   > **Common Quantiles:**
   > - 0.5: Median (50th percentile)
   > - 0.9: 90th percentile
   > - 0.95: 95th percentile
   > - 0.99: 99th percentile

3. **Analyze Latency by Handler:**
   ```promql
   # Calculate median (50th percentile) latency by handler
   histogram_quantile(0.5, sum by (handler, le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
   ```
   
   > **Explanation:** This query calculates the median latency for each handler separately by keeping the `handler` label during aggregation. This allows you to compare performance across different endpoints or services.

4. **Calculate Error Budget with Histograms:**
   ```promql
   # Percentage of requests under 500ms (0.5s) SLO threshold
   (sum(rate(prometheus_http_request_duration_seconds_bucket{le="0.5"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100
   ```
   
   > **Explanation:** This query calculates what percentage of requests complete within the 500ms SLO threshold. It divides the count of requests in buckets under 0.5s by the total count, then multiplies by 100 to get a percentage. This is essential for SLO monitoring.
   >
   > You can also calculate the error rate (requests exceeding the SLO threshold):
   >
   > ```promql
   > # Percentage of requests exceeding 500ms SLO threshold
   > (1 - sum(rate(prometheus_http_request_duration_seconds_bucket{le="0.5"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100
   > ```
   >
   > **SLO Components:**
   > - **SLI (Service Level Indicator)**: The actual measurement (request latency)
   > - **SLO (Service Level Objective)**: The target (e.g., 99% of requests < 500ms)
   > - **Error Budget**: Allowable amount of non-compliance (e.g., 1% of requests can exceed 500ms)

5. **Working with Gauge Metrics:**
   ```promql
   # Calculate rate of change for a gauge metric
   deriv(node_memory_Active_bytes{instance="localhost:9100"}[5m])
   ```
   
   > **Explanation:** The `deriv` function calculates the per-second derivative of a gauge metric, showing how quickly a gauge value is changing. Using a 5-minute window provides quick feedback in a lab setting while still being useful for understanding trends in resource usage.
   >
   > **Note:** While not a histogram function, `deriv` is important when analyzing the rate of change for metrics that aren't counters. Unlike counters which can use `rate()`, gauges need `deriv()` to find their rate of change.
   > 
   > **Predict future values** with linear prediction based on recent trends:
   >
   > ```promql
   > # Predict memory usage 5 minutes in the future
   > predict_linear(node_memory_Active_bytes{instance="localhost:9100"}[5m], 300)
   > ```

## Challenge

Create queries to analyze the behavior of Prometheus's HTTP API using the histogram metrics from `prometheus_http_request_duration_seconds_bucket` that you've already explored.

1. Compare the 90th percentile latency for different handlers to identify which endpoints are the slowest
2. Find the percentage of requests that take less than 0.1s for each handler
3. Create a query that shows both the median (50th) and 95th percentile latencies side by side

<details>
<summary>🧩 <b>Show Solution</b></summary>

### 1. Compare 90th percentile latency by handler:

```promql
# 90th percentile latency by handler
histogram_quantile(0.90, 
  sum by(handler, le) (
    rate(prometheus_http_request_duration_seconds_bucket[5m])
  )
)
```

This query:
- Groups by handler and bucket boundary (`le`)
- Calculates the rate of requests in each bucket
- Uses histogram_quantile to compute the 90th percentile for each handler
- Allows you to easily compare performance across different endpoints

### 2. Percentage of fast requests (<0.1s) by handler:

```promql
# Percentage of requests under 0.1s by handler
(
  sum by (handler) (rate(prometheus_http_request_duration_seconds_bucket{le="0.1"}[5m])) /
  sum by (handler) (rate(prometheus_http_request_duration_seconds_count[5m]))
) * 100
```

This query:
- Calculates what percentage of requests complete within 0.1 seconds for each handler
- Divides the count of requests in buckets under 0.1s by the total count
- Multiplies by 100 to get a percentage
- Helps identify which endpoints consistently provide fast responses

### 3. Compare median and 95th percentile side by side:

```promql
# Median and 95th percentile latencies as separate time series
{
  quantile="0.5",
  value=histogram_quantile(0.5, sum by(le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
} or
{
  quantile="0.95",
  value=histogram_quantile(0.95, sum by(le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
}
```

This query:
- Uses the `or` operator to combine two separate quantile calculations
- Labels each with its respective quantile value (0.5 or 0.95)
- Allows for side-by-side comparison between median and 95th percentile performance
- Helps visualize the difference between typical and worst-case scenarios

This analysis helps you understand:
- Which endpoints are consistently slow (high median latency)
- Which endpoints have inconsistent performance (large gap between median and 95th percentile)
- Which endpoints meet your latency SLOs and which need optimization

</details>

---

## 🌟 Congratulations! You've completed all the PromQL labs!

You've now mastered a comprehensive set of PromQL skills, from basic queries to advanced histogram analysis. These skills will be invaluable for effective monitoring, alerting, and troubleshooting of your systems using Prometheus.

### What Next?
- Try applying these concepts to your own infrastructure metrics
- Create your own Grafana dashboards using these advanced PromQL queries
- Implement SLOs for your services using the histogram techniques you've learned
- Share your knowledge with your team to improve observability practices

Remember that mastering PromQL is an ongoing journey - the more you practice, the more effective you'll become at using Prometheus for observability and troubleshooting.
