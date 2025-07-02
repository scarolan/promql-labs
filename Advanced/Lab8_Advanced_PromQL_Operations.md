# 🔍 Lab 8: Advanced PromQL Operations

## Objectives
- Learn how to use label manipulation functions
- Understand offset modifier for historical comparisons
- Master subqueries for complex time-based analysis
- Use topk and bottomk functions for value ranking

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

2. **Historical Comparisons with Offset:**
   ```
   # Compare current CPU usage with 1 hour ago
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m]))
   and
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m] offset 1h))
   ```
   
   > **Explanation:** The `offset` modifier allows you to look back in time. This query displays both the current CPU usage rate and the rate from exactly 1 hour ago, enabling direct historical comparison. This pattern is extremely useful for day-over-day or week-over-week comparisons.

3. **Finding Resource Hogs with TopK:**
   ```
   # Find the top 3 CPU-consuming processes
   topk(3, sum by (process) (rate(process_cpu_seconds_total{instance="localhost:9100"}[5m])))
   ```
   
   > **Explanation:** The `topk` function selects the 3 highest values from the vector. This query ranks processes by their CPU consumption and shows only the top 3 resource consumers. Replace `topk` with `bottomk` to find the least resource-intensive processes instead.

4. **Using Subqueries for Trend Analysis:**
   ```
   # Calculate the max CPU usage in 5m intervals over the last 30m
   max_over_time(rate(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[5m])[30m:5m])
   ```
   
   > **Explanation:** This subquery calculates the 5-minute rate of CPU usage every 5 minutes over a 30-minute window, then finds the maximum value in that period. Subqueries are powerful for analyzing how rates or other calculations have changed over time, detecting trends, and finding anomalies.

5. **Detecting Missing Data:**
   ```
   # Check if metrics are missing
   absent(node_cpu_seconds_total{instance="localhost:9100"})
   ```
   
   > **Explanation:** The `absent` function returns 1 if the metric doesn't exist, and nothing if it does exist. This is useful for alerting on missing metrics, which could indicate a scrape failure or service outage.

## Challenge
- Create a query that compares current memory usage with memory usage exactly one day ago and calculates the percentage change.

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

2. **For better readability, you could use recording rules to simplify this complex query.**

> **Note:** This query will only work if you have at least 24 hours of historical data. For testing purposes, you might want to use a smaller offset (like `1h` instead of `1d`).

</details>

---

# 🌟 Great work! You've mastered some advanced PromQL techniques!
