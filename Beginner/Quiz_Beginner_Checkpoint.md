# 📝 Beginner Checkpoint Quiz

## Test Your Knowledge

Before moving on to Intermediate labs, make sure you understand these fundamental concepts!

---

### Question 1: Metric Types
What type of Prometheus metric is `node_cpu_seconds_total`?

<details>
<summary>Show Answer</summary>

**Counter** - The `_total` suffix indicates this is a counter metric that only increases (or resets). It tracks the cumulative CPU seconds used.

</details>

---

### Question 2: Label Filtering
What does this query return?

```promql
node_cpu_seconds_total{mode="idle", instance="localhost:9100"}
```

<details>
<summary>Show Answer</summary>

Returns the `node_cpu_seconds_total` metric filtered to only show:
- Idle CPU time (`mode="idle"`)
- From the specific instance `localhost:9100`

This gives you one time series per CPU core showing accumulated idle time.

</details>

---

### Question 3: Rate Function
Why do we use `rate()` with counter metrics?

<details>
<summary>Show Answer</summary>

Counters only go up, so their raw values aren't very useful. `rate()` calculates:
- The **per-second average rate of increase** over a time window
- Properly handles counter resets

Example: `rate(node_cpu_seconds_total{mode="user"}[5m])` tells you how much CPU time per second was spent in user mode, averaged over 5 minutes.

</details>

---

### Question 4: Aggregation
What's the difference between these two queries?

```promql
# Query A
sum(rate(node_cpu_seconds_total{mode="user"}[5m]))

# Query B
sum by (instance) (rate(node_cpu_seconds_total{mode="user"}[5m]))
```

<details>
<summary>Show Answer</summary>

**Query A:** Returns a single value - the total user CPU rate across ALL cores and ALL instances.

**Query B:** Returns one value per instance - the total user CPU rate summed across cores but kept separate per instance.

`by (label)` preserves that label in the output, grouping results by it.

</details>

---

### Question 5: Range Vectors
What does `[5m]` mean in this query?

```promql
rate(node_cpu_seconds_total[5m])
```

<details>
<summary>Show Answer</summary>

`[5m]` creates a **range vector** - it selects all data points from the last 5 minutes for each time series.

Functions like `rate()`, `increase()`, `avg_over_time()` require range vectors because they need multiple data points to calculate trends.

</details>

---

### Question 6: Practical Application
You want to see CPU usage as a percentage. Which query is correct?

```promql
# Option A
node_cpu_seconds_total{mode="idle"} / node_cpu_seconds_total

# Option B  
100 * (1 - rate(node_cpu_seconds_total{mode="idle"}[5m]))

# Option C
100 * (1 - (sum(rate(node_cpu_seconds_total{mode="idle"}[5m])) / count(rate(node_cpu_seconds_total{mode="idle"}[5m]))))
```

<details>
<summary>Show Answer</summary>

**Option C** is the most accurate for overall CPU usage percentage:

1. Calculate idle rate per core
2. Sum all idle rates
3. Divide by core count to get average idle %
4. Subtract from 1 to get usage %
5. Multiply by 100 for percentage

**Option A** is wrong - you can't divide counters directly without using `rate()`.

**Option B** is partially correct but assumes single-core or gives per-core results.

</details>

---

### Score Yourself

| Score | Next Steps |
|-------|-----------|
| 6/6 | 🎉 Ready for Intermediate labs! |
| 4-5/6 | Review the labs where you missed questions |
| 0-3/6 | Revisit Labs 0-2 before continuing |

---

# 🚀 Ready for More? [Continue to Intermediate Labs](../Intermediate/Lab3_Memory_Filesystem.md)
