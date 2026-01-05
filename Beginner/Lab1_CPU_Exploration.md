# 🧩 Lab 1: Exploring CPU Metrics with PromQL

## Objectives
- Learn how to find and filter basic metrics in Prometheus
- Understand the structure of `node_cpu_seconds_total`
- Practice using label filters

## Instructions
1. **Open Grafana Explore** and set your data source to Prometheus.
2. **Query the raw metric:**
   ```promql
   node_cpu_seconds_total
   ```
   What do you see? How many time series are returned?
   
   > **Explanation:** You're looking at a counter metric that constantly increases over time. Each line represents a different CPU core and mode combination, showing how many CPU seconds each core has spent in each mode since the system started or the counter was last reset.
3. **Filter by instance:**
   ```promql
   node_cpu_seconds_total{instance="localhost:9100"}
   ```
   How does the result change?
   
   > **Explanation:** This filters your view to show only the CPU metrics from a specific machine (localhost), which is useful in multi-server environments. The curly braces `{}` allow you to filter by label values.
4. **Filter by CPU mode:**
   Try filtering for just the `user` mode:
   ```promql
   node_cpu_seconds_total{instance="localhost:9100", mode="user"}
   ```
   What does this show?
   
   > **Explanation:** Now you're seeing only the time each CPU core has spent running user processes (application code) rather than kernel/system processes or idle time. Multiple label conditions are combined with AND logic.

## Challenge
- Try filtering for a different mode, like `system` or `idle`. What do you notice?

<details>
<summary>🔮 <b>Show Solution</b></summary>

To filter for different CPU modes, follow these steps:

1. **Filter for system mode:**
   ```promql
   node_cpu_seconds_total{instance="localhost:9100", mode="system"}
   ```
   This shows how much time each CPU core has spent executing system calls and kernel code.

2. **Filter for idle mode:**
   ```promql
   node_cpu_seconds_total{instance="localhost:9100", mode="idle"}
   ```
   This shows how much time each CPU core has spent doing nothing (being idle).

3. **Compare the results:**
   - You'll notice that `idle` mode typically has much higher values than `user` or `system`, as most systems spend the majority of time idle.
   - The `system` mode values are usually lower than `user`, as most workloads spend more time in user applications than in the kernel.
   - Each mode represents a different aspect of CPU time allocation, giving you insight into what your CPU is doing.

By examining different modes, you can understand how your CPU resources are being utilized across different types of operations.

</details>

---

# 🌟 [Continue to Lab 2: Calculating CPU Use Rates](../Beginner/Lab2_CPU_Rates.md)
