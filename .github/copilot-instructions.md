# GitHub Copilot Instructions for PromQL Labs

## Project Overview

This is a comprehensive educational resource for learning Prometheus Query Language (PromQL) with Node Exporter metrics. The project contains **twelve progressive labs** (0-11) organized into three difficulty levels (Beginner, Intermediate, Advanced) designed for Killercoda workshop environments.

## Repository Structure

```
promql-labs/
├── Beginner/           # Labs 0-2: Fundamentals, CPU exploration, CPU rates
├── Intermediate/       # Labs 3-4: Memory/filesystem, network/load
├── Advanced/           # Labs 5-11: Anomaly detection, correlation, rules, 
│                       #            label manipulation, subqueries, histograms, joins
├── docs/               # Reveal.js slide decks for each lab
│   ├── common.css      # Shared slide styling
│   ├── common-scripts.js # Shared JavaScript
│   └── XX_LabName/     # Individual lab slides (index.html)
├── Tests/              # Query validation and coverage testing
│   ├── queries.py      # ALL test queries must be defined here
│   ├── test_queries.py # Main test runner
│   ├── check_query_coverage.py # Ensures all lab queries have tests
│   └── config.json     # Prometheus server configuration (USER MUST CONFIGURE)
├── Scripts/            # Helper scripts (install-rules.sh)
└── .github/workflows/  # CI/CD for query testing
```

## Python Environment

**Always use a Python virtual environment for testing and CLI operations.**

```bash
# Create and activate venv (first time)
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate   # Windows PowerShell

# Install dependencies
pip install requests
```

## Test Configuration

Before running tests, the user **MUST** configure `Tests/config.json` with a working Prometheus URL:

```json
{
    "prometheus_url": "http://localhost:9090/",
    "instance_name": "localhost:9100"
}
```

For Killercoda environments, use the provided external URL (e.g., `https://xxxxx-9090.saci.r.killercoda.com/`).

## Key Conventions

### PromQL Code Blocks
- **All PromQL queries MUST use triple backticks with `promql` language identifier**
- Example queries use `instance="localhost:9100"` for Node Exporter
- Process exporter uses `instance="localhost:9256"`  
- Test queries use `$INSTANCE` placeholder (replaced at runtime with `localhost:9100`)

```promql
# Example format in lab markdown files
rate(node_cpu_seconds_total{instance="localhost:9100",mode="user"}[5m])
```

### Lab Markdown Structure
Each lab follows this pattern:
1. Title with emoji (e.g., `# 🔍 Lab 8: Label Manipulation & Offset`)
2. `## Objectives` section with bullet points
3. `## Instructions` section with numbered steps and explanations
4. `## Challenge` section with `<details>` spoiler for solutions
5. Navigation link to next lab at the bottom

### Slide Decks (docs/)

Each lab has a corresponding slide deck in `docs/XX_LabName/index.html`. Follow these conventions strictly:

#### Framework & CDN
- **Reveal.js 4.3.1** from jsdelivr CDN
- **Theme**: `night` (dark background)
- Include `../common.css` and `../common-scripts.js`

```html
<!-- Required CSS (in <head>) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reset.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/theme/night.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/highlight/monokai.css">
<link rel="stylesheet" href="../common.css">

<!-- Required JS (before </body>) -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/markdown/markdown.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/highlight/highlight.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/notes/notes.js"></script>
<script src="../common-scripts.js"></script>
```

#### Title Slide Format (CRITICAL)
- **Title**: Use `# Lab X: Title` (h1 markdown, NOT `##`)
- **Subtitle**: Emoji + category on separate line (e.g., `📊 Advanced PromQL`)
- **NO ALL CAPS** - use title case only
- **NO emoji in the title line** - emoji goes on subtitle line only

```markdown
# Lab 8: Label Manipulation & Offset

📊 Advanced PromQL

[All Slides](../index.html)
```

#### Slide Structure
- Use `data-markdown` sections with `<textarea data-template>`
- Separate slides with `---`
- Include `<aside class="notes">` for speaker notes
- Navigation link at bottom of title slide: `[All Slides](../index.html)`

#### Example Title Slide Section
```html
<section data-markdown>
<textarea data-template>
# Lab 8: Label Manipulation & Offset

📊 Advanced PromQL

[All Slides](../index.html)

<aside class="notes">
Speaker notes for this slide go here.
</aside>
</textarea>
</section>
```

#### Consistency Checklist
- [ ] Title uses `#` (h1), not `##`
- [ ] No ALL CAPS anywhere
- [ ] Emoji on subtitle line, not title line
- [ ] Navigation link present
- [ ] Speaker notes included
- [ ] CDN links use jsdelivr (not cdnjs or unpkg)

### Testing Requirements - CRITICAL
- **Every PromQL query** in any lab markdown file MUST have an associated test in `Tests/queries.py`
- All queries MUST use `promql` code fence format
- Tests should use `$INSTANCE` placeholder (auto-replaced with `localhost:9100`)
- CI will fail if any query is untested or produces an error
- Use short time windows (≤5m) for faster test feedback

### Adding New Queries Workflow
1. Add the query to the lab markdown using ` ```promql ` code blocks
2. Add a corresponding test to `Tests/queries.py` in the appropriate `labX_queries` list
3. Run `python Tests/check_query_coverage.py` to verify coverage
4. Run `python Tests/test_queries.py` to validate queries work

## Lab Content Guidelines

### Query Explanations
Each query should have a `> **Explanation:**` blockquote explaining:
- What the query does
- Why each function/operator is used
- Expected output format
- Real-world use cases

### Challenge Solutions
- Use `<details><summary>🧠 <b>Show Solution</b></summary>` format
- Break down complex solutions step by step
- Include alternative approaches when applicable

### Common Prometheus Metrics Used
- **Node Exporter** (port 9100): `node_cpu_seconds_total`, `node_memory_*`, `node_filesystem_*`, `node_network_*`, `node_load*`
- **Prometheus internal**: `prometheus_http_request_duration_seconds_*`
- **Process Exporter** (port 9256): `namedprocess_namegroup_*`

## Known Issues & Troubleshooting

### Labs 8-10 Considerations
These advanced labs have complex queries that may behave differently based on environment:

**Lab 8 (Advanced Operations):**
- `absent()` returns empty if metric exists (expected behavior for existing metrics)
- Offset queries require sufficient historical data
- Memory percentage change calculations can return `NaN` if divisor is zero

**Lab 9 (Histograms):**
- `prometheus_http_request_duration_seconds_bucket` may have sparse data
- `histogram_quantile` returns `NaN` if no data in bucket range
- `deriv()` requires gauge metrics with variation over time window

**Lab 10 (Joins):**
- Vector matching requires labels to align properly
- `group_left`/`group_right` queries may return empty if cardinality doesn't match
- Boolean joins (`and`, `or`) require both sides to have matching label sets

### Testing Tips
- Ensure Prometheus has been running for at least 5-10 minutes before testing
- Some queries may return empty results in low-activity environments (this is valid)
- Recording rules in Lab 7+ require `Scripts/install-rules.sh` to be run first

## CI/CD

The GitHub Actions workflow (`.github/workflows/promql-tests.yml`) runs:
1. Query syntax validation
2. Query coverage check (all markdown queries have tests)
3. Live query testing against a Prometheus instance

## Common Tasks

### When editing a lab:
1. Ensure all new queries have tests in `queries.py`
2. Keep explanations clear and educational
3. Maintain consistent formatting with other labs
4. Update corresponding slide deck if needed

### When adding a new lab:
1. Create markdown in appropriate difficulty folder
2. Create slide deck in `docs/XX_LabName/index.html`
3. Add all queries to `Tests/queries.py` as `labX_queries`
4. Add to `all_queries` list at bottom of `queries.py`
5. Update main `README.md` with lab link
6. Run full test suite before committing

## Environment

- **Target platform**: Killercoda workshop environments
- **Prometheus**: localhost:9090
- **Node Exporter**: localhost:9100
- **Process Exporter**: localhost:9256 (optional)
- **Grafana**: Available for visualization exercises
