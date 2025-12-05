# 📝 Advanced Checkpoint Quiz

## Master-Level Knowledge Check

Congratulations on completing all the advanced labs! Test your mastery of PromQL with these challenging questions.

---

### Question 1: Recording Rules
Why would you use a recording rule instead of running a complex query directly?

<details>
<summary>Show Answer</summary>

**Recording rules** pre-compute expensive queries and store results as new time series:

1. **Performance**: Dashboard loads faster (simple lookup vs. complex calculation)
2. **Consistency**: Same calculation used everywhere
3. **Historical data**: Can query pre-computed values historically
4. **Reduced load**: Prometheus evaluates once, not per dashboard/alert

Example rule:
```yaml
- record: instance:node_cpu_usage:percent
  expr: 100 * (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

</details>

---

### Question 2: Subquery Syntax
What does `[30m:5m]` mean in this query?

```promql
max_over_time(rate(node_cpu_seconds_total{mode="user"}[5m])[30m:5m])
```

<details>
<summary>Show Answer</summary>

**Subquery syntax**: `[range:resolution]`

- `30m`: Look back 30 minutes
- `5m`: Evaluate the inner query every 5 minutes (resolution)

So this evaluates `rate(...[5m])` at 5-minute intervals over the last 30 minutes, then finds the maximum.

**Result**: The peak CPU user rate seen in any 5-minute window over the last half hour.

</details>

---

### Question 3: Vector Matching
What's the difference between `on()` and `ignoring()`?

<details>
<summary>Show Answer</summary>

Both control which labels are used for matching:

**`on(label1, label2)`**: Match ONLY on the specified labels
```promql
metric_a / on(instance) metric_b
# Matches only where 'instance' labels are equal
```

**`ignoring(label1, label2)`**: Match on ALL labels EXCEPT the specified ones
```promql
metric_a / ignoring(device) metric_b
# Matches on all labels except 'device'
```

Use `on()` when vectors have different label sets.
Use `ignoring()` when vectors have mostly the same labels but you need to exclude some.

</details>

---

### Question 4: Group Modifiers
When do you need `group_left()` or `group_right()`?

<details>
<summary>Show Answer</summary>

Use them for **many-to-one** or **one-to-many** joins:

```promql
# Many-to-one: multiple network interfaces joined to one memory metric
rate(node_network_receive_bytes_total{device!="lo"}[5m]) 
  / on(instance) group_left() 
  node_memory_MemTotal_bytes
```

- **`group_left()`**: "Left" side (before operator) has many matching series
- **`group_right()`**: "Right" side (after operator) has many matching series
- **`group_left(extra_label)`**: Bring labels from the "one" side to the result

Without group modifiers, PromQL requires 1:1 cardinality matching.

</details>

---

### Question 5: Histogram Quantiles
What's wrong with this percentile calculation?

```promql
histogram_quantile(0.99, prometheus_http_request_duration_seconds_bucket)
```

<details>
<summary>Show Answer</summary>

**Missing `rate()` and proper grouping!**

Histograms need:
1. `rate()` to calculate the rate of increase in bucket counts
2. Grouping by `le` (the bucket boundary label)

**Correct query**:
```promql
histogram_quantile(0.99, 
  sum by(le) (rate(prometheus_http_request_duration_seconds_bucket[5m]))
)
```

Without `rate()`, you're calculating percentiles over cumulative counts, which is meaningless.

</details>

---

### Question 6: The `absent()` Function
Why does `absent(node_cpu_seconds_total)` return empty when the metric exists?

<details>
<summary>Show Answer</summary>

**That's the intended behavior!**

- `absent()` returns `1` only when the metric is **missing**
- Returns **empty/nothing** when the metric **exists**

This is designed for alerting:
```yaml
- alert: NodeExporterDown
  expr: absent(node_cpu_seconds_total{job="node"})
  # Only fires when the metric is missing
```

Think of it as: "absent returns a value when the metric is absent."

</details>

---

### Question 7: Label Functions
What does this query do?

```promql
label_replace(
  node_filesystem_size_bytes{mountpoint="/"},
  "disk_type", 
  "root", 
  "mountpoint", 
  "/"
)
```

<details>
<summary>Show Answer</summary>

Creates a new label `disk_type` with value `root`:

Parameters:
1. Source metric: `node_filesystem_size_bytes{mountpoint="/"}`
2. New label name: `"disk_type"`
3. Replacement value: `"root"`
4. Source label: `"mountpoint"`
5. Regex to match: `"/"`

**Result**: Same metric but with an additional `disk_type="root"` label.

Useful for grouping/joining metrics that don't share common labels.

</details>

---

### Question 8: Offset Modifier
What's the practical difference between these two queries?

```promql
# Query A
rate(node_cpu_seconds_total[5m]) - rate(node_cpu_seconds_total[5m] offset 1h)

# Query B
delta(rate(node_cpu_seconds_total[5m])[1h:5m])
```

<details>
<summary>Show Answer</summary>

**Query A**: Compares current rate to rate exactly 1 hour ago
- Simple point-in-time comparison
- Might miss trends between the two points

**Query B**: Uses a subquery to track the change over the hour
- `delta()` calculates the difference between first and last value
- More computationally expensive but captures trend

**Best practice**: Use offset for simple before/after comparisons, subqueries for trend analysis.

</details>

---

### Question 9: SLO Calculation
You need 99.9% of requests under 500ms. Which approach is correct?

```promql
# Option A
histogram_quantile(0.999, sum by(le) (rate(http_request_duration_seconds_bucket[5m])))

# Option B
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) 
  / sum(rate(http_request_duration_seconds_count[5m]))
```

<details>
<summary>Show Answer</summary>

**Option B** is correct for SLO measurement!

- **Option A** tells you the latency of the 99.9th percentile request (might be 400ms or 800ms)
- **Option B** tells you what percentage of requests are under 500ms (your SLO target)

For SLOs, you typically want: "X% of requests must be under Y milliseconds"

Option B directly answers: "What percentage of requests met the 500ms SLO?"

</details>

---

### Question 10: Complex Join Challenge
You have these metrics:
- `node_load1{instance, job}`
- `node_cpu_seconds_total{instance, job, cpu, mode}`
- `node_memory_MemAvailable_bytes{instance, job}`

Write a query for: "Load per CPU core, only for instances where memory usage > 50%"

<details>
<summary>Show Answer</summary>

```promql
(
  node_load1 
  / on(instance) 
  count by(instance) (node_cpu_seconds_total{mode="idle"})
)
and on(instance) 
(
  (1 - node_memory_MemAvailable_bytes / on(instance) node_memory_MemTotal_bytes) > 0.5
)
```

**Breakdown**:
1. `node_load1 / count(...)`: Load divided by CPU cores
2. `on(instance)`: Match only on instance label
3. `and on(instance) (memory > 0.5)`: Filter to high-memory instances only

</details>

---

### Score Yourself

| Score | Level |
|-------|-------|
| 9-10/10 | 🏆 **PromQL Master** - You're ready to write production monitoring! |
| 7-8/10 | ⭐ **Advanced** - Solid understanding, review missed concepts |
| 5-6/10 | 📚 **Intermediate** - Revisit Labs 8-10 |
| 0-4/10 | 🔄 **Needs Review** - Go through the Advanced labs again |

---

## 🎓 Congratulations!

You've completed the entire PromQL Labs curriculum! You now have the skills to:

- ✅ Query and filter Prometheus metrics
- ✅ Calculate rates, percentages, and aggregations
- ✅ Build recording rules and alerts
- ✅ Use advanced functions like subqueries and histograms
- ✅ Perform complex vector joins and matching
- ✅ Design SLO-based monitoring

### Next Steps

1. **Practice**: Apply these skills in your own Prometheus environment
2. **Explore**: Check out [PromLabs Blog](https://promlabs.com/blog/) for advanced patterns
3. **Share**: Help others learn PromQL!

---

# 🏠 [Return to Lab Index](../README.md)
