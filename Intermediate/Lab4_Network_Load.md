# 🌐 Lab 4: Network, Load, and Advanced Aggregations

## Objectives
- Query network traffic and system load metrics
- Use advanced PromQL aggregations
- Build multi-metric dashboards

## Instructions
1. **Query network receive and transmit rates:**
   ```
   rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   ```
   ```
   rate(node_network_transmit_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   ```
   What do you notice about the traffic patterns?
   
   > **Explanation:** These queries measure the bytes per second flowing in (receive) and out (transmit) of your network interfaces. The `device!="lo"` filter excludes the loopback interface, focusing on real network traffic. The `rate()` function converts the ever-increasing byte counters into a readable bytes-per-second gauge.
2. **Query system load averages:**
   ```
   node_load1{instance="localhost:9100"}
   ```
   ```
   node_load5{instance="localhost:9100"}
   ```
   ```
   node_load15{instance="localhost:9100"}
   ```
   How do these values compare to your CPU core count?
   
   > **Explanation:** Load averages represent the number of processes waiting for or using CPU resources, averaged over 1, 5, and 15 minutes. A healthy system typically has load averages lower than its CPU core count. Values consistently higher than the core count indicate potential CPU contention.
3. **Aggregate network traffic across all interfaces:**
   ```
   sum by (instance) (rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   ```
   ```
   sum by (instance) (rate(node_network_transmit_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   ```
   
   > **Explanation:** These queries sum up all network traffic across all interfaces (except loopback) on each server. The `sum by (instance)` aggregator combines the rates while preserving the instance label, giving you total network throughput per server rather than per individual interface. This is useful for overall traffic monitoring.
4. **(Optional) Build a dashboard panel with all these metrics.**
   
   > **Tip:** Combining network traffic and system load metrics in a single dashboard gives you a comprehensive view of system performance. Consider using different visualization types like graphs for network traffic and gauges for load averages.

## Challenge
- Can you create an alert for high load average (e.g., load1 > core count)?

<details>
<summary>🚀 <b>Show Solution</b></summary>

To create an alert for high load average (when load1 exceeds the CPU core count):

1. **First, we need to know the number of CPU cores:**
   ```
   count without(cpu, mode) (node_cpu_seconds_total{instance="localhost:9100"})
   ```

2. **Create a Grafana alert based on this query:**
   ```
   # This compares 1-minute load average to the core count
   node_load1{instance="localhost:9100"} > count without(cpu, mode) (node_cpu_seconds_total{instance="localhost:9100"})
   ```

3. **Alternative approach using a ratio:**
   ```
   # This gives a ratio of load to core count (values > 1 indicate overload)
   node_load1{instance="localhost:9100"} / count without(cpu, mode) (node_cpu_seconds_total{instance="localhost:9100"})
   ```

4. **In Grafana, set up the alert:**
   - Create a new panel with one of the above queries
   - Go to the Alert tab and set condition: "IS ABOVE 1"
   - Set "For" duration to 5m (to avoid alerting on brief spikes)
   - Add a notification message like "System load exceeds available CPU cores"
   - Save the alert

This alert will trigger when the 1-minute load average exceeds your system's CPU core count for 5 minutes, which is a common indicator of CPU resource contention.

</details>

---

## 🌟 Great job! You’re ready for the [Advanced Labs](../Advanced/README.md).
