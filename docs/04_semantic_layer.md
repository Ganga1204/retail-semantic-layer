# Step 7: MetricFlow Semantic Layer Architecture

## 1. Metric Catalog

| Metric Name | Label | Type | Owner | Source Measure / Calculation | Business Definition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `active_customers` | Active Customers (official, 90d) | Simple | Marketing | `active_90d_count` (sum of `is_active_90d`) | Canonical active customer count: completed order in past 90 days as of 2026-06-30. |
| `active_customers_365d` | Retained Customers (12m, Finance) | Simple | Finance | `active_365d_count` (sum of `is_active_365d`) | Finance retention view: completed order in past 365 days. |
| `engaged_customers_30d` | Engaged Customers (30d, Support) | Simple | Support | `engaged_30d_count` (sum of `is_active_30d_support`) | Support engagement view: ticket OR order in past 30 days. |
| `total_revenue` | Total Revenue | Simple | Finance | `revenue` (sum of `amount`) | Sum of gross revenue across recorded orders. |
| `revenue_per_active_customer` | Revenue per Active Customer | Ratio | Executive | `total_revenue / active_customers` | Average revenue generated per canonical active customer. |

## 2. Why a Central Semantic Layer Beats SQL in Dashboards

Traditional BI architectures embed SQL metric logic directly inside dashboard visual tools (Tableau, Power BI, Looker, Metabase). This pattern leads to severe organizational friction:
- **Logic Drift:** Different dashboard designers write subtle variations of `WHERE status = 'completed'` or `WHERE date >= CURRENT_DATE - 90`, producing inconsistent figures for executive meetings.
- **Maintenance Overhead:** Updating a single metric definition requires opening and editing dozens of individual dashboard workbooks and scheduled SQL views.
- **Lack of Governance & Testing:** SQL snippets embedded in visual UI tools cannot easily be versioned with Git, peer-reviewed, or automatically tested in CI/CD pipelines.

By shifting metric logic into a code-governed MetricFlow semantic layer:
1. **Define Once, Query Anywhere:** Metrics are declared in version-controlled YAML (`models/marts/semantic.yml`). BI tools, notebooks, and LLMs query the same semantic API (`mf query`).
2. **Automated Validation:** MetricFlow parses join trees, time dimensions, and ratio dependencies automatically.
3. **CI/CD Integration:** Unit tests run on every pull request, preventing schema drift or broken calculations before deployment to production.
