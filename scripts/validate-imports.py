"""Load test for the import block: resolves owl:imports through catalog-v001.xml,
merges the closure, and reports what is present vs missing."""
import sys, os, xml.etree.ElementTree as ET
import rdflib
from rdflib.namespace import OWL, RDF

CAT = "catalog-v001.xml"
ns = {"c": "urn:oasis:names:tc:entity:xmlns:xml:catalog"}
cat = {u.get("name"): u.get("uri") for u in ET.parse(CAT).getroot().findall("c:uri", ns)}
print(f"catalog: {len(cat)} redirects\n")

g = rdflib.Graph()
g.parse("aia-ont.ttl", format="turtle")
root = next(g.subjects(RDF.type, OWL.Ontology))
imports = sorted(str(i) for i in g.objects(root, OWL.imports))

print(f"ontology IRI : {root}")
print(f"version IRI  : {next(g.objects(root, OWL.versionIRI))}")
print(f"imports      : {len(imports)}\n")

closure, missing = rdflib.Graph(), []
for iri in imports:
    target = cat.get(iri)
    status = "NOT IN CATALOG"
    if target and os.path.exists(target):
        fmt = "turtle" if target.endswith(".ttl") else "xml"
        sub = rdflib.Graph(); sub.parse(target, format=fmt)
        closure += sub
        status = f"OK  {len(sub):>5} triples  <- {target}"
    elif target:
        missing.append((iri, target)); status = f"MISSING FILE      <- {target}"
    print(f"  {iri}\n      {status}")

merged = g + closure
print(f"\nmerged closure: {len(merged)} triples "
      f"({len(g)} local + {len(closure)} imported)")

# axioms that could make the model inconsistent from outside the local file
for label, pred in [("owl:disjointWith", OWL.disjointWith),
                    ("owl:propertyDisjointWith", OWL.propertyDisjointWith)]:
    print(f"  {label:28} {len(list(closure.triples((None, pred, None))))}")
for label, t in [("owl:Restriction", OWL.Restriction),
                 ("owl:FunctionalProperty", OWL.FunctionalProperty),
                 ("owl:AllDisjointClasses", OWL.AllDisjointClasses)]:
    print(f"  {label:28} {len(set(closure.subjects(RDF.type, t)))}")

if missing:
    print("\nnot vendored in this environment (run ./fetch-imports.sh):")
    for iri, target in missing:
        print(f"  {iri}  ->  {target}")
    sys.exit(0)