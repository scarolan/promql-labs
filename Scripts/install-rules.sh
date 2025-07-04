#!/bin/bash
# install-rules.sh
# 
# This script installs Prometheus recording and alert rules from the PromQL Labs training
# It overwrites the existing prometheus.yml file with a known working configuration
# Finally, it restarts Prometheus to apply the changes
#
# Usage: sudo ./install-rules.sh
#
# NOTE: This script assumes Prometheus is installed as a service named 'prometheus'
#       If your service name is different, edit the PROMETHEUS_SERVICE variable below

set -e  # Exit on any error

# Configuration variables - edit these to match your environment
PROMETHEUS_DIR="/etc/prometheus"
PROMETHEUS_SERVICE="prometheus"

# Check if running as root (required for service operations)
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root or with sudo."
    exit 1
fi

echo "=== PromQL Labs - Installing Prometheus Rules ==="
echo ""

# Create rules directory if it doesn't exist
mkdir -p ${PROMETHEUS_DIR}/rules

echo "Creating recording rules..."

# Create CPU recording rules
cat > ${PROMETHEUS_DIR}/rules/cpu_rules.yml <<EOF
groups:
  - name: cpu_rules
    rules:
      - record: instance:node_cpu_usage:percent
        expr: 100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) / count by (instance) (node_cpu_seconds_total{mode="idle"})))
EOF

echo "✅ Created CPU recording rules"

# Create memory recording rules
cat > ${PROMETHEUS_DIR}/rules/memory_rules.yml <<EOF
groups:
  - name: memory_usage
    rules:
      - record: memory_usage_percent
        expr: 100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
EOF

echo "✅ Created memory recording rules"

# Create alert rules
cat > ${PROMETHEUS_DIR}/rules/alert_rules.yml <<EOF
groups:
  - name: alerts
    rules:
      - alert: HighCPUUsage
        expr: instance:node_cpu_usage:percent > 80
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% on {{ \$labels.instance }}"
      
      - alert: HighMemoryUsage
        expr: memory_usage_percent > 80
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 80% on {{ \$labels.instance }}"
EOF

echo "✅ Created alert rules"

# Create new prometheus.yml with the rules included
cat > ${PROMETHEUS_DIR}/prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/cpu_rules.yml"
  - "rules/memory_rules.yml"
  - "rules/alert_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
        
  - job_name: 'process'
    static_configs:
      - targets: ['localhost:9256']

  # If you have other exporters, add them here
EOF

echo "✅ Created new prometheus.yml configuration"
echo ""

# Set correct permissions
echo "Setting correct permissions..."
chown -R prometheus:prometheus ${PROMETHEUS_DIR}/rules/
chmod 644 ${PROMETHEUS_DIR}/prometheus.yml ${PROMETHEUS_DIR}/rules/*.yml

echo "✅ Set correct permissions on rule files"
echo ""

# Validate configuration
echo "Validating Prometheus configuration..."
if command -v promtool &>/dev/null; then
    if promtool check config ${PROMETHEUS_DIR}/prometheus.yml; then
        echo "✅ Configuration validated successfully"
    else
        echo "❌ Configuration validation failed"
        echo "Please check your configuration manually"
        exit 1
    fi
else
    echo "⚠️ promtool not found, skipping configuration validation"
    echo "  (Configuration will be validated when Prometheus restarts)"
fi

echo ""

# Restart Prometheus
echo "Restarting Prometheus service..."
if systemctl restart ${PROMETHEUS_SERVICE}; then
    echo "✅ Prometheus service restarted successfully"
else
    echo "❌ Failed to restart Prometheus service"
    echo "Trying alternative service management..."
    
    # Try alternative service management methods
    if service ${PROMETHEUS_SERVICE} restart; then
        echo "✅ Prometheus service restarted successfully (using service command)"
    else
        echo "❌ Failed to restart Prometheus service"
        echo ""
        echo "Please restart Prometheus manually using one of these commands:"
        echo "  sudo systemctl restart ${PROMETHEUS_SERVICE}"
        echo "  sudo service ${PROMETHEUS_SERVICE} restart"
        exit 1
    fi
fi

echo ""
echo "=== Installation Complete! ==="
echo ""
echo "Recording rules installed:"
echo "  - instance:node_cpu_usage:percent"
echo "  - memory_usage_percent"
echo ""
echo "Alert rules installed:"
echo "  - HighCPUUsage (>80% for 1m)"
echo "  - HighMemoryUsage (>80% for 1m)"
echo ""
echo "You can verify the rules are working by visiting:"
echo "  http://localhost:9090/rules"
echo ""
echo "To check if your rules are working, try these PromQL queries:"
echo "  instance:node_cpu_usage:percent"
echo "  memory_usage_percent"
echo ""
