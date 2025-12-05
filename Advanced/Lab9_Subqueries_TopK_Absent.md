# 🔬 Lab 8b: Subqueries, Ranking & Missing Data Detection

## 🎯 Scenario: The Performance Investigation

> *The SRE team is investigating intermittent performance issues. They ask: "We're seeing occasional slowdowns, but by the time we look at dashboards, everything seems fine. Can you help us find the peak resource usage and identify which processes are the biggest consumers? Also, we need to know immediately if any exporters stop reporting."*
>
> In this lab, you'll learn techniques for analyzing trends over time windows, ranking resource consumers, and detecting when metrics go missing.

## Objectives
- Use subqueries for trend analysis over time windows
- Apply `topk` and `bottomk` functions to find resource hogs
- Use `absent` to detect missing metrics for alerting

## Instructions

### Part 1: Finding Resource Hogs with TopK/BottomK

When troubleshooting performance issues, you often need to find the biggest consumers of a resource quickly.

1. **Find the Top CPU-Consuming Modes:**
   ```promql
   # Find the top 3 CPU-consuming modes
   topk(3, sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])))
   ```
   
   > **Explanation:** The `topk` function selects the 3 highest values from the vector. This query ranks CPU modes by their consumption and shows only the top 3 resource consumers.

   > 📋 **Real-World Use Case:** During an incident, quickly identify what's consuming CPU: Is it user processes? System calls? I/O wait? This directs your investigation.

2. **Find the Least-Used Resources with BottomK:**
   ```promql
   # Find the 3 least-used CPU modes
   bottomk(3, sum by (mode) (rate(node_cpu_seconds_total{instance="localhost:9100"}[5m])))
   ```
   
   > **Explanation:** `bottomk` is the opposite of `topk`—it returns the lowest values. Useful for finding underutilized resources.

   > 📋 **Real-World Use Case:** Capacity planning—find servers or services with the most headroom for additional workload.

3. **TopK with Filesystem Metrics:**
   ```promql
   # Find the top 3 filesystems by usage percentage
   topk(3, 100 * (1 - (node_filesystem_free_bytes{instance="localhost:9100",fstype!="tmpfs"} / node_filesystem_size_bytes{instance="localhost:9100",fstype!="tmpfs"})))
   ```
   
   > **Explanation:** This shows the top 3 filesystems sorted by disk usage percentage—useful for quickly finding which disks are filling up.

### Part 2: Subqueries for Trend Analysis

Subqueries let you analyze how computed values (like rates) have changed over time—essential for finding intermittent spikes that regular queries might miss.

4. **Find Peak CPU Usage Over a Time Window:**
   ```promql
   # What was the maximum CPU usage in any 5-minute window over the last 30 minutes?
   max_over_time(rate(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[5m])[30m:5m])
   ```
   
   > **Explanation:** This subquery:
   > - Calculates the 5-minute rate of CPU usage
   > - Evaluates this every 5 minutes over the last 30 minutes
   > - Returns the maximum value seen
   
   > **Subquery Syntax:** `<inner_query>[<range>:<resolution>]`
   > - `range`: Total time window to analyze (30m)
   > - `resolution`: How often to evaluate the inner query (5m)

   > 📋 **Real-World Use Case:** "Our users complained about slowness around 2 PM, but our 5-minute average dashboard shows everything was fine." Subqueries reveal those brief spikes that averaging hides!

5. **Find Minimum Values (for SLO Analysis):**
   ```promql
   # What was the minimum available memory in the last hour?
   min_over_time(node_memory_MemAvailable_bytes{instance="localhost:9100"}[1h:5m])
   ```
   
   > **Explanation:** This finds the lowest memory availability seen in any 5-minute sample over the last hour. Critical for understanding if you're getting close to resource exhaustion.

### Part 3: Detecting Missing Data

Monitoring your monitoring is crucial. If an exporter stops reporting, you need to know immediately.

6. **Check if a Metric Exists:**
   ```promql
   # This returns nothing if the metric exists (which is good!)
   absent(node_cpu_seconds_total{instance="localhost:9100"})
   ```
   
   > **Explanation:** The `absent` function returns `1` if the metric doesn't exist, and returns nothing if it does exist. This might seem backwards, but it's perfect for alerting.

7. **Test with a Non-Existent Metric:**
   ```promql
   # This WILL return 1 because the metric doesn't exist
   absent(non_existent_metric{instance="localhost:9100"})
   ```
   
   > **Explanation:** Try this query—you'll see it returns `1`, confirming the metric is indeed missing.

   > 📋 **Real-World Use Case:** Create alerts like:
   > ```yaml
   > - alert: NodeExporterDown
   >   expr: absent(node_cpu_seconds_total{job="node"})
   >   for: 5m
   >   annotations:
   >     summary: "Node exporter is not reporting metrics"
   > ```

## ⚠️ Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Subquery resolution too small | `[1h:1s]` creates 3600 data points—very slow! | Use reasonable resolution: `[1h:1m]` or `[1h:5m]` |
| Expecting `absent()` to return data | `absent(existing_metric)` returns empty, not 0 | This is correct behavior—use in alerts, not dashboards |
| TopK with high cardinality | `topk(10, metric)` on millions of series | Filter first, then apply topk |

## Challenge

> *The SRE team needs a comprehensive health check. They ask: "Can you create queries that will help us:*
> 1. *Find the peak CPU usage (any mode) over the last 30 minutes*
> 2. *Identify the top 2 filesystems by usage percentage*
> 3. *Alert us if disk metrics stop reporting"*

<details>
<summary>🧠 <b>Show Solution</b></summary>

**1. Peak CPU usage over 30 minutes:**
```promql
max_over_time(
  (sum(rate(node_cpu_seconds_total{instance="localhost:9100",mode!="idle"}[5m])) * 100)[30m:5m]
)
```

This calculates total non-idle CPU rate, converts to percentage, then finds the max over 30 minutes.

**2. Top 2 filesystems by usage percentage:**
```promql
topk(2, 
  100 * (1 - (
    node_filesystem_free_bytes{instance="localhost:9100",fstype!="tmpfs"} 
    / 
    node_filesystem_size_bytes{instance="localhost:9100",fstype!="tmpfs"}
  ))
)
```

**3. Alert for missing disk metrics:**
```promql
absent(node_filesystem_size_bytes{instance="localhost:9100"})
```

> **Pro Tip:** In a real alerting setup, you'd combine this with `for: 5m` to avoid alerting on brief scrape failures.

</details>

---

# 🌟 [Continue to Lab 9: Histograms and Quantiles](../Advanced/Lab9_Histograms_Quantiles.md)
