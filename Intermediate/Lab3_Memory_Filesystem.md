# 💾 Lab 3: Memory and Filesystem Usage

## Objectives
- Query and interpret memory and filesystem metrics
- Calculate memory usage percentage
- Visualize memory and disk usage in Grafana

## Instructions
1. **Query total and available memory:**
   ```
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   node_memory_MemAvailable_bytes{instance="localhost:9100"}
   ```
2. **Calculate memory usage %:**
   ```
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
   ```
   What does this value represent?
   
   **Query Breakdown:**
   ```
   # Step 1: Calculate the ratio of available memory to total memory
   # This gives the fraction of memory that's free
   node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Step 2: Subtract from 1 to get the fraction that's used
   1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})
   
   # Step 3: Multiply by 100 to convert to percentage
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
   ```
3. **Query filesystem usage:**
   ```
   node_filesystem_size_bytes{instance="localhost:9100",fstype!="tmpfs",mountpoint!="/run"}
   node_filesystem_free_bytes{instance="localhost:9100",fstype!="tmpfs",mountpoint!="/run"}
   ```
4. **Calculate disk usage % for `/` mount:**
   ```
   100 * (1 - (node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"} / node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}))
   ```
   
   **Query Breakdown:**
   ```
   # Step 1: Get bytes free on the root filesystem
   node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"}
   
   # Step 2: Get total size of the root filesystem
   node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}
   
   # Step 3: Calculate the ratio of free space to total size
   node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"} / node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}
   
   # Step 4: Subtract from 1 to get the used fraction, then convert to percentage
   100 * (1 - (node_filesystem_free_bytes{instance="localhost:9100",mountpoint="/"} / node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"}))
   ```

## Challenge
- Try visualizing memory and disk usage as gauges in Grafana.

<details>
<summary>🧠 <b>Show Solution</b></summary>

- The memory usage % shows how much RAM is in use.
- Disk usage % for `/` shows how full your root filesystem is.
- Gauges are great for at-a-glance health checks.

</details>

---

# 🌟 Awesome! Try the next lab for more PromQL fun.
