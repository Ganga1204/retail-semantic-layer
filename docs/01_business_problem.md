# Step 1 & 2: Business Problem & Context

## 1. Context
In modern retail organizations, cross-departmental alignment on core KPIs is frequently hindered by fragmented data definitions. Marketing, Finance, and Support teams each report an "active customer" count to leadership, yet the reported metrics never match. 

This disagreement leads to inefficient executive decision-making, redundant reporting pipelines, and lack of trust in data platform analytics.

## 2. Conflicting Definitions

The following table summarizes how each business domain currently defines an "active customer":

| Department | Definition of "Active Customer" | Business Rationale & Impact |
| :--- | :--- | :--- |
| **Marketing** | Placed a completed order in the last **90 days** | Focuses on recent campaign conversions and customer re-engagement windows. |
| **Finance** | Placed a completed order in the last **365 days** | Focuses on annual recurring retention and active customer base for annual valuation. |
| **Support** | Raised a ticket OR placed an order in the last **30 days** | Focuses on short-term high-touch operational workloads and immediate service interaction. |

Without a governed semantic framework, each team queries raw transaction tables using ad-hoc SQL snippets, producing three conflicting numbers for executive reporting.

## 3. Project Goal
Build an **Ontology-Driven Semantic Layer** using dbt MetricFlow and DuckDB that establishes:
- **One Canonical Definition:** Standardized as `active_customers` (Marketing's 90-day window, governed by ADR-001).
- **Explicit Named Variants:** Clearly codified metric variants for Finance (`active_customers_365d`) and Support (`engaged_customers_30d`).
- **Single Source of Calculation:** All metrics defined in code, version-controlled, and served directly to BI tools, APIs, and LLMs without code duplication.
- **Ontology Governance:** A machine-readable knowledge map (`ontology.yaml` + RDF/SPARQL) mapping business concepts directly to warehouse physical schemas.

## 4. Success Criteria
1. **Single Source of Truth:** Every customer metric in reports and queries traces back to a unified MetricFlow definition.
2. **Semantic Clarity:** The business ontology explicitly maps domain terms, cardinality, and actions to Gold mart models (`dim_customer`, `fct_orders`, `fct_tickets`).
3. **Automated Governance Testing:** CI pytest assertions guarantee that ontology properties and metric definitions remain 100% aligned with warehouse physical schemas.
