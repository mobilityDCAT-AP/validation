from pathlib import Path
from pyshacl import validate
from rdflib import Graph

BASE_DIR = Path.cwd()
DATA_ROOT = BASE_DIR / "data"
SHACL_DIR = BASE_DIR / "shacl"

# Get all TTL files to validate
ttl_files = list(DATA_ROOT.rglob("*.ttl"))
print(f"Found {len(ttl_files)} TTL files")

# Merge all SHACL files into one graph
shacl_graph = Graph()
for sh_file in SHACL_DIR.glob("*.ttl"):
    shacl_graph.parse(str(sh_file), format="turtle")
    print("Loaded SHACL file:", sh_file.name)

print("\n--- STARTING VALIDATION ---")

for data_file in ttl_files:
    print("\n========================================")
    print("\nValidating:", data_file.relative_to(DATA_ROOT))

    conforms, _, report_text = validate(
        data_graph=str(data_file),
        shacl_graph=shacl_graph,  # <-- pass merged rdflib.Graph
        inference="rdfs",
        debug=False
    )

    print(" → Conforms:", conforms)
    if not conforms:
        print("---- Validation Report ----")
        print(report_text)
    else:
        print("No violations found.")

print("\n--- VALIDATION FINISHED ---")
