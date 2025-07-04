# PromQL Queries for Testing
# This file contains all the queries from our labs for automated testing

# Lab 0 - PromQL Fundamentals
lab0_queries = [
    {
        "name": "Basic metric query",
        "query": "node_memory_MemTotal_bytes",
        "expected_type": "vector"
    },
    {
        "name": "Filter by instance",
        "query": "node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Regex filter",
        "query": "node_memory_MemTotal_bytes{instance=~\"local.*\"}",
        "expected_type": "vector"
    },
    {
        "name": "Basic arithmetic",
        "query": "(node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} - node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"}) / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Percentage calculation",
        "query": "100 * ((node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} - node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"}) / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"})",
        "expected_type": "vector"
    },
    {
        "name": "Time range query",
        "query": "node_cpu_seconds_total{instance=\"$INSTANCE\"}[5m]",
        "expected_type": "matrix"
    },
    {
        "name": "Sum function",
        "query": "sum(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"system\"})",
        "expected_type": "vector"
    },
    {
        "name": "Average function",
        "query": "avg(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"system\"})",
        "expected_type": "vector"
    },
    {
        "name": "Count cores (Option 1)",
        "query": "count by(instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"})",
        "expected_type": "vector"
    },
    {
        "name": "Count cores (Option 2)",
        "query": "count without(mode) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"})",
        "expected_type": "vector"
    }
]

# Lab 1 - CPU Exploration
lab1_queries = [
    {
        "name": "Raw CPU metric",
        "query": "node_cpu_seconds_total",
        "expected_type": "vector"
    },
    {
        "name": "Filtered by instance",
        "query": "node_cpu_seconds_total{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Filtered by instance and mode",
        "query": "node_cpu_seconds_total{instance=\"$INSTANCE\", mode=\"user\"}",
        "expected_type": "vector"
    },
    {
        "name": "Filtered by system mode",
        "query": "node_cpu_seconds_total{instance=\"$INSTANCE\", mode=\"system\"}",
        "expected_type": "vector"
    },
    {
        "name": "Filtered by idle mode",
        "query": "node_cpu_seconds_total{instance=\"$INSTANCE\", mode=\"idle\"}",
        "expected_type": "vector"
    }
]

# Lab 2 - CPU Rates
lab2_queries = [
    {
        "name": "CPU rate",
        "query": "rate(node_cpu_seconds_total{instance=\"$INSTANCE\"}[5m])",
        "expected_type": "vector"
    },
    {
        "name": "Sum by mode",
        "query": "sum by (mode) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\"}[5m]))",
        "expected_type": "vector"
    },
    {
        "name": "Sum by mode excluding idle",
        "query": "sum by (mode) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode!=\"idle\"}[5m]))",
        "expected_type": "vector"
    }
]

# Lab 3 - Memory and Filesystem
lab3_queries = [
    {
        "name": "Memory total",
        "query": "node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Memory available",
        "query": "node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage %",
        "query": "100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}))",
        "expected_type": "vector"
    },
    {
        "name": "Filesystem size",
        "query": "node_filesystem_size_bytes{instance=\"$INSTANCE\",fstype!=\"tmpfs\",mountpoint!=\"/run\"}",
        "expected_type": "vector"
    },
    {
        "name": "Filesystem free",
        "query": "node_filesystem_free_bytes{instance=\"$INSTANCE\",fstype!=\"tmpfs\",mountpoint!=\"/run\"}",
        "expected_type": "vector"
    },
    {
        "name": "Disk usage % for root",
        "query": "100 * (1 - (node_filesystem_free_bytes{instance=\"$INSTANCE\",mountpoint=\"/\"} / node_filesystem_size_bytes{instance=\"$INSTANCE\",mountpoint=\"/\"}))",
        "expected_type": "vector"
    }
]

# Lab 4 - Network and Load
lab4_queries = [
    {
        "name": "Network receive rate",
        "query": "rate(node_network_receive_bytes_total{instance=\"$INSTANCE\",device!=\"lo\"}[5m])",
        "expected_type": "vector"
    },
    {
        "name": "Network transmit rate",
        "query": "rate(node_network_transmit_bytes_total{instance=\"$INSTANCE\",device!=\"lo\"}[5m])",
        "expected_type": "vector"
    },
    {
        "name": "Load 1m",
        "query": "node_load1{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Load 5m",
        "query": "node_load5{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Load 15m",
        "query": "node_load15{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    },
    {
        "name": "Aggregated network receive",
        "query": "sum by (instance) (rate(node_network_receive_bytes_total{instance=\"$INSTANCE\",device!=\"lo\"}[5m]))",
        "expected_type": "vector"
    },
    {
        "name": "Aggregated network transmit",
        "query": "sum by (instance) (rate(node_network_transmit_bytes_total{instance=\"$INSTANCE\",device!=\"lo\"}[5m]))",
        "expected_type": "vector"
    },
    {
        "name": "Load compared to CPU cores",
        "query": "node_load1{instance=\"$INSTANCE\"} > on(instance) count by(instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"})",
        "expected_type": "vector"
    },
    {
        "name": "Load divided by CPU cores",
        "query": "node_load1{instance=\"$INSTANCE\"} / on(instance) count by(instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"})",
        "expected_type": "vector"
    }
]

# Lab 5 - Advanced CPU Anomaly Detection
lab5_queries = [
    {
        "name": "CPU saturation detection",
        "query": "max_over_time((100 * (1 - (sum by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))))[30m:1m])",
        "expected_type": "vector"
    },
    {
        "name": "CPU spikes using increase",
        "query": "increase(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"user\"}[10m])",
        "expected_type": "vector"
    },
    {
        "name": "Max increase over time",
        "query": "max_over_time(increase(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"user\"}[1m])[30m:1m])",
        "expected_type": "vector"
    },
    {
        "name": "User mode avg percentage over time",
        "query": "max_over_time((avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"user\"}[1m])) * 100)[30m:1m])",
        "expected_type": "vector"
    }
]

# Lab 6 - Correlating Metrics
lab6_queries = [
    {
        "name": "CPU usage %",
        "query": "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"})))",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage %",
        "query": "100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}))",
        "expected_type": "vector"
    },
    {
        "name": "Network receive rate aggregate",
        "query": "sum by (instance) (rate(node_network_receive_bytes_total{instance=\"$INSTANCE\",device!=\"lo\"}[5m]))",
        "expected_type": "vector"
    },
    {
        "name": "High CPU and Memory alert",
        "query": "(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))) > bool 80) and on(instance) (100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"})) > bool 80)",
        "expected_type": "vector"
    },
    {
        "name": "High CPU alert boolean",
        "query": "(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))) > bool 80)",
        "expected_type": "vector"
    },
    {
        "name": "High memory alert boolean",
        "query": "(100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"})) > bool 80)",
        "expected_type": "vector"
    }
]

# Lab 7 - Recording Rules and Alerting
lab7_queries = [
    {
        "name": "CPU usage for recording rule",
        "query": "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m]))))",
        "expected_type": "vector"
    },
    {
        "name": "Alert expression simulation",
        "query": "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))) > 80",
        "expected_type": "vector"
    },
    {
        "name": "CPU recording rule query",
        "query": "instance:node_cpu_usage:percent{instance=\"$INSTANCE\"}",
        "expected_type": "vector"
    }
]

# Lab 8 - Advanced PromQL Operations
lab8_queries = [
    {
        "name": "Label replace function",
        "query": "label_replace(node_filesystem_size_bytes{instance=\"$INSTANCE\",mountpoint=\"/\"}, \"disk_type\", \"root_disk\", \"mountpoint\", \"/\")",
        "expected_type": "vector"
    },
    {
        "name": "Label join function",
        "query": "label_join(node_filesystem_size_bytes{instance=\"$INSTANCE\",mountpoint=\"/\"}, \"instance_path\", \"-\", \"instance\", \"mountpoint\")",
        "expected_type": "vector"
    },
    {
        "name": "Historical comparison with offset",
        "query": "sum(rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode!=\"idle\"}[5m])) and sum(rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode!=\"idle\"}[5m] offset 5m))",
        "expected_type": "vector"
    },
    {
        "name": "Historical difference calculation",
        "query": "sum(rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode!=\"idle\"}[5m])) - sum(rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode!=\"idle\"}[5m] offset 5m))",
        "expected_type": "vector"
    },
    {
        "name": "Top K resources",
        "query": "topk(3, sum by (mode) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\"}[5m])))",
        "expected_type": "vector"
    },
    {
        "name": "Subquery for trend analysis",
        "query": "max_over_time(rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"user\"}[5m])[30m:5m])",
        "expected_type": "vector"
    },
    {
        "name": "Detecting missing data",
        "query": "absent(node_cpu_seconds_total{instance=\"$INSTANCE\"})",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage change with offset",
        "query": "(100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"})) - 100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} offset 5m / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} offset 5m))) / (100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} offset 5m / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} offset 5m))) * 100",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage with offset 5m",
        "query": "100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} offset 5m / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} offset 5m))",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage change with offset 1m",
        "query": "((100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"}))) - (100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} offset 1m / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} offset 1m)))) / (100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$INSTANCE\"} offset 1m / node_memory_MemTotal_bytes{instance=\"$INSTANCE\"} offset 1m))) * 100",
        "expected_type": "vector"
    },
    {
        "name": "Memory usage percent change",
        "query": "(memory_usage_percent - memory_usage_percent offset 5m) / memory_usage_percent offset 5m * 100",
        "expected_type": "vector"
    }
]

# Lab 9 - Histograms and Quantiles
lab9_queries = [
    {
        "name": "Histogram bucket exploration",
        "query": "prometheus_http_request_duration_seconds_bucket",
        "expected_type": "vector"
    },
    {
        "name": "Histogram specific handler",
        "query": "prometheus_http_request_duration_seconds_bucket{handler=\"/api/v1/query\"}",
        "expected_type": "vector"
    },
    {
        "name": "95th percentile latency",
        "query": "histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))",
        "expected_type": "vector"
    },
    {
        "name": "90th percentile latency",
        "query": "histogram_quantile(0.9, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))",
        "expected_type": "vector"
    },
    {
        "name": "Median latency by handler",
        "query": "histogram_quantile(0.5, sum by (handler, le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))",
        "expected_type": "vector"
    },
    {
        "name": "SLO calculation - success rate",
        "query": "(sum(rate(prometheus_http_request_duration_seconds_bucket{le=\"0.5\"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100",
        "expected_type": "vector"
    },
    {
        "name": "SLO calculation - error rate",
        "query": "(1 - sum(rate(prometheus_http_request_duration_seconds_bucket{le=\"0.5\"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100",
        "expected_type": "vector"
    },
    {
        "name": "Gauge derivative",
        "query": "deriv(node_memory_Active_bytes{instance=\"$INSTANCE\"}[5m])",
        "expected_type": "vector"
    },
    {
        "name": "Linear prediction",
        "query": "predict_linear(node_memory_Active_bytes{instance=\"$INSTANCE\"}[5m], 300)",
        "expected_type": "vector"
    },
    {
        "name": "CPU usage synthetic histogram",
        "query": "sum(count_values(\"le\", floor(clamp_max(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))), 100) / 5) * 5)) by (le)",
        "expected_type": "vector"
    },
    {
        "name": "CPU usage bucketed into 5% ranges",
        "query": "floor(clamp_max(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=\"$INSTANCE\",mode=\"idle\"}))), 100) / 5) * 5",
        "expected_type": "vector"
    }
]

# All queries combined
all_queries = (
    lab0_queries + 
    lab1_queries + 
    lab2_queries + 
    lab3_queries +
    lab4_queries +
    lab5_queries +
    lab6_queries +
    lab7_queries +
    lab8_queries +
    lab9_queries
)
