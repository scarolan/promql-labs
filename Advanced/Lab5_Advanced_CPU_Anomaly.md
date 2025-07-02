# 🔍 Lab 5: Advanced CPU Analysis & Anomaly Detection

## Objectives
- Detect CPU saturation and spikes using PromQL
- Use `max_over_time` and `increase` for anomaly detection
- Build a panel to visualize CPU anomalies

## Instructions
1. **Detect CPU saturation (high usage):**
   ```
   max_over_time((100 * (1 - (sum by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])) / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))))[30m:1m])
   ```
   
   > **Explanation:** This advanced query shows the highest CPU usage percentage observed in any 1-minute window over the last 30 minutes. It first calculates the average idle CPU rate across all cores, converts this to a usage percentage, then uses `max_over_time` with a subquery to find peak values. This is especially useful for detecting short-lived CPU spikes that might be missed by regular polling.
2. **Find CPU spikes using `increase`:**
   ```
   increase(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[10m])
   ```
   What does a sudden jump indicate?
   
   > **Explanation:** The `increase()` function calculates how much the CPU counter has increased over a 10-minute window. This shows the absolute number of CPU seconds spent in user mode during that time period. A sudden jump in this value indicates a burst of application activity. Unlike `rate()`, which gives an average, `increase()` helps you see the total CPU consumption over a defined period.
3. **Visualize anomalies:**
   - Create a time series panel in Grafana for the above queries.
   - Try setting alert thresholds for high CPU usage.
   
   > **Tip:** When visualizing these metrics in Grafana, consider using different thresholds and color bands to highlight normal, elevated, and critical CPU levels. For alerts, you might want to trigger on sustained high usage rather than brief spikes to reduce alert noise.

## Challenge
- Can you combine `increase` and `max_over_time` to highlight only the most extreme spikes?

<details>
<summary>🔬 <b>Show Solution</b></summary>

To combine `increase` and `max_over_time` to highlight extreme CPU spikes, follow these steps:

1. **Create a query to find the maximum increase in user-mode CPU time in short intervals:**
   ```
   max_over_time(increase(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[1m])[30m:1m])
   ```
   
   This query:
   - Uses `increase` to measure the growth in user CPU time over 1-minute windows
   - Uses `max_over_time` with a subquery `[30m:1m]` to find the highest 1-minute increase within a 30-minute period
   - Effectively identifies the most intense 1-minute CPU burst in the last half hour

2. **For a percentage-based anomaly detection, try this more advanced query:**
   ```
   max_over_time(
     (increase(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[1m]) 
     / 
     scalar(count(node_cpu_seconds_total{instance="localhost:9100",cpu="0"})))
   [30m:1m]) * 100
   ```
   
   This query:
   - Normalizes the increase by dividing by the number of CPU cores
   - Multiplies by 100 to express as a percentage
   - Shows the highest percentage of CPU capacity used in any 1-minute period

These queries are particularly useful for identifying short-lived but intensive CPU bursts that might indicate application issues or attacks, even if they don't appear significant on regular 5-minute rate calculations.

</details>

---

# 🌟 [Continue to Lab 6: Correlating Metrics & Building Composite Dashboards](../Advanced/Lab6_Correlating_Metrics.md)
