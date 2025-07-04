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
   ```
   
   ```
   # Filter by instance
   node_memory_MemTotal_bytes{instance="localhost:9100"}
   ```
   
   ```
   # Use regular expressions for label matching
   node_memory_MemTotal_bytes{instance=~"local.*"}
   ```
   
   > **Explanation:** These queries show how to query a metric by name and filter results using labels. The first returns all instances of the metric, the second filters to a specific instance, and the third uses a regex pattern to match multiple instances.
3. **Try basic operators:**
   ```
   # Division - Calculate memory used as fraction of total
   (node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"}
   ```
   
   ```
   # Multiplication - Convert to percentage
   100 * ((node_memory_MemTotal_bytes{instance="localhost:9100"} - node_memory_MemAvailable_bytes{instance="localhost:9100"}) / node_memory_MemTotal_bytes{instance="localhost:9100"})
   ```
   
   > **Explanation:** These queries demonstrate how PromQL allows you to perform calculations directly in your query. The first calculates memory usage as a fraction (0-1), while the second converts it to a percentage (0-100%).
4. **Explore time ranges:**
   ```
   # Get data for the last 5 minutes
   node_cpu_seconds_total{instance="localhost:9100"}[5m]
   ```
   
   > **Note:** Range queries like this don't graph in the UI, but are used with functions. The square brackets `[5m]` change the query from an "instant vector" (single point in time) to a "range vector" (series of points over a time range). This is essential for functions like `rate()` that need to calculate changes over time.
5. **Use basic functions:**
   ```
   # Get the sum of all CPU cores for system mode
   sum(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   ```
   
   ```
   # Get the average
   avg(node_cpu_seconds_total{instance="localhost:9100",mode="system"})
   ```
   
   > **Explanation:** These aggregation functions allow you to combine multiple time series into a single value. `sum()` adds up values from all CPU cores, while `avg()` calculates the mean value across all cores.

## Challenge
- Try using the `count` function to determine how many CPU cores your system has.

<details>
<summary>🧩 <b>Show Solution</b></summary>

To count the number of CPU cores, you have two options:

**Option 1 (Simple and Direct):**
```
count by(instance) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})
```

This approach counts the number of CPU cores by grouping by instance and filtering for the idle mode.

**Option 2 (Alternative Approach):**
```
count without(mode, cpu) (node_cpu_seconds_total{instance="localhost:9100",mode="idle"})
```

This counts the CPU cores by preserving all labels except the mode and cpu labels, while still filtering for just the idle mode.

**Helpful Operators for Future Reference:**

For regular expression matches:
- `=~` means "matches regex" (e.g., `{instance=~"local.*"}`)
- `!~` means "doesn't match regex" (e.g., `{instance!~"test.*"}`)
  
For mathematical and logical operations:
- Arithmetic: `+, -, *, /, %, ^`
- Comparison: `==, !=, >, <, >=, <=`
- Logical: `and, or, unless`

</details>

---

# 🌟 [Continue to Lab 1: Exploring CPU Metrics](../Beginner/Lab1_CPU_Exploration.md)
