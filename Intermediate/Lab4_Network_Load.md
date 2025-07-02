# 🌐 Lab 4: Network, Load, and Advanced Aggregations

## Objectives
- Query network traffic and system load metrics
- Use advanced PromQL aggregations
- Build multi-metric dashboards

## Instructions
1. **Query network receive and transmit rates:**
   ```
   rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   rate(node_network_transmit_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   ```
   What do you notice about the traffic patterns?
   
   **Query Breakdown:**
   ```
   # Step 1: Access the network counter metrics (excludes loopback interface)
   node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}
   node_network_transmit_bytes_total{instance="localhost:9100",device!="lo"}
   
   # Step 2: Calculate the per-second rate over a 5-minute window
   # This converts counters (always increasing) to gauges (bytes/second)
   rate(node_network_receive_bytes_total{...}[5m])
   rate(node_network_transmit_bytes_total{...}[5m])
   ```
2. **Query system load averages:**
   ```
   node_load1{instance="localhost:9100"}
   node_load5{instance="localhost:9100"}
   node_load15{instance="localhost:9100"}
   ```
   How do these values compare to your CPU core count?
3. **Aggregate network traffic across all interfaces:**
   ```
   sum by (instance) (rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   sum by (instance) (rate(node_network_transmit_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   ```
   
   **Aggregation Query Breakdown:**
   ```
   # Step 1: Calculate per-second rates for each network interface
   rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m])
   
   # Step 2: Sum these rates but keep the instance label
   # This combines traffic across all interfaces for each server
   sum by (instance) (rate(node_network_receive_bytes_total{instance="localhost:9100",device!="lo"}[5m]))
   ```
   The result is total network traffic per server rather than per interface.
4. **(Optional) Build a dashboard panel with all these metrics.**

## Challenge
- Can you create an alert for high load average (e.g., load1 > core count)?

<details>
<summary>🚀 <b>Show Solution</b></summary>

- Network traffic queries show bytes per second in/out.
- Load averages should be compared to CPU core count for health.
- Aggregating by instance gives total traffic per host.
- Alerts can be set in Grafana or Prometheus for high load.

</details>

---

# 🌟 You’re now a PromQL wrangler! Try the Advanced labs for more challenges.
