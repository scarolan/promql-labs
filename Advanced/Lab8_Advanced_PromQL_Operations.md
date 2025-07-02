# 🔍 Lab 8: Advanced PromQL Operations

## Objectives
- Learn how to use label manipulation functions
- Understand the offset modifier for historical comparisons
- Master subqueries for complex time-based analysis
- Use topk and bottomk functions for value ranking
- Apply the absent function to detect missing metrics

## Instructions

1. **Using Label Manipulation Functions:**
   ```
   # Transform metric labels with label_replace
   label_replace(
     node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"},
     "disk_type",
     "root_disk",
     "mountpoint",
     "/"
   )
   ```
   
   > **Explanation:** The `label_replace` function adds a new label `disk_type` with value `root_disk` to metrics where the `mountpoint` label matches the regex pattern `/`. This is useful for categorizing or grouping metrics by adding meaningful labels at query time.
   >
   > **Format:** `label_replace(v instant-vector, dst_label string, replacement string, src_label string, regex string)` - Matches the regex against the src_label and creates/replaces the dst_label with the replacement text.

   Another useful label manipulation function is `label_join`:
   
   ```
   # Join labels with label_join
   label_join(
     node_filesystem_size_bytes{instance="localhost:9100",mountpoint="/"},
     "instance_path",
     "-",
     "instance",
     "mountpoint"
   )
   ```
   
   > **Explanation:** The `label_join` function creates a new label `instance_path` by joining the values of the `instance` and `mountpoint` labels with the separator `-`. The result would be a label like `instance_path="localhost:9100-/"`.
   >
   > **Format:** `label_join(v instant-vector, dst_label string, separator string, src_label1 string, src_label2 string, ...)` - Joins all source label values with the separator and stores the result in the destination label.

2. **Historical Comparisons with Offset:**
   ```
   # Compare current CPU usage with 1 hour ago
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m])) and sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m] offset 1h))
   ```
   
   > **Explanation:** The `offset` modifier allows you to look back in time. This query displays both the current CPU usage rate and the rate from exactly 1 hour ago, enabling direct historical comparison. This pattern is extremely useful for day-over-day or week-over-week comparisons.
   
   You can also calculate the difference between current and historical values:
   
   ```
   # Calculate CPU usage increase from 1 hour ago
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m])) - sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m] offset 1h))
   ```
   
   > **Explanation:** This query calculates the absolute difference between current CPU usage and usage from 1 hour ago. Positive values indicate increased usage, while negative values indicate decreased usage.

3. **Finding Resource Hogs with TopK:**
   ```
   # Find the top 3 CPU-consuming modes
   topk(3, sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])))
   ```
   
   > **Explanation:** The `topk` function selects the 3 highest values from the vector. This query ranks CPU modes by their consumption and shows only the top 3 resource consumers. Replace `topk` with `bottomk` to find the least resource-intensive modes instead.
   >
   > **Note:** For process-specific metrics, you would need the process exporter running. If it's available, you could use this query. Note that the process exporter "instance" is running on port 9256.
   > ```
   > topk(3, sum by (groupname) (rate(namedprocess_namegroup_cpu_seconds_total{instance="localhost:9256"}[5m])))
   > ```

4. **Using Subqueries for Trend Analysis:**
   ```
   # Calculate the max CPU usage in 5m intervals over the last 30m
   max_over_time(rate(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[5m])[30m:5m])
   ```
   
   > **Explanation:** This subquery calculates the 5-minute rate of CPU usage every 5 minutes over a 30-minute window, then finds the maximum value in that period. Subqueries are powerful for analyzing how rates or other calculations have changed over time, detecting trends, and finding anomalies.
   >
   > **Subquery Syntax:** `<inner_query>[<range>:<resolution>]`
   > - `inner_query`: The query to be executed at each resolution step
   > - `range`: Total time window to analyze (e.g., 30m)
   > - `resolution`: How frequently to evaluate the inner query (e.g., 5m)

5. **Detecting Missing Data:**
   ```
   # Check if metrics are missing
   absent(node_cpu_seconds_total{instance="localhost:9100"})
   ```
   
   > **Explanation:** The `absent` function returns 1 if the metric doesn't exist, and nothing if it does exist. This is useful for alerting on missing metrics, which could indicate a scrape failure or service outage.
   >
   > **Testing Tip:** To see this function in action, you can query for a non-existent metric:
   > ```
   > absent(non_existent_metric{instance="localhost:9100"})
   > ```
   > This should return a value of 1, confirming that the metric is indeed missing.

## Challenge
- Create a query that compares current memory usage with memory usage exactly one day ago and calculates the percentage change.
- Bonus: Try to make your solution work even if your Prometheus server has less than 24 hours of data by using a shorter offset.

<details>
<summary>🧠 <b>Show Solution</b></summary>

To compare current memory usage with memory usage from one day ago and calculate the percentage change:

1. **Build the query step by step:**

   **Step 1: Create a query for current memory usage percentage:**
   ```
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
   ```

   **Step 2: Create a query for memory usage percentage from one day ago:**
   ```
   100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1d / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1d))
   ```

   **Step 3: Calculate the percentage change between them:**
   ```
   (
     (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})))
     -
     (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1d / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1d)))
   )
   /
   (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1d / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1d)))
   * 100
   ```

   The final query calculates the percent difference by:
   1. Subtracting the old memory usage from the current usage
   2. Dividing by the old usage to get the relative change
   3. Multiplying by 100 to convert to a percentage

   Positive values indicate increased memory usage compared to yesterday, while negative values indicate decreased usage.

2. **For testing in environments with limited historical data:**
   ```
   # Use 1h offset instead of 1d
   (
     (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})))
     -
     (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1h / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1h)))
   )
   /
   (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1h / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1h)))
   * 100
   ```

3. **For better readability in production, you could use recording rules to simplify this complex query:**
   ```yaml
   # In prometheus.yml rules section:
   groups:
     - name: memory_usage
       rules:
         - record: memory_usage_percent
           expr: 100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
   ```

   Then you could write a simpler comparison query:
   ```
   (memory_usage_percent - memory_usage_percent offset 1d) / memory_usage_percent offset 1d * 100
   ```

> **Note:** The offset duration (1d, 1h, etc.) must be less than or equal to your Prometheus retention period. If you're just setting up Prometheus, start with a small offset like 15m or 1h.

</details>

---

# 🌟 [Continue to Lab 9: Histograms and Quantiles](../Advanced/Lab9_Histograms_Quantiles.md)
