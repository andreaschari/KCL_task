# scripts/

Run from the repository root unless noted. Python dependencies: `rdflib`, `owlrl`, `pyshacl`.
The Java-based scripts use the jars bundled with Protégé 5.6.9 and need a JDK on `PATH`.

| File | Purpose |
| --- | --- |
| `validate-imports.py` | Resolves `owl:imports` through the catalog and merges the closure. Run from `ontology/`. |
| `check-reasoner.py` | OWL 2 RL consistency and entailment checks over the core and its imports |
| `run-cq-queries.py` | Runs CQ1–CQ5 over the inferred graph; writes `reports/cq-results.md` |
| `check-shapes.py` | SHACL validation plus deliberately broken graphs each shape must catch |
| `compute-metrics.py` | Computes the automated evaluation metrics (consistency, CQ answerability, annotation completeness, provision coverage); writes `reports/metrics-results.md` |
| `page-count.py` | Renders a markdown file to PDF and reports its page count (needs `markdown`, `soffice`, `pdfinfo`) |
| `fetch-imports.sh` | Reproduces the vendored set in `ontology/imports/` |
| `run-hermit.sh`, `RunHermit.java` | HermiT over the full import closure via the OWL API, outside the Protégé GUI |
