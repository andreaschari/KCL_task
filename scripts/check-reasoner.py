"""Reasoner checks over ontology/aia-ont.ttl, its import closure and the worked example.

Each check prints PASS or FAIL; the exit status is non-zero if any fails.
Sections, in run order:

  external term stubs   every dpv/* IRI the imports reference is declared, and
                        the stub set matches the one recomputed from the closure
  object properties     domain and range declared; union domains exercised in
                        both directions; domain/range propagation catches misuse
  article resources     ELI subdivisions of the Act that entail eli:Work and
                        satisfy the article patterns the CQ queries bind
  role individuals      roles are individuals of aia:Role, never classes
  obligations           role, article and tier per duty; OJ wording checks
  Art. 5 practices      practices, exemption distribution, no practice typed as
                        an AI system, no orphaned exemption
  alignment module      bound axioms present, forbidden ones absent, no
                        disjointness introduced, core unaffected
  classification rule   aia:HighRiskByGround entails the imported
                        eu-aiact:HighRiskAISystem and is sufficient-only
  worked example        consistent with the core; the rule fires on exactly the
                        expected systems; tiers, dual-role actors and Art. 25(1)
                        limbs present
  Art. 25(2)            terminated assignments are entailed, not asserted; CQ3
                        and CQ4 return residual duties for them and not the
                        duties of the ended role

Reasoning is OWL 2 RL via owlrl. The rules the entailments need (cls-svf1,
cls-uni, cax-eqc, cax-sco, prp-dom, prp-rng, prp-inv) are all in OWL 2 RL.
owlrl reports inconsistency through error_messages rather than by deriving
owl:Nothing membership, so consistency is read from error_messages.

Run from the repository root:  python3 scripts/check-reasoner.py
Needs: rdflib, owlrl.
"""
import os, sys
import rdflib
from rdflib.namespace import RDF, RDFS, OWL
from owlrl import OWLRL_Semantics

ROOT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ONT   = os.path.join(ROOT, "ontology")
AIA   = rdflib.Namespace("https://w3id.org/aia-ont#")
EX    = rdflib.Namespace("https://example.org/test#")
AIACT = rdflib.Namespace("https://w3id.org/dpv/legal/eu/aiact/owl#")
AIRO  = rdflib.Namespace("https://w3id.org/airo#")
ELI   = rdflib.Namespace("http://data.europa.eu/eli/ontology#")
DPV   = rdflib.Namespace("https://w3id.org/dpv/owl#")
ACT   = rdflib.URIRef("http://data.europa.eu/eli/reg/2024/1689/oj")
SKOSDEF = rdflib.URIRef("http://www.w3.org/2004/02/skos/core#definition")
ALL_IMPORTS = [("eu-aiact-owl.ttl","turtle"), ("airo.ttl","turtle"),
               ("eli.owl","xml"), ("skos.rdf","xml")]
PFX = ("@prefix aia: <https://w3id.org/aia-ont#> .\n"
       "@prefix ex:  <https://example.org/test#> .\n"
       "@prefix eli: <http://data.europa.eu/eli/ontology#> .\n"
       "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
       "@prefix airo: <https://w3id.org/airo#> .\n")

def load(imports=ALL_IMPORTS, extra=None, base=None, example=False):
    """Parse the local file (or `base` instead) + chosen imports + inline data.

    `example=True` adds the worked example. It is off by default so
    that every check before the worked-example section tests the model on its own: a
    fixture that happened to supply a missing triple would otherwise mask the
    gap it was meant to expose.
    """
    g = rdflib.Graph()
    g.parse(os.path.join(ONT, "aia-ont.ttl"), format="turtle") if base is None \
        else g.parse(data=base, format="turtle")
    if example:
        g.parse(os.path.join(ONT, "aia-example.ttl"), format="turtle")
    for f, fmt in imports:
        g.parse(os.path.join(ONT, "imports", f), format=fmt)
    if extra:
        g.parse(data=PFX + extra, format="turtle")
    return g

def expand(g):
    r = OWLRL_Semantics(g, False, False, False)
    r.closure(); r.flush_stored_triples()
    return g, getattr(r, "error_messages", [])

results = []
def check(ok, label, detail=""):
    results.append(bool(ok))
    print(f"  {'PASS' if ok else '**FAIL**':9} {label}")
    if detail and not ok:
        print(f"            {detail}")

def section(t):
    print(f"\n{t}\n" + "-" * len(t))

# ═══════════════════════════════════════════════════════════════════════
section("External term stubs")
g = load()
declared = (set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, OWL.ObjectProperty))
          | set(g.subjects(RDF.type, OWL.DatatypeProperty))
          | set(g.subjects(RDF.type, OWL.AnnotationProperty))
          | set(g.subjects(RDF.type, RDFS.Class)))
dangling = set()
for s, p, o in g:
    if (isinstance(o, rdflib.URIRef) and o not in declared
            and str(o).startswith("https://w3id.org/dpv/")
            and p in (RDFS.subClassOf, RDFS.subPropertyOf, RDF.type, RDFS.domain, RDFS.range)):
        dangling.add(o)
check(not dangling, f"no undeclared dpv/* IRI remains in the closure ({len(dangling)} found)",
      detail="; ".join(sorted(str(d) for d in dangling)[:4]))
local = rdflib.Graph(); local.parse(os.path.join(ONT, "aia-ont.ttl"), format="turtle")
stubs = {s for s in local.subjects(RDF.type, None) if str(s).startswith("https://w3id.org/dpv/")}
check(len(stubs) == 55, f"stub count is 55 as recorded (found {len(stubs)})")
for t in (DPV.Authority, DPV.RiskLevel, DPV.hasRiskLevel, AIACT.ConformityAssessmentBody):
    check((t, RDF.type, None) in g, f"{t.split('/')[-1]:34} is declared (needed by CQ1/CQ5)")

# ═══════════════════════════════════════════════════════════════════════
section("Object properties")
PROPS = ["definedIn","statedIn","prohibitedBy","providedFor","hasRiskCategory",
         "classifiedOnGround","concernsSystem","hasRole","heldBy","triggeredBy",
         "promotes","establishes","terminates","terminatedBy","borneBy",
         "appliesToCategory","hasExemption","oversees","assignedTo",
         "appliesToObligation"]
missing = [p for p in PROPS if (AIA[p], RDF.type, OWL.ObjectProperty) not in local]
check(not missing, f"all {len(PROPS)} object properties declared", detail=str(missing))
norange = [p for p in PROPS if not list(local.objects(AIA[p], RDFS.range))]
check(not norange, "every property has an rdfs:range", detail=str(norange))
nodomain = [p for p in PROPS if not list(local.objects(AIA[p], RDFS.domain))]
check(nodomain == ["definedIn"],
      f"only aia:definedIn lacks a domain, deliberately (found {nodomain})")
# every query term is now declared
qterms = set()
import re, glob
for f in glob.glob(os.path.join(ROOT, "queries", "*.rq")):
    qterms |= set(re.findall(r"aia:([A-Za-z][A-Za-z0-9_]*)", open(f).read()))
undeclared = sorted(t for t in qterms if (AIA[t], RDF.type, None) not in local)
check(undeclared == ["ExampleRecruitmentScreeningSystem"],
      f"the core declares every query term except the worked example: {undeclared}")
# ... and with the worked example loaded, nothing the queries name is undeclared.
exg = rdflib.Graph(); exg.parse(os.path.join(ONT, "aia-example.ttl"), format="turtle")
undeclared = sorted(t for t in qterms
                    if (AIA[t], RDF.type, None) not in local
                    and (AIA[t], RDF.type, None) not in exg)
check(undeclared == [],
      f"with ontology/aia-example.ttl loaded, NO query term is undeclared: {undeclared}")

section("The union-domain trap, both directions")
# (a) as written, using the property on BOTH disjoint subject kinds is consistent
_, e = expand(load(imports=[("airo.ttl","turtle")], extra="""
ex:RA a aia:RoleAssignment   ; aia:concernsSystem ex:Sys .
ex:RR a aia:RoleReassignment ; aia:concernsSystem ex:Sys .
ex:Ob a aia:Obligation                 ; aia:statedIn aia:art_16 .
ex:CR a aia:ConformityAssessmentRoute  ; aia:statedIn aia:art_43 .
"""))
check(not e, "union domain: concernsSystem/statedIn used across disjoint kinds is CONSISTENT",
      detail="; ".join(e[:2]))
# (b) the trap is real: the same file with two rdfs:domain instead goes inconsistent
trap = open(os.path.join(ONT, "aia-ont.ttl")).read().replace(
    "    rdfs:domain [ a owl:Class ; owl:unionOf ( aia:RoleAssignment aia:RoleReassignment ) ] ;",
    "    rdfs:domain aia:RoleAssignment , aia:RoleReassignment ;")
_, e2 = expand(load(imports=[("airo.ttl","turtle")], base=trap, extra="""
ex:RA a aia:RoleAssignment ; aia:concernsSystem ex:Sys .
"""))
check(e2, "control: rewriting it as two rdfs:domain triples DOES go inconsistent",
      detail="expected an inconsistency, got none")

section("Domain/range propagation")
g3, e3 = expand(load(imports=[("airo.ttl","turtle")], extra="""
ex:RA a aia:RoleAssignment ; aia:concernsSystem ex:Sys ; aia:heldBy ex:Acme .
ex:Ob a aia:Obligation ; aia:borneBy ex:SomeRole .
"""))
check(not e3, "propagation data is consistent", detail="; ".join(e3[:2]))
check((EX.Sys, RDF.type, AIRO.AISystem) in g3, "range propagates airo:AISystem onto the system")
check((EX.Acme, RDF.type, AIRO.AIOperator) in g3, "range propagates airo:AIOperator onto the actor")
check((EX.SomeRole, RDF.type, AIA.Role) in g3, "range propagates aia:Role onto the role")
for label, data in [
    ("an Obligation used where a Role belongs",
     "ex:Ob a aia:Obligation . ex:RA a aia:RoleAssignment ; aia:hasRole ex:Ob ."),
    ("a Role used as the system of an assignment",
     "ex:R a aia:Role . ex:RA a aia:RoleAssignment ; aia:concernsSystem ex:R ."),
    ("an actor used as the system of an assignment",
     "ex:RA a aia:RoleAssignment ; aia:heldBy ex:A ; aia:concernsSystem ex:A ."),
    ("an Exemption used as an oversight target",
     "ex:X a aia:Exemption . ex:OA a aia:OversightAssignment ; aia:oversees ex:X ."),
]:
    _, en = expand(load(imports=[("airo.ttl","turtle")], extra=data))
    check(en, f"NEGATIVE control caught: {label}")

# ═══════════════════════════════════════════════════════════════════════
section("Article resources")
ARTS = ["art_3","art_5","art_6","art_16","art_17","art_25","art_26","art_43","art_50",
        "art_70","art_74","art_75","annex_I","annex_II","annex_III","annex_VI","annex_VII"]
bad = [a for a in ARTS if (AIA[a], RDF.type, ELI.LegalResourceSubdivision) not in local]
check(not bad, f"all {len(ARTS)} article/annex resources typed eli:LegalResourceSubdivision",
      detail=str(bad))
bad = [a for a in ARTS if (AIA[a], ELI.is_part_of, ACT) not in local]
check(not bad, "every one is eli:is_part_of the Act's ELI URI", detail=str(bad))
bad = [a for a in ARTS if not list(local.objects(AIA[a], ELI.number))]
check(not bad, "every one carries eli:number", detail=str(bad))
check((ACT, RDF.type, ELI.LegalResource) in local, "the Act itself is typed eli:LegalResource")

gA, eA = expand(load())
check(not eA, "closure with the article resources is CONSISTENT", detail="; ".join(eA[:2]))
check((AIA.art_5, RDF.type, ELI.Work) in gA,
      "articles entail eli:Work (LegalResourceSubdivision -> LegalResource -> Work)")
check((AIA.art_5, RDF.type, ELI.WorkSubdivision) in gA,
      "and eli:WorkSubdivision -- the v1.4 second superclass CQ2 depends on")
# the exact pattern CQ2 binds
q2 = list(gA.query("""PREFIX eli: <http://data.europa.eu/eli/ontology#>
  SELECT ?a ?n WHERE { ?a a eli:LegalResourceSubdivision ;
    eli:is_part_of <http://data.europa.eu/eli/reg/2024/1689/oj> ; eli:number ?n }"""))
check(len(q2) == len(ARTS), f"CQ2's article pattern binds all {len(ARTS)} (got {len(q2)})")
# the exact pattern CQ1 binds for tier provenance
q1 = list(gA.query("""PREFIX aia: <https://w3id.org/aia-ont#>
  PREFIX eu: <https://w3id.org/dpv/legal/eu/aiact/owl#>
  SELECT ?c ?a WHERE { ?c a eu:RiskLevel ; aia:definedIn ?a }"""))
check(len(q1) == 3, f"CQ1's tier->article pattern binds 3 tiers (got {len(q1)})")
check(all((a, RDF.type, ELI.LegalResourceSubdivision) in local for _, a in q1),
      "every tier's aia:definedIn target is a declared article resource")

# ═══════════════════════════════════════════════════════════════════════
section("Role individuals")
ROLES = ["Provider","Deployer","AuthorisedRepresentative","Importer",
         "Distributor","ProductManufacturer"]
bad = [r for r in ROLES if (AIA[r], RDF.type, AIA.Role) not in local]
check(not bad, f"all {len(ROLES)} roles are individuals of aia:Role", detail=str(bad))
bad = [r for r in ROLES if (AIA[r], RDF.type, OWL.NamedIndividual) not in local]
check(not bad, "each is declared owl:NamedIndividual (OWL 2 DL round-tripping)", detail=str(bad))
# roles must NOT be classes -- that is the whole modelling commitment
asclass = [r for r in ROLES if (AIA[r], RDF.type, OWL.Class) in local]
check(not asclass, "no role is also declared an owl:Class (the reification commitment)",
      detail=str(asclass))
bad = [r for r in ROLES if not list(local.objects(AIA[r], AIA.definedIn))]
check(not bad, "each role carries aia:definedIn provenance", detail=str(bad))
# roles are deliberately NOT pairwise distinct
check(not list(local.triples((None, OWL.differentFrom, None))),
      "no owl:differentFrom between roles (cumulative-role reading of Recital 83)")

gR, eR = expand(load())
check(not eR, "closure with the roles is CONSISTENT", detail="; ".join(eR[:2]))
# a role must not be inferred to be an actor or a system -- the disjointness earns its keep
for r in ("Provider", "Deployer"):
    check((AIA[r], RDF.type, AIRO.AIOperator) not in gR,
          f"aia:{r} is NOT inferred to be an airo:AIOperator (role != actor)")
    check((AIA[r], RDF.type, AIRO.AISystem) not in gR,
          f"aia:{r} is NOT inferred to be an airo:AISystem")
# NEGATIVE control: an actor asserted to BE a role must be caught
_, en = expand(load(imports=[("airo.ttl","turtle")], extra="""
ex:RA a aia:RoleAssignment ; aia:heldBy aia:Provider .
"""))
check(en, "NEGATIVE control caught: a role used as the actor holding it")

# ═══════════════════════════════════════════════════════════════════════
section("Obligations, Arts. 16, 25(2) and 26")
OB16 = [f"ob_art16_{c}" for c in "abcdefghijkl"]
OB26 = [f"ob_art26_{n}" for n in (1,2,4,5,6,7,8,9,10,11,12)]
for label, obs, role, art in [("Art. 16", OB16, AIA.Provider, AIA.art_16),
                              ("Art. 26", OB26, AIA.Deployer, AIA.art_26)]:
    bad = [o for o in obs if (AIA[o], RDF.type, AIA.Obligation) not in local]
    check(not bad, f"{label}: all {len(obs)} are individuals of aia:Obligation", detail=str(bad))
    bad = [o for o in obs if (AIA[o], AIA.borneBy, role) not in local]
    check(not bad, f"{label}: every one is aia:borneBy the right role", detail=str(bad))
    bad = [o for o in obs if (AIA[o], AIA.statedIn, art) not in local]
    check(not bad, f"{label}: every one is aia:statedIn the right article", detail=str(bad))
    bad = [o for o in obs if (AIA[o], AIA.appliesToCategory, AIACT.RiskLevelHigh) not in local]
    check(not bad, f"{label}: every one applies to RiskLevelHigh", detail=str(bad))
    bad = [o for o in obs if not list(local.objects(AIA[o], rdflib.URIRef(
        "http://www.w3.org/2004/02/skos/core#definition")))]
    check(not bad, f"{label}: every one has a skos:definition", detail=str(bad))
check(len(OB16) == 12, "Art. 16 has all twelve points (a)-(l)")
# Art. 26(3) is a savings clause, not a duty -- it must be absent
check((AIA.ob_art26_3, RDF.type, None) not in local,
      "Art. 26(3) is absent, being a savings clause rather than an obligation")
# Arts. 16 and 26 are both OJ-verified as of 2026-09-26. Assert that no stale
# UNVERIFIED marker survives anywhere -- the flag was machine-enforced while the
# debt was open, so it must be machine-enforced now that it is closed, or the
# tracking silently inverts and a future unverified term looks verified.
SKOSD = rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#comment")
stale = [o for o in OB16 + OB26
         if any("UNVERIFIED" in str(c) for c in local.objects(AIA[o], SKOSD))]
check(not stale, "no Art. 16/26 obligation still carries an UNVERIFIED marker", detail=str(stale))
unmarked = [o for o in OB26
            if not any("VERIFIED" in str(c) for c in local.objects(AIA[o], SKOSD))]
check(not unmarked, "every Art. 26 obligation records its VERIFIED status", detail=str(unmarked))
# the four corrections the consolidated text forced
check(any("2016/680" in str(c) for c in local.objects(AIA.ob_art26_9, SKOSD)),
      "Art. 26(9) cites Directive (EU) 2016/680, not Regulation (EU) 2018/1725")
# The definition is the normative statement and must be clean; the rdfs:comment
# deliberately NAMES the wrong instrument, because a correction note that does not
# say what was corrected is not a correction note.
check(not any("2018/1725" in str(o) for o in local.objects(AIA.ob_art26_9, SKOSDEF)),
      "Art. 26(9)'s DEFINITION is free of the wrong instrument (2018/1725)")
check(any("2018/1725" in str(c) for c in local.objects(AIA.ob_art26_9, SKOSD)),
      "Art. 26(9)'s comment still records which instrument was wrong")
check(any("48 hours" in str(o) for o in local.objects(AIA.ob_art26_10, SKOSDEF)),
      "Art. 26(10) carries the 48-hour limit")
check(any("except" in str(o).lower() for o in local.objects(AIA.ob_art26_10, SKOSDEF)),
      "Art. 26(10) carries the initial-identification exception")

gO, eO = expand(load())
check(not eO, "closure with all obligations is CONSISTENT", detail="; ".join(eO[:2]))
# CQ3's obligation half must now bind for both roles
for role, n in [("Provider", 12), ("Deployer", 11)]:
    rows = list(gO.query("""PREFIX aia: <https://w3id.org/aia-ont#>
      PREFIX eu: <https://w3id.org/dpv/legal/eu/aiact/owl#>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
      SELECT ?o WHERE { ?o a aia:Obligation ; aia:borneBy ?r ;
        aia:appliesToCategory eu:RiskLevelHigh ; skos:prefLabel ?l ; aia:statedIn ?a }""",
      initBindings={"r": AIA[role]}))
    check(len(rows) == n, f"CQ3's obligation pattern binds {n} for aia:{role} (got {len(rows)})")
# obligations must not be inferred to be roles or systems
check((AIA.ob_art16_a, RDF.type, AIA.Role) not in gO,
      "an obligation is NOT inferred to be a Role")
# NEGATIVE control: an obligation borne by something that is not a role
_, en = expand(load(imports=[("airo.ttl","turtle")], extra="""
ex:Sys a airo:AISystem . ex:Ob a aia:Obligation ; aia:borneBy ex:Sys .
"""))
check(en, "NEGATIVE control caught: an obligation borne by an AI system rather than a role")

# ═══════════════════════════════════════════════════════════════════════
section("Art. 5 practices and exemptions")
PRACTICES = [f"pp_art5_1_{c}" for c in ["a","b","ba","bb","c","d","e","f","g","h"]]
EXEMPT = ["ex_art5_1_d_human","ex_art5_1_f_medical","ex_art5_1_g_lawful_dataset",
          "ex_art5_1_g_law_enforcement","ex_art5_1_h_victims","ex_art5_1_h_threat",
          "ex_art5_1_h_suspect","ex_art5_1_h_procedural",
          "ex_art5_1a_scope","ex_art5_1b_no_increased_exposure","ex_art5_1_bb_without_right"]
RDFSC = rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#comment")
bad = [x for x in PRACTICES if (AIA[x], RDF.type, AIA.ProhibitedPractice) not in local]
check(not bad, f"all 10 Art. 5(1) practices (a)-(h) with (ba) and (bb) are individuals", detail=str(bad))
bad = [x for x in PRACTICES if (AIA[x], AIA.prohibitedBy, AIA.art_5) not in local]
check(not bad, "every practice is aia:prohibitedBy Article 5", detail=str(bad))
bad = [x for x in EXEMPT if (AIA[x], RDF.type, AIA.Exemption) not in local]
check(not bad, f"all {len(EXEMPT)} exemptions are individuals of aia:Exemption", detail=str(bad))
bad = [x for x in EXEMPT if (AIA[x], AIA.providedFor, AIA.art_5) not in local]
check(not bad, "every exemption is aia:providedFor Article 5", detail=str(bad))
# practices must NOT be typed as eu-aiact prohibited-system classes
crossed = [x for x in PRACTICES
           if any(str(o).startswith(str(AIACT)) for o in local.objects(AIA[x], RDF.type))]
check(not crossed, "no practice is typed as a eu-aiact:ProhibitedAISystem (practice != artefact)",
      detail=str(crossed))
bad = [x for x in PRACTICES if not list(local.objects(AIA[x], RDFS.seeAlso))]
check(not bad, "each practice cross-references its eu-aiact class by rdfs:seeAlso", detail=str(bad))
# (ba) and (bb) postdate eu-aiact v2.3, so they cross-reference the act that inserted them
AMENDING = rdflib.URIRef("http://data.europa.eu/eli/reg/2026/1744/oj")
bad = [x for x in ("pp_art5_1_ba", "pp_art5_1_bb")
       if (AIA[x], RDFS.seeAlso, AMENDING) not in local]
check(not bad, "(ba) and (bb) cross-reference Regulation (EU) 2026/1744, having no eu-aiact term",
      detail=str(bad))
# the exemption distribution is the substantive claim -- assert it exactly
EXPECTED = {"pp_art5_1_a":0,"pp_art5_1_b":0,"pp_art5_1_ba":2,"pp_art5_1_bb":2,
            "pp_art5_1_c":0,"pp_art5_1_d":1,"pp_art5_1_e":0,"pp_art5_1_f":1,
            "pp_art5_1_g":2,"pp_art5_1_h":4}
actual = {x: len(list(local.objects(AIA[x], AIA.hasExemption))) for x in PRACTICES}
check(actual == EXPECTED, f"exemption counts are exactly as intended {actual}")
unconditional = sorted(x for x, n in actual.items() if n == 0)
check(unconditional == ["pp_art5_1_a","pp_art5_1_b","pp_art5_1_c","pp_art5_1_e"],
      f"the four unconditional prohibitions are (a)(b)(c)(e) and no others: {unconditional}")
# every exemption is reachable from some practice -- an orphan would never be returned
reachable = {str(o).split("#")[-1] for o in local.objects(None, AIA.hasExemption)}
check(reachable == set(EXEMPT), "no exemption is orphaned (all reachable via aia:hasExemption)",
      detail=str(set(EXEMPT) - reachable))
# Art. 5 is OJ-verified as of 2026-09-26; no stale marker may survive
stale = [x for x in PRACTICES + EXEMPT
         if any("UNVERIFIED" in str(c) for c in local.objects(AIA[x], RDFSC))]
check(not stale, "no Art. 5 individual still carries an UNVERIFIED marker", detail=str(stale))
unmarked = [x for x in PRACTICES + EXEMPT
            if not any("VERIFIED" in str(c) for c in local.objects(AIA[x], RDFSC))]
check(not unmarked, "every Art. 5 individual records its VERIFIED status", detail=str(unmarked))
# the reading that 5(1)(c)'s limbs are ELEMENTS, not exceptions -- confirmed by the OJ
check(len(list(local.objects(AIA.pp_art5_1_c, AIA.hasExemption))) == 0,
      "Art. 5(1)(c) still has no exemption: limbs (i)/(ii) are elements, CONFIRMED by the OJ")
# 5(1)(h)(iii)'s corrected threshold, and its Annex II link
check(any("MAXIMUM PERIOD" in str(o) for o in local.objects(AIA.ex_art5_1_h_suspect, SKOSDEF)),
      'Art. 5(1)(h)(iii) states the "maximum period" test, not a bare four-year term')
check((AIA.ex_art5_1_h_suspect, AIA.providedFor, AIA.annex_II) in local,
      "Art. 5(1)(h)(iii) is linked to the now-minted Annex II")
check((AIA.annex_II, RDF.type, ELI.LegalResourceSubdivision) in local,
      "Annex II is minted as an ELI subdivision")
# Art. 5(1a) narrows BOTH new prohibitions; 5(1b) only (ba); the defence only (bb)
check({str(p).split("#")[-1] for p in local.subjects(AIA.hasExemption, AIA.ex_art5_1a_scope)}
      == {"pp_art5_1_ba", "pp_art5_1_bb"},
      "Art. 5(1a) is an exemption of both (ba) and (bb)")
check((AIA.pp_art5_1_ba, AIA.hasExemption, AIA.ex_art5_1b_no_increased_exposure) in local
      and (AIA.pp_art5_1_bb, AIA.hasExemption, AIA.ex_art5_1_bb_without_right) in local,
      "Art. 5(1b) qualifies (ba), and the \"without right\" defence qualifies (bb)")
# consent in (ba) is an ELEMENT of the prohibition, stated in its definition
check(any("without that person's" in str(o) for o in local.objects(AIA.pp_art5_1_ba, SKOSDEF)),
      "Art. 5(1)(ba)'s absence of consent is in the definition, not modelled as an exemption")

g7, e7 = expand(load())
check(not e7, "closure with practices and exemptions is CONSISTENT", detail="; ".join(e7[:2]))
check((AIA.pp_art5_1_a, RDF.type, AIRO.AISystem) not in g7,
      "a practice is NOT inferred to be an AI system")
# CQ2's full pattern, including the OPTIONAL exemption half
rows = list(g7.query("""PREFIX aia: <https://w3id.org/aia-ont#>
  PREFIX eli: <http://data.europa.eu/eli/ontology#>
  PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  SELECT ?p ?e WHERE {
    ?p a aia:ProhibitedPractice ; skos:prefLabel ?l ; aia:prohibitedBy ?art .
    ?art a eli:LegalResourceSubdivision ;
         eli:is_part_of <http://data.europa.eu/eli/reg/2024/1689/oj> .
    OPTIONAL { ?p aia:hasExemption ?e . ?e a aia:Exemption ; skos:prefLabel ?el } }"""))
check(len(rows) == 16, f"CQ2 returns 16 rows: 4 unconditional + 12 exemption bindings (got {len(rows)})")
check(sum(1 for _, e in rows if e is None) == 4,
      "exactly 4 of those rows have no exemption binding")
_, en = expand(load(imports=[("airo.ttl","turtle")], extra="""
ex:P a aia:ProhibitedPractice ; aia:hasExemption ex:NotAnExemption .
ex:NotAnExemption a aia:Obligation .
"""))
check(en, "NEGATIVE control caught: an obligation used as an exemption")

# ═══════════════════════════════════════════════════════════════════════
section("Alignment module")
ALIGN = os.path.join(ONT, "aia-align.ttl")
check(os.path.exists(ALIGN), "ontology/aia-align.ttl exists")
al = rdflib.Graph(); al.parse(ALIGN, format="turtle")
PROV = rdflib.Namespace("http://www.w3.org/ns/prov#")
ORG  = rdflib.Namespace("http://www.w3.org/ns/org#")
ODRL = rdflib.Namespace("http://www.w3.org/ns/odrl/2/")
for s_, p_, o_, lbl in [
    (AIA.RoleAssignment, RDFS.subClassOf,    PROV.Association, "aia:RoleAssignment -> prov:Association"),
    (AIA.heldBy,         RDFS.subPropertyOf, PROV.agent,       "aia:heldBy -> prov:agent"),
    (AIA.hasRole,        RDFS.subPropertyOf, PROV.hadRole,     "aia:hasRole -> prov:hadRole"),
    (AIA.Provider,       RDF.type,           PROV.Role,        "aia:Provider a prov:Role"),
    (AIA.Role,           RDFS.subClassOf,    ORG.Role,         "aia:Role -> org:Role"),
    (AIA.Obligation,     RDFS.subClassOf,    DPV.Obligation,   "aia:Obligation -> dpv-owl:Obligation"),
]:
    check((s_, p_, o_) in al, f"bound axiom present: {lbl}")
# the decisions FORBID these
check((AIA.RoleAssignment, RDFS.subClassOf, ORG.Membership) not in al,
      "org:Membership is NOT subclassed (functional-property hazard)")
check(not any(o == ODRL.Duty for o in al.objects(None, RDFS.subClassOf)),
      "ODRL is rdfs:seeAlso only, never rdfs:subClassOf (no double-parenting)")
check(list(al.objects(AIA.Obligation, RDFS.seeAlso)), "the ODRL seeAlso annotation is present")
# the core must stay free of alignment commitments
for s_, p_, o_, lbl in [(AIA.Role, RDFS.subClassOf, ORG.Role, "org:Role"),
                        (AIA.Obligation, RDFS.subClassOf, DPV.Obligation, "dpv-owl:Obligation")]:
    check((s_, p_, o_) not in local, f"the CORE does not carry the {lbl} alignment")
check(not list(local.objects(None, OWL.imports))[0:0] or
      rdflib.URIRef("https://w3id.org/aia-ont/align") not in set(local.objects(None, OWL.imports)),
      "aia-ont.ttl does not import the alignment module")
# no disjointness may leak in from the aligned vocabularies
check(not list(al.triples((None, OWL.disjointWith, None)))
      and not list(al.subjects(RDF.type, OWL.AllDisjointClasses)),
      "the module introduces NO disjointness axiom (the PROV-O/ODRL hazard stays out)")
# and the aligned closure must still be consistent
gal = rdflib.Graph(); gal.parse(ALIGN, format="turtle")
gal.parse(os.path.join(ONT, "aia-ont.ttl"), format="turtle")
for f, fmt in ALL_IMPORTS:
    gal.parse(os.path.join(ONT, "imports", f), format=fmt)
_, eal = expand(gal)
check(not eal, "core + imports + ALIGNMENT module is CONSISTENT", detail="; ".join(eal[:2]))
check((AIA.Provider, RDF.type, ORG.Role) in gal,
      "with the module loaded, aia:Provider entails org:Role (alignment does work)")
# catalog must resolve the core so the module loads offline
cat = open(os.path.join(ONT, "catalog-v001.xml")).read()
check('name="https://w3id.org/aia-ont"' in cat,
      "catalog-v001.xml maps the core's IRI, so the module resolves offline")

# ═══════════════════════════════════════════════════════════════════════
section("Classification rule")
g9, e9 = expand(load(extra="""
ex:Recruitment aia:classifiedOnGround ex:GroundRecruit .
ex:GroundRecruit a aia:AnnexIIIGround , aia:PurposeGround .
ex:Machinery aia:classifiedOnGround ex:GroundMachine .
ex:GroundMachine a aia:AnnexIGround .
ex:Chatbot aia:classifiedOnGround ex:GroundChat .
ex:GroundChat a aia:PurposeGround .
ex:Formatter aia:classifiedOnGround ex:GroundFormat .
ex:GroundFormat a aia:DerogatedAnnexIIIGround , aia:PurposeGround .
"""))
check(not e9, "rule + data is consistent", detail="; ".join(e9[:2]))
for subj, cls, exp, label in [
    (EX.Recruitment, AIACT.HighRiskAISystem, True, "Annex III -> eu-aiact:HighRiskAISystem (CQ1 ASK, imported class)"),
    (EX.Recruitment, AIA.HighRiskByGround,  True, "Annex III -> aia:HighRiskByGround"),
    (EX.Machinery,   AIACT.HighRiskAISystem, True, "Annex I   -> eu-aiact:HighRiskAISystem"),
    (EX.Chatbot,     AIACT.HighRiskAISystem, False, "purpose ground ONLY -> NOT high-risk (sufficient-only)"),
    (EX.Formatter,   AIACT.HighRiskAISystem, False, "Art. 6(3)-derogated Annex III ground -> NOT high-risk"),
]:
    check(((subj, RDF.type, cls) in g9) == exp, label)
for label, data in [("Role + Obligation", "ex:B a aia:Role , aia:Obligation ."),
                    ("ground both Annex III and derogated under Art. 6(3)",
                     "ex:G a aia:AnnexIIIGround , aia:DerogatedAnnexIIIGround ."),
                    ("ground typed as a Role", "ex:G a aia:Role . ex:S aia:classifiedOnGround ex:G .")]:
    _, en = expand(load(imports=[("airo.ttl","turtle")], extra=data))
    check(en, f"NEGATIVE control caught: {label}")

# ═══════════════════════════════════════════════════════════════════════
section("Worked example")
EXF = os.path.join(ONT, "aia-example.ttl")
check(os.path.exists(EXF), "ontology/aia-example.ttl exists")
exg = rdflib.Graph(); exg.parse(EXF, format="turtle")
EXAMPLE_IRI = rdflib.URIRef("https://w3id.org/aia-ont/example")
check((EXAMPLE_IRI, OWL.imports, rdflib.URIRef("https://w3id.org/aia-ont")) in exg,
      "the example imports the core, and is not imported BY it")
check(rdflib.URIRef("https://w3id.org/aia-ont/example") not in
      set(local.objects(None, OWL.imports)),
      "aia-ont.ttl does not import the example: the core stays free of the fixture")
cat = open(os.path.join(ONT, "catalog-v001.xml")).read()
check('name="https://w3id.org/aia-ont/example"' in cat,
      "catalog-v001.xml maps the example's IRI, so it opens offline in Protege")

SYSTEMS = {
    "ExampleRecruitmentScreeningSystem":            AIACT.RiskLevelHigh,
    "ExampleMedicalImagingTriageSoftware":             AIACT.RiskLevelHigh,
    "ExampleWorkforceAnalyticsSystem":              AIACT.RiskLevelHigh,
    "ExampleCustomerServiceChatbot":                AIACT.RiskLevelTransparencyRequired,
    "ExampleWorkplaceEmotionRecognitionSystem":     AIACT.RiskLevelProhibited,
    "ExampleSpamFilter":                            AIACT.RiskLevelMinimal,
    "ExampleCVFormattingTool":                      AIACT.RiskLevelMinimal,
}
bad = [k for k in SYSTEMS if (AIA[k], RDF.type, AIRO.AISystem) not in exg]
check(not bad, f"all {len(SYSTEMS)} example systems are airo:AISystem, not a local system class",
      detail=str(bad))
bad = [k for k, t in SYSTEMS.items() if (AIA[k], AIA.hasRiskCategory, t) not in exg]
check(not bad, "every system carries the risk tier intended for it", detail=str(bad))
bad = [k for k in SYSTEMS if len(list(exg.objects(AIA[k], AIA.hasRiskCategory))) != 1]
check(not bad, "and exactly one tier each", detail=str(bad))
# Decision 2 in ../reports/STATUS.md is only DEMONSTRATED if all four tiers are instantiated.
TIERS = {AIACT.RiskLevelProhibited, AIACT.RiskLevelHigh,
         AIACT.RiskLevelTransparencyRequired, AIACT.RiskLevelMinimal}
used = set(exg.objects(None, AIA.hasRiskCategory))
check(used == TIERS,
      f"all four risk tiers are instantiated, including Art. 50's (decision 2): {len(used)}")
# No system may be typed with a eu-aiact Annex class: that would satisfy CQ1's ASK
# by re-assertion and the entailment would test nothing.
preclassified = [k for k in SYSTEMS
                 if any(str(o).startswith(str(AIACT)) for o in exg.objects(AIA[k], RDF.type))]
check(not preclassified,
      "no system is pre-typed with a eu-aiact class, so CQ1's ASK tests the rule",
      detail=str(preclassified))

g10, e10 = expand(load(example=True))
check(not e10, "core + worked example + all four imports is CONSISTENT",
      detail="; ".join(e10[:2]))
# The rule must fire on exactly the three systems with an Annex ground, and no others.
EXPECT_HIGH = {"ExampleRecruitmentScreeningSystem", "ExampleMedicalImagingTriageSoftware",
               "ExampleWorkforceAnalyticsSystem"}
for k in SYSTEMS:
    got = (AIA[k], RDF.type, AIACT.HighRiskAISystem) in g10
    check(got == (k in EXPECT_HIGH),
          f"{k:44} entailed eu-aiact:HighRiskAISystem = {got}")
check((AIA.ExampleCustomerServiceChatbot, RDF.type, AIA.HighRiskByGround) not in g10,
      "NEGATIVE control in the DATA: the purpose-only system is not high-risk")
check((AIA.ExampleCVFormattingTool, RDF.type, AIA.HighRiskByGround) not in g10
      and (AIA.g_cvformat_annexIII_4a_derogated, RDF.type, AIA.DerogatedAnnexIIIGround) in exg,
      "NEGATIVE control in the DATA: the Art. 6(3)-derogated Annex III system is not high-risk")

# The dual-role actor: one actor, one system, two concurrent role assignments.
rows = list(g10.query("""PREFIX aia: <https://w3id.org/aia-ont#>
  SELECT ?actor ?sys (COUNT(DISTINCT ?role) AS ?n) WHERE {
    ?a a aia:RoleAssignment ; aia:heldBy ?actor ; aia:concernsSystem ?sys ; aia:hasRole ?role }
  GROUP BY ?actor ?sys HAVING (COUNT(DISTINCT ?role) > 1)"""))
check(len(rows) == 4,
      f"four actors hold MORE THAN ONE role for one system -- one per Art. 25(1) "
      f"limb, plus Recital 83's distributor/importer (got {len(rows)})")
nb = [r for r in rows if r[0] == AIA.ExampleActorNorthBoroughCouncil]
check(len(nb) == 1 and int(nb[0][2]) == 2,
      "North Borough Council holds exactly two roles for the recruitment system")
# and the roles it holds are Provider and Deployer, which is what CQ3 returns twice
held = {o for a in g10.subjects(AIA.heldBy, AIA.ExampleActorNorthBoroughCouncil)
        for o in g10.objects(a, AIA.hasRole)}
check(held == {AIA.Provider, AIA.Deployer},
      f"and they are Provider and Deployer: {sorted(str(h).split('#')[-1] for h in held)}")
# An actor must never be typed as a role -- the error the reification prevents
badtype = [a for a in set(exg.subjects(RDF.type, AIRO.AIOperator))
           if (a, RDF.type, AIA.Role) in g10]
check(not badtype, "no actor is inferred to be an aia:Role", detail=str(badtype))

# All three limbs of Art. 25(1), from three different prior roles.
RR = ["rr_recruitment_northborough", "rr_medical_rhine", "rr_workforce_peoplemetrics"]
bad = [r for r in RR if (AIA[r], RDF.type, AIA.RoleReassignment) not in exg]
check(not bad, "all three Art. 25(1) reassignments are present", detail=str(bad))
conds = set(exg.objects(None, AIA.triggeredBy))
check(len(conds) == 3, f"three distinct reassignment conditions are used (got {len(conds)})")
fromroles = {o for r in RR for a in exg.objects(AIA[r], AIA.promotes)
             for o in exg.objects(a, AIA.hasRole)}
check(fromroles == {AIA.Deployer, AIA.Importer, AIA.Distributor},
      f"promoted from deployer, importer and distributor: "
      f"{sorted(str(f).split('#')[-1] for f in fromroles)}")
# aia:promotes must NOT end the prior assignment; aia:terminates must end a provider's
terminated = set(exg.objects(None, AIA.terminates))
promoted   = set(exg.objects(None, AIA.promotes))
check(not (terminated & promoted),
      "no assignment is both promoted and terminated: the asymmetry holds in the data")
bad = [t for t in terminated if (t, AIA.hasRole, AIA.Provider) not in exg]
check(not bad, "every terminated assignment is a PROVIDER assignment (Art. 25(2))",
      detail=str(bad))
# Art. 25(1)(c) is a reassignment condition AND a classification ground at once.
C = AIA.rc_art25_1_c_purpose_modification
check((C, RDF.type, AIA.ReassignmentCondition) in exg
      and (C, RDF.type, AIA.AnnexIIIGround) in exg,
      "Art. 25(1)(c) is typed both ReassignmentCondition and AnnexIIIGround")
check((C, RDF.type, AIA.ClassificationGround) in g10,
      "and entails aia:ClassificationGround, which is in the disjointness axiom -- "
      "consistent only because ReassignmentCondition was deliberately left out of it")
check((AIA.ExampleWorkforceAnalyticsSystem, AIA.classifiedOnGround, C) in exg
      and (AIA.rr_workforce_peoplemetrics, AIA.triggeredBy, C) in exg,
      "and it is used in BOTH positions, which is what makes the omission earn its keep")

# Every reified node is complete. OWL cannot object to a partial one -- that is
# check-shapes.py's job -- but a partial one silently drops rows from CQ3 and CQ4.
for cls, props, label in [
    (AIA.RoleAssignment, [AIA.concernsSystem, AIA.hasRole, AIA.heldBy], "role assignment"),
    (AIA.RoleReassignment, [AIA.concernsSystem, AIA.promotes, AIA.establishes,
                            AIA.triggeredBy, AIA.statedIn], "reassignment"),
    (AIA.OversightAssignment, [AIA.oversees, AIA.assignedTo], "oversight assignment"),
    (AIA.ConformityAssessmentRoute, [AIA.appliesToObligation, AIA.statedIn], "route"),
]:
    nodes = set(exg.subjects(RDF.type, cls))
    bad = [n for n in nodes for pr in props if not list(exg.objects(n, pr))]
    check(nodes and not bad,
          f"all {len(nodes)} example {label}s carry every argument they need",
          detail=str(bad))
# Every example individual is labelled: the specification asks for annotation.
inds = {s for s in exg.subjects(RDF.type, OWL.NamedIndividual)}
bad = [i for i in inds if not list(exg.objects(i, rdflib.URIRef(
    "http://www.w3.org/2004/02/skos/core#prefLabel")))]
check(inds and not bad, f"all {len(inds)} example individuals carry a skos:prefLabel",
      detail=str(bad))
bad = [i for i in inds if not list(exg.objects(i, SKOSDEF))]
check(not bad, "and a skos:definition", detail=str(bad))
# CQ3's target system must be high-risk, or CQ3 returns nothing at all
check((AIA.ExampleRecruitmentScreeningSystem, AIA.hasRiskCategory, AIACT.RiskLevelHigh) in exg,
      "CQ3's VALUES system is at RiskLevelHigh, which its first pattern requires")

# ═══════════════════════════════════════════════════════════════════════
section("Article 25(2) — terminated role assignments")
# The axioms. aia:terminatedBy must add a DIRECTION and no fact: inverseOf and
# nothing else, or it becomes a second place the termination can be recorded and
# the two can disagree.
check((AIA.terminatedBy, OWL.inverseOf, AIA.terminates) in local,
      "aia:terminatedBy is declared owl:inverseOf aia:terminates")
check(not list(local.objects(None, AIA.terminatedBy)),
      "and NOTHING asserts it: every use is entailed from aia:terminates")
check((AIA.TerminatedRoleAssignment, RDFS.subClassOf, AIA.RoleAssignment) in local,
      "aia:TerminatedRoleAssignment is a subclass of aia:RoleAssignment")
check(list(local.objects(AIA.TerminatedRoleAssignment, OWL.equivalentClass)),
      "and is DEFINED, not primitive -- membership is entailed, never asserted")
check(not list(local.triples((None, RDF.type, AIA.TerminatedRoleAssignment))),
      "no individual is asserted to be one, in the core")
check(not list(exg.triples((None, RDF.type, AIA.TerminatedRoleAssignment))),
      "nor in the worked example: the fixture records the EVENT and nothing else")
# The Act supplies no dates, so no date property may creep in on the back of this.
datep = [pr for pr in local.subjects(RDF.type, OWL.DatatypeProperty)
         if str(pr).startswith(str(AIA))]
check(not datep,
      f"no datatype property was minted for a validity interval, which the Act "
      f"does not supply: {datep}")

# The entailment, over the worked example.
TERM_EXPECTED = {"ra_recruitment_talentflow_provider", "ra_medical_helvetia_provider"}
got = {str(x).split("#")[-1] for x in g10.subjects(RDF.type, AIA.TerminatedRoleAssignment)}
check(got == TERM_EXPECTED,
      f"exactly the two terminated assignments are entailed aia:TerminatedRoleAssignment: "
      f"{sorted(got)}")
check((AIA.ra_recruitment_talentflow_provider, AIA.terminatedBy,
       AIA.rr_recruitment_northborough) in g10,
      "the inverse triple is entailed, so the fact is reachable FROM the assignment")
# Terminated is not deleted: the assignment keeps every argument, because the
# residual duties of Art. 25(2) hang off it.
for pr in (AIA.concernsSystem, AIA.hasRole, AIA.heldBy):
    check(list(exg.objects(AIA.ra_recruitment_talentflow_provider, pr)),
          f"the terminated assignment retains {str(pr).split('#')[-1]} (terminated != deleted)")
# The promoted assignment must NOT be swept up by this.
check((AIA.ra_recruitment_northborough_deployer, RDF.type,
       AIA.TerminatedRoleAssignment) not in g10,
      "NEGATIVE control: the PROMOTED deployer assignment is not terminated -- "
      "Art. 25(1) does not end the prior role")
check((AIA.ra_recruitment_northborough_provider, RDF.type,
       AIA.TerminatedRoleAssignment) not in g10,
      "NEGATIVE control: the newly established provider assignment is not terminated")

# CQ3 must now exclude it, and the exclusion must be entailment-driven: over
# asserted triples the filter removes nothing, which is why the query says so.
cq3 = open(os.path.join(ROOT, "queries", "cq3-actor-obligations.rq")).read()
check("TerminatedRoleAssignment" in cq3,
      "CQ3 cites aia:TerminatedRoleAssignment rather than restating the rule")
rows_inf = len(list(g10.query(cq3)))
plain = load(example=True)
rows_ass = len(list(plain.query(cq3)))
check(rows_ass == 35 and rows_inf == 27,
      f"CQ3 returns 35 rows asserted and 27 inferred -- the 12 duties Art. 25(2) "
      f"ended are replaced by its 4 residual ones (got {rows_ass} / {rows_inf})")
tf = [r for r in g10.query(cq3) if "TalentFlow" in str(r[0])]
tf_duties = {str(r[3]).split("#")[-1] for r in tf}
check(tf_duties == {"ob_art25_2_cooperate", "ob_art25_2_a", "ob_art25_2_b", "ob_art25_2_c"},
      f"TalentFlow, no longer the provider, returns ONLY its four Art. 25(2) residual "
      f"duties: {sorted(tf_duties)}")
check(all(r[2] is not None for r in tf),
      "and every TalentFlow row is marked as ended by Art. 25(2)")
actors = {str(r[0]) for r in g10.query(cq3)}
check(any("North Borough" in a for a in actors),
      "while the dual-role actor still returns, once per role")

# The residual duties must never reach a LIVE provider: aia:borneOnTermination is
# deliberately not a subproperty of aia:borneBy.
RESID = ["ob_art25_2_cooperate", "ob_art25_2_a", "ob_art25_2_b", "ob_art25_2_c"]
bad = [x for x in RESID if (AIA[x], AIA.borneOnTermination, AIA.Provider) not in local]
check(not bad, "the four Art. 25(2) residual duties are borne on termination of the provider role",
      detail=str(bad))
bad = [x for x in RESID if list(g10.objects(AIA[x], AIA.borneBy))]
check(not bad, "and NONE is entailed aia:borneBy any role, so no live provider bears them",
      detail=str(bad))
nb_rows = [r for r in g10.query(cq3) if "North Borough" in str(r[0])]
check(not any(str(r[3]).split("#")[-1] in RESID for r in nb_rows),
      "NEGATIVE control: the NEW provider is not returned with the initial provider's duties")
cq4 = open(os.path.join(ROOT, "queries", "cq4-role-reassignment.rq")).read()
cq4_rows = list(g10.query(cq4))
ended = {str(r.initialProviderLabel): str(r.initialProviderDuties) for r in cq4_rows
         if r.initialProviderLabel is not None}
check(len(ended) == 2 and all(d.count(";") == 3 for d in ended.values()),
      f"CQ4 reports the four residual duties for each of the two initial providers: "
      f"{sorted(ended)}")

print(f"\n{'='*72}\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
