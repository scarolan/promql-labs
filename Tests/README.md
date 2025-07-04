# PromQL Labs Test Suite

This folder contains scripts to validate the PromQL queries used in the labs against a Prometheus server. The test suite ensures all queries in the lab markdown files are working correctly and that every query is properly tested.

## Core Requirements

1. **Every PromQL query** in any lab markdown file MUST have an associated test in `queries.py`
2. All queries MUST use the code fence format: \```promql ... \```
3. All lab queries and test queries should use short time windows (≤5m) for faster feedback

## Test Files Overview

- `queries.py`: Contains all test query definitions (this is where you add new tests)
- `test_queries.py`: Main test runner script for all queries
- `check_query_coverage.py`: Validates that all markdown queries have associated tests
- `test_recording_rules.py`: Verifies recording rules are correctly installed
- `config.json`: Configuration for Prometheus server URL

## How to Use

1. **Setup**: Update the `config.json` file with your Prometheus server URL
2. **Run Tests**: Execute `python test_queries.py` to validate all queries
3. **Verify Coverage**: Run `python check_query_coverage.py` to ensure all markdown queries have tests
4. **Check Rules**: Run `python test_recording_rules.py` to verify recording rules

## Adding New Queries

When adding new queries to lab markdown files:

1. Add the query to the lab using \```promql code blocks
2. Add a corresponding test to `queries.py` using the same format as existing tests
3. Run the coverage checker to verify your query is recognized and tested

## CI Integration

These tests are run in CI pipelines to ensure:
- All queries work correctly against a test Prometheus instance
- All lab markdown queries have associated tests
- Recording rules are correctly installed and functioning

The CI will fail if any query is untested or produces an error.
