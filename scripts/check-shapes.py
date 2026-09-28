"""SHACL validation of the ontology and the worked example.

Validates ontology/aia-ont.ttl + ontology/aia-example.ttl + the four vendored
imports against shapes/aia-shapes.ttl, then runs negative controls: broken
graphs that each shape must report. Exit status is non-zero if any check fails.

Inference is off. Several shapes check the type of a value (aia:heldBy to an
airo:AIOperator, aia:concernsSystem to an airo:AISystem) on properties that
have rdfs:range; with inference on, the type would be entailed from the
assertion and the constraint could not fail. The imports are still loaded,
because sh:class follows rdf:type/rdfs:subClassOf* into imported axioms.

advanced=True enables the SHACL-AF SPARQL target used by
shp:LocalTermAnnotationShape. The shapes file defines no SHACL rules.

Run from the repository root:  python3 scripts/check-shapes.py
Needs: rdflib, pyshacl.
"""
import os, sys
import rdflib
from pyshacl import validate as shacl_validate

ROOT   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ONT    = os.path.join(ROOT, "ontology")
SHAPES = os.path.join(ROOT, "shapes", "aia-shapes.ttl")
SH     = rdflib.Namespace("http://www.w3.org/ns/shacl#")
IMPORTS = [("eu-aiact-owl.ttl", "turtle"), ("airo.ttl", "turtle"),
           ("eli.owl", "xml"), ("skos.rdf", "xml")]
PFX = """
@prefix aia:  <https://w3id.org/aia-ont#> .
@prefix ex:   <https://example.org/test#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix eli:  <http://data.europa.eu/eli/ontology#> .
@prefix airo: <https://w3id.org/airo#> .
@prefix org:  <http://www.w3.org/ns/org#> .
@prefix eu-aiact-owl: <https://w3id.org/dpv/legal/eu/aiact/owl#> .
"""

shapes_graph = rdflib.Graph().parse(SHAPES, format="turtle")

def data(extra=None):
    g = rdflib.Graph()
    g.parse(os.path.join(ONT, "aia-ont.ttl"), format="turtle")
    g.parse(os.path.join(ONT, "aia-example.ttl"), format="turtle")
    for f, fmt in IMPORTS:
        g.parse(os.path.join(ONT, "imports", f), format=fmt)
    if extra:
        g.parse(data=PFX + extra, format="turtle")
    return g

def run(extra=None):
    """Return (violations, warnings, infos) as lists of (focus, message)."""
    conforms, report, _ = shacl_validate(
        data(extra), shacl_graph=shapes_graph, inference="none",
        advanced=True, allow_warnings=True, allow_infos=True, debug=False)
    buckets = {SH.Violation: [], SH.Warning: [], SH.Info: []}
    for r in report.subjects(rdflib.RDF.type, SH.ValidationResult):
        sev = next(report.objects(r, SH.resultSeverity), SH.Violation)
        focus = next(report.objects(r, SH.focusNode), None)
        msg = " ".join(str(m) for m in report.objects(r, SH.resultMessage))
        buckets.setdefault(sev, []).append((focus, msg))
    return buckets[SH.Violation], buckets[SH.Warning], buckets[SH.Info]

results = []
def check(ok, label, detail=""):
    results.append(bool(ok))
    print(f"  {'PASS' if ok else '**FAIL**':9} {label}")
    if detail and not ok:
        print(f"            {detail}")

def section(t):
    print(f"\n{t}\n" + "-" * len(t))

# ═══════════════════════════════════════════════════════════════════════
section("Shapes file")
nshapes = len(set(shapes_graph.subjects(rdflib.RDF.type, SH.NodeShape)))
check(nshapes >= 12, f"{nshapes} node shapes parse from shapes/aia-shapes.ttl")
check(list(shapes_graph.triples((None, SH.sparql, None))),
      "SHACL-SPARQL constraints present (the Art. 25 integrity rules)")
check(list(shapes_graph.subjects(rdflib.RDF.type, SH.SPARQLTarget)),
      "one SHACL-AF SPARQL target present (annotation completeness over aia:)")

# ═══════════════════════════════════════════════════════════════════════
section("The repository as it stands")
v, w, i = run()
check(not v, f"core + worked example + imports: NO violations (found {len(v)})",
      detail="; ".join(f"{f}: {m}" for f, m in v[:3]))
check(not w, f"and no warnings either (found {len(w)})",
      detail="; ".join(f"{f}: {m}" for f, m in w[:3]))

# ═══════════════════════════════════════════════════════════════════════
section("Negative controls — each shape must catch its own failure")
CONTROLS = [
    ("role assignment with no actor",
     """ex:RA a aia:RoleAssignment ; skos:prefLabel "x"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Provider .""",
     "held by exactly one"),

    ("role assignment concerning two systems",
     """ex:RA a aia:RoleAssignment ; skos:prefLabel "x"@en ;
            aia:hasRole aia:Provider ; aia:heldBy aia:ExampleActorTalentFlowGmbH ;
            aia:concernsSystem aia:ExampleSpamFilter , aia:ExampleCustomerServiceChatbot .""",
     "exactly one airo:AISystem"),

    ("role assignment whose role is an obligation, not a role",
     """ex:RA a aia:RoleAssignment ; skos:prefLabel "x"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH ; aia:hasRole aia:ob_art16_a .""",
     "aia:Role individual"),

    ("ORPHANED EXEMPTION — reachable from no practice",
     """ex:Orphan a aia:Exemption ; aia:providedFor aia:art_5 ;
            skos:prefLabel "x"@en ; skos:definition "y"@en .""",
     "ORPHANED EXEMPTION"),

    ("obligation borne by two roles",
     """ex:Ob a aia:Obligation ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:appliesToCategory eu-aiact-owl:RiskLevelHigh ; aia:statedIn aia:art_16 ;
            aia:borneBy aia:Provider , aia:Deployer .""",
     "exactly one role"),

    ("high-risk system whose only Annex ground is an Art. 6(3) derogation",
     """ex:S a airo:AISystem ; skos:prefLabel "x"@en ;
            aia:hasRiskCategory eu-aiact-owl:RiskLevelHigh ;
            aia:classifiedOnGround aia:g_cvformat_annexIII_4a_derogated .""",
     "takes the system out of high risk"),

    ("obligation borne both by a live role and on termination",
     """ex:Ob a aia:Obligation ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:appliesToCategory eu-aiact-owl:RiskLevelHigh ; aia:statedIn aia:art_25 ;
            aia:borneBy aia:Provider ; aia:borneOnTermination aia:Provider .""",
     "not both and not neither"),

    ("obligation with no definition",
     """ex:Ob a aia:Obligation ; skos:prefLabel "x"@en ; aia:borneBy aia:Provider ;
            aia:appliesToCategory eu-aiact-owl:RiskLevelHigh ; aia:statedIn aia:art_16 .""",
     "cannot be checked against the Official Journal"),

    ("practice typed as an AI system (practice != artefact)",
     """ex:P a aia:ProhibitedPractice , airo:AISystem ; skos:prefLabel "x"@en ;
            skos:definition "y"@en ; rdfs:seeAlso eu-aiact-owl:ProhibitedAISystem-A5-1-a ;
            aia:prohibitedBy aia:art_5 .""",
     "not artefacts"),

    ("practice with no cross-reference to its eu-aiact term",
     """ex:P a aia:ProhibitedPractice ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:prohibitedBy aia:art_5 .""",
     "supplements the import"),

    ("Art. 25 event establishing an assignment held by a DIFFERENT actor",
     """ex:RR a aia:RoleReassignment ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:statedIn aia:art_25 ;
            aia:triggeredBy aia:rc_art25_1_a_own_name ;
            aia:promotes ex:Prior ; aia:establishes ex:New .
        ex:Prior a aia:RoleAssignment ; skos:prefLabel "p"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Deployer ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .
        ex:New a aia:RoleAssignment ; skos:prefLabel "n"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Provider ;
            aia:heldBy aia:ExampleActorPeopleMetricsLtd .""",
     "SAME actor"),

    ("Art. 25 event whose established assignment is not a provider assignment",
     """ex:RR a aia:RoleReassignment ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:statedIn aia:art_25 ;
            aia:triggeredBy aia:rc_art25_1_a_own_name ;
            aia:promotes ex:Prior ; aia:establishes ex:New .
        ex:Prior a aia:RoleAssignment ; skos:prefLabel "p"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Deployer ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .
        ex:New a aia:RoleAssignment ; skos:prefLabel "n"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Importer ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .""",
     "PROVIDER assignment"),

    ("Art. 25 event touching an assignment about another system",
     """ex:RR a aia:RoleReassignment ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:statedIn aia:art_25 ;
            aia:triggeredBy aia:rc_art25_1_a_own_name ;
            aia:promotes ex:Prior ; aia:establishes ex:New .
        ex:Prior a aia:RoleAssignment ; skos:prefLabel "p"@en ;
            aia:concernsSystem aia:ExampleCustomerServiceChatbot ; aia:hasRole aia:Deployer ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .
        ex:New a aia:RoleAssignment ; skos:prefLabel "n"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Provider ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .""",
     "same AI system"),

    ("Art. 25 event terminating a NON-provider assignment (Art. 25(2))",
     """ex:RR a aia:RoleReassignment ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:statedIn aia:art_25 ;
            aia:triggeredBy aia:rc_art25_1_a_own_name ;
            aia:promotes ex:Prior ; aia:establishes ex:New ;
            aia:terminates aia:ra_recruitment_northborough_deployer .
        ex:Prior a aia:RoleAssignment ; skos:prefLabel "p"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Deployer ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .
        ex:New a aia:RoleAssignment ; skos:prefLabel "n"@en ;
            aia:concernsSystem aia:ExampleSpamFilter ; aia:hasRole aia:Provider ;
            aia:heldBy aia:ExampleActorTalentFlowGmbH .""",
     "INITIAL PROVIDER"),

    ("system in two risk tiers at once",
     """ex:S a airo:AISystem ; skos:prefLabel "x"@en ;
            aia:hasRiskCategory eu-aiact-owl:RiskLevelHigh , eu-aiact-owl:RiskLevelMinimal .""",
     "exactly one risk tier"),

    ("bare ClassificationGround, typed with no Art. 6 route",
     """ex:G a aia:ClassificationGround ; skos:prefLabel "x"@en ; skos:definition "y"@en .""",
     "the bare parent class classifies nothing"),

    ("oversight assignment on a body that is not one of CQ5's four",
     """ex:OA a aia:OversightAssignment ; skos:prefLabel "x"@en ;
            aia:oversees aia:ob_art16_a ; aia:assignedTo ex:SomeBody .
        ex:SomeBody a org:Organization ; skos:prefLabel "b"@en .""",
     "four authority kinds"),

    ("oversight assignment on a body not typed org:Organization",
     """ex:OA a aia:OversightAssignment ; skos:prefLabel "x"@en ;
            aia:oversees aia:ob_art16_a ; aia:assignedTo ex:SomeBody .
        ex:SomeBody a eu-aiact-owl:AIOffice ; skos:prefLabel "b"@en .""",
     "org:Organization"),

    ("conformity route stated in something other than Annex VI, Annex VII or Art. 43(3)",
     """ex:R a aia:ConformityAssessmentRoute ; skos:prefLabel "x"@en ; skos:definition "y"@en ;
            aia:appliesToObligation aia:ob_art16_f ; aia:statedIn aia:art_16 .""",
     "exactly three procedures"),

    ("a role ALSO declared an owl:Class (the punning error)",
     """aia:Provider a owl:Class .""",
     "never classes of actors"),

    ("an actor also typed as a role",
     """ex:A a airo:AIOperator , aia:Role ; skos:prefLabel "x"@en ;
            skos:definition "y"@en ; aia:definedIn aia:art_3 .""",
     "not a role"),

    ("article resource with two eli:number values",
     """aia:art_5 eli:number "5bis" .""",
     "exactly one eli:number"),

    ("article resource with two values on ELI's FUNCTIONAL eli:type_subdivision",
     """aia:art_5 eli:type_subdivision <http://example.org/a> , <http://example.org/b> .""",
     "owl:FunctionalProperty"),

    ("article resource not part of the Act",
     """ex:Art a eli:LegalResourceSubdivision ; eli:number "99" ; skos:prefLabel "x"@en ;
            eli:is_part_of <http://example.org/other-act> .""",
     "eli:is_part_of the Act's own ELI URI"),

    ("a locally minted class with no skos:definition",
     """aia:SomeNewClass a owl:Class ; skos:prefLabel "x"@en .""",
     "skos:definition"),
]
for label, extra, keyword in CONTROLS:
    v, w, i = run(extra)
    caught = bool(v) and any(keyword in m for _, m in v)
    check(caught, f"caught: {label}",
          detail=(f"no violation at all" if not v else
                  f"violations found but none mentioning {keyword!r}: "
                  + "; ".join(m[:90] for _, m in v[:2])))

# ═══════════════════════════════════════════════════════════════════════
section("Severity control — the one case that must NOT be a violation")
# Art. 6(3) can withdraw the high-risk category and Art. 6 is not the only route
# the Act uses, so a high-risk system with no recorded ground is under-described
# rather than wrong. Reporting it as a violation would contradict the
# decision that the classification rule is sufficient-only.
v, w, i = run("""ex:Ungrounded a airo:AISystem ; skos:prefLabel "x"@en ;
                     aia:hasRiskCategory eu-aiact-owl:RiskLevelHigh .""")
check(not v, f"a high-risk system with no ground raises NO violation (found {len(v)})",
      detail="; ".join(m[:90] for _, m in v[:2]))
check(any("under-described" in m for _, m in w),
      f"it raises a WARNING instead ({len(w)} warning(s))",
      detail="; ".join(m[:90] for _, m in w[:2]))

print(f"\n{'='*72}\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
