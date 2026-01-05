# 📝 Intermediate Checkpoint Quiz

## Test Your Knowledge

Before moving on to Advanced labs, verify your understanding of memory, filesystem, network, and load metrics!

---

### Question 1: Memory Metrics
What's the difference between `MemFree` and `MemAvailable`?

<details>
<summary>Show Answer</summary>

**`MemFree`**: Memory that is completely unused (not even cached)

**`MemAvailable`**: Memory available for new applications, INCLUDING memory that can be reclaimed from caches/buffers

**Best Practice**: Use `MemAvailable` for capacity planning as it's a better indicator of actual usable memory.

```promql
# This is the preferred way to calculate memory usage %
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

</details>

---

### Question 2: Filesystem Queries
Why do we often exclude `tmpfs` filesystems?

```promql
node_filesystem_size_bytes{fstype!="tmpfs"}
```

<details>
<summary>Show Answer</summary>

`tmpfs` is a **temporary filesystem stored in RAM**, not on disk. Including it would:
- Mix memory-backed storage with actual disk storage
- Give misleading disk usage metrics
- Show filesystems that don't persist across reboots

We filter it out to focus on real disk partitions.

</details>

---

### Question 3: Network Rates
What does this query measure?

```promql
sum by (instance) (rate(node_network_receive_bytes_total{device!="lo"}[5m]))
```

<details>
<summary>Show Answer</summary>

This measures the **total network receive throughput per instance** in bytes/second:

- `rate(...[5m])`: Per-second receive rate averaged over 5 minutes
- `device!="lo"`: Excludes loopback (localhost-to-localhost traffic)
- `sum by (instance)`: Combines all network interfaces per host

To convert to megabits/second: multiply by 8 / 1024 / 1024

</details>

---

### Question 4: Load Average
When is a system considered "overloaded" based on load average?

```promql
node_load1 > count(node_cpu_seconds_total{mode="idle"})
```

<details>
<summary>Show Answer</summary>

A system is typically considered overloaded when **load average exceeds the number of CPU cores**.

- `node_load1`: 1-minute load average (average number of processes waiting for CPU)
- If load > core count: processes are waiting for CPU time
- If load < core count: system has spare capacity

The query checks if load1 exceeds the CPU core count, which indicates saturation.

</details>

---

### Question 5: Multi-Metric Correlation
You see high CPU and memory usage at the same time. What PromQL operator helps you alert on this condition?

<details>
<summary>Show Answer</summary>

The **`and`** boolean operator for vector matching:

```promql
(cpu_usage > 80) and on(instance) (memory_usage > 80)
```

- `and`: Both conditions must be true
- `on(instance)`: Match vectors by the `instance` label

This only returns results when BOTH CPU AND memory are high on the same instance.

</details>

---

### Question 6: Practical Scenario
You need to find which disk will fill up first. Which approach is best?

```promql
# Option A
node_filesystem_free_bytes

# Option B
100 * (1 - (node_filesystem_free_bytes / node_filesystem_size_bytes))

# Option C
predict_linear(node_filesystem_free_bytes[24h], 7*24*3600)
```

<details>
<summary>Show Answer</summary>

**Option C** is best for predicting which disk fills up first!

- `predict_linear()` uses linear regression on the last 24 hours of data
- Projects 7 days into the future (7*24*3600 seconds)
- Accounts for the RATE of change, not just current state

**Option B** shows current usage % but doesn't predict trends.

**Option A** just shows raw free bytes with no context.

</details>

---

### Question 7: Label Matching
What's wrong with this query?

```promql
node_filesystem_free_bytes{mountpoint="/"} / node_memory_MemTotal_bytes
```

<details>
<summary>Show Answer</summary>

**Label mismatch!** The filesystem metric has labels like `device`, `fstype`, `mountpoint` that memory metrics don't have.

**Fix**: Use explicit matching:

```promql
node_filesystem_free_bytes{mountpoint="/"} / on(instance) node_memory_MemTotal_bytes
```

The `on(instance)` tells PromQL to only match on the `instance` label, ignoring others.

</details>

---

### Score Yourself

| Score | Next Steps |
|-------|-----------|
| 6-7/7 | 🎉 Ready for Advanced labs! |
| 4-5/7 | Review Labs 3-4 for the concepts you missed |
| 0-3/7 | Practice more with memory/filesystem/network queries |

---

# 🚀 Ready for Advanced Topics? [Continue to Advanced Labs](../Advanced/Lab5_Advanced_CPU_Anomaly.md)
