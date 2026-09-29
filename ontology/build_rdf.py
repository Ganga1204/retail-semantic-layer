import yaml
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

EX = Namespace("http://example.org/retail#")
onto = yaml.safe_load(open("ontology/ontology.yaml"))
g = Graph()
g.bind("ex", EX)

for name, obj in onto["object_types"].items():
    g.add((EX[name], RDF.type, OWL.Class))
    g.add((EX[name], RDFS.comment, Literal(obj["description"])))
    for prop_name, prop in obj["properties"].items():
        p = EX[f"{name}_{prop_name}"]
        g.add((p, RDF.type, OWL.DatatypeProperty))
        g.add((p, RDFS.domain, EX[name]))

for link in onto["links"]:
    p = EX[link["name"]]
    g.add((p, RDF.type, OWL.ObjectProperty))
    g.add((p, RDFS.domain, EX[link["from"]]))
    g.add((p, RDFS.range, EX[link["to"]]))

g.serialize("ontology/ontology.ttl", format="turtle")
print(f"Generated RDF graph with {len(g)} triples saved to ontology/ontology.ttl")

q = """
PREFIX ex: <http://example.org/retail#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?link ?from ?to WHERE { ?link rdfs:domain ?from ; rdfs:range ?to . }
"""
print("\nExecuting SPARQL relationship query:")
for row in g.query(q):
    link_str = str(row.link).split("#")[-1]
    from_str = str(row["from"]).split("#")[-1]
    to_str = str(row.to).split("#")[-1]
    print(f"  {link_str} : {from_str} -> {to_str}")
