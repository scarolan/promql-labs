# 💾 Lab 3: Memory and Filesystem Usage

## Objectives
- Query and interpret memory and filesystem metrics
- Calculate memory usage percentage
- Visualize memory and disk usage in Grafana

## Instructions
1. **Query total and available memory:**
   ```promql
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   ```
   
   ```promql
   node_memory_MemAvailable_bytes{instance="localhost:9100"}
   ```
   
   > **Explanation:** These metrics show the total physical memory on your system and how much is currently available for applications to use.
2. **Calculate memory usage %:**
   ```promql
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
   ```
   What does this value represent?
   
   > **Explanation:** This query calculates the percentage of memory currently in use. It first determines what fraction of memory is free (available/total), then subtracts from 1 to get the used fraction, and finally multiplies by 100 to express it as a percentage.
3. **Query filesystem usage:**
   ```promql
   node_filesystem_size_bytes{instance="localhost:9100",fstype!="tmpfs",mountpoint!="/run"}
   ```
   
   ```promql
   node_filesystem_free_bytes{instance="localhost:9100",fstype!="tmpfs",mountpoint!="/run"}
   ```
   
   > **Explanation:** These queries show the total size and free space of your filesystems. The filters (`fstype!="tmpfs",mountpoint!="/run"`) exclude temporary filesystems which aren't relevant for monitoring persistent disk usage.
4. **Calculate disk usage % for `/` mount:**
   ```promql
   100 * (1 - (node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"} / node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}))
   ```
   
   > **Explanation:** This query calculates the percentage of disk space used on the root filesystem (`/`). Similar to the memory calculation, it first finds the fraction of free space, subtracts from 1 to get the used fraction, then multiplies by 100 for a percentage. This is a critical metric for monitoring disk usage.

## Challenge
- Try visualizing memory and disk usage as gauges in Grafana.

<details>
<summary>🧠 <b>Show Solution</b></summary>

To create gauge visualizations for memory and disk usage in Grafana:

1. **Create a memory usage gauge:**
   - Click "+ Add panel" in Grafana and select the "Gauge" visualization
   - Enter the memory usage query:
     ```promql
     100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
     ```
   - Set threshold values:
     - Green: 0-70%
     - Yellow: 70-85%
     - Red: 85-100%
   - Label the panel "Memory Usage %"

2. **Create a disk usage gauge:**
   - Create another gauge panel
   - Enter the disk usage query:
     ```promql
     100 * (1 - (node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"} / node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}))
     ```
   - Set threshold values:
     - Green: 0-75%
     - Yellow: 75-90%
     - Red: 90-100%
   - Label the panel "Root Filesystem Usage %"

3. **Arrange both gauges side by side** in your dashboard for an at-a-glance overview of system resource usage.

Gauges are particularly effective for metrics with well-defined thresholds, allowing you to quickly assess the health of your system without needing to interpret line graphs.

</details>

---

# 🌟 [Continue to Lab 4: Network, Load, and Advanced Aggregations](../Intermediate/Lab4_Network_Load.md)
