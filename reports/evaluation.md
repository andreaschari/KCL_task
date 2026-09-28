# Ontology Evaluation: Metrics and Methods

Five metrics. The first four are computed by `scripts/compute-metrics.py`, with values in
`metrics-results.md`; the fifth is manual.

| # | Metric | Why | Method | Current value | Limitation |
|---|---|---|---|---|---|
| 1 | Consistency | Required by the task: the ontology must load in Protégé and be consistent under a standard reasoner | HermiT as bundled with Protégé 5.6.9, in the GUI and via `scripts/run-hermit.sh`; OWL 2 RL (`owlrl`) in the scripts | Consistent; 0 unsatisfiable classes (HermiT); 0 OWL 2 RL inconsistencies | Consistency says nothing about whether the content is right: axioms that never interact are trivially consistent |
| 2 | CQ answerability | The standard test of whether an ontology does its job (Grüninger & Fox, 1995); the task asks for competency questions | Each CQ query run over the asserted and the inferred graph; rows returned, projected cells bound, and whether the answer depends on inference. `check-reasoner.py` also asserts expected answers over the worked example (e.g. CQ3's 27 rows, with the initial provider holding only its four Art. 25(2) residual duties) | 6/6 queries return; 797/1018 projected cells bound (78%); 4/6 depend on inference | Returning rows is not returning the right rows; the expected answers are the builder's own |
| 3 | Annotation completeness | Required by the task: labels, short descriptions and article references | `skos:prefLabel`, `skos:definition` and an `aia:definedIn` article anchor, per local class, property and individual | Labels 92/92; definitions 92/92; article anchors 86/92 | Presence, not quality. The 6 unanchored terms are modelling devices with no defining provision |
| 4 | Provision coverage | Measures "represents the main elements of the Act" against the Act's own enumerations rather than the ontology's | Modelled individuals against lists taken from the Act's numbering: the Art. 3(8) operators, the ten Art. 5(1) practices, Art. 16(a)–(l), Art. 25(1) and 25(2), Art. 26 | 46/46 in scope; 12/113 articles and 5/13 annexes have an article resource | The in-scope lists are the builder's choice of scope (`report.md` §1) |
| 5 | Expert legal review | The only check that catches a wrong or overstated reading of the law, which none of the automated checks detect | Two reviewers with legal training classify each obligation, practice and exemption against the Official Journal as correct, overstated, understated or citing the wrong provision | Not run | Needs reviewers outside the project. The builder's own checks against the Official Journal, listed in `ai-workflow-log.md`, found errors of exactly this kind |


## References

- Grüninger, M., Fox, M. S. (1995). Methodology for the design and evaluation of ontologies. *IJCAI Workshop on Basic Ontological Issues in Knowledge Sharing*.
