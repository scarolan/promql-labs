# 📈 Lab 2: Calculating CPU Usage Rates

## Objectives
- Use the `rate()` function to calculate CPU usage
- Aggregate CPU usage by mode
- Visualize CPU usage in Grafana

## Instructions
1. **Start with your filtered query from Lab 1:**
   ```
   node_cpu_seconds_total{instance="localhost:9100"}
   ```
2. **Wrap it with `rate()` to get per-second usage:**
   ```
   rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])
   ```
   What does this show compared to the raw counter?
   
   **Query Breakdown:**
   ```
   # Step 1: Select the raw counter metric for all CPU modes
   node_cpu_seconds_total{instance="localhost:9100"}
   
   # Step 2: Apply rate() over a 5-minute window to convert the counter to per-second
   # This calculates how many CPU seconds were used per second (essentially a percentage)
   rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])
   ```
   The result shows the fraction of each CPU core spent in each mode per second (a value between 0 and 1).
3. **Sum by mode to see total usage per mode:**
   ```
   sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m]))
   ```
   Which mode uses the most CPU?
   
   **Query Breakdown:**
   ```
   # Step 1: Calculate rate for each CPU core and each mode
   rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])
   
   # Step 2: Sum the rates across all cores, but keep separate values for each mode
   # This aggregates CPU usage for all cores, grouped by mode (user, system, idle, etc.)
   sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m]))
   ```
   The result shows total CPU seconds used per second across all cores for each mode.
   Values greater than 1.0 indicate usage across multiple cores (e.g., 3.2 means usage equivalent to 3.2 cores).
4. **(Optional) Visualize in Grafana:**
   - Click “Add to dashboard” and create a time series panel.
   - Set the legend to `{{mode}}` and Y-axis to `percent (0.0 - 1.0)`.

## Challenge
- Filter out the `idle` mode. What does the graph look like now?

<details>
<summary>💡 <b>Show Solution</b></summary>

- `rate()` converts the counter to a per-second rate, showing real usage.
- Summing by mode shows how CPU time is split.
- Filtering out `idle` focuses on active CPU usage.

</details>

---

# 🌟 Great job! You’re ready for Intermediate Labs.
