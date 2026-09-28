# EU AI Act Ontology Report

Proof-of-concept OWL 2 DL ontology (`ontology/aia-ont.ttl`, namespace `aia:`).

## 1. Scope

**Version.** The Act **as amended by Regulation (EU) 2026/1744** (consolidated OJ text, 27 July 2026).

**Coverage:**

- the four risk tiers: prohibited, high-risk, transparency-required, minimal
- the two ways a system becomes high-risk (Art. 6): as a product, or safety component of one,
  under Annex I legislation that requires third-party assessment; or by an Annex III use case
- the ten prohibited practices of Art. 5 and their exemptions
- provider (Art. 16) and deployer (Art. 26) duties; when another party becomes provider (Art. 25)
- who supervises each duty, and how a high-risk system's conformity is assessed (Art. 43): by the
  provider itself, by a notified body, or under its Annex I sector law

**Excluded:** general-purpose AI models (Ch. V), Art. 50 transparency duties, Art. 27 impact assessments.

**Existing ontologies.**

Imported:

- [DPV `eu-aiact` v2.3](https://w3id.org/dpv/legal/eu/aiact): risk tiers, Annex I and III lists, authorities
- [AIRO 1.0](https://w3id.org/airo): AI systems and operators
- [ELI 1.4](https://op.europa.eu/en/web/eu-vocabularies/eli): the Act's articles as citable legal resources
- [SKOS](https://www.w3.org/TR/skos-reference/): The task asks for a label and description on every term, and `eu-aiact` uses `skos:prefLabel` and `skos:definition`.

Aligned: [PROV-O](https://www.w3.org/TR/prov-o/) and [ORG](https://www.w3.org/TR/vocab-org/) model an
agent acting in a role, as our role assignments do; [DPV core](https://w3id.org/dpv) is what `eu-aiact` extends; [ODRL](https://www.w3.org/TR/odrl-vocab/) is the standard vocabulary of duties and permissions.

**Added.** Seventeen local classes to meet the competency questions:

- role assignment, reassignment and termination:
  `aia:Role`, `RoleAssignment`, `RegulatoryEvent`, `RoleReassignment`,
  `ReassignmentCondition`, `TerminatedRoleAssignment`
- classification grounds: `ClassificationGround`, `PurposeGround`, `AnnexIIIGround`, `DerogatedAnnexIIIGround`, `AnnexIGround`, `HighRiskByGround`
- duties and prohibitions: `aia:Obligation`, `ProhibitedPractice`, `Exemption`
- oversight and conformity: `OversightAssignment`, `ConformityAssessmentRoute`

A worked example (`aia-example.ttl`) covers all four tiers (see `README.md` for details).

## 2. AI-assisted pipeline

A Claude Project (**Opus 5.0**) holding the task specification was used to plan the deliverables and draft a survey of existing ontologies, competency questions, SPARQL and SHACL shapes. Claude Code (Opus 5.0 and 5.5) was used to generate the ontology and ran first-pass validation in parallel with my verification in intermediate steps; Claude Code ran HermiT reasoning and SHACL validation in a command shell as part of its development process. I then manually loaded the ontology into Protégé and ran HermiT for validation (see screenshots in `evidence/`).

Nothing Claude proposed was finalised until checked against **parsed RDF** (claims about an
ontology) and **the Official Journal** (the Act).

## 3. Key modelling decisions

**Roles are reified.** A role is held per system: under Article 25(1)(b) a deployer that
substantially modifies a high-risk system becomes the provider of that system, and Article
25(2) ends the original provider's role for it alone. `aia:RoleAssignment` therefore links actor,
role and system.

**Obligations attach to roles.** The Act addresses duties to roles: Article 16 lists what providers
must do and Article 26 what deployers must do, so a party's duties follow from the roles it holds.
No surveyed ontology links a duty to the party bound by it, so `aia:borneBy` links each obligation
to its role, and `aia:borneOnTermination` carries the duties Article 25(2) leaves the former provider.

**Annex III is split in two.** Article 6(3) takes some Annex III systems back out of high risk, and
OWL cannot retract an inference, so the exception is recorded as a separate class:
`aia:AnnexIIIGround` makes a system high-risk, `aia:DerogatedAnnexIIIGround` does not. An AI system acting as a
recruitment tool that ranks candidates is high-risk; one that only reformats CVs is a narrow procedural task and is not.

**Article 5 prohibits practices, not systems.** What is banned is how a system is used, not the
system itself: an emotion-recognition system is prohibited in the workplace or education (Art. 5(1)(f)) but allowed there for
medical or safety reasons. `aia:ProhibitedPractice` therefore models the use, separately from
`eu-aiact:ProhibitedAISystem`.

## 4. Competency questions and SPARQL

1. Into which risk category does a system fall, and on what grounds — intended purpose, Annex
   III area, or Annex I product route?
2. Which practices are prohibited, which article prohibits each, and which have conditional
   exemptions?
3. Which obligations attach to the provider of a high-risk system, and which to its deployer?
4. Under what conditions does a deployer, distributor or importer become a provider, which
   obligations does it acquire, and what becomes of the initial provider?
5. Which authority oversees a given obligation, and which conformity assessment route applies?

The queries for all five are in `queries/`. **CQ3**, below, shows a provider whose role ended keeping only its residual duties.

```sparql
SELECT ?actorLabel ?roleLabel ?standing ?obligationLabel ?article WHERE {
  VALUES ?system { aia:ExampleRecruitmentScreeningSystem }
  ?system aia:hasRiskCategory eu-aiact:RiskLevelHigh .
  ?a a aia:RoleAssignment ; aia:concernsSystem ?system ;
     aia:hasRole ?role ; aia:heldBy ?actor .
  ?actor skos:prefLabel ?actorLabel . ?role skos:prefLabel ?roleLabel .
  FILTER (?role IN (aia:Provider, aia:Deployer))
  OPTIONAL { ?a a aia:TerminatedRoleAssignment . BIND ("ended" AS ?standing) }
  ?obligation a aia:Obligation ; aia:appliesToCategory eu-aiact:RiskLevelHigh ;
     skos:prefLabel ?obligationLabel ; aia:statedIn ?article .
  FILTER ( (!BOUND(?standing) && EXISTS { ?obligation aia:borneBy ?role })
        || ( BOUND(?standing) && EXISTS { ?obligation aia:borneOnTermination ?role }) )
} ORDER BY ?actorLabel ?roleLabel ?article
```

## 5. Validation and evaluation metrics

The ontology loads in Protégé and is consistent under HermiT
(see screenshots in `evidence/`). Proposed metrics:

- **CQ answerability:** all five competency questions return answers over the worked example.
- **Annotation completeness:** every term has a label, a definition and an article reference.
- **Provision coverage:** modelled items against the Act's own lists, e.g. all ten Art. 5 practices.
- **Expert legal review** of each obligation and practice, the only check that catches a wrong reading of the law.
