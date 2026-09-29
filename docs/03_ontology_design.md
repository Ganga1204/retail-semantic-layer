# Step 5 & 6: Ontology Design & RDF Knowledge Graph

## 1. Ontology vs Data Model

| Dimension | Data Model (Relational / Star Schema) | Business Ontology (Knowledge Model) |
| :--- | :--- | :--- |
| **Primary Focus** | Storage, performance, SQL join paths, indexing | Business semantics, domain concepts, real-world context |
| **Core Elements** | Tables, columns, foreign keys, data types | Object types, properties, domain relationships, business actions |
| **Target Audience** | Data engineers, database administrators | Domain experts, business analysts, AI agents / LLMs |
| **Change Frequency**| Tied to database migration scripts & pipelines | Governed by enterprise vocabulary changes and ADRs |

## 2. ADR-001: Official Definition of "Active Customer"

```markdown
# ADR-001: Official definition of "active customer"
Status: Accepted
Decision: 90-day completed order window.
Rationale: Aligns directly with marketing acquisition/retention lifecycle and current campaign re-engagement cadence. Other departmental views are retained as explicitly named metric variants so no team loses visibility into their specific operational numbers.
Consequences: Finance and Support must query the variant metric names (`active_customers_365d` and `engaged_customers_30d` respectively) when reporting team-specific numbers, while executive reports use `active_customers`.
```

## 3. Knowledge Graph & RDF Export

The business ontology specified in `ontology/ontology.yaml` is translated into standard Web Ontology Language (OWL) / Resource Description Framework (RDF) Turtle format using `rdflib`.

- **Classes (OWL Class):** `ex:Customer`, `ex:Order`, `ex:SupportTicket`
- **Object Properties (Relationships):** `ex:places` (`Customer` -> `Order`), `ex:raises` (`Customer` -> `SupportTicket`)
- **Datatype Properties:** Properties mapped directly to physical mart columns via `maps_to`.

### SPARQL Verification Query
```sparql
PREFIX ex: <http://example.org/retail#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?link ?from ?to WHERE {
  ?link rdfs:domain ?from ;
        rdfs:range ?to .
}
```
*Output:*
- `places : Customer -> Order`
- `raises : Customer -> SupportTicket`
