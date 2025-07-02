# PowerShell version of the queries data
# This contains all the PromQL queries from our labs for automated testing

# Lab 0 - PromQL Fundamentals
$lab0_queries = @(
    @{
        Name = "Basic metric query"
        Query = "node_memory_MemTotal_bytes"
        ExpectedType = "vector"
    },
    @{
        Name = "Filter by instance" 
        Query = "node_memory_MemTotal_bytes{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Regex filter"
        Query = "node_memory_MemTotal_bytes{instance=~`"local.*`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Basic arithmetic"
        Query = "(node_memory_MemTotal_bytes{instance=`"$instanceName`"} - node_memory_MemAvailable_bytes{instance=`"$instanceName`"}) / node_memory_MemTotal_bytes{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Percentage calculation"
        Query = "100 * ((node_memory_MemTotal_bytes{instance=`"$instanceName`"} - node_memory_MemAvailable_bytes{instance=`"$instanceName`"}) / node_memory_MemTotal_bytes{instance=`"$instanceName`"})"
        ExpectedType = "vector"
    },
    @{
        Name = "Time range query"
        Query = "node_cpu_seconds_total{instance=`"$instanceName`"}[5m]"
        ExpectedType = "matrix"
    },
    @{
        Name = "Sum function"
        Query = "sum(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"system`"})"
        ExpectedType = "vector"
    },
    @{
        Name = "Average function"
        Query = "avg(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"system`"})"
        ExpectedType = "vector"
    },
    @{
        Name = "Count cores"
        Query = "count without(cpu, mode) (node_cpu_seconds_total{instance=`"$instanceName`"})"
        ExpectedType = "vector"
    }
)

# Lab 1 - CPU Exploration
$lab1_queries = @(
    @{
        Name = "Raw CPU metric"
        Query = "node_cpu_seconds_total"
        ExpectedType = "vector"
    },
    @{
        Name = "Filtered by instance"
        Query = "node_cpu_seconds_total{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Filtered by instance and mode"
        Query = "node_cpu_seconds_total{instance=`"$instanceName`", mode=`"user`"}"
        ExpectedType = "vector"
    }
)

# Lab 2 - CPU Rates
$lab2_queries = @(
    @{
        Name = "CPU rate"
        Query = "rate(node_cpu_seconds_total{instance=`"$instanceName`"}[5m])"
        ExpectedType = "vector"
    },
    @{
        Name = "Sum by mode"
        Query = "sum by (mode) (rate(node_cpu_seconds_total{instance=`"$instanceName`"}[5m]))"
        ExpectedType = "vector"
    }
)

# Lab 3 - Memory and Filesystem
$lab3_queries = @(
    @{
        Name = "Memory total"
        Query = "node_memory_MemTotal_bytes{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Memory available"
        Query = "node_memory_MemAvailable_bytes{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Memory usage %"
        Query = "100 * (1 - (node_memory_MemAvailable_bytes{instance=`"$instanceName`"} / node_memory_MemTotal_bytes{instance=`"$instanceName`"}))"
        ExpectedType = "vector"
    },
    @{
        Name = "Filesystem size"
        Query = "node_filesystem_size_bytes{instance=`"$instanceName`",fstype!=`"tmpfs`",mountpoint!=`"/run`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Filesystem free"
        Query = "node_filesystem_free_bytes{instance=`"$instanceName`",fstype!=`"tmpfs`",mountpoint!=`"/run`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Disk usage % for root"
        Query = "100 * (1 - (node_filesystem_free_bytes{instance=`"$instanceName`",mountpoint=`"/`"} / node_filesystem_size_bytes{instance=`"$instanceName`",mountpoint=`"/`"}))"
        ExpectedType = "vector"
    }
)

# Lab 4 - Network and Load
$lab4_queries = @(
    @{
        Name = "Network receive rate"
        Query = "rate(node_network_receive_bytes_total{instance=`"$instanceName`",device!=`"lo`"}[5m])"
        ExpectedType = "vector"
    },
    @{
        Name = "Network transmit rate"
        Query = "rate(node_network_transmit_bytes_total{instance=`"$instanceName`",device!=`"lo`"}[5m])"
        ExpectedType = "vector"
    },
    @{
        Name = "Load 1m"
        Query = "node_load1{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Load 5m"
        Query = "node_load5{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Load 15m"
        Query = "node_load15{instance=`"$instanceName`"}"
        ExpectedType = "vector"
    },
    @{
        Name = "Aggregated network receive"
        Query = "sum by (instance) (rate(node_network_receive_bytes_total{instance=`"$instanceName`",device!=`"lo`"}[5m]))"
        ExpectedType = "vector"
    },
    @{
        Name = "Aggregated network transmit"
        Query = "sum by (instance) (rate(node_network_transmit_bytes_total{instance=`"$instanceName`",device!=`"lo`"}[5m]))"
        ExpectedType = "vector"
    }
)

# Lab 5 - Advanced CPU Anomaly Detection
$lab5_queries = @(
    @{
        Name = "CPU saturation detection"
        Query = "max_over_time((100 * (1 - (sum by (instance) (rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}))))[30m:1m])"
        ExpectedType = "vector"
    },
    @{
        Name = "CPU spikes using increase"
        Query = "increase(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"user`"}[10m])"
        ExpectedType = "vector"
    }
)

# Lab 6 - Correlating Metrics
$lab6_queries = @(
    @{
        Name = "CPU usage %"
        Query = "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"})))"
        ExpectedType = "vector"
    },
    @{
        Name = "Memory usage %"
        Query = "100 * (1 - (node_memory_MemAvailable_bytes{instance=`"$instanceName`"} / node_memory_MemTotal_bytes{instance=`"$instanceName`"}))"
        ExpectedType = "vector"
    },
    @{
        Name = "Network receive rate aggregate"
        Query = "sum by (instance) (rate(node_network_receive_bytes_total{instance=`"$instanceName`",device!=`"lo`"}[5m]))"
        ExpectedType = "vector"
    },
    @{
        Name = "High CPU and Memory alert"
        Query = "(100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}))) > 80) and (100 * (1 - (node_memory_MemAvailable_bytes{instance=`"$instanceName`"} / node_memory_MemTotal_bytes{instance=`"$instanceName`"})) > 80)"
        ExpectedType = "vector"
    }
)

# Lab 7 - Recording Rules and Alerting
$lab7_queries = @(
    @{
        Name = "CPU usage for recording rule"
        Query = "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}[5m]))))"
        ExpectedType = "vector"
    },
    @{
        Name = "Alert expression simulation"
        Query = "100 * (1 - (avg by (instance) (rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}[5m])) / count by (instance) (node_cpu_seconds_total{instance=`"$instanceName`",mode=`"idle`"}))) > 80"
        ExpectedType = "vector"
    }
)

# Lab 8 - Advanced PromQL Operations
$lab8_queries = @(
    @{
        Name = "Label replace function"
        Query = "label_replace(node_filesystem_size_bytes{instance=`"$instanceName`",mountpoint=`"/`"}, `"disk_type`", `"root_disk`", `"mountpoint`", `"/`")"
        ExpectedType = "vector"
    },
    @{
        Name = "Historical comparison with offset"
        Query = "sum(rate(node_cpu_seconds_total{instance=`"$instanceName`",mode!=`"idle`"}[5m])) and sum(rate(node_cpu_seconds_total{instance=`"$instanceName`",mode!=`"idle`"}[5m] offset 1h))"
        ExpectedType = "vector"
    },
    @{
        Name = "Top K resources"
        Query = "topk(3, sum by (mode) (rate(node_cpu_seconds_total{instance=`"$instanceName`"}[5m])))"
        ExpectedType = "vector"
    },
    @{
        Name = "Subquery for trend analysis"
        Query = "max_over_time(rate(node_cpu_seconds_total{instance=`"$instanceName`",mode=`"user`"}[5m])[30m:5m])"
        ExpectedType = "vector"
    },
    @{
        Name = "Detecting missing data"
        Query = "absent(node_cpu_seconds_total{instance=`"$instanceName`"})"
        ExpectedType = "vector"
    }
)

# Lab 9 - Histograms and Quantiles
$lab9_queries = @(
    @{
        Name = "Histogram bucket exploration"
        Query = "prometheus_http_request_duration_seconds_bucket"
        ExpectedType = "vector"
    },
    @{
        Name = "95th percentile latency"
        Query = "histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))"
        ExpectedType = "vector"
    },
    @{
        Name = "Median latency by handler"
        Query = "histogram_quantile(0.5, sum by (handler, le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))"
        ExpectedType = "vector"
    },
    @{
        Name = "SLO calculation"
        Query = "(sum(rate(prometheus_http_request_duration_seconds_bucket{le=`"0.5`"}[5m])) / sum(rate(prometheus_http_request_duration_seconds_count[5m]))) * 100"
        ExpectedType = "vector"
    },
    @{
        Name = "Gauge derivative"
        Query = "deriv(node_memory_Active_bytes{instance=`"$instanceName`"}[1h])"
        ExpectedType = "vector"
    }
)

# All queries combined
# This variable is used in test_queries.ps1 through dot sourcing
# Do not remove this variable - it is essential for the testing infrastructure
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVarsMoreThanAssignments', '', Justification='Used in test_queries.ps1 via dot sourcing')]
$allQueries = $lab0_queries + $lab1_queries + $lab2_queries + $lab3_queries + $lab4_queries + $lab5_queries + $lab6_queries + $lab7_queries + $lab8_queries + $lab9_queries

# No need for Export-ModuleMember when using dot sourcing
# Export-ModuleMember is only for formal PowerShell modules
