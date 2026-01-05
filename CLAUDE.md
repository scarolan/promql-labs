# CLAUDE.md - AI Assistant Guide for PromQL Labs

## Project Overview

PromQL Labs is a comprehensive educational resource for learning Prometheus Query Language (PromQL) through hands-on exercises. The project contains **twelve progressive labs** (0-11) organized into three difficulty levels (Beginner, Intermediate, Advanced), designed for workshop environments (particularly Killercoda).

**Key Features:**
- 12 hands-on labs with progressive difficulty
- Reveal.js slide decks for each lab
- 100% automated test coverage for all queries
- CI/CD validation via GitHub Actions
- Real Node Exporter metrics, not synthetic data

## Repository Structure

```
promql-labs/
├── Beginner/           # Labs 0-2: Fundamentals, CPU exploration, CPU rates
├── Intermediate/       # Labs 3-4: Memory/filesystem, network/load
├── Advanced/           # Labs 5-11: Anomaly detection, correlation, rules,
│                       #            label manipulation, subqueries, histograms, joins
├── docs/               # Reveal.js slide decks (13 total: 1 overview + 12 labs)
│   ├── index.html      # Landing page with links to all decks
│   ├── common.css      # Shared slide styling
│   ├── common-scripts.js # Shared JavaScript (Grafana logo, speaker notes)
│   └── XX_LabName/     # Individual lab slide decks (index.html)
├── Tests/              # Query validation and coverage testing
│   ├── queries.py      # ALL test queries MUST be defined here
│   ├── test_queries.py # Main test runner (validates against live Prometheus)
│   ├── check_query_coverage.py # Ensures all lab queries have tests
│   ├── test_recording_rules.py # Validates recording rules
│   └── config.json     # Prometheus server configuration (USER MUST CONFIGURE)
├── Scripts/            # Helper scripts
│   ├── install-rules.sh # Sets up Prometheus recording/alerting rules
│   ├── histogram_traffic_generator.py # Generates histogram data for Lab 10
│   └── histogram_traffic_generator.sh # Bash version of traffic generator
└── .github/workflows/  # CI/CD for automated query testing
    └── promql-tests.yml # GitHub Actions workflow
```

## Key Conventions

### Lab Markdown Structure
Each lab follows this pattern:
1. **Title with emoji**: `# 🔍 Lab 0: PromQL Fundamentals`
2. **Objectives section**: Bullet points of learning goals
3. **Instructions section**: Numbered steps with queries and explanations
4. **Challenge section**: `<details>` spoiler tags for solutions
5. **Navigation link**: Link to next lab at bottom

### PromQL Code Blocks - CRITICAL
- **ALL PromQL queries MUST use triple backticks with `promql` language identifier**
- Lab queries use `instance="localhost:9100"` for Node Exporter
- Test queries use `$INSTANCE` placeholder (replaced at runtime with `localhost:9100`)
- Process exporter uses `instance="localhost:9256"`

Example:
```promql
rate(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[5m])
```

### Slide Deck Standards - CRITICAL

**Framework:**
- Reveal.js 4.3.1 from jsdelivr CDN (NOT cdnjs or unpkg)
- Theme: `night` (dark background)
- Monokai syntax highlighting for code blocks
- Include `../common.css` and `../common-scripts.js`

**Title Slide Format (MUST FOLLOW EXACTLY):**
- Title uses `#` (h1), NOT `##`
- Format: `# Lab X: Title` (no emoji in title line)
- Emoji on subtitle line: `📊 Advanced PromQL`
- NO ALL CAPS anywhere
- Navigation link: `[All Slides](../index.html)`

Example:
```markdown
# Lab 8: Label Manipulation & Offset

📊 Advanced PromQL

[All Slides](../index.html)
```

**Common Mistakes to Avoid:**
- Using `##` for title (should be `#`)
- Putting emoji in title line (should be on subtitle line)
- Using ALL CAPS for emphasis
- Mixing HTML and Markdown inconsistently
- Using wrong CDN (must be jsdelivr)

### Testing Requirements - CRITICAL

**Core Rule: Every PromQL query in ANY lab markdown file MUST have a corresponding test in `Tests/queries.py`**

**Testing Workflow:**
1. Add query to lab markdown using ` ```promql ` code blocks
2. Add corresponding test to `Tests/queries.py` in appropriate `labX_queries` list
3. Run `python Tests/check_query_coverage.py` to verify coverage
4. Run `python Tests/test_queries.py` to validate queries work
5. CI will fail if any query is untested or produces an error

**Test Structure:**
```python
lab0_queries = [
    {
        "name": "Basic metric query",
        "query": "node_memory_MemTotal_bytes",
        "expected_type": "vector"  # or "matrix" or "scalar"
    }
]
```

## Python Environment Setup

**ALWAYS use a Python virtual environment:**

```bash
# Create and activate venv (first time)
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate   # Windows PowerShell

# Install dependencies
pip install requests
```

## Test Configuration

Before running tests or QA, update `Tests/config.json` with your Prometheus endpoint:

```json
{
    "prometheus_url": "http://localhost:9090/",
    "instance_name": "localhost:9100"
}
```

For Killercoda environments, use the provided external URL (e.g., `https://xxxxx-9090.saci.r.killercoda.com/`).

## QA Process - Your Primary Task

### QA Philosophy
Act as a student going through the labs. The goal is to ensure:
- Every query works against a real Prometheus instance
- Explanations are clear and accurate
- Labs flow logically and build on each other
- Challenges are appropriate for the skill level
- No broken links or navigation issues

### QA Workflow

1. **Setup:**
   - Update `Tests/config.json` with Prometheus URL
   - Verify Node Exporter is running and collecting metrics
   - Wait 5-10 minutes for sufficient historical data

2. **For Each Lab:**
   - Read the objectives and context
   - Execute EVERY query in the Prometheus UI
   - Verify results match expectations
   - Check explanations are accurate
   - Attempt challenges without looking at solutions
   - Verify solutions work correctly
   - Check navigation links work
   - Evaluate flow and clarity

3. **Document Issues:**
   - Queries that fail or return unexpected results
   - Unclear explanations or missing context
   - Difficulty spikes or gaps in progression
   - Navigation or formatting problems
   - Suggestions for improvement

4. **Automated Testing:**
   ```bash
   # Run full test suite
   python Tests/test_queries.py

   # Check test coverage
   python Tests/check_query_coverage.py

   # Test recording rules (Labs 7+)
   python Tests/test_recording_rules.py
   ```

### Common QA Issues to Watch For

**Query Issues:**
- Queries returning empty results (may need more data/time)
- NaN or unexpected values (division by zero, missing metrics)
- Queries that work in one environment but not another
- Time ranges that are too long or too short

**Content Issues:**
- Explanations that don't match what query actually does
- Difficulty jumps that skip necessary concepts
- Challenges that are too hard or too easy
- Missing context for why a technique is useful

**Technical Issues:**
- Broken navigation links
- Inconsistent formatting
- Missing code fence language identifiers
- Slide deck formatting inconsistencies

## Common Tasks

### When Editing a Lab:
1. Read the lab markdown file completely
2. Update queries as needed (maintain `promql` code fences)
3. Update corresponding tests in `Tests/queries.py`
4. Run `check_query_coverage.py` to verify
5. Run `test_queries.py` to validate queries work
6. Update corresponding slide deck if needed
7. Test navigation links

### When Adding a New Lab:
1. Create markdown in appropriate difficulty folder
2. Follow lab structure conventions
3. Create slide deck in `docs/XX_LabName/index.html`
4. Add all queries to `Tests/queries.py` as `labX_queries`
5. Add to `all_queries` list at bottom of `queries.py`
6. Update main `README.md` with lab link
7. Update `docs/index.html` landing page
8. Run full test suite before committing

### When Fixing a Query:
1. Identify the issue (syntax, metric availability, time range, etc.)
2. Test fix in Prometheus UI first
3. Update lab markdown
4. Update corresponding test in `queries.py`
5. Run test suite to verify fix
6. Check if explanation needs updating

## Common Prometheus Metrics

**Node Exporter (port 9100):**
- CPU: `node_cpu_seconds_total` (labels: mode, cpu)
- Memory: `node_memory_*` (MemTotal_bytes, MemAvailable_bytes, etc.)
- Filesystem: `node_filesystem_*` (size_bytes, avail_bytes, etc.)
- Network: `node_network_*` (receive_bytes_total, transmit_bytes_total, etc.)
- Load: `node_load1`, `node_load5`, `node_load15`

**Prometheus Internal:**
- HTTP Request Duration: `prometheus_http_request_duration_seconds_*`

**Process Exporter (port 9256):**
- Process metrics: `namedprocess_namegroup_*`

## Known Issues & Edge Cases

### Lab-Specific Considerations

**Lab 7+ (Recording Rules):**
- Requires `Scripts/install-rules.sh` to be run first
- Recording rules may not exist in test environments
- Tests fall back to testing equivalent raw queries

**Lab 8 (Label Manipulation & Offset):**
- `absent()` returns empty if metric exists (expected behavior)
- Offset queries require sufficient historical data (10+ minutes)
- Memory percentage change can return `NaN` if divisor is zero

**Lab 10 (Histograms):**
- `prometheus_http_request_duration_seconds_bucket` may have sparse data
- Run `histogram_traffic_generator.py` to generate test data
- `histogram_quantile` returns `NaN` if no data in bucket range
- `deriv()` requires gauge metrics with variation over time

**Lab 11 (Joins):**
- Vector matching requires labels to align properly
- `group_left`/`group_right` may return empty if cardinality doesn't match
- Boolean joins (`and`, `or`) require matching label sets

### Environment Requirements

**Minimum for Testing:**
- Prometheus running for 5-10 minutes minimum
- Node Exporter actively collecting metrics
- Some system activity to generate varied metrics
- For histogram labs: run traffic generator script

**Target Environment:**
- Killercoda workshop platform (Ubuntu 22.04)
- Prometheus: localhost:9090
- Node Exporter: localhost:9100
- Process Exporter: localhost:9256 (optional)
- Grafana: Available for visualization exercises

## CI/CD

The GitHub Actions workflow (`.github/workflows/promql-tests.yml`) runs:
1. Query coverage check (all markdown queries have tests)
2. Prometheus + Node Exporter + Process Exporter setup
3. Recording rules installation
4. Live query testing against Prometheus instance
5. Results uploaded as artifacts

## Lab Progression

**Beginner (Labs 0-2):** Basic syntax, filtering, rates, aggregations
**Intermediate (Labs 3-4):** Memory, filesystem, network, load averages
**Advanced (Labs 5-11):** Anomaly detection, correlation, recording rules, label manipulation, subqueries, histograms, vector matching

Each lab builds on previous knowledge. QA should verify this progression is smooth and concepts are introduced at the right time.

## Best Practices for AI Assistants

1. **Always test queries** before claiming they work
2. **Read existing content** before making changes
3. **Maintain consistency** with established patterns
4. **Verify test coverage** after any query changes
5. **Act as a student** during QA, don't assume expertise
6. **Document findings** clearly and completely
7. **Suggest improvements** when flow or clarity could be better
8. **Respect the conventions** in this guide

## Getting Help

- GitHub Issues: https://github.com/scarolan/promql-labs/issues
- Test results: Check `Tests/results.log` after running test suite
- CI logs: View GitHub Actions workflow runs for detailed error messages

---

**Remember:** This is an educational project. Clarity, accuracy, and smooth progression are more important than advanced optimization. If something is confusing to you as an AI assistant, it will be confusing to students too.
