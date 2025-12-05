[![PromQL Tests](https://github.com/scarolan/promql-labs/actions/workflows/promql-tests.yml/badge.svg)](https://github.com/scarolan/promql-labs/actions/workflows/promql-tests.yml)

# PromQL Labs

A comprehensive set of hands-on lab exercises for learning Prometheus Query Language (PromQL) with Node Exporter metrics.

## 📚 Course Structure

This training consists of **twelve hands-on labs** organized into three difficulty levels, each with a checkpoint quiz:

### 🐣 Beginner Labs
- **Lab 0:** [PromQL Fundamentals](Beginner/Lab0_PromQL_Fundamentals.md) - Learn basic PromQL syntax and operators
- **Lab 1:** [CPU Metrics Exploration](Beginner/Lab1_CPU_Exploration.md) - Discover and filter basic metrics
- **Lab 2:** [CPU Usage Rates](Beginner/Lab2_CPU_Rates.md) - Calculate and visualize usage over time
- 📝 **[Beginner Checkpoint Quiz](Beginner/Quiz_Beginner_Checkpoint.md)**

### 👩‍💻 Intermediate Labs
- **Lab 3:** [Memory and Filesystem Usage](Intermediate/Lab3_Memory_Filesystem.md) - Track system resources
- **Lab 4:** [Network, Load, and Advanced Aggregations](Intermediate/Lab4_Network_Load.md) - Analyze traffic and system load
- 📝 **[Intermediate Checkpoint Quiz](Intermediate/Quiz_Intermediate_Checkpoint.md)**

### 😎 Advanced Labs
- **Lab 5:** [Advanced CPU Anomaly Detection](Advanced/Lab5_Advanced_CPU_Anomaly.md) - Find unusual patterns
- **Lab 6:** [Correlating Metrics & Dashboards](Advanced/Lab6_Correlating_Metrics.md) - Connect multiple metrics
- **Lab 7:** [Recording Rules and Alerting](Advanced/Lab7_Recording_Rules_Alerting.md) - Operationalize monitoring
- **Lab 8a:** [Label Manipulation & Historical Comparisons](Advanced/Lab8a_Label_Manipulation_Offset.md) - Master label_replace, label_join, and offset
- **Lab 8b:** [Subqueries, Ranking & Missing Data](Advanced/Lab8b_Subqueries_TopK_Absent.md) - Use subqueries, topk/bottomk, and absent()
- **Lab 9:** [Histograms and Quantiles](Advanced/Lab9_Histograms_Quantiles.md) - Work with histogram metrics, percentiles, and SLOs
- **Lab 10:** [Join Queries & Vector Matching](Advanced/Lab10_Join_Queries_Vector_Matching.md) - Master PromQL joins, vector matching, and complex multi-metric operations
- 📝 **[Advanced Checkpoint Quiz](Advanced/Quiz_Advanced_Checkpoint.md)**

## 🚀 Prerequisites

- Access to Prometheus with Node Exporter metrics (localhost:9100)
- Grafana instance connected to Prometheus
- Basic understanding of Linux system metrics

## 🔍 About These Labs

Each lab is designed to take approximately 30 minutes and includes:
- Clear learning objectives
- Step-by-step instructions
- Real-world scenario-based learning
- Practical challenges
- Hidden solutions
- Real-world Unix Node Exporter metrics

Start with the Beginner labs and progress through to Advanced for a complete learning experience.

## 🧪 Testing the Labs

You can automatically test all PromQL queries against your Prometheus server:

1. Update the URL in `Tests/config.json` with your Prometheus endpoint
2. Run the python test script: `python Tests\test_queries.py`
3. Check the results in `Tests\results.log`
