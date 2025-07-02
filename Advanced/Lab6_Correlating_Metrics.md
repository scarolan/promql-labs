# 🧠 Lab 6: Correlating Metrics & Building Composite Dashboards

## Objectives
- Correlate CPU, memory, and network metrics in a single dashboard
- Use PromQL to build composite queries
- Practice troubleshooting with multi-metric panels

## Instructions
1. **Query CPU, memory, and network usage together:**
   ```
   # CPU usage %
   100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
     / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})))

   # Memory usage %
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))

   # Network receive rate (bytes/sec)
   sum by (instance) (rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   ```
   
   **CPU Query Breakdown:**
   ```
   # Step 1: Get the rate of idle CPU time for each core over 5m
   rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])
   
   # Step 2: Calculate the average idle rate across all cores
   avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
   
   # Step 3: Get the total number of CPU cores
   count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})
   
   # Step 4: Convert idle rate to total CPU usage percentage
   100 * (1 - (avg idle rate / core count))
   ```
   
   **Memory Query Breakdown:**
   ```
   # Step 1: Get available memory in bytes
   node_memory_MemAvailable_bytes{instance="localhost:9100"}
   
   # Step 2: Get total memory in bytes
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Step 3: Calculate percentage of memory used
   100 * (1 - (available memory / total memory))
   ```
   
   **Network Query Breakdown:**
   ```
   # Step 1: Get network bytes received on all interfaces except loopback
   node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}
   
   # Step 2: Calculate the per-second rate over 5 minutes
   rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   
   # Step 3: Sum across all network interfaces for the instance
   sum by (instance) (rate(...))
   ```
2. **Build a composite dashboard panel:**
   - Add all three queries to a single Grafana panel (or use separate panels in a dashboard).
   - Look for patterns: do CPU spikes correlate with memory or network usage?
3. **Troubleshoot a simulated incident:**
   - Imagine a sudden CPU spike. What do the other metrics show at the same time?

## Challenge
- Can you write a PromQL query that returns a warning if both CPU and memory usage are above 80%?

<details>
<summary>🧪 <b>Show Solution</b></summary>

- Composite dashboards help you spot correlations and root causes.
- Example warning query:
  ```
  (100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
    / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))) > 80)
  and
  (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})) > 80)
  ```

- **Warning Query Breakdown:**
  ```
  # Step 1: Calculate CPU usage % and check if it's above 80%
  (CPU usage % > 80)
  
  # Step 2: Calculate Memory usage % and check if it's above 80% 
  (Memory usage % > 80)
  
  # Step 3: Combine using 'and' operator - both conditions must be true
  (CPU condition) and (Memory condition)
  ```
  This query only returns data points where both CPU AND memory usage are above 80%.

</details>

---

# 🌟 You’ve mastered advanced PromQL!
