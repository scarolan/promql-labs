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
   
   > **Explanation:** These three queries provide a comprehensive view of system performance:
   > - The CPU query calculates the percentage of CPU being used across all cores by first finding the average idle rate, then subtracting from 100%.
   > - The memory query shows the percentage of memory currently in use by comparing available memory to total memory.
   > - The network query measures the total bytes per second being received across all network interfaces (excluding loopback).
   > 
   > By examining these metrics together, you can identify patterns and correlations between system resources.
2. **Build a composite dashboard panel:**
   - Add all three queries to a single Grafana panel (or use separate panels in a dashboard).
   - Look for patterns: do CPU spikes correlate with memory or network usage?
   
   > **Tip:** When creating composite dashboards, consider using a shared legend and consistent color scheme across panels. For example, use red for CPU, blue for memory, and green for network. This makes it easier to visually correlate metrics at a glance.
3. **Troubleshoot a simulated incident:**
   - Imagine a sudden CPU spike. What do the other metrics show at the same time?
   
   > **Explanation:** This exercise simulates a real-world troubleshooting scenario. By examining multiple metrics during an incident, you can identify potential causes. For example, a CPU spike accompanied by increased network traffic but stable memory usage might indicate a network-intensive process rather than a memory leak.

## Challenge
- Can you write a PromQL query that returns a warning if both CPU and memory usage are above 80%?

<details>
<summary>🧪 <b>Show Solution</b></summary>

To write a PromQL query that returns a warning when both CPU and memory usage exceed 80%:

1. **Build the query step by step:**

   **Step 1: Create the CPU usage threshold condition:**
   ```
   (100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
     / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))) > 80)
   ```

   **Step 2: Create the memory usage threshold condition:**
   ```
   (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})) > 80)
   ```

   **Step 3: Combine both conditions with the `and` operator:**
   ```
   (100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
     / count by (instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"}))) > 80)
   and
   (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})) > 80)
   ```

2. **Use this query in Grafana or Prometheus:**
   - In Grafana, this query will only return data points when both conditions are true
   - In Prometheus alerting, you can use this expression to trigger alerts only when both CPU and memory are under stress
   - This creates a more specific alert that reduces false positives from brief spikes in just one resource

3. **To test the query:**
   - Run a stress test on your system that consumes both CPU and memory
   - Use `stress-ng` or a similar tool: `stress-ng --cpu 4 --vm 2 --vm-bytes 1G --timeout 60s`

> **Explanation:** This query combines boolean operators with PromQL to create an alerting condition. It only returns data points where both CPU AND memory usage are above 80%, which can identify critical system resource constraints. This approach is particularly useful for detecting genuine system overload versus temporary spikes in individual resources.

</details>

---

# 🌟 You’ve mastered advanced PromQL!
