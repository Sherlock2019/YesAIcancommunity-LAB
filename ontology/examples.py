from .registry import OntologyRegistry


def build_example_graph(registry: OntologyRegistry) -> OntologyRegistry:
    hr = registry.create("Department", name="HR")
    infra = registry.create("Department", name="Cloud Infra")
    finance = registry.create("Department", name="Finance")

    john = registry.create("Human", name="John Lennon")
    john.link("department", hr)
    john.link("skills", registry.create("Skill", name="AI Strategy"))

    challenge = registry.create("Challenge", title="Automate Billing Reconciliation")
    solution = registry.create("Solution", description="AI Ledger Matcher")
    challenge.link("solution", solution)

    project = registry.create("Project", title="Billing AI MVP")
    project.link("solution", solution)

    agent = registry.create("Agent", name="Credit Appraisal Agent")
    project.link("agent", agent)

    dataset = registry.create("Dataset", name="billing_ledger.csv")
    agent.link("dataset", dataset)

    system = registry.create("System", name="ERP-X")
    dataset.link("system", system)

    return registry
