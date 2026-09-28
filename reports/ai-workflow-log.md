# AI-assisted workflow — where the output was checked and overridden

*Companion to §2 of `../report.md`. The note states the method; this file is the
record of what the method caught. Every row points to the place in this repository where the
correction was first recorded, so each can be checked independently.*

## Method

For the initial brainstorm a Claude Project was created with the postdoc specification task as context where I iterated a plan for the deliverables. Using Opus 5.0, I drafted survey entries, the Competency Questions and SPARQL queries, shapes and scripts; nothing it produced entered the build until it had been checked manually by me using the three rules below. The LLM was not asked to check its own output, and it was not asked to check the build. It was asked to check the Act and the external ontologies, but only against their authoritative sources.

For the ontology coding Claude Code with Opus 5.0 and Opus 5.5 was used to generate the ontology and perform some basic validation. Ontology was then loaded in Protégé and validated manually by me.

Three sources count as primary, and one rule goes with
each:

1. **For claims about an ontology: the parsed RDF.**
2. **For claims about the law: the Official Journal text.** This was the consolidated text
   `02024R1689-20260727`, which incorporates Regulation (EU) 2026/1744, read alongside the
   amending act itself (OJ L, 24.7.2026).
3. **For claims about the build: running it.** A claim that the build behaves a certain way
   does not count until the build has been run and shown to do so.

The prompt that opened the work is in `prompts/prompt-ontology-survey.md`. It fixes the
modelling commitments before any candidate is assessed, so the LLM judges candidates against
them rather than proposing alternatives. It also frames import as the expensive option.

## 1. Claims about external ontologies, corrected against parsed RDF

| Claim as first made | What the RDF showed | Recorded in |
|---|---|---|
| ODRL is a "logical view", with no reasoning consequences | `owl:Ontology` with **10 `owl:disjointWith` axioms**, including `Permission ⊥ Duty` | `ontology-reuse-survey.md`, ODRL entry |
| ORG declares no disjointness | **10 disjointness axioms**; the whole backbone is pairwise disjoint | survey, ORG entry |
| SKOS encodes `related ⊥ broaderTransitive` as a property-disjointness axiom | Zero occurrences. It is a prose integrity condition, and the schema predates OWL 2 | survey, SKOS entry |
| SKOS declares no object properties | **17** `owl:ObjectProperty` | `STATUS.md`, "SKOS profile correction"; survey entry fixed 2026-09-27 |
| PROV-O class and property counts, as given in its specification | The specification undercounts both: 39 classes, 44 object properties | survey, PROV-O entry |
| ELI is v1.5 | The canonical download is **v1.4**, with no `owl:versionIRI` | survey, ELI entry; `reuse-decisions.md` |
| Align `aia:Obligation ⊑ dpv:Obligation` | `eu-aiact`'s OWL file references only the **`/owl#`** namespaces. `dpv:` would create a second, disconnected DPV graph | `reuse-decisions.md`, "Correction to the survey" |
| `eu-aiact`'s external references span eight prefixes | That was the prefix table of the *base* serialisation. The OWL file has 78 references over 51 terms in five `/owl#` namespaces | survey, `eu-aiact` entry |
| AIRO supplies a high-risk determination pattern, and was built on a draft of the Act | AIRO has **no risk-category classes**, and was updated against the adopted text | `competency-questions.md`, AIRO corrections |
| Six CQ terms as local `aia:` classes | Each has an existing `eu-aiact` term. All six were retargeted, as the reuse decisions require | `competency-questions.md` |

Four of the five candidates first assessed from their specifications, when their hosts could
not be reached, produced corrections once their RDF was parsed. That result is the reason for
rule 1.

## 2. Claims about the Act, corrected against the Official Journal

| Provision | Draft | Official Journal |
|---|---|---|
| Art. 5(1)(h)(iii) | offence punishable by "at least four years" | "for a **maximum period** of at least four years", which is a different, narrower test |
| Art. 26(9) | Regulation (EU) 2018/1725 | **Directive (EU) 2016/680** |
| Art. 26(10) | no time limit and no exception | a 48-hour outer limit, plus an express **exception** for initial identification on objective and verifiable facts |
| Art. 26(8) | registration duty only | also a consequent prohibition on using an unregistered system |
| Art. 26(5) | unqualified duty | law-enforcement and financial-institution carve-outs |
| Art. 25(2) | the initial provider's residual duties are new with Regulation (EU) 2026/1744, and the as-adopted provider has none | the duty to cooperate with the new provider is in the **as-adopted** text; the amendment only lists its components. The ontology had omitted a duty |
| Annex I | the worked example's machinery safety controller bears Art. 16 duties | machinery is in **Section B** (point 21, Regulation (EU) 2023/1230), and Art. 2(2) applies only Arts. 6(1), 60a and 102–112 to Section B products |
| Art. 6(3) | the reason the classification rule is sufficient-only; left unmodelled | it takes Annex III systems **out** of high risk, so it bears on the rule's other direction: a derogated system was classified high-risk. Now recorded as `aia:DerogatedAnnexIIIGround` |
| Art. 43 | two conformity routes, Annex VI and Annex VII | a third: Art. 43(3) sends Annex I, Section A systems through their sectoral procedure |
| Regulation (EU) 2026/1744 | 70 amendment points across 23 articles and Annex VIII | 43 numbered points, touching over 40 articles and Annexes I, VIII and XIV |

Recorded in `STATUS.md`, "Verification against the Official Journal". `check-reasoner.py`
now tests for the corrected wording.

The dangerous kind is an omitted exception, as at 26(10). The ontology then states a
**stronger** duty than the Act imposes, and no query or reasoner run would show it. Only
reading the source catches it.

## 3. Claims about the build, falsified by running it

| Claim | What running it showed | Recorded in |
|---|---|---|
| The `eu-aiact` download URL in `fetch-imports.sh` works | It returned a 404. The working URL was found by following DPV's own links and checked byte-identical by md5 | `STATUS.md`, "Imports" |
| HermiT cannot classify the full closure, and Protégé would fail the same way | The GUI claim had never been tested. Protégé uses `ignoreUnsupportedDatatypes = true`, and with that setting HermiT classifies the closure: consistent, 0 unsatisfiable | `evidence/protege-hermit-findings.md` |
| CQ3 returns the obligations currently borne | It returned 12 Art. 16 duties for a provider whose role Art. 25(2) had **ended**. This led to decision 5 (`aia:TerminatedRoleAssignment`) | `STATUS.md`, decision 5 |
| The CQ3 defect is a fourth case of the conditional-obligation gap | It was not. Fixing it left the conditional duties exactly as they were, which shows the two are separate mechanisms | `competency-questions.md`, finding 4 |
| The report fits its length budget | The word-count estimate was about 1,000 words short. Page count is now measured by rendering the note | `scripts/page-count.py` docstring |
