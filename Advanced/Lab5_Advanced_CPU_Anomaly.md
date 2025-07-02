# 🔍 Lab 5: Advanced CPU Analysis & Anomaly Detection

## Objectives
- Detect CPU saturation and spikes using PromQL
- Use `max_over_time` and `increase` for anomaly detection
- Build a panel to visualize CPU anomalies

## Instructions
1. **Detect CPU saturation (high usage):**
   ```
   max_over_time(
     (100 * (1 - (sum by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
       / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))))
   [30m:1m]
   ```
   This shows the highest CPU usage % in any 1-minute window over the last 30 minutes.

   **Query Breakdown:**
   Let's understand this complex query step by step:
   ```
   # Step 1: Calculate the rate of idle CPU time per second for each CPU core
   rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])
   
   # Step 2: Sum the idle CPU rates across all cores for the instance
   sum by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
   
   # Step 3: Count how many CPU cores the system has (using mode="idle" as reference)
   count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})
   
   # Step 4: Divide the sum by the count to get average idle rate
   sum by (instance) (...) / count by (instance) (...)
   
   # Step 5: Calculate CPU usage % (subtract idle % from 100%)
   100 * (1 - (average idle rate))
   
   # Step 6: Apply max_over_time to find the highest value in each 1m period over 30m
   max_over_time((CPU usage %)[30m:1m])
   ```
2. **Find CPU spikes using `increase`:**
   ```
   increase(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[10m])
   ```
   What does a sudden jump indicate?
   
   **Query Breakdown:**
   ```
   # Step 1: Start with the raw counter metric for user mode CPU time
   node_cpu_seconds_total{instance="localhost:9100",mode="user"}
   
   # Step 2: Apply increase() to calculate how much this counter increased over 10m
   # This shows the number of CPU seconds spent in user mode during that time window
   increase(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[10m])
   ```
3. **Visualize anomalies:**
   - Create a time series panel in Grafana for the above queries.
   - Try setting alert thresholds for high CPU usage.

## Challenge
- Can you combine `increase` and `max_over_time` to highlight only the most extreme spikes?

<details>
<summary>🔬 <b>Show Solution</b></summary>

- `max_over_time` helps spot short-lived CPU peaks.
- `increase` shows how much CPU time was spent in a mode over a window.
- Combining both can help you alert on unusual CPU bursts.

</details>

---

# 🌟 Nice work! Continue to the next advanced lab.
