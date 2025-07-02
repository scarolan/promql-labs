# 📊 Lab 9: Histograms and Quantiles

## Objectives
- Understand histogram metrics and their structure
- Learn how to use histogram_quantile function
- Analyze latency distributions with bucketing
- Calculate SLO-related metrics

## Instructions

1. **Explore Histogram Metrics:**
   ```
   # Examine the structure of a histogram metric
   prometheus_http_request_duration_seconds_bucket
   ```
   
   > **Explanation:** Histogram metrics have multiple time series with a `le` (less than or equal) label representing bucket boundaries. The value of each time series is the count of observations falling within that bucket. This allows for percentile calculation across the distribution.

2. **Calculate Percentile Latencies:**
   ```
   # Calculate 95th percentile latency
   histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))
   ```
   
   > **Explanation:** The `histogram_quantile` function calculates the specified quantile (0.95 = 95th percentile) from bucket data. This gives you the value below which 95% of observations fall. This query first aggregates request rates across all buckets, then calculates the 95th percentile.

3. **Analyze Latency by Handler:**
   ```
   # Calculate median (50th percentile) latency by handler
   histogram_quantile(0.5, sum by (handler, le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
   ```
   
   > **Explanation:** This query calculates the median latency for each handler separately by keeping the `handler` label during aggregation. This allows you to compare performance across different endpoints or services.

4. **Calculate Error Budget with Histograms:**
   ```
   # Percentage of requests under 500ms (0.5s) SLO threshold
   (sum(rate(prometheus_http_request_duration_seconds_bucket{le="0.5"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100
   ```
   
   > **Explanation:** This query calculates what percentage of requests complete within the 500ms SLO threshold. It divides the count of requests in buckets under 0.5s by the total count, then multiplies by 100 to get a percentage. This is essential for SLO monitoring.

5. **Working with Gauge Histograms:**
   ```
   # Calculate rate of change for a gauge metric
   deriv(node_memory_Active_bytes{instance="localhost:9100"}[1h])
   ```
   
   > **Explanation:** The `deriv` function calculates the per-second derivative of a gauge metric, showing how quickly a gauge value is changing. This is useful for understanding trends in resource usage and predicting future needs.

## Challenge
- Create a heatmap-compatible query that shows the distribution of CPU usage over time using quantiles.

<details>
<summary>🧩 <b>Show Solution</b></summary>

Creating a heatmap of CPU usage quantiles involves synthetic bucketing since CPU metrics aren't typically stored as histograms. Here's how to do it:

1. **Create synthetic buckets from CPU usage:**

   ```
   # Define CPU usage buckets with quantize function
   quantize(
     clamp_max(
       100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])) / 
       count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))),
       100
     ),
     5
   ) by (instance)
   ```

   This query:
   - Calculates CPU usage as a percentage
   - Uses `clamp_max` to ensure no values exceed 100%
   - Uses `quantize` to create synthetic buckets with 5% increments

2. **For a proper heatmap in Grafana:**

   ```
   # Create a histogram from CPU usage data for heatmap visualization
   sum(count_values("le", floor(clamp_max(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])) / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))), 100) / 5) * 5)) by (le)
   ```

   This query:
   - Creates CPU usage buckets with 5% granularity (0-5%, 5-10%, etc.)
   - Groups the values using `count_values` with the bucket upper bound as the label
   - Aggregates the counts by bucket, creating a histogram-like structure

3. **In Grafana:**
   - Use this query with a heatmap visualization
   - Set "Format as" to "Time series buckets"
   - Set the bucket bounds from the query metric labels

This approach creates a heatmap showing the distribution of CPU usage over time, with color intensity indicating frequency of observations in each range.

</details>

---

## 🌟 Congratulations! You've completed all the PromQL labs!
