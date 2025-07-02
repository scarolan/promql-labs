# 🔍 Lab 0: PromQL Fundamentals

## Objectives
- Learn PromQL basic syntax and operators
- Understand time ranges and functions
- Get comfortable with the Prometheus UI

## Instructions
1. **Open Prometheus UI** (not Grafana) and navigate to the Graph section.
2. **Explore simple metric queries:**
   ```
   # Return all metrics for node_memory_MemTotal_bytes
   node_memory_MemTotal_bytes
   
   # Filter by instance
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Use regular expressions for label matching
   node_memory_MemTotal_bytes{instance=~"local.*"}
   ```
3. **Try basic operators:**
   ```
   # Division - Calculate memory used as fraction of total
   (node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Multiplication - Convert to percentage
   100 * ((node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"})
   ```
   
   **Query Breakdown:**
   ```
   # Step 1: Get total memory in bytes
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Step 2: Get available memory in bytes
   node_memory_MemAvailable_bytes{instance="localhost:9100"}
     
   # Step 3: Calculate used memory (total - available)
   (node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"})
   
   # Step 4: Divide by total to get the fraction used (between 0 and 1)
   (node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"}
   
   # Step 5: Multiply by 100 to convert to percentage (0-100%)
   100 * ((node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"})
   ```
   This demonstrates how PromQL allows you to perform calculations directly in your query.
4. **Explore time ranges:**
   ```
   # Get data for the last 5 minutes
   node_cpu_seconds_total{instance="localhost:9100"}[5m]
   ```
   Note: Range queries like this don't graph in the UI, but are used with functions.
   
   **Query Breakdown:**
   ```
   # Step 1: Start with the basic CPU metric
   node_cpu_seconds_total{instance="localhost:9100"}
   
   # Step 2: Add a time range selector [5m] to get 5 minutes of data points
   # Instead of a single value, you get a range of values over time
   node_cpu_seconds_total{instance="localhost:9100"}[5m]
   ```
   The square brackets `[5m]` change the query from an "instant vector" (single point in time)
   to a "range vector" (series of points over a time range). This is essential for functions 
   like `rate()` that need to calculate changes over time.
5. **Use basic functions:**
   ```
   # Get the sum of all CPU cores for system mode
   sum(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   
   # Get the average
   avg(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   ```
   
   **Query Breakdown:**
   ```
   # Step 1: Filter to get system mode CPU time for all cores
   node_cpu_seconds_total{instance="localhost:9100",mode="system"}
   
   # Step 2a: Sum across all CPU cores
   # This combines values from different CPU cores into one total
   sum(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   
   # Step 2b: Alternative - average across all CPU cores
   # This gives you the mean value across all CPU cores
   avg(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   ```
   These aggregation functions allow you to combine multiple time series into a single value.

## Challenge
- Try using the `count` function to determine how many CPU cores your system has.

<details>
<summary>🧩 <b>Show Solution</b></summary>

- To count the number of CPU cores:
  ```
  count(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}) / count without(mode) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})
  ```
  or more simply:
  ```
  count without(cpu, mode) (node_cpu_seconds_total{instance="localhost:9100"})
  ```

- Regular expression matches:
  - `=~` means "matches regex"
  - `!~` means "doesn't match regex"
  
- Common operators:
  - `+, -, *, /, %, ^`
  - `==, !=, >, <, >=, <=`
  - `and, or, unless`

</details>

---

# 🌟 Now you're ready to explore specific metrics in the next lab!
