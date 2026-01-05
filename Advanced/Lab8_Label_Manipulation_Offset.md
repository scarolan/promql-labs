# 🏷️ Lab 8: Label Manipulation & Offset

## 🎯 Scenario: The Capacity Planning Investigation

> *Your team lead asks: "We're planning infrastructure changes. Can you help analyze how our systems have changed over time and categorize our storage by type?"*
>
> In this lab, you'll learn techniques for reshaping metric labels and comparing current vs. historical data—essential skills for capacity planning and trend analysis.

## Objectives
- Use `label_replace` to add meaningful categorizations to metrics
- Use `label_join` to create composite identifiers
- Master the `offset` modifier for historical comparisons
- Calculate percentage changes over time

## Instructions

### Part 1: Label Manipulation Functions

Sometimes metrics don't have all the labels you need for analysis. Label manipulation functions let you reshape data at query time without changing the underlying metrics.

1. **Categorizing Metrics with `label_replace`:**
   ```promql
   # Add a "disk_type" label to categorize the root filesystem
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
   > **Format:** `label_replace(v instant-vector, dst_label string, replacement string, src_label string, regex string)`

   > 📋 **Real-World Use Case:** Imagine you're building a dashboard that groups storage metrics by tier (SSD vs HDD, or production vs backup). Rather than relying on your exporters to provide these labels, you can add them dynamically based on mountpoint patterns.

2. **Creating Composite Identifiers with `label_join`:**
   ```promql
   # Create a combined "instance_path" label
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
   > **Format:** `label_join(v instant-vector, dst_label string, separator string, src_label1 string, src_label2 string, ...)`

   > 📋 **Real-World Use Case:** When building alerts, you might want a single label that uniquely identifies both the server and the specific disk, making alert messages more informative: "Disk space critical on `web-server-01-/var/log`"

### Part 2: Historical Comparisons with Offset

The `offset` modifier is your time machine—it lets you look at what metrics were doing in the past and compare them to now.

3. **Side-by-Side Historical Comparison:**
   ```promql
   # Compare current CPU usage with 5 minutes ago
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m])) 
   and 
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m] offset 5m))
   ```
   
   > **Explanation:** The `offset` modifier allows you to look back in time. This query displays both the current CPU usage rate and the rate from 5 minutes ago, enabling direct historical comparison.
   
   > 📋 **Real-World Use Case:** During incident response, quickly check if current behavior is abnormal by comparing to recent baselines. In production, you'd typically use longer offsets like `offset 1d` (day-over-day) or `offset 7d` (week-over-week) for meaningful comparisons.

4. **Calculating Change Over Time:**
   ```promql
   # Calculate CPU usage increase from 5 minutes ago
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m])) 
   - 
   sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m] offset 5m))
   ```
   
   > **Explanation:** This query calculates the absolute difference between current CPU usage and usage from 5 minutes ago. Positive values indicate increased usage, while negative values indicate decreased usage.

## ⚠️ Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `offset` inside aggregation | `sum(metric offset 5m)` doesn't work as expected | Put offset on the metric: `sum(metric) offset 5m` or `sum(metric offset 5m)` |
| Forgetting regex in label_replace | The 4th argument is a regex, not a literal string | Use proper regex: `"/"` matches `/`, `".*"` matches anything |
| Offset longer than retention | Querying `offset 30d` when you only have 15d of data | Check your Prometheus retention settings |

## Challenge

> *Your team lead returns: "Great work on the categorization! Now I need to see how memory usage has changed. Can you create a query that shows the percentage change in memory usage compared to 5 minutes ago?"*

Create a query that:
1. Calculates current memory usage percentage
2. Calculates memory usage percentage from 5 minutes ago
3. Shows the percentage change between them

**Bonus:** Adjust your solution to use a 1-minute offset for more responsive feedback.

<details>
<summary>🧠 <b>Show Solution</b></summary>

**Step 1: Current memory usage percentage:**
```promql
100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"}))
```

**Step 2: Memory usage percentage from 5 minutes ago:**
```promql
100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 5m / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 5m))
```

**Step 3: Percentage change calculation:**
```promql
(
  (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})))
  -
  (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 5m / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 5m)))
)
/
(100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 5m / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 5m)))
* 100
```

**Bonus: Using 1-minute offset:**
```promql
(
  (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} / node_memory_MemTotal_bytes{instance="localhost:9100"})))
  -
  (100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1m / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1m)))
)
/
(100 * (1 - (node_memory_MemAvailable_bytes{instance="localhost:9100"} offset 1m / node_memory_MemTotal_bytes{instance="localhost:9100"} offset 1m)))
* 100
```

> **Interpretation:** Positive values mean memory usage increased; negative means it decreased. A value of `5` means usage is 5% higher than before.

</details>

---

# 🌟 [Continue to Lab 9: Subqueries, TopK & Absent](../Advanced/Lab9_Subqueries_TopK_Absent.md)
