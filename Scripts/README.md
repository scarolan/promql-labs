# Helper Scripts for PromQL Labs

This directory contains helper scripts for the PromQL Labs training.

## histogram_traffic_generator.py / .sh

These scripts generate HTTP traffic to Prometheus to populate the histogram metrics used in Lab 9.

### Why you need this

Lab 9 uses `prometheus_http_request_duration_seconds` histogram metrics. If Prometheus hasn't received enough queries, the histogram data may be sparse and some percentile calculations might return unexpected results.

### Usage

**Python version (recommended - cross-platform):**
```bash
# Default: 5 requests/second for 5 minutes
python histogram_traffic_generator.py

# Custom settings
python histogram_traffic_generator.py --url http://localhost:9090 --duration 300 --rps 10
```

**Bash version (Linux/Mac):**
```bash
chmod +x histogram_traffic_generator.sh
./histogram_traffic_generator.sh

# Or with custom settings
PROMETHEUS_URL=http://localhost:9090 DURATION=300 REQUESTS_PER_SECOND=10 ./histogram_traffic_generator.sh
```

### When to run

Run this script **before** starting Lab 9 (Histograms and Quantiles). Let it run for at least 2-3 minutes to generate sufficient histogram data.

---

## install-rules.sh

This script helps students to easily set up Prometheus with the recording and alert rules used in the training.

### What it does

- Creates recording rules for CPU usage (`instance:node_cpu_usage:percent`)
- Creates recording rules for memory usage (`memory_usage_percent`)
- Creates alert rules for high CPU and memory usage
- Sets up a standard Prometheus configuration file
- Restarts Prometheus to apply the changes

### Prerequisites

- Prometheus installed as a system service
- Node Exporter installed and running on port 9100
- Process Exporter installed and running on port 9256 (optional)
- sudo/root access

### Usage

```bash
# Make the script executable
chmod +x install-rules.sh

# Run the script with sudo
sudo ./install-rules.sh
```

### Customization

You may need to modify the script to match your specific environment:

1. Edit the `PROMETHEUS_DIR` variable if your Prometheus configuration is not in `/etc/prometheus`
2. Edit the `PROMETHEUS_SERVICE` variable if your Prometheus service is not named `prometheus`
3. Modify the `scrape_configs` section in the generated `prometheus.yml` if you have different targets

### Troubleshooting

If the script fails to restart Prometheus:

1. Check that the Prometheus service name is correct
2. Try restarting Prometheus manually:
   ```bash
   sudo systemctl restart prometheus
   # or
   sudo service prometheus restart
   ```
3. Check the Prometheus logs:
   ```bash
   sudo journalctl -u prometheus -f
   ```
