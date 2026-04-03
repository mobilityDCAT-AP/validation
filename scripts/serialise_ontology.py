#!/usr/bin/env python3
"""
Serialize a Turtle (.ttl) ontology file to RDF/XML.
JSON-LD is NOT auto-generated because rdflib expands all URIs
and destroys the manually crafted @context. Edit JSON-LD separately.

Usage:
  uv run scripts/serialise_ontology.py drafts/1.1.0-draft-0.1/mobilitydcat-ap_v1.1.0.ttl
"""
import sys
from pathlib import Path
from rdflib import Graph


def serialise(ttl_path: Path):
    print(f"Parsing {ttl_path}...")
    g = Graph()
    g.parse(ttl_path, format="turtle")
    print(f"  Loaded {len(g)} triples")

    # RDF/XML
    rdf_path = ttl_path.with_suffix(".rdf")
    g.serialize(rdf_path, format="xml")
    print(f"✓ Generated {rdf_path}")

    # JSON-LD — warn only
    print(f"⚠  JSON-LD ({ttl_path.with_suffix('.jsonld')}) must be maintained manually.")
    print("   rdflib expands all URIs and destroys the @context block.")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mobilitydcat-ap_v1.1.0.ttl")
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)
    serialise(path)