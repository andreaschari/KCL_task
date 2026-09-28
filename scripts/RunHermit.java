import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.util.SimpleIRIMapper;
import org.semanticweb.HermiT.Configuration;
import org.semanticweb.HermiT.ReasonerFactory;

import java.io.File;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Loads the ontology through the same OWL API + catalog mapping Protege uses, then
 * runs the HermiT reasoner bundled with Protege (org.semanticweb.hermit-*.jar) over
 * the full import closure, with ignoreUnsupportedDatatypes=true — the setting
 * Protege's own org.semanticweb.HermiT.ProtegeReasonerFactory uses (the plain OWL
 * API default, SimpleConfiguration, leaves this false and throws on ELI's xsd:date
 * property ranges; Protege's "Start reasoner" does not, because of this flag).
 * See scripts/run-hermit.sh for how to build the classpath.
 *
 * Usage: java RunHermit <ontology-dir> [entry-file, default aia-example.ttl]
 */
public class RunHermit {
    public static void main(String[] args) throws Exception {
        File ontDir = new File(args[0]);
        File coreFile = new File(ontDir, "aia-ont.ttl");
        File entryFile = args.length > 1 ? new File(ontDir, args[1]) : new File(ontDir, "aia-example.ttl");

        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

        map(manager, "https://w3id.org/dpv/legal/eu/aiact/owl#", new File(ontDir, "imports/eu-aiact-owl.ttl"));
        map(manager, "https://w3id.org/airo", new File(ontDir, "imports/airo.ttl"));
        map(manager, "http://data.europa.eu/eli/ontology#", new File(ontDir, "imports/eli.owl"));
        map(manager, "http://data.europa.eu/eli/ontology", new File(ontDir, "imports/eli.owl"));
        map(manager, "http://www.w3.org/2004/02/skos/core", new File(ontDir, "imports/skos.rdf"));
        map(manager, "https://w3id.org/aia-ont", coreFile);

        System.out.println("Loading " + entryFile + " ...");
        OWLOntology ontology = manager.loadOntologyFromOntologyDocument(entryFile);

        System.out.println("Loaded ontology: " + ontology.getOntologyID());
        System.out.println("Imports closure size (ontologies): " + ontology.getImportsClosure().size());
        long axiomCount = ontology.getImportsClosure().stream().mapToLong(OWLOntology::getAxiomCount).sum();
        System.out.println("Axiom count across closure: " + axiomCount);

        System.out.println();
        System.out.println("=== Starting HermiT reasoner ===");
        long t0 = System.currentTimeMillis();
        ReasonerFactory factory = new ReasonerFactory();
        // Protege's own HermiT plugin (org.semanticweb.HermiT.ProtegeReasonerFactory)
        // sets this true; the plain OWL API default (SimpleConfiguration) leaves it
        // false, which is why a raw ReasonerFactory.createReasoner(ontology, new
        // SimpleConfiguration()) call throws on ELI's xsd:date ranges where Protege's
        // own "Start reasoner" does not.
        Configuration config = new Configuration();
        config.ignoreUnsupportedDatatypes = true;
        OWLReasoner reasoner = factory.createReasoner(ontology, config);

        boolean consistent = reasoner.isConsistent();
        long t1 = System.currentTimeMillis();
        System.out.println("Consistent: " + consistent + "  (" + (t1 - t0) + " ms)");

        reasoner.precomputeInferences(InferenceType.CLASS_HIERARCHY, InferenceType.CLASS_ASSERTIONS, InferenceType.OBJECT_PROPERTY_HIERARCHY);
        long t2 = System.currentTimeMillis();
        System.out.println("Precomputed class hierarchy + class assertions + object property hierarchy (" + (t2 - t1) + " ms)");

        Node<OWLClass> bottom = reasoner.getUnsatisfiableClasses();
        Set<OWLClass> unsat = bottom.getEntities().stream()
                .filter(c -> !c.isOWLNothing())
                .collect(Collectors.toSet());
        System.out.println();
        System.out.println("Unsatisfiable classes (excluding owl:Nothing itself): " + unsat.size());
        for (OWLClass c : unsat) {
            System.out.println("  UNSATISFIABLE: " + c.getIRI());
        }

        OWLDataFactory df = manager.getOWLDataFactory();

        System.out.println();
        System.out.println("=== CQ1 entailment check (classification rule) ===");
        OWLClass highRiskAISystem = df.getOWLClass(IRI.create("https://w3id.org/dpv/legal/eu/aiact/owl#HighRiskAISystem"));
        OWLIndividual exampleSystem = df.getOWLNamedIndividual(IRI.create("https://w3id.org/aia-ont#ExampleRecruitmentScreeningSystem"));
        Set<OWLNamedIndividual> highRiskInstances = reasoner.getInstances(highRiskAISystem, false).getFlattened();
        System.out.println("ExampleRecruitmentScreeningSystem entailed a HighRiskAISystem: " + highRiskInstances.contains(exampleSystem));
        System.out.println("Total individuals entailed HighRiskAISystem: " + highRiskInstances.size());

        System.out.println();
        System.out.println("=== Terminated role assignment entailment (decision 5) ===");
        OWLClass terminatedRA = df.getOWLClass(IRI.create("https://w3id.org/aia-ont#TerminatedRoleAssignment"));
        Set<OWLNamedIndividual> terminated = reasoner.getInstances(terminatedRA, false).getFlattened();
        System.out.println("Individuals entailed aia:TerminatedRoleAssignment: " + terminated.size());
        terminated.forEach(i -> System.out.println("  " + i.getIRI().getShortForm()));

        System.out.println();
        System.out.println("=== Reasoner identification ===");
        System.out.println("Reasoner name: " + reasoner.getReasonerName());
        System.out.println("Reasoner version: " + reasoner.getReasonerVersion());

        reasoner.dispose();
        System.out.println();
        System.out.println("DONE");
    }

    private static void map(OWLOntologyManager manager, String iri, File file) {
        manager.getIRIMappers().add(new SimpleIRIMapper(IRI.create(iri), IRI.create(file)));
    }
}
