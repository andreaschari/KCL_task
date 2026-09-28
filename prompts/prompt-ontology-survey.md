# Prompt — existing ontology survey

*Intermediate artefact. Used to run the reuse survey for the EU AI Act proof-of-concept ontology. Recorded here for the "prompts, scripts, and intermediate artefacts" output required by the task specification.*

---

## Prompt

You are surveying existing ontologies and vocabularies to decide what can be reused in a proof-of-concept OWL ontology of Regulation (EU) 2024/1689 (the EU AI Act).

This is a **reuse decision**, not a literature review. For every candidate the operative question is: *which of the competency questions below could this help answer, and what would it cost to use it?* Do not summarise what an ontology is "about" except insofar as that bears on the decision.

### Competency questions

- **CQ1** — Into which risk category does a given AI system fall, and on what grounds (intended purpose, Annex III area, Annex I product-safety route)?
- **CQ2** — Which practices are prohibited, which article prohibits each, and which are subject to conditional exemption?
- **CQ3** — Which obligations attach to the provider of a high-risk system, and which to the deployer of that same system?
- **CQ4** — Under what conditions does a deployer, distributor or importer become a provider, which obligations does it acquire, and what becomes of the initial provider?
- **CQ5** — Which authorities oversee which obligations, and via which conformity assessment route?

### Modelling commitments already made

These are fixed. Assess candidates against them rather than proposing alternatives.

1. **Roles are reified.** An actor's role holds relative to a particular AI system and is contingent on conduct. The ontology uses a `RoleAssignment` node relating actor, role and system, with attachment points for the grounds, the period, and the establishing provision. Roles are **not** pairwise disjoint.
2. **Articles are addressable.** Every substantive term carries a reference to the provision that establishes it, at article granularity, under the AI Act's ELI URI `http://data.europa.eu/eli/reg/2024/1689/oj`.
3. **Annotations are mandatory.** Every class and property carries a label, a short description, and an article reference.

### Hard constraint

The result must load in Protégé and be consistent under a standard reasoner (HermiT or ELK). This bears directly on the reuse verdict: `owl:imports` of a large external ontology brings its full axiom set under the reasoner, so an inconsistency may originate several layers away from anything written locally, and may push the model out of a tractable profile. Treat import as the expensive option and say so where it applies.

### Candidates

Start with these, then find others. Do not assume the list is complete; there has been substantial AI Act modelling activity and something may exist that is closer to the target than anything below.

- AIRO — AI Risk Ontology (`w3id.org/airo`)
- VAIR — Vocabulary of AI Risks (`w3id.org/vair`)
- DPV and its AI extensions (`w3id.org/dpv`)
- ELI — European Legislation Identifier (`data.europa.eu/eli/ontology`)
- LKIF-Core, and legal-domain ontologies generally
- PROV-O, ORG, SKOS
- ODRL, for the obligation/deontic layer
- Any AI-Act-specific ontology published since 2024

### Per candidate, report

| Field | What to record |
|---|---|
| **Identity** | Name, namespace IRI, publisher, date, maintenance status, licence |
| **CQs borne on** | Which of CQ1–CQ5, and which *part* of each |
| **Coverage gaps** | Concepts the CQs need that this does not have |
| **Structural gaps** | Concepts it has, but linked in a way that will not support the traversal the CQ needs. Pay particular attention to whether its treatment of actors is compatible with reified roles — a candidate that models provider/deployer as disjoint classes conflicts with commitment 1 above |
| **Alignment cost** | If aligned rather than imported, which axioms would be needed, and are any of them likely to be contested? |
| **Import risk** | Size of axiom set, OWL profile, known disjointness or cardinality axioms that could conflict |
| **Verdict** | `import` / `align` / `neither`, with the reason in one or two sentences |

### Accuracy requirements

- **Verify every term IRI against the published specification**, not from memory. Where a term is asserted without having been checked against a retrievable spec document, mark it explicitly as unverified rather than presenting it as confirmed.
- Give a retrievable URL for each candidate's specification. Where none exists, say so.
- Note where an ontology was built against a **draft** version of the AI Act — its risk taxonomy may not align with the adopted four-tier structure, and this is an alignment cost rather than a reason to discard it.
- Where two candidates overlap, say which is the better attachment point and why. Do not recommend both without distinguishing them.

### Stop criterion

Stop when the CQs are covered or you are confident they are not — not when the candidate space is exhausted.

### Weight the near misses

An ontology that models the right concepts at the wrong granularity, or that breaks the CQ3/CQ4 traversal, is more useful to report on than one that is simply irrelevant. It is where the justification for building rather than reusing comes from. Report those in full rather than dismissing them in a line.

### Output

A per-candidate table as specified above, followed by:

1. A **coverage matrix** — CQ1–CQ5 against candidates, showing which questions remain unanswered by anything surveyed.
2. A **reuse recommendation** — the proposed set of imports and alignments, with the residual gap the local ontology must fill stated explicitly.
