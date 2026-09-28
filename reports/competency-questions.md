# EU AI Act Ontology — Competency Questions and SPARQL

*Competency questions, their mapping to the task specification, and their SPARQL (also in `../queries/`). Version modelled: the Act **as amended by Regulation (EU) 2026/1744**, `http://data.europa.eu/eli/reg/2024/1689/oj`, read in the consolidated text of 27 July 2026 (`report.md` §1).*

---

## Namespace prefixes

All queries below assume the following prefix block.

```sparql
PREFIX aia:  <https://w3id.org/aia-ont#>
PREFIX eli:  <http://data.europa.eu/eli/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX airo: <https://w3id.org/airo#>
PREFIX vair: <https://w3id.org/vair#>
PREFIX dpv:  <https://w3id.org/dpv/owl#>
PREFIX org:  <http://www.w3.org/ns/org#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX eu-aiact: <https://w3id.org/dpv/legal/eu/aiact/owl#>
```

`eu-aiact:` is the **OWL** serialisation of DPV's AI Act extension (the SKOS one, `…/aiact#`, does not declare `owl:Class`); the ontology file binds the same IRI as `eu-aiact-owl:`. `dpv:` is the `/owl#` namespace, because `eu-aiact` references only the `/owl#` variants (survey, candidate 4).

No article-level ELI URIs exist for this regulation (`…/1689/art_6` resolves to the whole act), so articles are minted in `aia:` as `eli:LegalResourceSubdivision` with `eli:is_part_of` the act. No query dereferences them.

Every query projects a label, a description and an article reference, so a null in those columns is an annotation gap in the ontology, not a query defect.

---

## What is local, and what is not

The skeleton's **fourteen** classes are each a gap in all sixteen surveyed candidates; nothing is minted where an imported term exists.

| Local | Imported and used as-is |
|---|---|
| `aia:Role`, `aia:RoleAssignment` | `airo:AISystem`, `airo:AIComponent`, `airo:GPAIModel` |
| `aia:RegulatoryEvent` → `aia:RoleReassignment` | `eu-aiact:RiskLevel` and its tiers |
| `aia:ReassignmentCondition` | `eu-aiact:HighRiskAISystem`, `…-AnnexI-*`, `…-AnnexIII-*` |
| `aia:Obligation` | `eu-aiact:ProhibitedAISystem-A5-1-a … -h` |
| `aia:ProhibitedPractice`, `aia:Exemption` | `eu-aiact:IntendedPurpose` |
| `aia:ClassificationGround` → `aia:PurposeGround`, `aia:AnnexIIIGround`, `aia:AnnexIGround` | `eu-aiact:NationalCompetentAuthority`, `MarketSurveillanceAuthority`, `NotifiedBody`, `AIOffice` |
| `aia:OversightAssignment`, `aia:ConformityAssessmentRoute` | `eu-aiact:SubstantialModification`, `ConformityAssessment` |

Two local classes resemble `eu-aiact` terms and are not duplicates:

- **`aia:ProhibitedPractice`** is not `eu-aiact:ProhibitedAISystem`, which is a subclass of `AISystem`. Article 5 prohibits *practices* — placing on the market, putting into service, use — not artefacts, and the same system may be lawfully deployed for one purpose and prohibited for another.
- **`aia:ConformityAssessmentRoute`** is not `eu-aiact:ConformityAssessment`, which is the assessment process (Art. 3(20)). The route is the *choice* between the Annex VI internal-control procedure and the Annex VII quality-management procedure, for which `eu-aiact` has no term.

The three `aia:ClassificationGround` subclasses are named for the classification route rather than for the Annex, because `eu-aiact:IntendedPurpose` already exists and a local `aia:IntendedPurpose` would collide with it.

**Disjointness.** One `owl:AllDisjointClasses` axiom covers `Role`, `RoleAssignment`, `RegulatoryEvent`, `Obligation`, `ProhibitedPractice`, `Exemption`, `ClassificationGround`, `ConformityAssessmentRoute`, `airo:AISystem` and `airo:AIOperator`. Two omissions are deliberate:

- `aia:OversightAssignment` is excluded, because an authority supervising a duty may later be modelled as holding a role, which would make oversight a kind of role assignment. Asserting disjointness now would foreclose that.
- `aia:ReassignmentCondition` is excluded, because Article 25(1)(c) is simultaneously a reassignment condition and a classification ground: modifying a system's intended purpose so that it becomes high-risk does both jobs at once.

The three `ClassificationGround` subclasses are likewise **not** pairwise disjoint, since under Article 6(2) a system is high-risk where its intended purpose falls within an Annex III use case — so one ground can be both a purpose ground and an Annex III ground.

Roles are not declared pairwise disjoint anywhere; that commitment is set out next.

---

## Modelling commitment: roles as reified assignments

CQ3 and CQ4 depend on this. A role under the Act holds relative to one AI system, is contingent on conduct, and can change hands: Article 25 can make a deployer the provider of one system while its other roles are untouched. Role classes cannot express this; asserting both loses which system each concerns, and making them disjoint makes the Article 25 case inconsistent.

`aia:RoleAssignment` therefore relates an actor, a role and a system, and gives the role-holding somewhere to carry its system, grounds and establishing provision. **`aia:Role` is a class whose members are roles**, so `aia:Provider` and `aia:Deployer` are individuals, unlike `eu-aiact:AIProvider`, a class of actors. Roles are not pairwise disjoint: an actor may hold several for one system and bear each set of obligations cumulatively.

The cost is a join in every obligation query. A binary `aia:isProviderOf` would scope roles to systems more cheaply, but CQ4 needs the grounds and the transfer to be representable.

No surveyed vocabulary offers this shape. AIRO, `eu-aiact` and AICat all model roles as classes; PROV-O's `prov:Association` and ORG's `org:Membership` reify correctly but bind the third argument to an activity and an organisation respectively, neither of which is an AI system, so both are aligned rather than subclassed.

---

## CQ1 — Risk category and its grounds

**Question.** Into which risk category does a given AI system fall, and on what grounds (intended purpose, Annex III area, or Annex I product-safety route)?

**Specification coverage.** AI system categories; high-risk systems; annotations (label, description, article reference).

**Reuse.** `eu-aiact:RiskLevel` and its tiers (`RiskLevelProhibited`, `RiskLevelHigh`, `RiskLevelTransparencyRequired`, `RiskLevelMinimal`) for the categories, and the `eu-aiact:HighRiskAISystem-AnnexI-1…20` and `-AnnexIII-1-a…8-b` enumerations for the grounds; `airo:AISystem` with AIRO's five Annex III determinant properties (`airo:isAppliedWithinDomain`, `airo:hasPurpose`, `airo:hasCapability`, `airo:isDeployedBy`, `airo:hasAISubject`); VAIR terms as determinant values; ELI for the Annex and article references; SKOS for labels and definitions.

AIRO defines **no risk-category classes**; the categories come from `eu-aiact`. Two pieces are local: the rule connecting grounds to category (`aia:ClassificationGround` and `aia:HighRiskByGround`), and `aia:hasRiskCategory`, because `eu-aiact:hasRiskLevel` ranges over punned class/individual terms through which subsumption does not propagate.

```sparql
SELECT ?system ?systemLabel ?category ?categoryLabel ?categoryDefinition
       ?groundType ?ground ?groundLabel ?article
WHERE {
  ?system a airo:AISystem ;
          skos:prefLabel ?systemLabel ;
          aia:hasRiskCategory ?category .

  ?category a eu-aiact:RiskLevel ;
            skos:prefLabel ?categoryLabel .

  OPTIONAL { ?category skos:definition ?categoryDefinition }
  OPTIONAL { ?category aia:definedIn   ?article }

  OPTIONAL {
    ?system aia:classifiedOnGround ?ground .
    ?ground a ?groundType ;
            skos:prefLabel ?groundLabel .
    VALUES ?groundType {
      aia:PurposeGround
      aia:AnnexIIIGround
      aia:DerogatedAnnexIIIGround
      aia:AnnexIGround
    }
  }
}
ORDER BY ?systemLabel ?categoryLabel
```

A ground returned twice, once under each of two ground types, is the Article 6(2) case — intended purpose falling within an Annex III use case — and is intended behaviour, not duplication. The three ground classes are not disjoint for exactly this reason.

**Reasoner variant.** The same question posed as an entailment check, to be run after classification in Protégé rather than as a data query:

```sparql
ASK {
  aia:ExampleRecruitmentScreeningSystem a eu-aiact:HighRiskAISystem .
}
```

This ASK is entailed through `aia:HighRiskByGround ⊑ eu-aiact:HighRiskAISystem`, with no axiom added to the import. An equivalence on the imported class would make a recorded ground necessary as well as sufficient, so a high-risk system recorded without its ground would be inconsistent rather than under-described (`STATUS.md`, decision 1).

**The Article 6(3) derogation is recorded, not inferred.** Article 6(3) takes an Annex III system out of high risk where it performs only a narrow procedural task, improves a completed human activity, detects decision patterns without replacing human assessment, or performs a preparatory task, unless it profiles natural persons. OWL cannot retract the rule's conclusion or infer a derogation from the absence of one, so such a use case is recorded as an `aia:DerogatedAnnexIIIGround`, disjoint from `aia:AnnexIIIGround` and not a disjunct of the rule. CQ1 returns it with the system's actual tier: in the worked example, the HireDesk CV formatter is in the Annex III 4(a) area, derogated under 6(3)(a), and minimal-risk.

**The Annex I route is narrower than Annex I.** Article 6(1a)–(1b) and the definition in Article 3(14) decide what counts as a safety component, and Article 6(1c) discounts a third-party assessment required only for risks other than health and safety. These conditions are applied when an `aia:AnnexIGround` is recorded; the reasoner does not test them. And under Article 2(2), a system related to an Annex I, **Section B** product (machinery among them since Regulation (EU) 2023/1230 moved to point 21) is high-risk but carries none of the Chapter III duties, which is why the worked example's Annex I system is a Section A medical device. `eu-aiact:HighRiskAISystem-A6-1` and its Annex I enumeration predate both points.

---

## CQ2 — Prohibited practices, with provenance and exceptions

**Question.** Which practices are prohibited, which article prohibits each, and which of them are subject to conditional exemption?

**Specification coverage.** Prohibited practices; annotations (label, description, article reference).

**Reuse.** `eu-aiact:ProhibitedAISystem-A5-1-a` … `-A5-1-h` for eight of the ten prohibitions; ELI for article-level identification of the prohibiting provision; SKOS for labels and definitions. `aia:hasExemption` and its range `aia:Exemption` are local: no surveyed vocabulary models the conditional exemptions, which is the half of this question that makes it more than a list.

`aia:ProhibitedPractice` is also local, and deliberately distinct from `eu-aiact:ProhibitedAISystem`, which is a subclass of `AISystem`. Article 5 prohibits practices, not artefacts. Each `aia:ProhibitedPractice` instance references the corresponding `eu-aiact:ProhibitedAISystem-A5-1-*` term rather than replacing it.

```sparql
SELECT ?practice ?practiceLabel ?practiceDefinition
       ?article ?articleNumber
       ?exemption ?exemptionLabel ?exemptionArticle
WHERE {
  ?practice a aia:ProhibitedPractice ;
            skos:prefLabel ?practiceLabel ;
            aia:prohibitedBy ?article .

  ?article a eli:LegalResourceSubdivision ;
           eli:is_part_of <http://data.europa.eu/eli/reg/2024/1689/oj> .

  OPTIONAL { ?practice skos:definition ?practiceDefinition }
  OPTIONAL { ?article  eli:number      ?articleNumber }

  OPTIONAL {
    ?practice aia:hasExemption ?exemption .
    ?exemption a aia:Exemption ;
               skos:prefLabel ?exemptionLabel .
    OPTIONAL { ?exemption aia:providedFor ?exemptionArticle }
  }
}
ORDER BY ?articleNumber ?practiceLabel
```

A prohibited practice returned with no `?exemption` binding is unconditionally prohibited; one with bindings is prohibition-with-conditions. This distinction is what prevents the prohibitions being modelled as a flat enumeration.

Article 5(1) lists ten prohibitions, lettered (a), (b), (ba), (bb), (c)–(h). `eu-aiact` was last modified four months before Regulation (EU) 2026/1744 inserted (ba) and (bb), and has no terms for them, so those two practices are minted locally and cross-reference the amending act instead. Both are narrowed by Article 5(1a), (ba) also by 5(1b) and (bb) by its "without right" defence, and all three are modelled as exemptions. Under Article 113(a) they apply from 2 December 2026.

---

## CQ3 — Actor-indexed obligations

**Question.** Which obligations attach to the provider of a high-risk AI system, and which to the deployer of that same system?

**Specification coverage.** Core actors (providers, deployers); major obligations; high-risk systems; annotations.

**Reuse.** `dpv:Obligation` — in the `/owl#` namespace — alone for the deontic parent; `org:Organization` for the actors holding the roles; ELI for the stating article. LKIF-Core was surveyed and rejected — it makes `Obligation` a subclass of `Permission`, which would entail that every Article 16 provider duty is a permission — and ODRL's assigner/assignee framing fits policies issued by a party over an asset it controls rather than duties imposed by statute. DAOnt, which does the equivalent job for the EU Data Act, declares no `owl:imports` at all and aligns to these vocabularies by reference; that is the pattern followed here.

`aia:borneBy` is local, and unavoidably so. **No surveyed ontology attaches an obligation to the role that bears it**: `dpv:hasObligation` has domain `dpv:Context` and MAILO's `hasObligation` has domain `RegulatoryFramework`, both attaching duties to the legal source rather than to the party bound. The traversal this query performs exists nowhere to be reused.

```sparql
SELECT ?actorLabel ?roleLabel ?standing ?obligation ?obligationLabel ?obligationDefinition ?article
WHERE {
  VALUES ?system { aia:ExampleRecruitmentScreeningSystem }

  ?system aia:hasRiskCategory eu-aiact:RiskLevelHigh .

  ?assignment a aia:RoleAssignment ;
              aia:concernsSystem ?system ;
              aia:hasRole        ?role ;
              aia:heldBy         ?actor .

  ?actor skos:prefLabel ?actorLabel .
  ?role  a aia:Role ;
         skos:prefLabel ?roleLabel .
  FILTER (?role IN (aia:Provider, aia:Deployer))

  # Article 25(2): an assignment the Act has ended no longer carries its role's
  # duties, only the residual ones attached to the ending. This cites a MODELLED
  # CLASS rather than restating the rule, so if the circumstances that end an
  # assignment are ever broadened, the axiom changes and this query follows.
  OPTIONAL { ?assignment a aia:TerminatedRoleAssignment .
             BIND ("ended by Art. 25(2)" AS ?standing) }

  ?obligation a aia:Obligation ;
              aia:appliesToCategory eu-aiact:RiskLevelHigh ;
              skos:prefLabel        ?obligationLabel ;
              aia:statedIn          ?article .
  FILTER ( (!BOUND(?standing) && EXISTS { ?obligation aia:borneBy ?role })
        || ( BOUND(?standing) && EXISTS { ?obligation aia:borneOnTermination ?role }) )

  OPTIONAL { ?obligation skos:definition ?obligationDefinition }
}
ORDER BY ?actorLabel ?roleLabel ?article
```

`aia:Provider` and `aia:Deployer` are individuals of `aia:Role`, not classes, which is why they appear in a `FILTER … IN` over values rather than as types. Where an actor holds more than one role in respect of the system — the post-Article 25 case — it is returned once per role, with the obligations of each. This is the intended behaviour, not duplication.

`aia:TerminatedRoleAssignment` is entailed, not asserted, so this query needs the inferred graph (finding 4). A terminated assignment returns only the residual duties of Article 25(2), marked `?standing`, instead of its role's full set.

---

## CQ4 — Role reassignment under Article 25

**Question.** Under what conditions does a deployer, distributor or importer become a provider, which obligations does it thereby acquire, and what becomes of the initial provider?

**Specification coverage.** Core actors; major obligations; annotations.

**Reuse.** PROV-O's qualified-association pattern (`aia:RoleAssignment ⊑ prov:Association`, `aia:heldBy ⊑ prov:agent`, `aia:hasRole ⊑ prov:hadRole`) and ORG's `org:Membership` as the design precedent — neither subclassed wholesale, since `prov:Association` takes no fourth argument for the system and `org:Membership`'s range is `org:Organization` with functional properties that would silently identify two systems as one. `eu-aiact:SubstantialModification` and `eu-aiact:DownstreamAIProvider` supply the trigger vocabulary; `eu-aiact`'s own roles are classes, so it has nothing to attach that vocabulary to.

The alignment axioms live in `aia-align.ttl`, which the core does not import.

A reassignment is modelled as an event relating role assignments for one system: `aia:RoleReassignment`, a subclass of `aia:RegulatoryEvent`, with its trigger typed `aia:ReassignmentCondition`. It is deliberately **asymmetric**:

- `aia:promotes` names the assignment whose holder acquires the provider role. That prior assignment is *not* ended. Article 25(1) provides that the party shall be considered a provider and be subject to the obligations of Article 16; it does not provide that the prior role ceases. Recital 83 supports the cumulative reading, contemplating operators that act in more than one role at once and must fulfil all associated obligations. Recitals are interpretive aids rather than operative provisions, and Recital 83's own example concerns an operator acting as distributor and importer, not the Article 25 case. This is therefore recorded as a modelling decision resting on a reading of Recital 83, not as a proposition stated in the operative text.
- `aia:terminates` names the initial provider's assignment, which does end. Article 25(2) provides in terms that the initial provider shall no longer be considered the provider of that specific system.

The initial provider does not simply drop out. Article 25(2) requires it to cooperate closely with the new provider and, in particular, to make technical documentation available, disclose known limitations and failure modes, and give targeted technical access, unless it clearly specified that the system was not to be made high-risk. These four duties are attached through `aia:borneOnTermination` to the role whose assignment was ended, and CQ4 returns them in `?initialProviderDuties`. This is the strongest case against role-as-class: a duty that outlives its role has nothing to attach to under class membership, whereas it can hang off an ended assignment.

```sparql
SELECT ?actorLabel ?fromRoleLabel ?conditionLabel ?triggeringArticle
       ?acquiredObligation ?acquiredLabel ?acquiredArticle
       ?initialProviderLabel ?initialProviderDuties
WHERE {
  ?reassignment a aia:RoleReassignment ;
                aia:concernsSystem ?system ;
                aia:promotes       ?priorAssignment ;
                aia:establishes    ?newAssignment ;
                aia:triggeredBy    ?condition ;
                aia:statedIn       ?triggeringArticle .

  ?priorAssignment aia:concernsSystem ?system ;
                   aia:hasRole        ?fromRole ;
                   aia:heldBy         ?actor .

  ?newAssignment   aia:concernsSystem ?system ;
                   aia:hasRole        aia:Provider ;
                   aia:heldBy         ?actor .

  ?actor     skos:prefLabel ?actorLabel .
  ?fromRole  skos:prefLabel ?fromRoleLabel .
  ?condition a aia:ReassignmentCondition ;
             skos:prefLabel ?conditionLabel .

  ?acquiredObligation a aia:Obligation ;
                      aia:borneBy    aia:Provider ;
                      skos:prefLabel ?acquiredLabel ;
                      aia:statedIn   ?acquiredArticle .

  # obligations genuinely acquired, i.e. not already borne in the retained prior role
  FILTER NOT EXISTS { ?acquiredObligation aia:borneBy ?fromRole }

  # Article 25(2): the initial provider's assignment is terminated
  OPTIONAL {
    ?reassignment aia:terminates ?initialProviderAssignment .
    ?initialProviderAssignment aia:concernsSystem ?system ;
                               aia:hasRole        aia:Provider ;
                               aia:heldBy         ?initialProvider .
    ?initialProvider skos:prefLabel ?initialProviderLabel .
    OPTIONAL {
      SELECT ?initialProviderAssignment
             (GROUP_CONCAT(DISTINCT ?dutyLabel; separator="; ") AS ?initialProviderDuties)
      WHERE {
        ?initialProviderAssignment a aia:TerminatedRoleAssignment ;
                                   aia:hasRole ?endedRole .
        ?duty aia:borneOnTermination ?endedRole ;
              skos:prefLabel ?dutyLabel .
      }
      GROUP BY ?initialProviderAssignment
    }
  }
}
ORDER BY ?actorLabel ?acquiredArticle
```

Binding `aia:heldBy` to the same `?actor` across the promoted and established assignments is what encodes that the *same* party changed standing, rather than one party gaining a role while an unrelated party lost one. The initial provider reached through `aia:terminates` is a distinct actor.

Expected results correspond to the three circumstances of Article 25(1) — affixing one's name or trademark to a high-risk system already placed on the market, making a substantial modification to such a system, and modifying the intended purpose of a system such that it becomes high-risk — with the acquired obligations being those of Article 16.

---

## CQ5 — Oversight and conformity assessment routes

**Question.** Which authority or body oversees a given obligation, and which conformity assessment route applies to a given high-risk AI system?

**Specification coverage.** Core actors (authorities); major obligations; high-risk systems; annotations.

**Reuse.** `eu-aiact:MarketSurveillanceAuthority`, `NationalCompetentAuthority`, `NotifiedBody`, `NotifyingAuthority`, `AIOffice` and `ConformityAssessmentBody` for the institutions, and `eu-aiact:ConformityAssessment`, `EUDeclarationOfConformity` and `CEMarking` for the route artefacts; `org:Organization` as their common type; ELI for the procedural articles and annexes. `aia:oversees` is local — `eu-aiact` names the authorities but does not connect them to the obligations they supervise, and that connection presupposes obligations as objects, so it fails for the same reason as CQ3.

There are three routes: Annex VI internal control or Annex VII quality management for Annex III systems (Article 43(1)–(2)), and the procedure of the relevant Annex I, Section A legislation for systems it covers, including those also listed in Annex III (Article 43(3)). The AI Office binds no row over the worked example: its competence over AI systems under Article 75(1) reaches only systems built on a general-purpose AI model by the same provider and systems in very large online platforms or search engines.

```sparql
SELECT ?obligation ?obligationLabel ?article
       ?authority ?authorityLabel ?authorityType
       ?route ?routeLabel ?routeArticle
WHERE {
  ?obligation a aia:Obligation ;
              skos:prefLabel ?obligationLabel ;
              aia:statedIn   ?article .

  OPTIONAL {
    ?oversight a aia:OversightAssignment ;
               aia:oversees   ?obligation ;
               aia:assignedTo ?authority .
    ?authority a org:Organization ;
               a ?authorityType ;
               skos:prefLabel ?authorityLabel .
    VALUES ?authorityType {
      eu-aiact:NationalCompetentAuthority
      eu-aiact:MarketSurveillanceAuthority
      eu-aiact:NotifiedBody
      eu-aiact:AIOffice
    }
  }

  OPTIONAL {
    ?route a aia:ConformityAssessmentRoute ;
           aia:appliesToObligation ?obligation ;
           skos:prefLabel          ?routeLabel ;
           aia:statedIn            ?routeArticle .
  }
}
ORDER BY ?article ?authorityLabel
```

---

## Coverage summary

| Specification element | CQ1 | CQ2 | CQ3 | CQ4 | CQ5 |
|---|---|---|---|---|---|
| AI system categories | ● | | | | |
| Prohibited practices | | ● | | | |
| High-risk systems | ● | | ● | ● | ● |
| Core actors — providers, deployers | | | ● | ● | |
| Core actors — authorities | | | | | ● |
| Major obligations | | | ● | ● | ● |
| Annotations (label, description, article ref.) | ● | ● | ● | ● | ● |
| Reuse of existing vocabularies | ● | ● | ● | ● | ● |

---

## Results

`scripts/run-cq-queries.py` loads the core, the worked example and the four imports, computes the OWL 2 RL closure and runs every file in `../queries/`. Full output: `cq-results.md`.

| Query | Form | Asserted graph | Inferred graph |
|---|---|---|---|
| CQ1 — risk category and grounds | SELECT | 10 rows | **10 rows** |
| CQ1 — reasoner variant | ASK | `false` | **`true`** |
| CQ2 — prohibited practices | SELECT | 17 rows | **17 rows** |
| CQ3 — actor-indexed obligations | SELECT | 35 rows | **27 rows** |
| CQ4 — Article 25 reassignment | SELECT | 36 rows | **36 rows** |
| CQ5 — oversight and conformity routes | SELECT | 29 rows | **31 rows** |

Three rows depend on the reasoner. CQ1's ASK is true only through `aia:HighRiskByGround`; nothing asserts it. CQ5 gains two rows from `eu-aiact`'s authority hierarchy (finding 2). CQ3 loses eight: the initial provider's twelve Article 16 duties give way to its four Article 25(2) residual duties, because the query cites an entailed class (finding 4). CQ4's `?initialProviderDuties` binds only over the inferred graph, for the same reason.

**1. CQ2 returns 17 rows, not 16.** Ten practices, four unconditional and six with twelve exemptions, give 16. The 17th is `aia:ex_art5_1_h_suspect`, which has two `aia:providedFor` values: Article 5 (the four-year threshold) and Annex II (the offence list). Both are load-bearing. `check-reasoner.py` expects 16 because it counts the practice/exemption pattern, not rows.

**2. CQ5 returns the market surveillance authority twice per obligation.** `eu-aiact` makes `MarketSurveillanceAuthority` a subclass of `NationalCompetentAuthority` (faithful to Article 3(48)), and both are in CQ5's `VALUES` list. A most-specific-type filter would remove the duplicate; the data is correct.

**3. CQ5 answers only half its question.** Routes relate to obligations (`aia:appliesToObligation`), not systems, so "which route applies to a given system" is answered per obligation. The fix, an `aia:appliesToSystem` property or a join through the role assignment, is not taken, because the property set is exactly what the queries bind.

**4. CQ3 returned a terminated role assignment; fixed.** Twelve of the first run's 35 rows were Article 16 duties of TalentFlow GmbH, whose provider assignment Article 25(2) ends: the initial provider "shall no longer be considered to be a provider of that specific AI system". The termination was an edge on the event, and CQ3 never looked at events. The fix derives liveness: `aia:terminatedBy` is the inverse of `aia:terminates`, `aia:TerminatedRoleAssignment ≡ ∃terminatedBy.RoleReassignment`, and CQ3 gives an assignment of that class only the duties `aia:borneOnTermination` its role. CQ3 now returns 27 rows: TalentFlow with its four Article 25(2) residual duties, and North Borough Council twice, with 12 provider and 11 deployer duties. `STATUS.md` decision 5 gives the rejected alternatives.

This is not the conditional-obligation gap. The termination qualifies no duty; it changes who holds the role. The conditional duties of Articles 16(e), 25(2), 26(8)–(11) and 5(2)–(5) remain open, and fixing this left them unchanged, which shows the two are separate mechanisms.

---

## Verification status

- **ELI terms** `eli:LegalResourceSubdivision`, `eli:is_part_of` and `eli:number` exist as used, and the typing satisfies ELI v1.4's domain axioms (`reuse-decisions.md`).
- **`airo:AISystem`** carries the Article 3(1) definition verbatim. AIRO defines no risk categories and was updated against the adopted text.
- **Articles 5, 16, 25, 26 and 43(3), Annex I and Recital 83** are checked against the consolidated Official Journal text of 27 July 2026; other cited provisions are not. The `?article` column binds on every row except CQ1's minimal-risk tier, which no article establishes.
- **Regulation (EU) 2026/1744** was read in full, all 43 amendment points. Those bearing on the model are Articles 2(2), 2(13), 3(14), 5, 6(1a)–(1c), 25(2), 43(3), 75(1), 99(4)(da) and 113 and Annex I; the rest concern sandboxes, notified-body designation, SME simplification, guidance and GPAI.
