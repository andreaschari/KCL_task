#!/usr/bin/env bash
# Runs HermiT (the jar Protege 5.6.9 bundles) over the ontology's import closure
# via the OWL API, with the reasoner configuration Protege uses. Prints
# consistency, unsatisfiable classes, the CQ1 entailment and the entailed
# aia:TerminatedRoleAssignment individuals.
#
# Usage: scripts/run-hermit.sh [entry-file, default aia-example.ttl]
#
# Requires a Protege 5.6.9 install (PROTEGE_HOME, default ~/.local/share/Protege-5.6.9),
# javac/java on PATH, and network access on first run only, to fetch
# dk.brics.automaton (a HermiT runtime dependency Protege does not vendor
# separately from its own jar).
set -euo pipefail

PROTEGE_HOME="${PROTEGE_HOME:-$HOME/.local/share/Protege-5.6.9}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ONT_DIR="$SCRIPT_DIR/../ontology"
BUILD_DIR="$SCRIPT_DIR/.hermit-build"

if [ ! -d "$PROTEGE_HOME" ]; then
  echo "PROTEGE_HOME not found: $PROTEGE_HOME" >&2
  exit 1
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

OWLAPI_JAR="$PROTEGE_HOME/bundles/owlapi-osgidistribution.jar"
HERMIT_JAR=$(ls "$PROTEGE_HOME"/plugins/org.semanticweb.hermit-*.jar | head -1)

# owlapi-osgidistribution.jar is an OSGi bundle: its runtime deps are nested jars
# under lib/, referenced only via Bundle-ClassPath, which a plain `java -cp` won't
# honour. Extract them once.
if [ ! -d lib ]; then
  unzip -oq "$OWLAPI_JAR" 'lib/*'
fi

# HermiT's datatype layer needs dk.brics.automaton for regex-pattern facets
# (xsd:pattern etc.); Protege does not ship it as a separate jar.
if [ ! -f automaton.jar ]; then
  curl -sSL -o automaton.jar \
    "https://repo1.maven.org/maven2/dk/brics/automaton/automaton/1.11-8/automaton-1.11-8.jar"
fi

CP="$OWLAPI_JAR:$HERMIT_JAR:automaton.jar"
for j in lib/*.jar; do CP="$CP:$j"; done
for j in guava slf4j-api logback-classic logback-core jul-to-slf4j log4j-over-slf4j \
         org.apache.servicemix.bundles.javax-inject jaxb-api jaxb-core jaxb-impl jsr305; do
  CP="$CP:$PROTEGE_HOME/bundles/$j.jar"
done

if [ ! -f RunHermit.class ] || [ "$SCRIPT_DIR/RunHermit.java" -nt RunHermit.class ]; then
  javac -cp "$CP" -d . "$SCRIPT_DIR/RunHermit.java"
fi

java -cp ".:$CP" RunHermit "$ONT_DIR" "${1:-aia-example.ttl}"
