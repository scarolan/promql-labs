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
- Create a heatmap-compatible query that shows the distribution of CPU usage over time using quantiles.
- Bonus: Try visualizing your query in Grafana's heatmap panel if you have access to Grafana.

<details>
<summary>🧩 <b>Show Solution</b></summary>

Creating a heatmap of CPU usage quantiles involves synthetic bucketing since CPU metrics aren't typically stored as histograms. Here's how to do it:

1. **Create synthetic buckets from CPU usage:**

   ```promql
   # Create CPU usage buckets using floor function for 5% increments
   floor(
     clamp_max(
       100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])) / 
       count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))),
       100
     ) / 5
   ) * 5
   ```

   This query:
   - Calculates CPU usage as a percentage
   - Uses `clamp_max` to ensure no values exceed 100%
   - Uses `floor` and multiplication to create synthetic buckets with 5% increments (0, 5, 10, 15, etc.)

2. **For a proper heatmap in Grafana:**

   ```promql
   # Create a histogram from CPU usage data for heatmap visualization
   sum(count_values("le", floor(clamp_max(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])) / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))), 100) / 5) * 5)) by (le)
   ```

   This query:
   - Creates CPU usage buckets with 5% granularity (0-5%, 5-10%, etc.)
   - Groups the values using `count_values` with the bucket upper bound as the label
   - Aggregates the counts by bucket, creating a histogram-like structure
   
   **Understanding the Components:**
   - `clamp_max(..., 100)`: Ensures values don't exceed 100%
   - `floor(.../ 5) * 5`: Rounds down to nearest 5% increment
   - `count_values("le", ...)`: Groups by bucket boundary and counts occurrences
   - `sum(...) by (le)`: Aggregates the counts per bucket

3. **In Grafana:**
   - Use this query with a heatmap visualization
   - Set "Format as" to "Time series buckets"
   - Set the bucket bounds from the query metric labels

This approach creates a heatmap showing the distribution of CPU usage over time, with color intensity indicating frequency of observations in each range.

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
