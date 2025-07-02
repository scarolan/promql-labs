# 🧩 Lab 1: Exploring CPU Metrics with PromQL

## Objectives
- Learn how to find and filter basic metrics in Prometheus
- Understand the structure of `node_cpu_seconds_total`
- Practice using label filters

## Instructions
1. **Open Grafana Explore** and set your data source to Prometheus.
2. **Query the raw metric:**
   ```
   node_cpu_seconds_total
   ```
   What do you see? How many time series are returned?
   
   **Query Breakdown:**
   ```
   # This query returns all CPU time counter metrics
   # It shows how many CPU seconds each core has spent in each mode
   # since the system started or the counter was last reset
   node_cpu_seconds_total
   ```
   You're looking at a counter metric that constantly increases over time.
   Each line represents a different CPU core and mode combination.
3. **Filter by instance:**
   ```
   node_cpu_seconds_total{instance="localhost:9100"}
   ```
   How does the result change?
   
   **Query Breakdown:**
   ```
   # Step 1: Start with the raw CPU metric
   node_cpu_seconds_total
   
   # Step 2: Add a label filter to view only a specific machine
   # The curly braces {} allow you to filter by label values
   node_cpu_seconds_total{instance="localhost:9100"}
   ```
   This filters your view to show only the CPU metrics from a specific machine,
   useful in multi-server environments.
4. **Filter by CPU mode:**
   Try filtering for just the `user` mode:
   ```
   node_cpu_seconds_total{instance="localhost:9100", mode="user"}
   ```
   What does this show?
   
   **Query Breakdown:**
   ```
   # Step 1: Start with the instance-filtered CPU metric
   node_cpu_seconds_total{instance="localhost:9100"}
   
   # Step 2: Add another filter condition to show only user mode CPU usage
   # Multiple label conditions are combined with AND logic
   node_cpu_seconds_total{instance="localhost:9100", mode="user"}
   ```
   Now you're seeing only the time each CPU core has spent running user processes
   (application code) rather than kernel/system processes or idle time.

## Challenge
- Try filtering for a different mode, like `system` or `idle`. What do you notice?

<details>
<summary>🔮 <b>Show Solution</b></summary>

- The raw metric returns one time series per CPU core, per mode, per instance.
- Filtering by instance narrows it to just your machine.
- Filtering by mode shows only the selected CPU mode (e.g., `user` time).

</details>

---

# 🌟 Well done! Move on to Lab 2 when ready.
