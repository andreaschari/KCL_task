# Protégé / HermiT evidence

*CLI run 2026-09-28, GUI run 2026-09-28. Protégé 5.6.9.*

**HermiT classifies the full import closure: consistent, 0 unsatisfiable classes.** It also
confirms the CQ1 classification rule (decision 1) and the Art. 25(2) termination (decision
5), matching `scripts/check-reasoner.py`'s OWL 2 RL results. Run two ways with the same
outcome.

## In the Protégé GUI

Each file opened from `ontology/` so `catalog-v001.xml` resolves the imports offline, then
Reasoner > HermiT > Start reasoner. Screenshots are taken with "Reasoner active" shown.

| File | Check | Result | Screenshot |
| --- | --- | --- | --- |
| `aia-ont.ttl` | Classification | No error; imported classes present in the inferred hierarchy | [inferred](protege-aia-ont-inferred.png) |
| `aia-ont.ttl` | DL Query `owl:Nothing` | Subclasses 0; equivalent classes only `owl:Nothing` itself | [nothing](protege-aia-ont-dlquery-nothing.png) |
| `aia-example.ttl` | DL Query `'High Risk AI System'`, instances | 48 of 48, including TalentFlow (Annex III), Helvetia MedTech (Annex I, Section A) and PeopleMetrics (Art. 25(1)(c)); the transparency-tier chatbot is absent | [1](protege-aia-example-cq1-highrisk-1.png), [2](protege-aia-example-cq1-highrisk-2.png) |
| `aia-example.ttl` | DL Query `'Terminated role assignment'`, instances | 2 of 2: TalentFlow and Helvetia MedTech as provider | [roles](protege-aia-example-terminated-roles.png) |

Protégé renders entities by label, so DL queries use labels in quotes rather than prefixed
names.

## From the command line

Same jar and settings ([`hermit-full-run.log`](hermit-full-run.log)). Loading
`aia-example.ttl` (6 ontologies, 4,812 axioms):

```text
Consistent: true  (502 ms)
Unsatisfiable classes (excluding owl:Nothing itself): 0

ExampleRecruitmentScreeningSystem entailed a HighRiskAISystem: true
Total individuals entailed HighRiskAISystem: 48
Individuals entailed aia:TerminatedRoleAssignment: 2
  ra_medical_helvetia_provider
  ra_recruitment_talentflow_provider
```

## Correction: the first CLI run was misreported

The first run used HermiT's plain OWL API entry point (`ReasonerFactory` with
`SimpleConfiguration()`). It threw `UnsupportedDatatypeException` on ELI's
`rdfs:range xsd:date` declarations, since `xsd:date` is outside the OWL 2 datatype map. That
was reported as "HermiT cannot classify the closure, and Protégé would fail the same way".
The Protégé claim was never tested, and it was wrong.

Protégé uses `org.semanticweb.HermiT.ProtegeReasonerFactory` (same jar,
`org.semanticweb.hermit-1.4.3.456.jar`), which sets:

```java
Configuration config = new Configuration();
config.ignoreUnsupportedDatatypes = true;
```

`scripts/RunHermit.java` now sets the same flag. The strict run is kept at
[`hermit-strict-default-run.log`](hermit-strict-default-run.log): a plain OWL API consumer
that omits the flag will still hit it, but it is not what Protégé does.

## Finding: ELI and SKOS disagree on four property types

Both runs log four warnings, for `skos:narrower`, `broader`, `hasTopConcept` and
`topConceptOf`:

```text
Illegal redeclarations of entities: reuse of entity http://www.w3.org/2004/02/skos/core#narrower
in punning not allowed [Declaration(ObjectProperty(...narrower)), Declaration(AnnotationProperty(...narrower))]
```

`imports/eli.owl` declares these terms `owl:AnnotationProperty`; SKOS's own `imports/skos.rdf`
declares them `owl:ObjectProperty`. OWL 2 DL forbids punning between the two, so loading both
imports violates it. The OWL API and Protégé downgrade this to a warning, and it does not
affect reasoning or anything this project asserts. `check-reasoner.py` does not detect it,
because `owlrl` has no notion of entity-kind consistency.

## Reproducing

```sh
scripts/run-hermit.sh                 # full closure, matches the GUI result
scripts/run-hermit.sh aia-ont.ttl     # core + four imports, no worked example
```

The script extracts the OWL API's nested jars from Protégé's OSGi bundle
`owlapi-osgidistribution.jar` (plain `java -cp` cannot follow `Bundle-ClassPath`), and on
first run fetches `dk.brics.automaton` (~170 KB) from Maven Central. Needs `PROTEGE_HOME`
(default `~/.local/share/Protege-5.6.9`) and a JDK on `PATH`.
