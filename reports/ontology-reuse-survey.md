# EU AI Act Ontology — Existing Ontology Reuse Survey

*Companion to `../prompts/prompt-ontology-survey.md`, the prompt that ran this survey. Every verdict below is now binding; the register is `reuse-decisions.md` (4 imported, 5 aligned, 7 excluded).*

---

## Method and verification status

Sixteen candidates were examined: the eight named in the prompt, plus five further AI-Act-specific artefacts and three methodological precedents found by search.

Every claim about a term IRI, axiom count or licence was checked against a retrieved serialisation, with counts computed from the RDF. Claims that could not be checked are marked **unverified**.

**Second pass, 2026-09-25.** ELI, PROV-O, ORG, SKOS and ODRL were first assessed from their specifications, their hosts being unreachable, then fetched and parsed. Four of the five produced corrections, marked *(corrected 2026-09-25)*; no verdict changed.

**Third pass, 2026-09-25 (build).** Each import's ontology IRI was read from its `owl:Ontology` declaration, and ELI from the canonical download. Four corrections, marked *(corrected in build)* and listed at the end.

| Candidate | Serialisation retrieved | Basis for term claims |
|---|---|---|
| AIRO | `airo.ttl`, 558 triples | parsed |
| VAIR | `vair.ttl`, 5,803 triples | parsed |
| DPV `eu-aiact` | `eu-aiact.ttl` / `eu-aiact-owl.ttl`, 2,407 / 2,173 triples | parsed |
| DPV core, `tech`, `ai`, `risk` | all four `.ttl` | parsed |
| ELI | `eli.owl`, **v1.4, canonical op.europa.eu download** | parsed *(corrected in build)* |
| LKIF-Core | 12 modules, 2,044 triples | parsed |
| PROV-O | `prov-o.ttl`, 68,795 bytes | parsed |
| ORG | `org.ttl`, 77,830 bytes | parsed |
| SKOS | `skos.rdf`, 28,966 bytes | parsed |
| ODRL | `ODRL22.ttl`, 90,970 bytes | parsed |
| AICat, AIUP | `aicat.ttl`, `aiup.ttl` | parsed |
| MAILO | `ontology.ttl`, 1,946 triples | parsed |
| TAIR | **none — not published** | paper only; all terms **unverified** |
| DAOnt | `DAOnt.ttl`, 1,073 triples | parsed |

Measured axiom profiles, for reference throughout:

| Ontology | Triples | Named classes | Obj. props | Data props | Individuals | `disjointWith` | Restrictions |
|---|---:|---:|---:|---:|---:|---:|---:|
| AIRO | 558 | 56 | 61 | 2 | 0 | 0 | 0 |
| VAIR | 5,803 | 448 | 0 | 0 | 538 | 0 | 0 |
| DPV `eu-aiact` (OWL) | 2,173 | 167 | 3 | 0 | 0 | 0 | 0 |
| LKIF-Core (12 modules) | 2,044 | 157 | 100 | 0 | 0 | **28** | **181** |
| MAILO | 1,946 | 65 | 43 | 39 | 0 | 0 | 0 |
| DAOnt | 1,073 | 84 | 66 | 24 | 4 | 4 | 10 |
| AIUP | 255 | 4 | 0 | 0 | 10 | 12 | 0 |
| AICat | 89 | 3 | 2 | 0 | 0 | 0 | 0 |
| ELI 1.4 | 1,505 | 27 | 71 | 18 | 0 | 0 | 11 |
| PROV-O | — | 39 | 44 | — | 0 | **4** | 1 |
| ORG | — | 13 | 31 | — | 0 | **10** | 1 |
| SKOS | — | 4 | 17 | — | 0 | **3** | 0 |
| ODRL 2.2 | — | 45 | 46 | — | 0 | **10** | 0 |

One finding conditions everything below and is stated once here. **The DPV family declares no disjointness, no cardinality and no class restrictions anywhere** — verified across core (14,909 triples), `tech`, `ai`, `risk` and `eu-aiact`. LKIF-Core is the opposite: 28 disjointness axioms and 181 restrictions in 2,044 triples. The import-risk verdicts follow almost mechanically from that contrast.

---

## Candidate 1 — AIRO (AI Risk Ontology)

| Field | Finding |
|---|---|
| **Identity** | AI Risk Ontology. Namespace `https://w3id.org/airo#`; ontology IRI `https://w3id.org/airo`, `owl:versionIRI` `https://w3id.org/airo/1.0`. ADAPT Centre, Trinity College Dublin (Golpayegani, Pandit, Lewis). `dcterms:created` 2021-09-01, `dcterms:modified` **2024-05-25**. CC BY 4.0. Spec: `https://w3id.org/airo` (resolves to `delaramglp.github.io/airo`). Serialisation: `raw.githubusercontent.com/DelaramGlp/airo/main/airo.ttl`. |
| **CQs borne on** | **CQ1, determinants only.** AIRO supplies precisely the five Annex III determinants and their relations, all verified present: `airo:Domain` / `airo:isAppliedWithinDomain`, `airo:Purpose` / `airo:hasPurpose`, `airo:AICapability` / `airo:hasCapability`, `airo:AIDeployer` / `airo:isDeployedBy`, `airo:AISubject` / `airo:hasAISubject`. **CQ3/CQ4, actor identity only**: `airo:AIOperator` with `airo:AIProvider` and `airo:AIDeployer` as subclasses, definitions quoted verbatim from Arts. 3(3) and 3(4) of the adopted text. `airo:AISystem` carries the Art. 3(1) definition and `airo:GPAIModel` the Art. 3(63) definition. |
| **Coverage gaps** | **AIRO defines no risk categories at all.** This is the single most consequential finding about it. Enumerating all 46 `airo:`-namespace class declarations returns no `HighRiskAISystem`, no `ProhibitedAISystem`, no `RiskLevel`, no risk-tier term of any kind. `airo:Risk` is the ISO 31000 sense — "the state of uncertainty associated with an AI system… expressed in terms of risk sources, consequences, impacts, likelihood, and severity" — not the Act's regulatory classification. The high-risk determination that the published documentation presents (Figure 2, "combinations… treated as rules for high-risk uses") lives in the paper, not in the axioms. Also absent: obligations, prohibited practices, authorities, conformity assessment routes. `airo:Regulation` and `airo:compliesWithRegulation` exist but are bare — a class with a one-line comment and an untyped range. |
| **Structural gaps** | Roles are **direct class membership** (`Acme rdf:type airo:AIProvider`), with binary properties `airo:isProvidedBy` / `airo:isDeployedBy` from system to actor. There is no attachment point for the grounds, the period or the establishing provision, so the ternary that commitment 1 requires cannot be expressed. The binary properties do scope role to system, which is the *easier* half of what reification buys; the Art. 25 half is unreachable. Compatibility with commitment 1 is nonetheless good in the negative sense: `AIProvider` and `AIDeployer` are sibling subclasses of `AIOperator` with **no disjointness axiom**, so nothing in AIRO blocks an actor holding both. |
| **Alignment cost** | Low and mostly one-directional. `aia:AISystem ⊑ airo:AISystem`; `aia:Provider`-as-role would align to `airo:AIProvider` only via the role-assignment node (`aia:RoleAssignment aia:hasRole aia:Provider` ⇒ holder `rdf:type airo:AIProvider`), which needs a property chain or a SWRL rule rather than a subclass axiom. Nothing likely to be contested — AIRO's definitions are quotations of the operative text. |
| **Import risk** | **Very low, with one live caveat.** 558 triples, no imports, no disjointness, no restrictions, no cardinality. But AIRO does declare **33 `rdfs:domain` and 50 `rdfs:range`** axioms, twelve of them `owl:unionOf` expressions. These are entailment-generating, not constraints: asserting `?x airo:isDeployedBy ?y` infers `?x rdf:type (airo:AISystem ⊔ airo:AIComponent)`. That is benign until it interacts with a disjointness axiom imported from elsewhere, at which point the inconsistency surfaces in AIRO's vocabulary while originating in the other ontology. It is the concrete form the prompt's "several layers away" risk takes here. |
| **Verdict** | **IMPORT** (decided). `owl:imports <https://w3id.org/airo>` — no trailing hash; AIRO separates ontology IRI from namespace correctly. Cheapest defensible attachment point for AI-system and actor identity, at negligible reasoner cost. It answers no CQ on its own. Binding consequence: `aia:` mints no AI-system, component, model or determinant-property term. |

---

## Candidate 2 — VAIR (Vocabulary of AI Risks)

| Field | Finding |
|---|---|
| **Identity** | Vocabulary of AI Risks. Namespace `https://w3id.org/vair#`; `owl:versionIRI` `https://w3id.org/vair/1.0`. Same authors and centre as AIRO. `dcterms:created` 2022-12-22, `dcterms:modified` **2024-07-18**. CC BY 4.0. Spec `https://w3id.org/vair`; serialisation `raw.githubusercontent.com/DelaramGlp/vair/main/vair.ttl`. |
| **CQs borne on** | **CQ1, the value space.** VAIR is the filler vocabulary for AIRO's slots: 448 terms across domains, purposes, capabilities, risk sources, consequences, impacts, areas of impact and controls. Several are recognisably the Annex III use descriptions — `vair:AssessingRiskOfOffending`, `vair:AssessingRiskOfReoffending`, `vair:AssessingRiskOfIrregularImmigration`, `vair:LifeInsuranceRiskAssessment`, `vair:HealthInsuranceRiskAssessment`, `vair:SmallScaleProvider`. |
| **Coverage gaps** | Same as AIRO and for the same reason: **no risk-tier terms**. A substring sweep for `HighRisk`, `Prohibited`, `RiskLevel`, `RiskCategory`, `Unacceptable` over all 448 terms returns only `vair:DetectingProhibitedBehaviourDuringTest` and `vair:MonitoringProhibitedBehaviourDuringTest` — both purposes, not classifications. No obligations, no authorities, no conformity routes. |
| **Structural gaps** | Two, both material. First, **every one of the 448 terms is punned**: each is declared `rdf:type rdfs:Class, owl:Class` *and* `rdf:type owl:NamedIndividual, skos:Concept, vair:Concept`. Class/individual punning is legal in OWL 2 DL, but the two facets are semantically independent, so a term's `rdfs:subClassOf` hierarchy does not propagate to it in its individual guise. Second, **hierarchy is `rdfs:subClassOf` only** — measured `skos:broader` count is **zero**, against 86 `skos:related`. The SKOS layer is annotation, not structure, so SKOS-based traversal of VAIR returns nothing. |
| **Alignment cost** | Low if VAIR is used as a value vocabulary — `aia:AnnexIIIArea` instances pointed at VAIR terms — and the punning then works in one's favour, since the terms are already individuals. Higher if used as classes, because the Annex III mapping is many-to-many and would need stating locally in any case. The contested point is whether VAIR's purpose taxonomy *is* the Annex III partition; it is adjacent to it but was not derived clause-by-clause from the adopted Annex, so equating them would be an overclaim. |
| **Import risk** | Low on axioms — 5,803 triples, zero object properties, zero disjointness, zero restrictions, zero domain/range. Two practical costs. It **redeclares 22 AIRO terms as bare stubs** (`airo:AIOperator rdf:type rdfs:Class, owl:Class .`) without importing AIRO, so importing VAIR alone gives the AIRO vocabulary stripped of AIRO's axioms; import both and the stubs merge harmlessly. And 448 punned terms in the Protégé class tree is a usability cost on a proof-of-concept. |
| **Verdict** | **ALIGN, not import** (decided). Reference individual VAIR terms as Annex III area and purpose values. Importing 5,803 triples of taxonomy to use perhaps thirty of them is a poor trade on a proof-of-concept, and it is the sub-vocabulary least likely to be exercised by the CQs. Binding consequence: VAIR's purpose taxonomy is **not** asserted to be the Annex III partition. |

---

## Candidate 3 — DPV `eu-aiact` extension *(the closest existing artefact)*

| Field | Finding |
|---|---|
| **Identity** | "EU Artificial Intelligence Act (AI Act)", an extension of the Data Privacy Vocabulary. Namespace `https://w3id.org/dpv/legal/eu/aiact#`; a parallel OWL serialisation uses the **distinct** namespace `https://w3id.org/dpv/legal/eu/aiact/owl#`. **The OWL serialisation declares its ontology IRI as `https://w3id.org/dpv/legal/eu/aiact/owl#` — identical to the namespace, trailing `#` included** *(corrected in build, 2026-09-25)*; `owl:versionIRI` `https://w3id.org/dpv/2.3/legal/eu/aiact/owl#`. Publisher W3C (DPVCG); creator Golpayegani; contributors Pandit, Esteves, Krog, Suriyawongkul. `owl:versionInfo` **2.3**. `dcterms:created` 2024-04-10, `dcterms:modified` **2026-02-25** — individual terms carry creation dates as recent as 2026-02-09. W3C Document Licence. DOI `10.5281/zenodo.12505841`. Spec `https://w3id.org/dpv/legal/eu/aiact`. |
| **CQs borne on** | **CQ1 — nearly in full.** `eu-aiact:RiskLevel` with `RiskLevelProhibited`, `RiskLevelHigh`, `RiskLevelTransparencyRequired`, `RiskLevelMinimal`, `RiskLevelNotHigh`, `RiskLevelPermitted` — the adopted four-tier structure, sourced `"AIA(Art.6)"`. Both Art. 6 routes are split out: `RiskLevelHigh-A6-1` and `RiskLevelHigh-A6-2`, matching `HighRiskAISystem-A6-1` / `-A6-2`. The grounds are enumerated to clause granularity: **`HighRiskAISystem-AnnexI-1` … `-AnnexI-20`** and **`HighRiskAISystem-AnnexIII-1-a` … `-AnnexIII-8-b`**. **CQ2 — in full at the enumeration level:** `ProhibitedAISystem` with `ProhibitedAISystem-A5-1-a` … `-A5-1-h`. **CQ4 — the trigger:** `eu-aiact:SubstantialModification`, `PredeterminedChange`, `NonpredeterminedChange`, `hasChangeCategory`, `hasChangeDescription`, plus `DownstreamAIProvider`. **CQ5 — the institutions:** `MarketSurveillanceAuthority`, `NationalCompetentAuthority`, `NotifiedBody`, `NotifyingAuthority`, `AIOffice`, `ConformityAssessmentBody`, `ConformityAssessment`, `EUDeclarationOfConformity`, `CEMarking`. Full role set for CQ3/CQ4: `AIProvider`, `AIDeployer`, `AIImporter`, `AIDistributor`, `AIProductManufacturer`, `AuthorisedRepresentative`, `AIOperator`. |
| **Coverage gaps** | **Obligations.** A substring sweep of all 191 `eu-aiact:` terms for `Obligation`, `Duty`, `Requirement`, `Right`, `Permission`, `Prohibition` returns **nothing**. The extension has the artefacts an obligation produces — `QualityManagementSystem`, `TechnicalDocumentation`, `PostMarketMonitoringSystem`, `FRIA`, `RiskManagementSystem`, `InstructionForUse`, `ProviderHumanOversightMeasure`, `DeployerHumanOversightMeasure` — but never states that a provider of a high-risk system *must* maintain a QMS under Art. 17. DPV core does supply `dpv:Obligation`, `dpv:Permission`, `dpv:Prohibition`, `dpv:hasObligation` and the fulfilment states `ObligationFulfilled` / `Unfulfilled` / `Violated`, but see structural gaps. Also absent: conditional exemptions to the Art. 5 prohibitions (CQ2's second half), which are flattened into the eight `A5-1-*` terms. |
| **Structural gaps** | Three, and they are the reason this is a near miss rather than a hit. **(i) `dpv:hasObligation` has `dcam:domainIncludes dpv:Context`** — obligations attach to a context, not to a role-bearing actor. The CQ3 traversal *actor → role → obligation* has no path. **(ii) Roles are classes, not reified.** `eu-aiact:AIProvider a rdfs:Class`, `rdfs:subClassOf eu-aiact:AIOperator, tech:Provider`. No disjointness, so an actor may be both — commitment 1 is not *blocked* — but there is no node on which to hang the grounds, period or establishing provision, so Art. 25 is inexpressible. **(iii) Risk levels are punned class/individual.** `eu-aiact:RiskLevelHigh` is simultaneously an `owl:Class`, an instance of `eu-aiact:RiskLevel`, and `rdfs:subClassOf eu-aiact:RiskLevelPermitted`. `hasRiskLevel` ranges over `RiskLevel` instances. Because punning keeps the two facets independent, asserting `?sys eu-aiact:hasRiskLevel eu-aiact:RiskLevelHigh` entails **nothing** about the system being permitted-level, despite the subclass axiom saying high ⊑ permitted. CQ1 answered by reasoning will silently under-return; answered by SPARQL over the class hierarchy it works. |
| **Alignment cost** | Moderate, concentrated in article provenance. Article references are **free-text literals** — `dct:source "AIA (Art. 3(3))"@en` — and the convention is not stable even within the file (`"AIA (Art. 3(3))"` beside `"AIA(Art.6)"`). **No ELI URI appears anywhere in the DPV family**, verified across all five retrieved files. Satisfying commitment 2 therefore means minting an `aia:definedIn` assertion to an ELI article resource for every reused term; the existing strings are a cross-check, not a source. Roughly 40–60 terms would be worth aligning, one axiom each, plus a `hasRiskLevel`-to-`aia:hasRiskCategory` bridge. None of it contested: these are quotations of the operative text by the same group that wrote AIRO. |
| **Import risk** | **Low on axioms, awkward on packaging.** The OWL serialisation is 2,173 triples, 167 named classes, 3 object properties, and — measured — **zero** disjointness, restrictions, cardinality, domain or range axioms. Nothing in it can make a model inconsistent. Two packaging costs. First, the base `eu-aiact.ttl` declares terms as `rdfs:Class` + `skos:Concept` and contains **zero `owl:Class` declarations**; a reasoner sees untyped entities, so the `/owl#` variant is the one to import, under its different namespace. Second, the extension declares **no `owl:imports`** but references external terms that consequently dangle. *(Corrected in build, 2026-09-25: the OWL serialisation references the **`/owl#` variants**, not the base namespaces — 78 structural references over 51 distinct terms: `dpv/owl#` 39, `dpv/tech/owl#` 25, `dpv/ai/owl#` 10, `dpv/risk/owl#` 3, `dpv/pd/owl#` 1. The earlier reading of "~55 external terms across `dpv:`, `tech:`, `ai:`, `risk:`, `pd:`, `org:`, `scoro:` and `schema:`" described the base serialisation's prefix table, not the OWL file's actual references. This changes the alignment target — see candidate 4.)* Import it alone and those dangle; import its dependencies and the reasoner carries roughly 2,400 further terms for the handful actually used. |
| **Verdict** | **IMPORT** (decided) — the `/owl#` serialisation, `eu-aiact` module only. `owl:imports <https://w3id.org/dpv/legal/eu/aiact/owl#>`, **trailing hash included**: written without it, Protégé cannot match the import to the loaded ontology. It is the best existing attachment point for CQ1 and CQ2 by a wide margin — the Annex I, Annex III and Art. 5 enumerations alone are weeks of work — and it is actively maintained against the adopted text. Accept the dangling external references rather than importing DPV core; declare the handful that matter locally. Binding consequence: local risk-category, prohibition, Annex and authority terms are **forbidden** where an `eu-aiact` term exists. |

---

## Candidate 4 — DPV core, `tech`, `ai`, `risk`

| Field | Finding |
|---|---|
| **Identity** | Data Privacy Vocabulary 2.3, W3C DPVCG, W3C Document Licence. `https://w3id.org/dpv#` (1,181 terms), `https://w3id.org/dpv/tech#` (199), `https://w3id.org/dpv/ai#` (257), `https://w3id.org/dpv/risk#` (565). Each has a parallel `/owl#` serialisation. Spec `https://w3c-cg.github.io/dpv/2.3/`. |
| **CQs borne on** | Indirectly. `dpv:Obligation` / `dpv:Permission` / `dpv:Prohibition` / `dpv:hasObligation` are the only retrievable, maintained deontic vocabulary among the candidates that is not theoretically loaded (contrast LKIF, below). `tech:Provider`, `tech:Deployer`, `tech:Actor` are the parents of the `eu-aiact` roles. `risk:` supplies incident and risk-management concepts relevant to Art. 73. |
| **Coverage gaps** | Nothing AI-Act-specific; that is what `eu-aiact` is for. |
| **Structural gaps** | `dpv:hasObligation domainIncludes dpv:Context` — the same gap noted above, stated here because it is DPV core's, not the extension's. `dpv:Obligation` is itself punned (`a rdfs:Class, skos:Concept, dpv:Rule`). |
| **Alignment cost** | Low: one axiom, uncontroversial. **The namespace matters, and the first reading was wrong** *(corrected in build, 2026-09-25)*. The alignment is `aia:Obligation ⊑ dpv-owl:Obligation` against **`https://w3id.org/dpv/owl#`**, not `https://w3id.org/dpv#`. The imported `eu-aiact` OWL file references the `/owl#` variants exclusively, so aligning to the base namespace would place the local obligation layer under a DPV vocabulary that nothing else in the closure references — two disconnected DPV graphs in one file. That is precisely the failure this survey catches in MAILO and DAOnt below. The bearer relation has to be local regardless. |
| **Import risk** | Low on axioms, high on volume: 14,909 triples in core alone, with — measured — zero `owl:Class` declarations in the base serialisation. Importing core to obtain four deontic terms is a poor trade. |
| **Verdict** | **ALIGN, not import** (decided). Subclass `aia:Obligation` under `dpv-owl:Obligation`. Importing 15k triples for four terms fails the Protégé-tractability constraint on proportionality grounds, not correctness ones. **Consequent decision taken in the build:** the 51 dangling `eu-aiact` external references are handled by declaring the load-bearing ones as local stubs rather than importing DPV core. Two are load-bearing for CQ1 — `dpv-owl:RiskLevel` is the parent of `eu-aiact:RiskLevel`, and `dpv-owl:hasRiskLevel` is the property CQ1 bridges from. |

---

## Candidate 5 — ELI (European Legislation Identifier)

| Field | Finding |
|---|---|
| **Identity** | Namespace `http://data.europa.eu/eli/ontology#`, Publications Office of the European Union. FRBR-derived. Imports SKOS Core. **The canonical download declares `owl:versionInfo "1.4"` and no `owl:versionIRI`** *(corrected in build, 2026-09-25 — this survey previously said version 1.5; the specification document describes 1.5, but the ontology file the Publications Office links as "ELI ontology" is 1.4)*. **Its declared ontology IRI is `http://data.europa.eu/eli/ontology#`, with the trailing `#`** — identical to the namespace, as with DPV's OWL serialisation. Retrieved from `op.europa.eu/documents/3938058/11669184/eli.owl/` (trailing slash required), linked from `op.europa.eu/en/web/eu-vocabularies/eli`. |
| **CQs borne on** | **Commitment 2 across all five CQs.** ELI is the only candidate that addresses provisions as resources rather than as strings. |
| **Coverage gaps** | None in scope — ELI is deliberately about legal bibliography, not legal content. |
| **Structural gaps** | None for this purpose, **but the reason is narrower than it looks and was worth checking** *(added in build, 2026-09-25)*. The CQ2 query types article resources as `eli:LegalResourceSubdivision` and then applies `eli:is_part_of` and `eli:number` to them. Neither property's domain mentions that class: `eli:is_part_of` has domain and range `eli:Work`, and `eli:number` has domain `LegalExpression ⊔ LegalResource`. The query is nonetheless sound, because v1.4 declares `LegalResourceSubdivision ⊑ LegalResource` **and** `⊑ WorkSubdivision`, with both parents under `Work` — so all three domains are satisfied with no unintended entailment. The second superclass was **added in v1.4**; pinned to v1.3 the query would have carried one. `eli:type_subdivision` (domain `WorkSubdivision`, functional) is likewise satisfied. This is an argument for pinning the import rather than resolving it live. |
| **Alignment cost** | Not applicable — ELI is used, not aligned. The one outstanding question is **resolved by test** (2026-09-25, via browser): `http://data.europa.eu/eli/reg/2024/1689/art_6` does **not** resolve to Article 6. The `art_6` component is silently ignored and the request serves the whole act. **The Publications Office does not mint article-level ELI URIs for this regulation.** The ELI URI template does carry a `{level 1…}` subdivision component, but it is optional and jurisdiction-defined, and the EU has not implemented it here. Article resources are therefore minted in the `aia:` namespace as `eli:LegalResourceSubdivision` instances with `eli:is_part_of` to the act-level URI — the Semantic Finlex pattern noted in the CQ draft. This is a local extension of ELI, not a departure from it, and the CQ2 query as drafted works unchanged, since it only requires `eli:is_part_of` to the act and never dereferences the article URI. Both act-level URIs were confirmed to resolve: `…/2024/1689/oj` serves the original as-adopted text, `…/2024/1689/2026-07-27` the consolidated version. |
| **Import risk** | Low. Parsed from the canonical v1.4 download: 27 `owl:Class`, 71 `owl:ObjectProperty`, 18 `owl:DatatypeProperty`, 7 annotation properties, one `owl:imports` (SKOS Core), **zero** disjointness axioms, 11 restrictions, and **13 functional properties** — `in_force`, `legal_value`, `licence`, `embodies`, `realizes`, `type_subdivision`, `rights`, `uri_schema`, `version_date`, `date_document`, `date_publication`, `first_date_entry_in_force`, `date_no_longer_in_force`. Two matter here: `type_subdivision` is functional, so an article resource may carry only one subdivision type, and `in_force` likewise. Both are better enforced by a SHACL shape than discovered through a silent `sameAs` entailment. Verified terms: `eli:LegalResourceSubdivision` is an `owl:Class`; `eli:is_part_of` and `eli:has_part` are object properties; **`eli:number` is a `DatatypeProperty`** with range `xsd:string`, which is what the CQ2 query assumes. *(These counts match the second pass's third-party v1.4 mirror exactly, confirming the mirror was the same file.)* |
| **Verdict** | **IMPORT** (decided). `owl:imports <http://data.europa.eu/eli/ontology#>`, trailing hash included. It is the only way to satisfy commitment 2, and nothing else surveyed competes: every other candidate records provenance as a string literal. **Resolution decision:** `http://data.europa.eu/eli/ontology` does **not** content-negotiate to this document — the RDF/XML is served only from the `op.europa.eu` path above — so the import is vendored and redirected through a Protégé catalog rather than resolved over the network. Binding consequence: provenance is by resource, never `xsd:string`. |

---

## Candidate 6 — LKIF-Core *(the instructive near miss)*

| Field | Finding |
|---|---|
| **Identity** | Namespace base `http://www.estrellaproject.org/lkif-core/`, one per module (`norm.owl#`, `role.owl#`, `expression.owl#`, `legal-role.owl#`, …). ESTRELLA consortium (IST-2004-027665); editor Rinke Hoekstra, University of Amsterdam. Version 1.1, **2008**; the documentation page describes v1.0.3, May 2008. Relicensed CC BY 4.0 in the GitHub mirror. **Unmaintained for ~18 years.** The canonical host serves a page carrying its own deprecation notice; the practical source is `github.com/RinkeHoekstra/lkif-core`. |
| **CQs borne on** | **CQ3, in principle.** It is the only candidate with a developed deontic layer: `norm.owl#Norm`, `#Obligation`, `#Permission`, `#Prohibition`, `#Right`, plus a Hohfeldian apparatus (`#Hohfeldian_Power`, `#Liberty_Right`, `#Liability_Right`, `#Potestative_Right`, `#Obligative_Right`, `#Exclusionary_Right`). **CQ3/CQ4 role structure:** `role.owl#Role`, `#played_by`, `#plays`, `legal-role.owl#Legal_Role`. |
| **Coverage gaps** | Everything AI-Act-specific. LKIF is a domain-neutral legal upper ontology; it has no AI system, no risk category, no provider, no conformity assessment. |
| **Structural gaps** | **Two, either of which is disqualifying on its own.** **(i) `norm.owl#Obligation rdfs:subClassOf norm.owl#Permission`, and `#Prohibition rdfs:subClassOf #Permission`.** This is a deliberate deontic-logic commitment, defensible in its own terms, and it is exactly the kind of axiom the prompt anticipates as "likely to be contested". Under it, every provider obligation under Art. 16 is inferred to be a permission. A CQ3 answer reporting that Art. 17's quality-management requirement *is a permission* is not a result one can put in front of a lawyer. **(ii) The role pattern is binary, not ternary.** `#played_by` relates a role instance to an agent. There is no third argument, so the system a role is held in respect of cannot be expressed — which is the whole point of commitment 1. LKIF's roles are closer to "occupations" than to conduct-contingent standing. Separately, `norm.owl`'s own object properties (`allowed_by`, `commanded_by`, `normatively_strictly_better`, …) are about comparing normative positions, not about attaching an obligation to a bearer; the bearer relation lives in `expression.owl#bears` / `#holds`. |
| **Alignment cost** | Would require *contradicting* LKIF rather than extending it: an `aia:Obligation` that is not an `lkif:Permission` cannot be a subclass of `lkif:Obligation`. Any alignment would have to be `rdfs:seeAlso` or a documented non-subsumption mapping — which is to say, not an alignment. |
| **Import risk** | **The highest in the survey, by a wide margin.** Measured across 12 modules: 2,044 triples but **28 `owl:disjointWith`, 181 `owl:Restriction`, 125 `someValuesFrom`, 50 `allValuesFrom`, 6 cardinality, 28 `intersectionOf`, 2 `complementOf`, 16 transitive properties, 50 inverses, 16 internal `owl:imports`**. Three disjointness axioms are directly hostile to this model: **`Agent ⊥ Role`**, **`Physical_Entity ⊥ Role`** and **`Process ⊥ Role`** mean that the moment any actor individual is typed as a role — the naive `Acme rdf:type aia:Provider` — the model is inconsistent. **`Organisation ⊥ Person`** cuts across the Act's own definitions, which run "natural or legal person, public authority, agency or other body" as a single category, and **`Private_Legal_Person ⊥ Public_Body`** does the same. This is the archetype of the prompt's concern: the inconsistency would surface in `aia:` terms while originating two import layers away in a 2008 ontology. Compounding it, `owl:imports` of the `estrellaproject.org` IRIs is fragile enough to need a local copy and a Protégé catalogue mapping. |
| **Verdict** | **NEITHER** (decided). The deontic layer is the one thing worth having and it is the one thing whose axioms cannot be accepted. Reported as the principal justification for building the obligation layer locally rather than reusing one. |

---

## Candidate 7 — PROV-O

| Field | Finding |
|---|---|
| **Identity** | `http://www.w3.org/ns/prov#`. W3C Recommendation, 30 April 2013. W3C document licence. Parsed: **39 `owl:Class`, 44 `owl:ObjectProperty`, 22 annotation properties** *(corrected 2026-09-25 — the spec's own cross-reference undercounts both)*. |
| **CQs borne on** | **CQ4, as a structural template**, and secondarily CQ3. The qualified-relation pattern — `prov:Activity` → `prov:qualifiedAssociation` → `prov:Association` → {`prov:agent`, `prov:hadRole`, `prov:hadPlan`} — is a reified ternary of exactly the shape commitment 1 describes. `prov:Role` is explicitly left open for domain extension. `prov:qualifiedAttribution` / `prov:Attribution` and `prov:qualifiedDelegation` / `prov:Delegation` extend the same pattern to entity–agent and agent–agent relations. |
| **Coverage gaps** | All domain content. PROV-O supplies a pattern and three anchor classes, nothing about AI or regulation. |
| **Structural gaps** | One, and it is a genuine design question rather than a defect. **PROV-O's reification hangs off an `Activity`, not off the artefact.** Commitment 1 anchors `RoleAssignment` to the *system*; PROV-O would anchor it to the conduct — placing on the market, putting into service, making a substantial modification. Given that the Act's own definitions are conduct-based ("places it on the market", "using an AI system under its authority", and Art. 25's three triggering acts), the Activity-centred version is arguably the more faithful reading, and it makes the Art. 25 grounds a first-class node rather than an annotation. It does not, however, match commitment 1 as written, and the commitment is fixed. Reusing `prov:Association` directly would therefore import an Activity-shaped hole; reusing the *pattern* costs nothing. |
| **Alignment cost** | If aligned: `aia:RoleAssignment ⊑ prov:Association`, `aia:heldBy ⊑ prov:agent`, `aia:hasRole ⊑ prov:hadRole`, `aia:Provider rdf:type prov:Role`. Four axioms, none contested — but note that `aia:concernsSystem` has no PROV-O counterpart, since `prov:Association` has no fourth argument. The alignment is therefore partial and should be documented as such rather than presented as a subsumption. |
| **Import risk** | **Low but non-zero, and the one real hazard is worth stating precisely.** `prov:Activity owl:disjointWith prov:Entity` is asserted. `prov:Agent` is *not* disjoint from either, so an actor may be both Agent and Entity. The hazard is modelling an AI system as a `prov:Entity` (the artefact placed on the market) while also treating it as a `prov:Activity` (the system in operation); those are disjoint and the model becomes inconsistent. Also present: `prov:Entity ⊥ prov:InstantaneousEvent`, `prov:Agent ⊥ prov:InstantaneousEvent`, and one `maxCardinality 0` on `prov:hadActivity` for `prov:ActivityInfluence`. No functional or inverse-functional properties. *(Added 2026-09-25.)* PROV-O also declares **13 `owl:propertyChainAxiom`** — mostly folding qualified influences back into their direct binary forms. They are benign, but they are the mechanism by which an assertion on a reified `prov:Association` propagates to `prov:wasAssociatedWith`, which is worth knowing if the reified role assignment is aligned to it. |
| **Verdict** | **ALIGN** (decided). Adopt the qualified-association pattern and declare the four subsumption axioms, documenting that `aia:concernsSystem` has no PROV-O analogue. Do not import for this alone; the `Activity ⊥ Entity` axiom is a trap that buys nothing the four axioms do not. |

---

## Candidate 8 — ORG (Organization Ontology) *(best structural template for commitment 1)*

| Field | Finding |
|---|---|
| **Identity** | `http://www.w3.org/ns/org#`. W3C Recommendation, 16 January 2014. W3C document licence. Parsed: 13 `owl:Class`, 31 `owl:ObjectProperty`. |
| **CQs borne on** | **CQ3 and CQ4, structurally; CQ5, substantively.** `org:Organization` is the natural type for competent authorities, market surveillance authorities and notified bodies, as the CQ5 query already assumes. |
| **Coverage gaps** | All AI Act content. |
| **Structural gaps** | Almost none — this is the closest structural match in the survey. **`org:Membership` is an explicitly reified n-ary relation between an Agent, an Organization and a Role**, with `org:member` (→ `foaf:Agent`), `org:organization` (→ `org:Organization`) and `org:role` (→ `org:Role`). Substitute the AI system for the organisation and this *is* `aia:RoleAssignment`. The one mismatch is that substitution: `org:organization` has range `org:Organization`, so `aia:RoleAssignment` cannot be a subclass of `org:Membership` without either typing AI systems as organisations (absurd) or overriding a published range. |
| **Alignment cost** | Low, and the honest form is imitation rather than subsumption. Reuse the *pattern*; reuse `org:Organization` and `org:Role` directly for authorities and for role terms. `aia:Role ⊑ org:Role` is one uncontested axiom. Do **not** assert `aia:RoleAssignment ⊑ org:Membership`. |
| **Import risk** | **Higher than the specification document suggests** *(corrected 2026-09-25)*. The published ORG specification lists no disjointness axioms; the RDF declares **ten**, making the whole backbone pairwise disjoint: `org:Organization`, `org:Role`, `org:Membership`, `org:Site` and `org:ChangeEvent` are mutually exclusive. `org:Organization ⊥ org:Role` and `org:Role ⊥ org:Membership` are the two that touch this model. Neither breaks the recommended alignment — a role is not an organisation and a role is not an assignment, so the axioms happen to agree with the intended design — but they mean ORG is not the inert vocabulary it was assessed as, and an actor typed `org:Organization` can never also be an `aia:Role`. Confirmed as originally stated: **`org:member` and `org:organization` are both `owl:FunctionalProperty`** with domain `org:Membership`, so reusing `org:Membership` directly and pointing one assignment at two systems would infer the two systems identical — a silent wrong entailment, not an error. One property chain into `prov:wasDerivedFrom` pulls PROV-O in transitively if ORG is imported. Together these make the align-don't-import verdict stronger than when it was first written. |
| **Verdict** | **ALIGN** (decided), and cite as the design precedent for `aia:RoleAssignment`. `aia:Role ⊑ org:Role` only. Whether to import ORG for `org:Organization` as the type of authorities — which the CQ5 query as drafted assumes — is deferred to the authority module as a separate decision. |

---

## Candidate 9 — SKOS

| Field | Finding |
|---|---|
| **Identity** | `http://www.w3.org/2004/02/skos/core#`; ontology IRI `http://www.w3.org/2004/02/skos/core`, no trailing hash. W3C Recommendation, 18 August 2009. |
| **CQs borne on** | All five, via commitment 3 — `skos:prefLabel` and `skos:definition` carry the mandatory label and description, as every query in the CQ draft assumes. |
| **Coverage gaps** | Not applicable. |
| **Structural gaps** | One point of care. `skos:Concept` is an `owl:Class` whose *instances* are individuals; using `skos:prefLabel` on `aia:` classes therefore mixes an individual-oriented vocabulary with class-level annotation. This is near-universal practice and Protégé accepts it, but if the annotation requirement is to be checked by a reasoner rather than by SPARQL, declaring the label properties as `owl:AnnotationProperty` locally avoids the question. Note also that **`skos:broader` is not transitive** (`skos:broaderTransitive` is), so any hierarchy traversal must use the right one. |
| **Alignment cost** | None. |
| **Import risk** | **Lower than first assessed** *(corrected 2026-09-25)*. The earlier entry asserted `skos:related owl:propertyDisjointWith skos:broaderTransitive` as an axiom. It is not one: parsing `skos.rdf` returns **zero** occurrences of `owl:propertyDisjointWith` or `owl:AllDisjointProperties`. S27 of the SKOS Reference states the related/broaderTransitive disjointness as an *integrity condition* in prose, and the 2009 schema predates OWL 2, so it was never encoded. A reasoner will not enforce it and it is not an inconsistency source. What the RDF does declare is **three class-level disjointness axioms** — `skos:Concept ⊥ skos:ConceptScheme` (S9), `skos:Collection ⊥ skos:Concept` and `skos:Collection ⊥ skos:ConceptScheme` (S37) — plus 3 transitive and 4 symmetric properties, 4 `owl:Class` and **17 `owl:ObjectProperty`** *(corrected 2026-09-27 — this entry previously said zero, with SKOS properties described as plain `rdf:Property`; the vendored `skos.rdf` types 17 as `owl:ObjectProperty`)*. The conflict test reported earlier still stands on its own terms and is worth keeping: the `skos:broader` transitive closure over DPV core (1,057 assertions), `eu-aiact` (176), `risk` (599) and VAIR (0), intersected with their `skos:related` assertions (23, 10, 0, 86), yields **zero** violations of S27 in all four — so the data respects the condition even though nothing enforces it. |
| **Verdict** | **IMPORT** (decided). `owl:imports <http://www.w3.org/2004/02/skos/core>`. Required by commitment 3, already assumed throughout the CQ draft, and verified not to conflict with the other proposed imports. Declared explicitly even though ELI imports it transitively, so the dependency does not rest on ELI keeping it. |

---

## Candidate 10 — ODRL

| Field | Finding |
|---|---|
| **Identity** | ODRL Vocabulary & Expression 2.2. Namespace **`http://www.w3.org/ns/odrl/2/`** — note `http`, not `https`; see the DAOnt entry for why this matters. W3C Recommendation, 15 February 2018. W3C permissive document licence. Parsed from `ODRL22.ttl`: 45 `owl:Class`, 46 `owl:ObjectProperty`, 16 annotation properties. |
| **CQs borne on** | **CQ3, as the deontic alternative to LKIF.** `odrl:Duty`, `odrl:Permission`, `odrl:Prohibition`, `odrl:Rule`, `odrl:Policy`, with `odrl:assignee` / `odrl:assigner` (→ `odrl:Party`), `odrl:target` (→ `odrl:Asset`), `odrl:action` and `odrl:constraint`. Structurally this is a good fit: a Duty with an assignee and a target is an obligation borne by a party in respect of an asset — the CQ3 shape, with the AI system as the asset. |
| **Coverage gaps** | All AI Act content. |
| **Structural gaps** | One conceptual, one formal. **Conceptually, ODRL models policies issued by a party over an asset the party controls.** The `assigner` is whoever grants or imposes the rule. Statutory obligations have no assigner in that sense; making the Union legislature the `assigner` of every Art. 16 duty is a modelling stretch that will read oddly to a legal reader and buys nothing. AIUP (below) takes exactly this route and is worth comparing. **Formally — and this was wrong in the first pass** *(corrected 2026-09-25)* — **ODRL is a proper OWL ontology.** The Information Model document describes a "logical view", which is what the earlier entry relied on; but the published vocabulary declares `odrl: a owl:Ontology` and carries 45 `owl:Class`, 46 `owl:ObjectProperty` and **ten disjointness axioms**. It will do reasoning work, and it can make a model inconsistent. |
| **Alignment cost** | Low: `aia:Obligation ⊑ odrl:Duty`, `aia:borneBy` related to `odrl:assignee`, `aia:appliesToSystem` to `odrl:target`. The contested part is not the axioms but the framing, and it should be argued rather than asserted. |
| **Import risk** | **Real, not negligible** *(corrected 2026-09-25)*. Ten `owl:disjointWith` axioms. Two groups: the deontic rules are pairwise disjoint — **`odrl:Permission ⊥ odrl:Prohibition`, `⊥ odrl:Duty`, and `odrl:Prohibition ⊥ odrl:Duty`** — and the six `odrl:Policy` subtypes (`Agreement`, `Offer`, `Privacy`, `Request`, `Ticket`, `Assertion`) are pairwise disjoint among themselves. The first group is what an importer would actually hit: align `aia:Obligation ⊑ odrl:Duty` and anything that also makes it an `odrl:Permission` is an inconsistency. That is the correct behaviour and it is what one wants, but it is an axiom acting on the model, not the inert vocabulary assessed here initially. It also explains AIUP's twelve disjointness axioms, recorded below: AIUP extends exactly this Policy-subtype pattern. |
| **Verdict** | **ALIGN — `rdfs:seeAlso` only** (decided). ODRL's `Duty`/`Permission`/`Prohibition` are cleanly separated, and the second pass shows the separation is **asserted axiomatically** (`Duty ⊥ Permission`), not merely left unstated — the exact inverse of LKIF's `Obligation ⊑ Permission`. That sharpens ODRL's advantage over LKIF considerably. But `dpv-owl:Obligation` carries the same separation without the assigner/assignee framing, and DPV is already in the import closure. Aligning to both is the double-parenting the prompt warns against; **DPV is the attachment point**, with ODRL cited by `rdfs:seeAlso` where the policy reading is useful. |

---

## Candidate 11 — AICat (AI Catalogue Application Profile)

| Field | Finding |
|---|---|
| **Identity** | `https://w3id.org/aicat#`. Golpayegani, Pandit, Lewis. `owl:versionInfo` 0.1; created 2024-05-05, modified 2024-09-13. CC BY 4.0. A DCAT application profile. 89 triples. |
| **CQs borne on** | **CQ5, marginally** — the EU database registration angle. Otherwise none. |
| **Coverage gaps** | Almost everything. It defines exactly three classes: `aicat:Catalog` and two **re-declarations of AIRO terms**. |
| **Structural gaps** | Worth recording as an accuracy point: **`aicat:AIProvider` and `aicat:AIDeployer` do not exist.** The file declares `airo:AIProvider` and `airo:AIDeployer` — AIRO's IRIs — as `rdfs:subClassOf foaf:Agent`. Anyone citing AICat for provider/deployer terms is citing AIRO. The file also contains defects: a duplicated `rdfs:` prefix (first bound to `https://www.w3.org/TR/rdf12-schema/`, then rebound), a `skos:member dcat:datset` typo, a `profile:hasResource aiup:aicat-html` pointing into the wrong namespace, and a `skos:member airo:license` referring to a term AIRO does not define (AIRO has `airo:License` and `airo:hasLicense`). |
| **Alignment cost** | Not worth incurring. |
| **Import risk** | Negligible — 89 triples, no axioms. |
| **Verdict** | **NEITHER** (decided). Cited in the survey for completeness. Its one genuinely useful feature is that it records `dcterms:source <http://data.europa.eu/eli/reg/2024/1689/oj>` — the **only** candidate found to use the AI Act's ELI URI at all, and then only at act level, not article level. |

---

## Candidate 12 — AIUP (AI Use Policy)

| Field | Finding |
|---|---|
| **Identity** | `https://w3id.org/aiup#`. Same authors. Created 2024-04-12; **no `dcterms:modified`**. CC BY 4.0. 255 triples, 4 classes. An ODRL profile. |
| **CQs borne on** | **CQ3 obliquely.** It expresses rules over the *use* of an AI system — intended purpose, prohibited uses — as ODRL policies: `aiup:UsePolicy`, `aiup:UseOffer`, `aiup:UseRequest`, `aiup:UseAgreement`. |
| **Coverage gaps** | It models a provider's contractual use policy, not the Regulation's statutory obligations. The two are different objects: a use policy binds a downstream party by agreement; Art. 16 binds a provider by law. AIUP answers no CQ as posed. |
| **Structural gaps** | It inherits ODRL's assigner/assignee framing, which is appropriate for its actual purpose and inappropriate for statutory duties — the clearest available illustration of why ODRL is the wrong parent for CQ3. |
| **Alignment cost** | Not worth incurring for these CQs. Would become relevant if the ontology were extended to Art. 25(1)(a)-style downstream contractual arrangements. |
| **Import risk** | Low but not zero: **12 `owl:disjointWith` axioms in a 4-class ontology**, all ODRL-internal (`UsePolicy ⊥ Agreement/Offer/Privacy/Request/Ticket/Assertion` and the four `Use*` classes pairwise disjoint). Harmless here, but a reminder that small does not mean axiom-free. |
| **Verdict** | **NEITHER** (decided), for this scope. Noted as adjacent work. |

---

## Candidate 13 — MAILO (Medical AI Legal Ontology) *(the second instructive near miss)*

| Field | Finding |
|---|---|
| **Identity** | `https://w3id.org/mailo#`. v5.2.3. KU Leuven (companion to the MAILO thesis). Serialisations at `github.com/vrkkao-eng/Mailo-ontology/docs/`; documentation at `vrkkao-eng.github.io/Mailo-ontology/index-en.html`. Measured: 1,946 triples, 65 classes, 43 object properties, 39 datatype properties. Licence not stated in the ontology header — **unverified**. |
| **CQs borne on** | **CQ3 and CQ5, partially.** It is the only candidate that models statutory obligations as first-class regulatory objects: `ComplianceObligation` with `DPIAObligation`, `ExplainabilityObligation`, `HumanOversightObligation`, `TransparencyObligation`, `DisclosureObligation`. Also `LegalArticle`, `LegalInstrument`, `EURegulation`, `RegulationVersion`, `PendingAmendment`, `ConformityAssessment`, `NotifiedBody`, `RegulatoryAuthority`, `NationalAuthority`, and — notably for CQ1 — `HighRiskRoute` with `hasHighRiskRoute`. It covers the AI Act as one of twelve frameworks, with CJEU case law encoded as `RatioDecidendi` individuals. |
| **Coverage gaps** | **No actor roles whatsoever.** A sweep of every IRI in the graph for `provider`, `deployer`, `role`, `actor` or `operator` returns one false positive (`identifiesInputFactors`). The provider/deployer distinction — the substance of CQ3 and the whole of CQ4 — is simply absent. Risk tiers are absent apart from `HighRiskRoute`. Scope is medical AI, so the Annex III areas outside health are out of frame. |
| **Structural gaps** | **`mailo:hasObligation` has `rdfs:domain mailo:RegulatoryFramework` and `rdfs:range mailo:ComplianceObligation`.** Obligations attach to the *instrument*, not to the party bound. This is the same failure as DPV's `hasObligation domainIncludes dpv:Context`, arrived at independently — which is itself the finding: **two of the three candidates that model AI Act obligations at all attach them to the legal source rather than to the obligated role.** The CQ3 traversal is unavailable in both. Quality signals worth noting: duplicated properties `interpretesArticle` / `interpretsArticle` and duplicated classes `EPOProceding` / `EPOProceeding` are both declared; `appliesToRoute`, `involvesArticle` and `triggersRoute` are declared with no domain or range; and the file declares **two** `owl:Ontology` subjects, `https://w3id.org/mailo` and `https://w3id.org/mailo#`, only the second carrying the `owl:versionIRI`. |
| **Alignment cost** | The obligation *subtype* vocabulary is reusable conceptually, but the bearer relation would have to be replaced, which is the part that matters. Not a cheap alignment. |
| **Import risk** | Low on axioms — zero disjointness, zero restrictions. But MAILO's own `owl:imports` are instructive, and there are now **two** defects in them, not one *(second noted in build, 2026-09-25)*. It imports `https://w3id.org/airo` correctly; `http://w3id.org/dpv` with `http`, where DPV's namespace is `https`, so that import will not resolve to DPV; and `http://data.europa.eu/eli/ontology` **without the trailing `#`**, where ELI declares its ontology IRI *with* it. Despite importing the ELI ontology, it uses an ELI act URI exactly once, and for a different regulation (`…/eli/reg/2026/1744/oj`), never for the AI Act. |
| **Verdict** | **NEITHER** (decided) — but reported in full. It is direct evidence that an independent, careful, recent effort to model EU regulatory obligations in OWL reached for AIRO, DPV and ELI, and still ended up attaching obligations to frameworks rather than roles. The residual gap this survey identifies is not an artefact of the candidate set. |

---

## Candidate 14 — TAIR (Trustworthy AI Requirements)

| Field | Finding |
|---|---|
| **Identity** | ADAPT Centre. Described in *An open knowledge graph-based approach for mapping concepts and requirements between the EU AI Act and international standards* (arXiv:2408.11925). Hosted at `tair.adaptcentre.ie` behind a GraphDB instance with a "public version (limited descriptions)" and a login-gated "private version". **No namespace IRI, licence, version or downloadable serialisation could be found — checked 2026-09-25 and unavailable as of that date.** |
| **CQs borne on** | On the paper's account: **CQ3 and CQ5**, more directly than anything else surveyed — 118 requirements extracted from the Act, 46 concepts from Art. 3, with an `implementedBy` property assigning responsibility to actors including Provider, Small Scale Provider, User, Operator and Deployer, and a mapping to harmonised standards. |
| **Coverage gaps** | Cannot be assessed. |
| **Structural gaps** | Cannot be assessed. |
| **Alignment cost** | **All term names above are unverified.** They are reported as the paper describes them and have not been checked against any retrievable specification, because none exists. They should not be cited as confirmed. |
| **Import risk** | Not assessable; an ontology that cannot be retrieved cannot be imported. This is a statement about 2026-09-25, not a permanent one — if TAIR is published later it should be re-surveyed before this reuse decision is treated as settled. |
| **Verdict** | **NEITHER — on availability grounds rather than fit** (decided, and provisional on that fact alone). On its published description it is the closest existing work to CQ3, which makes its unavailability the most significant negative finding in the survey: the one artefact that may already do what is needed cannot be obtained, inspected or reused. Worth a sentence in the report's reuse rationale and, separately, worth an email to the authors. |

---

## Candidate 15 — DAOnt (EU Data Act Ontology) *(methodological precedent)*

| Field | Finding |
|---|---|
| **Identity** | `https://w3id.org/def/daont`, `owl:versionIRI` `https://w3id.org/def/daont/2.0`. Ontology Engineering Group, UPM (`github.com/oeg-upm/DAOnt`). Formal OWL ontology of Regulation (EU) 2023/2854. Measured: 1,073 triples, 84 classes, 66 object properties, 24 datatype properties, 4 disjointness axioms, 10 restrictions. |
| **Relevance** | Not a reuse candidate — wrong regulation — but the **closest methodological precedent available**, and it is the precedent the CQ draft already cites for the deontic layer. Its README states that it "integrates 3 foundational standards—LKIF-Core, ODRL, and DPV". |
| **What it actually does** | Three findings, all of which bear on the recommendation below. **(i) It declares no `owl:imports` at all.** The integration is by reference: 15 ODRL IRIs and 4 LKIF IRIs appear in the file, cited alongside DAOnt's own `daont:Duty`, `daont:Permission`, `daont:Prohibition`, `daont:Right` and `daont:Party`. The nearest comparable project chose alignment over import — including, and especially, for LKIF. **(ii) Article references are string literals.** `daont:articleReference` is an `owl:DatatypeProperty` with `rdfs:range xsd:string` and the comment "Article number (e.g., 'Article 4(1)')". **No ELI URI appears anywhere in DAOnt.** **(iii) Its ODRL prefix is bound to `https://www.w3.org/ns/odrl/2/`**, whereas the W3C Recommendation's namespace is `http://www.w3.org/ns/odrl/2/`. All 15 ODRL references are therefore to IRIs that are not ODRL's. Combined with MAILO's two defective imports, that is two of two recent regulatory ontologies with namespace errors in their external references — an argument for machine-checking every external IRI in this build rather than trusting the prefix block. |
| **Verdict** | **NEITHER — precedent only** (decided). Cited as precedent for **aligning rather than importing** the deontic layer, and as the caution on namespace hygiene. Its use of string article references is the practice commitment 2 exists to improve on, which is worth saying explicitly in the report. |

---

## Candidate 16 — Obligation-extraction knowledge graph (Rodrigues et al.)

*Approaching the AI Act with AI: LLMs and knowledge graphs to extract and analyse obligations* (`github.com/thiagordp/obligation_extraction_for_compliance`). Produces a **GraphML** graph, not an OWL ontology; no namespace, no persistent identifier, no licence stated. Not reusable.

**NEITHER — design check only** (decided). Recorded because its seven-element obligation model — **deontic modality, addressee, predicate, target, specifications, pre-conditions, beneficiary** — is a useful independent check on the shape of the local `aia:Obligation` node. In particular it separates *addressee* (who is bound) from *beneficiary* (who is protected), a distinction none of the OWL candidates make and one that CQ3 will need if deployer obligations under Art. 26 are to be distinguished from the affected-persons rights they create.

---

## Coverage matrix

`●` full · `◐` partial · `○` determinants or infrastructure only · blank none.

| Candidate | CQ1 risk category | CQ2 prohibitions | CQ3 role-indexed obligations | CQ4 role reassignment | CQ5 oversight & conformity |
|---|:--:|:--:|:--:|:--:|:--:|
| AIRO | ○ | | ○ | ○ | |
| VAIR | ○ | | | | |
| **DPV `eu-aiact`** | **●** | **◐** | ◐ | ◐ | **◐** |
| DPV core / tech / ai / risk | | | ○ | | ○ |
| ELI | ○ | ○ | ○ | ○ | ○ |
| LKIF-Core | | | ○ | | |
| PROV-O | | | ○ | ○ | |
| ORG | | | ○ | ○ | ○ |
| SKOS | ○ | ○ | ○ | ○ | ○ |
| ODRL | | | ○ | | |
| AICat | | | | | ○ |
| AIUP | | | ○ | | |
| MAILO | ○ | | ◐ | | ◐ |
| TAIR *(unverified, unavailable)* | | | *◐* | | *◐* |
| **Best available** | **●** | **◐** | **○** | **○** | **◐** |

Read down the columns:

- **CQ1** is essentially solved by `eu-aiact`. The categories, both Art. 6 routes, all twenty Annex I items and all Annex III clauses are present; AIRO and VAIR supply the determinants that feed the classification. What remains local is the *rule* connecting determinants to category — the thing AIRO's Figure 2 states in prose and no candidate states in axioms — plus the punning workaround for `hasRiskLevel`.
- **CQ2** is half-solved. The eight Art. 5(1) prohibitions are enumerated as `ProhibitedAISystem-A5-1-a`…`-h`. **No candidate models the conditional exemptions**, which is the half of CQ2 that makes it more than a list.
- **CQ3 is the deep gap.** Three candidates model AI Act obligations (`eu-aiact` implicitly via artefacts, MAILO explicitly, TAIR reportedly). Of the two that can be inspected, **both attach obligations to the legal source rather than to the obligated role** — `mailo:hasObligation` domain `RegulatoryFramework`, `dpv:hasObligation` domain `dpv:Context`. The traversal *system → role assignment → role → obligation* exists in no surveyed ontology.
- **CQ4 is unreachable everywhere.** `eu-aiact` supplies the trigger vocabulary (`SubstantialModification`, `DownstreamAIProvider`) but has nothing to attach it to, because its roles are classes. PROV-O and ORG supply the reification pattern but no domain content. Nothing surveyed can express that an actor's provider status began on given grounds at a given time under Art. 25, still less that the initial provider's status ended under Art. 25(2).
- **CQ5** is reasonably served for the institutions and the conformity artefacts, and served by nothing for the *relation* — which authority oversees which obligation. That relation presupposes obligations as objects, so it fails with CQ3.

---

## Reuse decision

*Recommendations converted to binding decisions 2026-09-25; the register with consequences is at `reuse-decisions.md`.*

### Import

Each IRI is the ontology IRI **as declared in the retrieved serialisation**. Two terminate in `#`, because those ontologies declare the ontology IRI identical to the namespace IRI. The four are not parallel in form.

| Ontology | `owl:imports` IRI | For | Cost |
|---|---|---|---|
| **DPV `eu-aiact`** | `https://w3id.org/dpv/legal/eu/aiact/owl#` | CQ1 and CQ2 substance: risk tiers, Annex I/III enumerations, Art. 5 prohibitions, roles, authorities, conformity vocabulary | 2,173 triples, **zero** constraining axioms; 51 dangling external references |
| **AIRO** | `https://w3id.org/airo` | AI system, component, model, GPAI model, stakeholder identity; the Annex III determinant properties | 558 triples, no disjointness; 83 domain/range axioms that generate entailments |
| **ELI** | `http://data.europa.eu/eli/ontology#` | Commitment 2 — article-granularity addressing | 1,505 triples; 13 functional properties; 11 restrictions |
| **SKOS** | `http://www.w3.org/2004/02/skos/core` | Commitment 3 — labels and definitions | Small; property-disjointness verified non-conflicting against all co-imports |

Total imported axiom burden is dominated by `eu-aiact`, which carries no disjointness, cardinality, restriction, domain or range axioms at all. The combination is well inside what HermiT will classify on a proof-of-concept — **verified in the build: the vendored closure classifies consistently, 223 classes and 64 object properties** — and, the point the hard constraint is really about, **there is almost nothing in it that can produce an inconsistency originating outside the local file.** That is the case for this particular set, not for imports generally.

**Resolution.** All four are vendored and redirected through a Protégé XML catalog rather than resolved over the network. This was forced rather than chosen: `http://data.europa.eu/eli/ontology` does not content-negotiate to the ELI document, which is served only from an `op.europa.eu` path. Since the task requires demonstrating a Protégé load and a reasoner run, making that depend on the reviewer's DNS and on the Publications Office's content negotiation is not acceptable.

### Align

| Ontology | Axioms | Rationale |
|---|---|---|
| **PROV-O** | `aia:RoleAssignment ⊑ prov:Association`; `aia:heldBy ⊑ prov:agent`; `aia:hasRole ⊑ prov:hadRole`; `aia:Provider rdf:type prov:Role` | Gets the qualified-association pattern's interoperability without the `Activity ⊥ Entity` hazard. Document that `aia:concernsSystem` has no PROV-O counterpart — the alignment is partial. |
| **ORG** | `aia:Role ⊑ org:Role` | Design precedent for `aia:RoleAssignment`. Do **not** subclass `org:Membership` — its `organization` range and its functional properties both fight the substitution. Whether to import for `org:Organization` is a separate, deferred decision. |
| **DPV core** | `aia:Obligation ⊑ dpv-owl:Obligation` | Deontic parent with clean Duty/Permission/Prohibition separation, already a dependency of `eu-aiact`. **The `/owl#` namespace, not the base one** — see candidate 4. |
| **VAIR** | Reference individual terms as `aia:AnnexIIIArea` / `aia:IntendedPurpose` values | Value vocabulary; importing 5,803 triples for ~30 terms is disproportionate. |
| **ODRL** | `rdfs:seeAlso` only | Where the use-policy reading illuminates, but DPV is the attachment point — see the DPV-vs-ODRL distinction under candidate 10. |

### Neither

**LKIF-Core**, **MAILO**, **AICat**, **AIUP**, **TAIR**, **DAOnt**, **Rodrigues et al.** The first two are the ones to report at length: LKIF because `Obligation ⊑ Permission`, `Agent ⊥ Role` and 181 restrictions make the one candidate with a real deontic layer unusable; MAILO because it is recent, careful, imports AIRO/DPV/ELI, and *still* attaches obligations to frameworks rather than roles.

### The residual gap

Four things must be built locally. None is a matter of the survey having been insufficiently thorough; each is absent from every candidate examined.

1. **The role-assignment reification.** `aia:RoleAssignment` relating actor, role and system, with attachment points for grounds, period and establishing provision. ORG and PROV-O supply the *pattern*; neither supplies a version whose third argument is an artefact. Every AI Act candidate — AIRO, `eu-aiact`, AICat — models roles as classes.

2. **The obligation layer and its bearer relation.** `aia:Obligation` with `aia:borneBy` ranging over roles and `aia:appliesToCategory` over risk categories. This is the CQ3 gap and it is the substantive one: no surveyed ontology attaches an obligation to a role. The two that model AI Act obligations at all attach them to the legal instrument. Only the parent class (`dpv-owl:Obligation`) is reusable; the relation that makes CQ3 answerable is not.

3. **Article-granularity provenance.** Every reused term needs an `aia:definedIn` assertion to an ELI article resource. The candidates record provenance as strings — `dct:source "AIA (Art. 3(3))"@en` in `eu-aiact`, `daont:articleReference` typed `xsd:string` in DAOnt — and AICat's act-level `dcterms:source` is the only ELI URI found in the entire survey. Article-level ELI URIs are **confirmed not to be minted** for 2024/1689 (tested 2026-09-25), so article resources are minted locally as `eli:LegalResourceSubdivision` instances with `eli:is_part_of` to the act-level URI — a local extension of ELI rather than a departure from it.

4. **The classification rule and the Art. 25 reassignment event.** `eu-aiact` gives the categories and the determinants exist in AIRO, but the rule connecting them is stated in prose in AIRO's documentation and in axioms nowhere. Likewise `aia:RoleReassignment` with `aia:promotes` / `aia:terminates`: `eu-aiact:SubstantialModification` and `eu-aiact:DownstreamAIProvider` are the right vocabulary with nothing to attach to.

To which the build adds a fifth, smaller one: **stubs for the load-bearing dangling references.** `eu-aiact` declares no `owl:imports` while referencing 51 external terms, two of which CQ1 depends on (`dpv-owl:RiskLevel`, `dpv-owl:hasRiskLevel`). These are declared locally rather than pulling in 14,909 triples of DPV core.

That residual gap is the justification for building rather than reusing, and it is a narrow and specific one: **the survey supplies the nouns and the local ontology supplies the verbs.** Risk categories, Annex enumerations, prohibitions, roles, authorities and conformity artefacts are all available and should be imported. What has to be built is the relational structure that makes them answer questions — which role holds in respect of which system on what grounds, and which obligation binds which role.

---

## Addendum — Regulation (EU) 2026/1744 and its effect on the reuse verdicts

*Added 2026-09-25, after the survey was written. Found while testing the ELI question above; it post-dates the model's training data and was verified against the consolidated text on EUR-Lex.*

Regulation (EU) 2024/1689 has been amended by **Regulation (EU) 2026/1744 of 8 July 2026** (OJ L, 24.7.2026), in force from 27 July 2026. Its Article 1 makes 43 numbered amendments to the AI Act. In the consolidated text (`CELEX 02024R1689-20260727`, ELI `http://data.europa.eu/eli/reg/2024/1689/2026-07-27`) they touch Articles 1–3, 4 (replaced), 5, 6, 10, 11, 17, 25, 27–30, 40, 42, 43, 50, 56–58, 60, 63, 64, 69, 70, 72, 75–77, 95–97, 99, 111 and 113, insert Articles 4a, 60a and 75a–75d, and amend Annexes I and VIII and add Annex XIV. Annex III is unamended.

Five changes bear on the competency questions.

- **Article 5(1) now enumerates ten prohibitions, not eight.** Points **(ba)** (non-consensual intimate imagery) and **(bb)** (child sexual abuse material) were inserted after (b), narrowed by new paragraphs 1a and 1b. Under Article 113(a) they apply from 2 December 2026.
- **Article 6 gains paragraphs 1a, 1b and 1c**, and Article 3(14) redefines "safety component". Together they qualify what counts as a safety component, and exclude products whose third-party assessment is required solely for risks other than health and safety. This changes the Annex I route in CQ1.
- **Annex I moves machinery from Section A to Section B.** Section A, point 1 (Directive 2006/42/EC) is deleted, and the Machinery Regulation (EU) 2023/1230 becomes Section B, point 21. Under amended Article 2(2), only Article 6(1), Article 60a and Articles 102–112 apply to Section B products. Machinery AI systems therefore stay high-risk but carry none of the Article 16 duties.
- **Article 25(2) is replaced.** The initial provider still ceases to be the provider of that specific system, so the `aia:terminates` modelling stands. Its duty to cooperate with the new provider was already in the as-adopted text; the amendment spells out three components of it (technical documentation sufficient to assess Article 16 compliance, disclosure of known limitations and failure modes, targeted technical access) and keeps the carve-out where the initial provider clearly specified that the system was not to be made high-risk.
- **Article 43(3) is replaced**, and **Article 75(1)** gives the AI Office exclusive competence over AI systems built on a general-purpose AI model by the same provider, and over systems in very large online platforms or search engines. Both bear on CQ5.

**Effect on the reuse verdicts.** One is materially affected and the rest are not.

DPV `eu-aiact` was last modified **2026-02-25**, four months before the amending regulation. Its prohibition enumeration therefore stops at `ProhibitedAISystem-A5-1-h` and **has no terms for (ba) or (bb)**, its Annex I enumeration still places machinery at point 1, and its `HighRiskAISystem-A6-1` / `-A6-2` split does not reflect Article 6(1a)–(1c). The import verdict is unchanged — the Annex I and Annex III enumerations remain the largest single reuse win available — but the two new prohibitions must be minted locally.

AIRO, VAIR, ELI, SKOS, PROV-O, ORG and the alignment set are unaffected: none enumerates Article 5 or Article 6 content.

**Scoping decision taken.** The ontology models the Act **as amended**: the consolidated text of 27 July 2026, cited through the Act's ELI `http://data.europa.eu/eli/reg/2024/1689/oj` with the amending act's ELI `http://data.europa.eu/eli/reg/2026/1744/oj` as a second `dct:source`. That requires minting `pp_art5_1_ba` and `-bb` locally, stating Article 6(1a)–(1c) in the Annex I ground, and splitting Article 25(2) into termination plus a residual-duty set. The last is the most interesting of the three, since an obligation that outlives the role bearing it cannot be expressed in a role-as-class model at all, and it sharpens the argument for reification.

---

## Corrections to `competency-questions.md`

Three items listed there as outstanding are now resolved, and two of the draft's working assumptions need amending.

- **ELI property names — confirmed.** `eli:LegalResourceSubdivision`, `eli:is_part_of` and `eli:number` all exist as used in the CQ2 query. The Semantic Finlex fallback remains the right contingency, but for the reason given above (whether article URIs are *minted*), not because the terms were wrong. **The build adds that the query is also sound under ELI's domain axioms, though only because `LegalResourceSubdivision` gained `WorkSubdivision` as a second superclass in v1.4.**
- **`airo:AISystem` — confirmed**, and it carries the adopted Art. 3(1) definition verbatim.
- **"AIRO's high-risk determination pattern" — this does not exist and the reuse note under CQ1 should be amended.** AIRO defines no risk-category class of any kind. The correct attachment point for CQ1's categories and grounds is DPV's `eu-aiact` extension; AIRO's contribution is the five determinants only.
- **"AIRO was built on a draft version of the Act" — no longer true and the reuse rationale should not say so.** AIRO was updated against the adopted text (`dcterms:modified` 2024-05-25); it cites `http://data.europa.eu/eli/reg/2024/1689/oj`, quotes Art. 3(1) and Art. 3(63), and its documentation describes Annex III combinations "as per the final version of the AI Act". The draft's anticipated alignment cost for a draft-versus-adopted mismatch does not arise. The real cost is different and larger: there are no risk categories to align.
- **CQ3's reuse note — "DPV / ODRL / LKIF-Core for the deontic structure" should be narrowed to DPV alone**, and to the **`/owl#` namespace**. LKIF is unusable (`Obligation ⊑ Permission`; `Agent ⊥ Role`), and ODRL's assigner/assignee framing fits contractual policies rather than statutory duties. DAOnt, the precedent the note cites, in fact declares no `owl:imports` and aligns by reference — which supports the narrowed recommendation.

## Corrections arising from the build, 2026-09-25

Four, all from reading `owl:Ontology` declarations rather than prefix tables or documentation.

1. **ELI is v1.4, not v1.5.** The canonical Publications Office download declares `owl:versionInfo "1.4"` and no `owl:versionIRI`. Its axiom counts match the second pass's third-party v1.4 mirror exactly, so the mirror was sound; it is this survey's "version 1.5" label that was wrong, taken from the specification document rather than the file.
2. **Two import IRIs terminate in `#`.** DPV `eu-aiact` (OWL) declares `https://w3id.org/dpv/legal/eu/aiact/owl#` and ELI declares `http://data.europa.eu/eli/ontology#`, each identical to its own namespace IRI. AIRO and SKOS separate the two conventionally. Written uniformly, two of the four imports would not match the loaded ontology.
3. **The DPV alignment namespace was wrong.** `aia:Obligation` subclasses `dpv-owl:Obligation` in `https://w3id.org/dpv/owl#`, not `dpv:Obligation` in `https://w3id.org/dpv#`. The imported `eu-aiact` OWL serialisation references the `/owl#` variants exclusively — 78 structural references over 51 distinct terms.
4. **MAILO has a second defective import**, `http://data.europa.eu/eli/ontology` without the hash, alongside its known `http://w3id.org/dpv`. With DAOnt's ODRL scheme error that makes three namespace defects across two recent regulatory ontologies — the clearest available evidence that machine-checking external IRIs is worth the trouble.

**SKOS**, not re-parsed in this pass, was vendored and re-parsed on 2026-09-26: 17 object properties, not 0 (see its entry).
