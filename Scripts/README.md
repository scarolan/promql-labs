# Helper Scripts for PromQL Labs

This directory contains helper scripts for the PromQL Labs training.

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
