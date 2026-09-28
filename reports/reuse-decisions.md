# Reuse decisions — binding

Converts each recommendation in `ontology-reuse-survey.md` into a decision and the
consequence it has for the build.

Decision date 2026-09-25. Scope: Regulation (EU) 2024/1689 **as amended by Regulation (EU) 2026/1744**. Where `eu-aiact` has no term for an amended provision, as for Art. 5(1)(ba) and (bb), the term is minted locally.

## Register

| # | Candidate | Decision | Binding consequence |
|---|---|---|---|
| 3 | DPV `eu-aiact` (OWL) | **IMPORT** | `owl:imports <https://w3id.org/dpv/legal/eu/aiact/owl#>`. Local risk-category, prohibition, Annex I/III and authority terms are **forbidden** where an `eu-aiact` term exists. |
| 1 | AIRO | **IMPORT** | `owl:imports <https://w3id.org/airo>`. `aia:` mints no AI-system, component, model or determinant-property term. |
| 5 | ELI | **IMPORT** | `owl:imports <http://data.europa.eu/eli/ontology#>`. Provenance is by resource, never `xsd:string`. Supersedes DAOnt's `articleReference` practice. |
| 9 | SKOS | **IMPORT** | `owl:imports <http://www.w3.org/2004/02/skos/core>`. Every `aia:` term carries `skos:prefLabel` + `skos:definition`; a term without both is a build failure, not a gap. |
| 7 | PROV-O | **ALIGN** | Four axioms only, in the alignment module: `aia:RoleAssignment ⊑ prov:Association`, `aia:heldBy ⊑ prov:agent`, `aia:hasRole ⊑ prov:hadRole`, `aia:Provider a prov:Role`. **Not** imported: `prov:Activity ⊥ prov:Entity` is a live hazard once AI systems are typed, and buys nothing the four axioms do not. Documented as partial — `aia:concernsSystem` has no PROV-O counterpart. |
| 8 | ORG | **ALIGN** | `aia:Role ⊑ org:Role` only. `org:Membership` is cited as precedent and **not** subclassed: `org:organization`'s range is `org:Organization`, and it plus `org:member` are functional, so pointing one assignment at two systems would infer the systems identical. Typing authorities as `org:Organization` was decided separately (`STATUS.md`, decision 4). |
| 4 | DPV core / `tech` / `ai` / `risk` | **ALIGN — retargeted** | `aia:Obligation ⊑ dpv-owl:Obligation` in the **`/owl#` namespace**, not `dpv:`. See "Correction" below; this is a change to the survey's recommendation, not a restatement of it. |
| 2 | VAIR | **ALIGN** | Individual VAIR terms referenced as `aia:AnnexIIIArea` / `aia:IntendedPurpose` values. No import: 5,803 triples for ~30 terms. VAIR's purpose taxonomy is **not** asserted to be the Annex III partition. |
| 10 | ODRL | **ALIGN — `rdfs:seeAlso` only** | No subsumption. `odrl:Duty ⊥ odrl:Permission` is sound and would be usable, but DPV is already in the closure and carries the same separation without the assigner/assignee framing. Aligning to both is double-parenting. |
| 6 | LKIF-Core | **NEITHER** | `norm:Obligation ⊑ norm:Permission` and `Agent ⊥ Role` are disqualifying. This is the principal reason the obligation layer is built locally. |
| 13 | MAILO | **NEITHER** | Reported at length: recent, careful, imports AIRO/DPV/ELI, and *still* attaches obligations to `RegulatoryFramework`. Evidence the CQ3 gap is real, not an artefact of the candidate set. |
| 11 | AICat | **NEITHER** | Cited once, for being the only surveyed artefact to use the Act's ELI URI at all. |
| 12 | AIUP | **NEITHER** | Noted as adjacent work; models contractual use policies, not statutory duties. |
| 14 | TAIR | **NEITHER — on availability** | Unretrievable 2026-09-25. Re-survey if published. Decision is provisional on that fact alone, not on fit. |
| 15 | DAOnt | **NEITHER — precedent only** | Cited for aligning-rather-than-importing the deontic layer, and as the caution on namespace hygiene. |
| 16 | Rodrigues et al. KG | **NEITHER — design check only** | Its addressee/beneficiary split is retained as a check on `aia:Obligation`'s shape. |

Four imports, five alignments, seven excluded.

## Resolution strategy — decided

All four imports are **vendored under `imports/` and redirected by `catalog-v001.xml`**;
`fetch-imports.sh` reproduces them.

This was forced rather than chosen. All four IRIs are unreachable from the build
environment, and two do not serve RDF at their ontology IRI in any environment:
`http://data.europa.eu/eli/ontology` does not content-negotiate to the ELI document,
which lives at `op.europa.eu/documents/3938058/11669184/eli.owl/`. Since the task
requires demonstrating a Protégé load and a reasoner run, making that depend on the
reviewer's network and on the Publications Office's content negotiation is not
acceptable.

## Correction to the survey — DPV namespace

The survey recommended `aia:Obligation ⊑ dpv:Obligation` against
`https://w3id.org/dpv#`. **Parsing the imported serialisation shows this is the wrong
namespace.** The `eu-aiact` OWL file references the OWL variants throughout — 78
structural references over 51 distinct terms:

| Namespace | Refs |
|---|---:|
| `https://w3id.org/dpv/owl#` | 39 |
| `https://w3id.org/dpv/tech/owl#` | 25 |
| `https://w3id.org/dpv/ai/owl#` | 10 |
| `https://w3id.org/dpv/risk/owl#` | 3 |
| `https://w3id.org/dpv/pd/owl#` | 1 |

Aligning to `https://w3id.org/dpv#Obligation` would place the local obligation layer
under a DPV vocabulary that nothing else in the closure references — two disconnected
DPV graphs in one file. That is precisely the failure the survey caught in MAILO
(`http://w3id.org/dpv`, wrong scheme) and DAOnt (`https://…/odrl/2/`, wrong scheme).
The alignment target is therefore **`dpv-owl:Obligation`**.

Consequence beyond the alignment: all 51 referenced terms dangle, `eu-aiact` declaring
no `owl:imports`. Two are load-bearing for CQ1 — `dpv-owl:RiskLevel` is the parent of
`eu-aiact:RiskLevel`, and `dpv-owl:hasRiskLevel` is the property CQ1 bridges from.
**Decision: declare the dangling terms as local stubs rather than import DPV core**
(14,909 triples for a handful of terms). 55 stubs are declared in `aia-ont.ttl`.

## Import IRI spellings — verified, not assumed

Each IRI is the ontology IRI **as declared in the retrieved serialisation**. Two of the
four end in `#`, because those ontologies declare the ontology IRI identical to the
namespace IRI. The four are not parallel in form and cannot be written as if they were.

| Ontology | Declared ontology IRI | Trailing `#`? |
|---|---|:--:|
| DPV `eu-aiact` (OWL) | `https://w3id.org/dpv/legal/eu/aiact/owl#` | yes |
| AIRO | `https://w3id.org/airo` | no |
| ELI | `http://data.europa.eu/eli/ontology#` | yes |
| SKOS | `http://www.w3.org/2004/02/skos/core` | no |

MAILO imports ELI as `http://data.europa.eu/eli/ontology`, without the hash — a third
namespace-hygiene defect to set beside its `http://w3id.org/dpv` and DAOnt's ODRL
scheme error. The catalog maps both ELI spellings so either resolves.

`aia:` follows AIRO's convention — ontology IRI `https://w3id.org/aia-ont` without the
hash, namespace `https://w3id.org/aia-ont#` with it. This is the OWL-standard separation
and avoids the mismatch that the hash-terminated IRIs invite.

## Verification status of the import block

Parsed from the vendored serialisations, not read from documentation:

| Ontology | Triples | Classes | ObjProps | disjointWith | Restrictions | domain/range | Functional |
|---|---:|---:|---:|---:|---:|---:|---:|
| DPV `eu-aiact` (OWL) v2.3 | 2,173 | 167 | 3 | 0 | 0 | 0 / 0 | 0 |
| AIRO 1.0 | 558 | 56 | 61 | 0 | 0 | 33 / 50 | 0 |
| ELI **1.4** | 1,505 | 27 | 71 | 0 | 11 | yes | 13 |
| SKOS | 252 | 4 | 17 | 3 | 0 | — | — |

The only disjointness in the imports is SKOS's pairwise `Concept` / `ConceptScheme` /
`Collection`. The merged closure is consistent under both `owlrl` and HermiT.

**ELI is v1.4, not v1.5**, and declares no `owl:versionIRI`. Its domain/range axioms were
checked against CQ2: `eli:number` and `eli:is_part_of` do not mention
`LegalResourceSubdivision`, but v1.4 places it under both `LegalResource` and
`WorkSubdivision` (the second added in v1.4), both under `Work`. Typing articles as
`eli:LegalResourceSubdivision` therefore satisfies all three domains. Under v1.3 it would not.
