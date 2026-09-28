# EU AI Act Ontology — Repo Guide

OWL ontology of Regulation (EU) 2024/1689 (the EU AI Act) as amended by Regulation (EU)
2026/1744 (`http://data.europa.eu/eli/reg/2024/1689/oj`, consolidated text of 27 July 2026).

- Ontology IRI: `https://w3id.org/aia-ont`
- Namespace: `https://w3id.org/aia-ont#` (prefix `aia:`)

## Overview

- **Reused.** [DPV `eu-aiact`](https://w3id.org/dpv/legal/eu/aiact) supplies the risk tiers,
  Annex I/III high-risk enumerations, authorities and conformity assessment bodies;
  [AIRO](https://w3id.org/airo) supplies AI systems and operators;
  [ELI](https://op.europa.eu/en/web/eu-vocabularies/eli) supplies the Act's articles as citable
  legal resources; [SKOS](https://www.w3.org/TR/skos-reference/) supplies labels and definitions.
- **Added.** 17 local classes to model:
  - obligations and who bears them, including the residual duties of a provider whose role
    Article 25(2) ends (`aia:Obligation`)
  - roles held per system, and their reassignment and termination under Article 25
    (`aia:Role`, `aia:RoleAssignment`, `aia:RegulatoryEvent`, `aia:RoleReassignment`,
    `aia:ReassignmentCondition`, `aia:TerminatedRoleAssignment`)
  - the grounds for high-risk classification, including Annex III use cases that Article 6(3)
    takes out of high risk (`aia:ClassificationGround`, `aia:PurposeGround`, `aia:AnnexIIIGround`,
    `aia:DerogatedAnnexIIIGround`, `aia:AnnexIGround`, `aia:HighRiskByGround`)
  - prohibited practices and their exemptions, including Article 5(1)(ba) and (bb), which
    `eu-aiact` predates (`aia:ProhibitedPractice`, `aia:Exemption`)
  - which authority oversees an obligation, and which conformity route applies
    (`aia:OversightAssignment`, `aia:ConformityAssessmentRoute`)

## Layout

| Path | Contents |
| --- | --- |
| [`report.md`](report.md) | The submission report |
| [`ontology/`](ontology/) | Core ontology and related files |
| [`queries/`](queries/) | SPARQL for the five competency questions |
| [`evidence/`](evidence/) | Protégé and HermiT run logs, screenshots and findings |
| [`shapes/`](shapes/) | SHACL shapes for closed-world completeness and integrity checks |
| [`scripts/`](scripts/) | Validation, query, reasoner and metrics scripts |
| [`reports/`](reports/) | Working reports on CQs, reuse survey and decisions, evaluation, AI workflow log, status |
| [`reports/evaluation.md`](reports/evaluation.md) | Proposed evaluation metrics and methods, with baseline values |
| [`prompts/`](prompts/) | Prompt used for the ontology reuse survey |

Each directory with more than one file has its own README describing its contents.

## Validation and evaluation

The ontology loads in Protégé and is consistent under HermiT, with no unsatisfiable classes
([`evidence/`](evidence/)); 177 OWL 2 RL checks and 32 SHACL checks pass. Proposed metrics
([`reports/evaluation.md`](reports/evaluation.md)): consistency, CQ answerability, annotation
completeness and provision coverage, computed automatically, plus expert legal review for what
automated checks miss. Computed values are in
[`reports/metrics-results.md`](reports/metrics-results.md).

## Imports

| Ontology | `owl:imports` IRI |
|---|---|
| DPV `eu-aiact` (OWL, v2.3) | `https://w3id.org/dpv/legal/eu/aiact/owl#` |
| AIRO 1.0 | `https://w3id.org/airo` |
| ELI 1.4 | `http://data.europa.eu/eli/ontology#` |
| SKOS | `http://www.w3.org/2004/02/skos/core` |

## Scripts

These scripts are used to validate the ontology, run the competency questions, check SHACL shapes and compute metrics. They are written in Python 3, except `run-hermit.sh`, which uses the HermiT and OWL API jars bundled with Protégé 5.6.9 and needs a JDK on `PATH`.

Python dependencies: `rdflib`, `owlrl`, `pyshacl`. Run everything from the repo root unless noted.

```sh
(cd ontology && python3 ../scripts/validate-imports.py)   # resolve and merge the import closure
python3 scripts/check-reasoner.py                        # OWL 2 RL consistency/entailment, 177 checks
python3 scripts/run-cq-queries.py                        # CQ1–CQ5, writes reports/cq-results.md
python3 scripts/check-shapes.py                          # SHACL + negative controls
python3 scripts/compute-metrics.py                       # writes reports/metrics-results.md
python3 scripts/page-count.py report.md  # needs markdown, soffice, pdfinfo
```