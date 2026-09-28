#!/usr/bin/env bash
# Reproduce the vendored import set under ontology/imports/.
#
# ontology/catalog-v001.xml redirects each owl:imports IRI to these files, so the
# ontology loads offline. http://data.europa.eu/eli/ontology does not
# content-negotiate to the ELI document, which is served only from the
# op.europa.eu path below.
#
# Run from the repository root:  ./scripts/fetch-imports.sh
# Then check with:              (cd ontology && python3 ../scripts/validate-imports.py)
#
# Expected ontology IRI, version and size of each file (two IRIs end in '#'):
#   eu-aiact-owl.ttl  https://w3id.org/dpv/legal/eu/aiact/owl#   2.3    2173 triples
#   airo.ttl          https://w3id.org/airo                      1.0     558 triples
#   eli.owl           http://data.europa.eu/eli/ontology#        1.4    1505 triples
#   skos.rdf          http://www.w3.org/2004/02/skos/core        —       252 triples

set -euo pipefail
cd "$(dirname "$0")/.."
DEST=ontology/imports
mkdir -p "$DEST"

fetch () {  # fetch <url> <outfile>
  echo "==> $2"
  curl -fsSL --retry 3 "$1" -o "$DEST/$2" \
    || { echo "    FAILED: $1" >&2; return 1; }
}

# --- DPV EU AI Act extension, OWL serialisation (v2.3) --------------------
# Ontology IRI: https://w3id.org/dpv/legal/eu/aiact/owl#   (trailing # included)
# The URL below was VERIFIED on 2026-09-26 and replaces the unverified guess
# carried in the reconstruction, which 404'd. Resolution notes:
#   - https://w3id.org/dpv/legal/eu/aiact/owl  redirects to w3c-cg.github.io but
#     404s there; the w3id redirect does not reach a serialisation.
#   - the version number is a PATH SEGMENT ('/2.3/'), ahead of 'legal/', so the
#     published path is not a suffix of the ontology IRI.
# Retrieved bytes are md5 70e797903d7ca7288380995d236c9e82 (132,429 B, 2,173
# triples), identical from the W3C source repo mirror:
#   https://raw.githubusercontent.com/w3c/dpv/master/2.3/legal/eu/aiact/eu-aiact-owl.ttl
# The file needed is the /owl# serialisation, not the base one, which contains
# zero owl:Class declarations.
fetch "https://w3c-cg.github.io/dpv/2.3/legal/eu/aiact/eu-aiact-owl.ttl" eu-aiact-owl.ttl

# --- AIRO 1.0 -------------------------------------------------------------
# Ontology IRI: https://w3id.org/airo   (no trailing #)
fetch "https://raw.githubusercontent.com/DelaramGlp/airo/main/airo.ttl" airo.ttl

# --- ELI 1.4, canonical Publications Office download ----------------------
# Ontology IRI: http://data.europa.eu/eli/ontology#   (trailing # included)
# The trailing slash on this URL is required.
fetch "https://op.europa.eu/documents/3938058/11669184/eli.owl/" eli.owl

# --- SKOS Core ------------------------------------------------------------
# Ontology IRI: http://www.w3.org/2004/02/skos/core   (no trailing #)
# The one import not re-parsed during the build pass: w3.org was unreachable
# from both the shell and the browser. Re-parsed 2026-09-26, which closes that
# gap and CORRECTS the inherited profile. Actual: 252 triples, 4 named classes
# (Concept, ConceptScheme, Collection, OrderedCollection) plus one anonymous
# one, 3 class-level owl:disjointWith axioms — and 17 owl:ObjectProperty
# declarations, not "no object properties" as the earlier pass recorded. The
# class and disjointness counts held; the property count did not.
fetch "https://www.w3.org/2009/08/skos-reference/skos.rdf" skos.rdf

echo
echo "Fetched into $DEST:"
ls -l "$DEST"
echo
echo "Next: verify declared ontology IRIs, then load ontology/aia-ont.ttl in"
echo "Protégé and run HermiT. The catalog redirects all four imports locally."
