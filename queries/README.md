# queries/

Each query assumes the prefixes in `prefixes.rq`. `scripts/run-cq-queries.py` runs them all
over the inferred graph and writes `reports/cq-results.md`.

| File | Question |
| --- | --- |
| `cq1-risk-category.rq` | CQ1: risk category of a system and the grounds for it |
| `cq1-highrisk-entailment.rq` | CQ1 as an ASK over the classified graph; false over asserted triples alone |
| `cq2-prohibited-practices.rq` | CQ2: prohibited practices, the prohibiting article, conditional exemptions |
| `cq3-actor-obligations.rq` | CQ3: obligations of the provider vs the deployer of a high-risk system |
| `cq4-role-reassignment.rq` | CQ4: when a deployer, distributor or importer becomes a provider, and the consequences |
| `cq5-oversight-conformity.rq` | CQ5: overseeing authority per obligation and conformity assessment route per system |
| `prefixes.rq` | Shared prefix block |
