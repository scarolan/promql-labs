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
   
   > **Explanation:** Recording rules are a powerful Prometheus feature that saves complex calculations as new metrics. The example above creates a new metric called `instance:node_cpu_usage:percent` that stores pre-calculated CPU usage percentages. This follows Prometheus naming conventions with colons separating the context (`instance`), metric name (`node_cpu_usage`), and unit (`percent`).
   
2. **Test the performance difference:**
   ```
   # Complex query - calculate in real time
   100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))))
   
   # With a recording rule (faster) - assuming rule is set up
   instance:node_cpu_usage:percent{instance="localhost:9100"}
   ```
   
   > **Explanation:** The first query calculates CPU usage in real-time, which can be resource-intensive. The second query uses a pre-computed recording rule which makes it much faster and more efficient. The recording rule precomputes this complex expression and stores the result under a new metric name `instance:node_cpu_usage:percent`, reducing load on Prometheus and improving dashboard performance.

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
   
   > **Explanation:** This alert rule configuration demonstrates Prometheus's alerting capabilities. The `expr` field contains the PromQL condition that triggers the alert. The `for` duration prevents flapping alerts by requiring the condition to be true for a specified period. The `labels` help categorize alerts (useful for routing), while `annotations` provide human-readable information with template variables like `{{ $labels.instance }}` that are replaced with actual values when the alert fires.

4. **Test alert expressions:**
   ```
   # This would trigger your alert when CPU > 80%
   instance:node_cpu_usage:percent{instance="localhost:9100"} > 80
   ```
   
   > **Explanation:** This query uses the recording rule metric to check if CPU usage exceeds 80%. The alert expression will return no data when CPU usage is below 80% and will return data points when CPU usage exceeds 80%. The Prometheus alert manager uses the `for: 5m` clause in the alert rule to only trigger an alert if this condition persists for at least 5 minutes, reducing alert noise from brief spikes.

## Challenge
- Create a recording rule expression for memory usage percentage, following Prometheus naming conventions.

<details>
<summary>🛡️ <b>Show Solution</b></summary>

To create a recording rule for memory usage percentage following Prometheus naming conventions:

1. **Create the recording rule configuration** in your `prometheus.yml` file or a separate rules file:

```yaml
groups:
  - name: memory_rules
    rules:
      - record: instance:node_memory_usage:percent
        expr: 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

The name `instance:node_memory_usage:percent` follows Prometheus naming conventions:
- `instance:` prefix indicates it's an instance-level metric
- `node_memory_usage` describes the metric's purpose
- `:percent` suffix indicates the unit

2. **Create an alert rule that uses this recording rule**:

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

3. **Reload Prometheus** to apply your new rules:
   - API: `curl -X POST http://localhost:9090/-/reload`
   - Or restart the Prometheus service

> **Benefits of using recording rules:**
> - **Performance**: Queries using recording rules execute faster since the computation is done ahead of time
> - **Consistency**: Using the same named metrics ensures consistent results across dashboards
> - **Readability**: Complex expressions are replaced with descriptive metric names
> - **Efficiency**: Reduces the load on Prometheus for frequently used or complex queries
> - **Maintainability**: Easier to update queries in one place when stored as recording rules

</details>

</details>

---

# 🌟 [Click here to continue to Lab 8: Advanced PromQL Operations](../Advanced/Lab8_Advanced_PromQL_Operations.md)
