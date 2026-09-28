# Status

*As of 2026-09-28. Tasks 1–15 are done.*

## Verified state

| | |
|---|---|
| Ontology IRI / version | `https://w3id.org/aia-ont`, `https://w3id.org/aia-ont/0.1` |
| Scope | Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744: consolidated text `02024R1689-20260727` |
| Local triples | 901 core + 28 alignment |
| Local classes | 17: 15 skeleton + `aia:HighRiskByGround` + `aia:TerminatedRoleAssignment` (the 2 defined classes) |
| Local object properties | 21: the 19 the CQ queries bind, plus `aia:classifiedOnGround` and `aia:terminatedBy` |
| Named individuals | 54: 6 roles, 27 obligations, 10 practices, 11 exemptions |
| External term stubs | 55 `dpv/*` IRIs, declaration only (task 2) |
| Article resources | 17 `eli:LegalResourceSubdivision` + the Act |
| Missing `skos:prefLabel` / `skos:definition` | none (stubs excluded) |
| Disjointness | 1 `owl:AllDisjointClasses` axiom over 10 classes (8 local plus `airo:AISystem`, `airo:AIOperator`), and `aia:AnnexIIIGround` ⊥ `aia:DerogatedAnnexIIIGround` |
| Imports | 4 declared, all vendored and resolving; merged closure 5,385 triples (901 local + 4,486 imported) |
| Worked example | `ontology/aia-example.ttl`, 319 triples, 43 individuals, imported by nothing |
| SHACL | 16 node shapes, 5 SHACL-SPARQL constraints, 1 SHACL-AF target, 1 at `sh:Warning`; 32/32 checks pass |
| Reasoner | `check-reasoner.py` (OWL 2 RL) 177/177; HermiT consistent, 0 unsatisfiable, in the Protégé GUI and via CLI |
| Competency questions | 5/5 return, plus the CQ1 ASK: 10 / 17 / 27 / 36 / 31 rows (`reports/cq-results.md`) |

`skos:prefLabel` and `skos:definition` are declared locally as `owl:AnnotationProperty`,
so applying them to `aia:` classes does not mix SKOS's individual-oriented vocabulary with
class-level annotation.

**Provenance.** 86 of 92 local terms carry an article-level `aia:definedIn` edge (or a
subproperty) to an `eli:LegalResourceSubdivision`. The other 6 have no defining provision;
the reasons are at the end of `aia-ont.ttl`. Paragraph precision stays in `rdfs:comment`.

### Imports

| Import IRI | Local file | Triples |
|---|---|---:|
| `https://w3id.org/dpv/legal/eu/aiact/owl#` | `imports/eu-aiact-owl.ttl` | 2,173 |
| `https://w3id.org/airo` | `imports/airo.ttl` | 558 |
| `http://data.europa.eu/eli/ontology#` | `imports/eli.owl` | 1,505 |
| `http://www.w3.org/2004/02/skos/core` | `imports/skos.rdf` | 252 |

`eu-aiact-owl.ttl` and `airo.ttl` match the survey's triple counts exactly. The
`eu-aiact` URL originally in `fetch-imports.sh` returned 404; the working URL
(`https://w3c-cg.github.io/dpv/2.3/legal/eu/aiact/eu-aiact-owl.ttl`) serves a file
byte-identical to the vendored copy (md5 `70e797903d7ca7288380995d236c9e82`).

Imported-side axiom profile: 3 `owl:disjointWith` (all SKOS), 11 `owl:Restriction`,
14 `owl:FunctionalProperty`, no property disjointness.

**SKOS profile correction.** An earlier pass recorded SKOS as having no object properties.
It declares 17 (`broader`, `narrower`, `related`, `exactMatch`, `inScheme`, …).

## Decisions

**1. The classification rule is a local defined class (task 9).** `aia:HighRiskByGround ≡
∃classifiedOnGround.AnnexIIIGround ⊔ ∃classifiedOnGround.AnnexIGround`, and
`⊑ eu-aiact-owl:HighRiskAISystem`. No axiom is added to an import.

- The rule is sufficient, not necessary. An equivalence on the imported class would make a
  recorded ground necessary for high risk, so a high-risk system recorded without its ground
  would be inconsistent rather than under-described.
- Art. 6(3) takes some Annex III systems out of high risk. OWL cannot retract the rule's
  conclusion or infer a derogation from its absence, so the derogation is recorded as data:
  such a use case is an `aia:DerogatedAnnexIIIGround`, disjoint from `aia:AnnexIIIGround`
  and not a disjunct of the rule. Art. 6(4) requires the provider to document that
  assessment anyway. The worked example's CV formatter is the negative control.
- `eu-aiact-owl` has 0 `owl:equivalentClass` axioms; adding the first from downstream would
  collide with any future version that defines the term.
- Subsumption keeps CQ1's ASK against `eu-aiact:HighRiskAISystem` entailed without a rival
  `aia:HighRiskAISystem`.

`aia:PurposeGround` is not a disjunct: purpose is how Annex III membership is determined,
not a separate route. The rule cannot use `eu-aiact:hasRiskLevel`, whose values are
punned class/individual. Every rule the entailment needs is OWL 2 RL, and HermiT confirms it.

**2. Scope exclusions are decided one by one.** The specification names five elements and
disclaims completeness, so an argued exclusion is worth more than silent breadth.

| Exclusion | Decision | Reason |
|---|---|---|
| Art. 50 risk tier | IN | "AI system categories" is named; the tier is already imported. The example must include one system at `RiskLevelTransparencyRequired` |
| Art. 50 obligations | OUT | `eu-aiact` has none; "major obligations" is served by Arts. 16 and 26 |
| GPAI, Chapter V | OUT | GPAI models are regulated as models, not systems (Art. 3(63) vs 3(1)): a parallel regime, not a gap |
| Art. 27 FRIA | OUT | One conditional deployer duty; `eu-aiact:FRIA` is the attachment point |

**3. The worked example is a separate file** (`aia-example.ttl`, IRI
`https://w3id.org/aia-ont/example`) that imports the core and is imported by nothing, so
loading the model does not load the fixture. Its individuals use the `aia:` namespace
because the CQ1 and CQ3 queries name `aia:ExampleRecruitmentScreeningSystem`; every example
term carries an `Example` / `ra_` / `rr_` / `rc_` / `g_` / `oa_` / `route_` prefix.

**4. Authorities are `org:Organization`.** CQ5 requires it. The ORG hazard
(`reuse-decisions.md`, candidate 8) comes from its functional properties, and none is
asserted here; `org:Organization` is a declaration-only stub in the example.

**5. Article 25(2) termination is derived, not asserted.** `aia:terminatedBy` is
`owl:inverseOf aia:terminates`, and `aia:TerminatedRoleAssignment ≡
∃terminatedBy.RoleReassignment`. A live assignment carries the duties `aia:borneBy` its
role; a terminated one carries only the residual duties `aia:borneOnTermination` it, the
four Art. 25(2) duties towards the new provider. `aia:borneOnTermination` is deliberately
not a subproperty of `aia:borneBy`, or the new provider would inherit them.

This fixed a defect found by running CQ3: 12 of its 35 rows were Art. 16 duties of
TalentFlow GmbH, whose provider role Art. 25(2) had ended. Over the inferred graph CQ3 now
returns 27 rows, TalentFlow's 12 replaced by its 4 residual duties. Rejected alternatives:

- *Validity interval.* The Act gives no dates; 25(2) is condition-triggered. Worth adding
  only when data comes from the Art. 49/71 EU database.
- *Filter on the event in the query.* Correct, but puts a rule of law in one query instead
  of an axiom every query follows.
- *Deleting the assignment.* Art. 25(2) imposes duties that outlast the role; they need
  something to attach to.

The biconditional here is deliberate where decision 1 refused one: 25(2) is the only way an
assignment ends in this model, while Art. 6 is not the only route to high risk.

**6. The Annex I example system is a Section A product.** It is a class IIa medical-device
system (Annex I, Section A, point 11) rather than a machinery safety controller. Annex I lists
the Machinery Regulation (EU) 2023/1230 in Section B, point 21, and Art. 2(2) applies only
Art. 6(1), Art. 60a and Arts. 102–112 to Section B products, so a machinery system can be
high-risk but cannot carry the Art. 16 duties or the Art. 25 reassignment the example
exercises. Its route is the third conformity route, the Section A sectoral procedure of
Art. 43(3).

## Known limitations

**Conditional obligations are not modelled.** Nine duties are asserted flatly although the
Act conditions them: 26(8) public-authority deployers only, 26(9) only where a DPIA is
required, 26(10) post-remote biometric identification only (with an express exception),
26(11) Annex III decisions about persons only, 16(e) "when under their control", and the
four Art. 25(2) residual duties, none of which applies where the initial provider clearly
specified that the system was not to be made high-risk. Two conditions reach every
high-risk duty: Art. 2(2) disapplies them for Annex I, Section B products, and Art. 2(13)
lets delegated acts limit the Art. 17–25 duties for Section A products. The model therefore
states stronger duties than the Act, and no query shows it.

Recommended fix: mint `aia:ApplicabilityCondition` with two subclasses, one for conditions
that trigger a duty (26(8)) and one for conditions that defeat it (Art. 5 exemptions,
26(10)'s exception). Make `aia:Exemption` a subclass of the defeating one and add
`aia:conditionedOn` from `aia:Obligation`. Represent and return the conditions; do not ask
the reasoner to evaluate them, since the provisions are defeasible and OWL is monotonic. A
SHACL shape can require `aia:conditionedOn` wherever a definition carries a condition cue.

**Art. 5(2) depends on Art. 27.** The 5(1)(h) exemptions require a completed Art. 27
impact assessment, which decision 2 excludes. The gate is described in prose; reasoning
over it would need Art. 27 back in scope.

**CQ5 answers half its question.** Routes relate to obligations, not systems, so "which
route applies to a given system" comes back obligation-indexed. The fix (`aia:appliesToSystem`
or a join through the role assignment) is not taken because no query binds such a property.

**Two results that look like defects and are not.**
(a) CQ2 returns 17 rows while `check-reasoner.py` expects 16 for the practice/exemption
pattern: `aia:ex_art5_1_h_suspect` has two `aia:providedFor` values (Art. 5 and Annex II),
both load-bearing.
(b) CQ5 returns the market surveillance authority twice per obligation, because `eu-aiact`
makes it a subclass of `NationalCompetentAuthority` (faithful to Art. 3(48)).

**ELI and SKOS disagree on four property types.** ELI declares `skos:broader`,
`narrower`, `hasTopConcept` and `topConceptOf` as annotation properties; SKOS declares them
object properties. OWL 2 DL forbids this punning; Protégé and the OWL API warn and continue.
`owlrl` does not detect it. See `evidence/protege-hermit-findings.md`.

**Verification against the Official Journal** covers Arts. 5, 16, 25, 26 and 43(3),
Annex I and Recital 83, against the consolidated text `02024R1689-20260727`, which
incorporates Regulation (EU) 2026/1744, and the amending act itself (OJ L, 24.7.2026).
All 43 amendment points were read for their effect on the model. Beyond those provisions,
only Arts. 2(2), 2(13), 3(14), 6(1a)–(1c), 75(1), 99(4)(da) and 113 bear on it; the rest
concern sandboxes, notified-body designation, SME simplification, guidance and GPAI. Other cited provisions are unverified.
Corrections made:

- Art. 5(1)(h)(iii): "for a **maximum period** of at least four years", not "at least four years".
- Art. 26(9): Directive (EU) 2016/680, not Regulation (EU) 2018/1725.
- Art. 26(10): the 48-hour outer limit and the exception for initial identification on
  objective and verifiable facts were missing.
- Art. 26(8): the prohibition on using an unregistered system was missing.
- Art. 26(5): the law-enforcement and financial-institution carve-outs were missing.

`check-reasoner.py` asserts the corrected wording. Art. 26(3) is a savings clause and is
correctly absent.

- Art. 25(2): the initial provider's duty to cooperate with the new provider was missing.
  It is in the as-adopted text as well as the amended one, which only lists its components.
- Art. 43: the shapes allowed only the Annex VI and VII routes; Art. 43(3) sends Annex I,
  Section A systems through their sectoral procedure.

**Application dates are not modelled.** Under Art. 113, Art. 5(1)(ba)–(bb) apply from
2 December 2026, and the Chapter III high-risk rules from 2 December 2027 for Annex III
systems and 2 August 2028 for Annex I systems. The model states what the Act requires once
applicable, not what applies on a given date.

## Tasks

| # | Task | Result |
|---|---|---|
| 1 | Vendor ELI and SKOS | All four imports vendored and validated |
| 2 | Stub dangling `eu-aiact` references | 55 `dpv/*` IRIs; the checker fails if the set drifts |
| 3 | Properties with domains and ranges | Read off the CQ queries; union domains on `concernsSystem` / `statedIn`; `definedIn` domainless by design |
| 4 | Article resources, `definedIn` | Minted locally, `eli:is_part_of` the Act |
| 5 | Role individuals | 6 roles of Art. 3(8) as individuals of `aia:Role` |
| 6 | Art. 16, 25(2) and 26 obligations | 27, OJ-verified; CQ3 binds 12 / 11, and 4 for an ended provider |
| 7 | Art. 5 practices and exemptions | 10 + 11, OJ-verified; (a)(b)(c)(e) unconditional, (ba)2, (bb)2, (d)1, (f)1, (g)2, (h)4 |
| 8 | Alignment module | `aia-align.ttl`, not imported: 6 axioms over PROV-O / ORG / DPV core, ODRL by `rdfs:seeAlso` |
| 9 | Classification rule | Decision 1 |
| 10 | Worked example | All four tiers, both Art. 6 routes (Annex I via a Section A medical device), all three Art. 25(1) limbs, four dual-role actors, negative controls for a purpose-only ground and an Art. 6(3) derogation |
| 11 | Run the CQs | `run-cq-queries.py`, asserted and inferred graphs; exposed the decision-5 defect |
| 12 | SHACL shapes | 32/32 with 25 negative controls; inference off |
| 13 | Protégé / HermiT evidence | `evidence/protege-hermit-findings.md` |
| 14 | Evaluation metrics | `reports/evaluation.md`: consistency, CQ answerability, annotation completeness, provision coverage, expert legal review |
| 15 | Trim the report | 2 pages, measured with `scripts/page-count.py` |
