# 🚨 Lab 7: Recording Rules and Alerting

## Objectives
- Understand Prometheus recording rules
- Create efficient, reusable PromQL queries
- Build effective alerting rules

## Instructions
1. **Understand recording rules:**
   Recording rules let you precompute frequently used or complex queries and save their results.

   Example recording rule file format:
   ```yaml
   groups:
     - name: cpu_rules
       rules:
         - record: instance:node_cpu_usage:percent
           expr: 100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m]))))
   ```
   
2. **Test the performance difference:**
   ```
   # Complex query - calculate in real time
   100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))))
   
   # With a recording rule (faster) - assuming rule is set up
   instance:node_cpu_usage:percent{instance="localhost:9100"}
   ```
   
   **Complex Query Breakdown:**
   ```
   # Step 1: Get rate of idle CPU time over 5m
   rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])
   
   # Step 2: Average across CPU cores for each instance
   avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))
   
   # Step 3: Convert from idle percentage to used percentage
   100 * (1 - (idle percentage))
   ```
   
   The recording rule precomputes this complex expression and stores the result under a new metric name `instance:node_cpu_usage:percent`, making queries much faster and reducing load on Prometheus.

3. **Learn alert rule structure:**
   ```yaml
   groups:
     - name: example_alerts
       rules:
         - alert: HighCPUUsage
           expr: instance:node_cpu_usage:percent > 80
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High CPU usage on {{ $labels.instance }}"
             description: "CPU usage has exceeded 80% for 5 minutes on {{ $labels.instance }}"
   ```

4. **Test alert expressions:**
   ```
   # This would trigger your alert when CPU > 80%
   instance:node_cpu_usage:percent{instance="localhost:9100"} > 80
   ```
   
   **Alert Expression Breakdown:**
   ```
   # Step 1: Use the precomputed CPU usage percentage from recording rule
   instance:node_cpu_usage:percent{instance="localhost:9100"}
   
   # Step 2: Apply a threshold comparison (> 80%)
   instance:node_cpu_usage:percent{instance="localhost:9100"} > 80
   ```
   
   The alert expression will return no data when CPU usage is below 80% and will return data points when CPU usage exceeds 80%. The Prometheus alert manager then uses the `for: 5m` clause to only trigger an alert if this condition persists for at least 5 minutes.

## Challenge
- Create a recording rule expression for memory usage percentage, following Prometheus naming conventions.

<details>
<summary>🛡️ <b>Show Solution</b></summary>

Recording rule for memory usage:

```yaml
groups:
  - name: memory_rules
    rules:
      - record: instance:node_memory_usage:percent
        expr: 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

Alert rule using this recording rule:

```yaml
groups:
  - name: memory_alerts
    rules:
      - alert: HighMemoryUsage
        expr: instance:node_memory_usage:percent > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage has exceeded 90% for 5 minutes on {{ $labels.instance }}"
```

Benefits of recording rules:
- Improved query performance
- Consistent metrics across dashboards
- Better readability for complex expressions
- Reduced load on Prometheus

</details>

---

# 🌟 Congratulations! You've completed all the PromQL labs!
