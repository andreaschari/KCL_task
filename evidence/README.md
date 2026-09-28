# evidence/

Protégé 5.6.9 / HermiT runs. [`protege-hermit-findings.md`](protege-hermit-findings.md) summarises what they show.

| File | Contents |
| --- | --- |
| `protege-hermit-findings.md` | Findings from the CLI and GUI runs |
| `hermit-full-run.log` | `scripts/run-hermit.sh` over core + imports + worked example |
| `hermit-strict-default-run.log` | The same run without `ignoreUnsupportedDatatypes`, as a plain OWL API consumer would hit it |
| `protege-aia-ont-inferred.png` | Core ontology classified in Protégé, imported classes in the inferred hierarchy |
| `protege-aia-ont-dlquery-nothing.png` | DL query `owl:Nothing`: no unsatisfiable classes |
| `protege-aia-example-cq1-highrisk-1.png`, `-2.png` | DL query `'High Risk AI System'` on the worked example: all expected systems inferred high-risk |
| `protege-aia-example-terminated-roles.png` | DL query `'Terminated role assignment'` on the worked example: both Article 25(2) terminations inferred |
