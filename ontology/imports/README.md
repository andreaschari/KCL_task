# Vendored imports

These files are **committed deliberately**, not gitignored. `../catalog-v001.xml`
redirects each `owl:imports` IRI here, so `aia-ont.ttl` loads in Protégé with no
network access. `../../scripts/fetch-imports.sh` reproduces the set.

Vendoring was forced rather than chosen. All four import IRIs were unreachable
from the build environment, and two do not serve RDF at their ontology IRI in
any environment: `http://data.europa.eu/eli/ontology` does not
content-negotiate to the ELI document, which lives under a separate
`op.europa.eu` path. Since the task requires demonstrating a Protégé load and a
reasoner run, making that depend on the reviewer's DNS is not acceptable.

| File | Ontology IRI as declared | Version |
|---|---|---|
| `eu-aiact-owl.ttl` | `https://w3id.org/dpv/legal/eu/aiact/owl#` | 2.3 |
| `airo.ttl` | `https://w3id.org/airo` | 1.0 |
| `eli.owl` | `http://data.europa.eu/eli/ontology#` | **1.4** |
| `skos.rdf` | `http://www.w3.org/2004/02/skos/core` | 2009 Recommendation |

Two terminate in `#` because those ontologies declare the ontology IRI
identical to the namespace IRI. The four are not parallel in form and cannot be
written as if they were.

All four are validated: `eu-aiact-owl.ttl` (2,173 triples) and `airo.ttl` (558) match the
survey's counts; `eli.owl` has 1,505 and `skos.rdf` 252. `cd .. && python3 ../scripts/validate-imports.py`
confirms the ontology loads with no missing or uncatalogued imports.
