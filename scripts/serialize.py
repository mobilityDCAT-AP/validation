"""
Serialize a Turtle (.ttl) file to RDF/XML and JSON-LD.
Usage: python scripts/serialize.py <path-to-ttl>
"""
import sys
from rdflib import Graph

ttl_path = sys.argv[1] if len(sys.argv) > 1 else "mobilitydcat-ap.ttl"
base = ttl_path.replace(".ttl", "")

g = Graph()
g.parse(ttl_path, format="turtle")
g.serialize(f"{base}.xml", format="xml")
g.serialize(f"{base}.jsonld", format="json-ld", indent=2)
print(f"Generated {base}.xml and {base}.jsonld")