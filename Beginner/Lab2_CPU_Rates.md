# 📈 Lab 2: Calculating CPU Use Rates

## Objectives
- Use the `rate()` function to calculate CPU usage
- Aggregate CPU usage by mode
- Visualize CPU usage in Grafana

## Instructions
1. **Start with your filtered query from Lab 1:**
   ```
   node_cpu_seconds_total{instance="localhost:9100"}
   ```
   
   > **Explanation:** This query selects the CPU metrics for all cores and all modes from your local system, providing the raw counter values that continuously increase over time.
2. **Wrap it with `rate()` to get per-second usage:**
   ```
   rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])
   ```
   What does this show compared to the raw counter?
   
   > **Explanation:** The `rate()` function calculates the per-second increase of the counter over the specified time window (5 minutes). The result shows the fraction of each CPU core spent in each mode per second (a value between 0 and 1). This essentially converts the ever-increasing counter into a percentage of CPU usage.
3. **Sum by mode to see total usage per mode:**
   ```
   sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m]))
   ```
   Which mode uses the most CPU?
   
   > **Explanation:** This query aggregates CPU usage across all cores but keeps the different modes separate. The result shows total CPU seconds used per second across all cores for each mode. Values greater than 1.0 indicate usage across multiple cores (e.g., 3.2 means usage equivalent to 3.2 cores).

4. **(Optional) Visualize in Grafana:**
   - Click “Add to dashboard” and create a time series panel.
   - Set the legend to `{{mode}}` and Y-axis to `percent (0.0 - 1.0)`.

## Challenge
- Filter out the `idle` mode. What does the graph look like now?

<details>
<summary>💡 <b>Show Solution</b></summary>

To filter out the `idle` mode and focus on active CPU usage, follow these steps:

1. **Start with the summed rate query from step 3:**
   ```
   sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m]))
   ```

2. **Add a filter to exclude the idle mode:**
   ```
   sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m]))
   ```

3. **Visualize the result:**
   - In Grafana, this creates a graph showing only the active CPU modes (user, system, iowait, etc.)
   - The graph now focuses on how your CPU is being actively used rather than including idle time
   - This makes it easier to see smaller variations in active CPU usage that might be hidden when the idle mode (which is often >90%) is included

This approach is particularly useful for monitoring production systems where you want to focus on actual CPU activity rather than idle time.

</details>

---

🌟 Great job! You’re ready for the [Intermediate Labs](../Intermediate/README.md).
