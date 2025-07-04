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

    **Creating Your First Recording Rule:**
    
    Follow these steps on your Ubuntu 22.04 server or Killercoda environment:
    
    1. Create a rules directory if it doesn't exist (you may need sudo permissions):
      ```
      mkdir -p /etc/prometheus/rules
      ```
    
    2. Create a file at `/etc/prometheus/rules/cpu_rules.yml` using your text editor of choice (VS Code, etc.).
      
    3. Copy and paste the YAML above into the file and save it.
    
    4. Open the main Prometheus configuration file at `/etc/prometheus/prometheus.yml` with your text editor.
      
    5. Find the `rule_files` section in the main Prometheus configuration file. It should look like this:

      ```yaml
      # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
      rule_files:
        # - "first_rules.yml"
        # - "second_rules.yml"
      ```

      Remove or comment out the example entries and add your new rule file path:

      ```yaml
      # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
      rule_files:
        - "/etc/prometheus/rules/*.yml"
      ```
      
    6. Reload Prometheus configuration:

      ```
      sudo systemctl restart prometheus
      ```
      
    7. Verify your rule is loaded by visiting Prometheus UI and clicking on "Rules" in the top menu.
   
2. **Test the performance difference:**
   ```
   # Complex query - calculate in real time
   100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m]))))
   ```
   
   ```
   # With a recording rule (faster) - assuming rule is set up
   instance:node_cpu_usage:percent{instance="localhost:9100"}
   ```
   
   > **Explanation:** The first query calculates CPU usage in real-time, which can be resource-intensive. The second query uses a pre-computed recording rule which makes it much faster and more efficient. The recording rule precomputes this complex expression and stores the result under a new metric name `instance:node_cpu_usage:percent`, reducing load on Prometheus and improving dashboard performance.

3. **Learn alert rule structure and create an alert:**
   ```yaml
   groups:
     - name: example_alerts
       rules:
         - alert: HighCPUUsage
           expr: instance:node_cpu_usage:percent > 50
           for: 1m
           labels:
             severity: warning
           annotations:
             summary: "High CPU usage on {{ $labels.instance }}"
             description: "CPU usage has exceeded 50% for 1 minute on {{ $labels.instance }}"
   ```
   
   > **Explanation:** This alert rule configuration demonstrates Prometheus's alerting capabilities. The `expr` field contains the PromQL condition that triggers the alert. The `for` duration prevents flapping alerts by requiring the condition to be true for a specified period. The `labels` help categorize alerts (useful for routing), while `annotations` provide human-readable information with template variables like `{{ $labels.instance }}` that are replaced with actual values when the alert fires.

   We are setting the duration very low (1 minute) to ensure we can test the alert quickly. In production, you would typically set this to a longer duration (e.g., 5 minutes) to avoid alert fatigue from brief spikes.
   
   **Setting Up Your First Alert Rule:**
   
   1. Create a file at `/etc/prometheus/rules/cpu_alerts.yml` using your text editor of choice.
      
   2. Copy and paste the YAML above into the file and save it.
   
   3. The alert is configured to use the recording rule we created earlier (`instance:node_cpu_usage:percent > 50`). If you skipped creating the recording rule or if it's not working, modify the `expr` in your alert file to use the direct calculation instead:
      ```yaml
      expr: 100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance="localhost:9100",mode="idle"}[5m])))) > 50
      ```
      
      Note: You may need to adjust the instance name in the query (e.g., "localhost:9100") to match your environment.
      
   4. Reload Prometheus configuration:
      ```
      sudo systemctl restart prometheus
      ```
      
   5. View your alert rules in the Prometheus UI:
      - Navigate to `http://localhost:9090/alerts` in your browser
      - You should see your HighCPUUsage alert listed
   
   6. To test the alert, you can generate CPU load (if stress-ng is not installed, you may need to install it first with `sudo apt-get install stress-ng`):
      ```
      stress-ng --cpu 1 --cpu-load 50 --timeout 300s
      ```
      This will stress 4 CPU cores for 5 minutes, which should trigger the alert.
      
      Note: If the alert doesn't appear after reloading, check that your recording rule is working correctly by querying `instance:node_cpu_usage:percent` in the Prometheus UI first.

4. **Test alert expressions in the Prometheus UI:**
   ```
   # This would trigger your alert when CPU > 50%
   instance:node_cpu_usage:percent{instance="localhost:9100"} > 50
   ```
   
   > **Explanation:** This query uses the recording rule metric to check if CPU usage exceeds 50%. The alert expression will return no data when CPU usage is below 50% and will return data points when CPU usage exceeds 50%. The Prometheus alert manager uses the `for: 5m` clause in the alert rule to only trigger an alert if this condition persists for at least 5 minutes, reducing alert noise from brief spikes.

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
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage has exceeded 90% for 5 minutes on {{ $labels.instance }}"
```

3. **Create the rules files and apply the changes:**
   
   - Create a file at `/etc/prometheus/rules/memory_rules.yml` using your text editor.
   - Copy the recording rule YAML into this file.
   
   - Create another file at `/etc/prometheus/rules/memory_alerts.yml`.
   - Copy the alert rule YAML into this file.
   
   - Reload Prometheus configuration:
     ```
     sudo systemctl restart prometheus
     ```
     
     Note: Some configurations may support using `curl -X POST http://localhost:9090/-/reload` if Prometheus was started with the `--web.enable-lifecycle` flag, but a restart is more reliable.
   
   4. **Verify your rules are working:**
   
   - Enter this query in the Prometheus UI query box:
     ```
     instance:node_memory_usage:percent
     ```
   
   - If everything is set up correctly, you should see data for this metric.
   - You can also check the Rules section in the Prometheus UI to confirm both rules are loaded.

> **Benefits of using recording rules:**
> - **Performance**: Queries using recording rules execute faster since the computation is done ahead of time
> - **Consistency**: Using the same named metrics ensures consistent results across dashboards
> - **Readability**: Complex expressions are replaced with descriptive metric names
> - **Efficiency**: Reduces the load on Prometheus for frequently used or complex queries
> - **Maintainability**: Easier to update queries in one place when stored as recording rules

</details>

---

# 🌟 [Continue to Lab 8: Advanced PromQL Operations](../Advanced/Lab8_Advanced_PromQL_Operations.md)
