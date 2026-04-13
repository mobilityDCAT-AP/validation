#!/usr/bin/env python3
"""Main validation script - clean, detailed output"""
import argparse
from pathlib import Path
from rdflib import Graph
from graph_loader import discover_rdf_files
from shacl_loader import load_shacl
from validator import validate_file, validate_multiple_files


def load_vocab_graph(vocab_dir: Path) -> Graph:
    """Load vocabulary stub files into a single graph"""
    vocab_graph = Graph()
    if vocab_dir.exists():
        vocab_files = sorted(vocab_dir.glob('*.ttl'))
        for vocab_file in vocab_files:
            vocab_graph.parse(vocab_file, format='turtle')
        if vocab_files:
            print(f"✓ Loaded {len(vocab_files)} vocabulary stub file(s)\n")
    return vocab_graph


def validate_single_file(data_file, shacl_graph, verbose=False, vocab_graph=None):
    """Validate a single file and report results"""
    result, error = validate_file(data_file, shacl_graph, extra_graph=vocab_graph)

    if error:
        print(f"❌ {error}")
        return False

    status = "✓ Valid" if result.conforms else "✗ Invalid"
    print(f"{status:12} {data_file.name}")

    # Show violations if invalid
    if not result.conforms:
        violations = result.get_violations()
        if violations:
            print(f"             Violations: {len(violations)}")
            if verbose:
                for i, v in enumerate(violations, 1):
                    print(f"             [{i}] Property: {v.get('property', 'unknown')}")
                    print(f"                 Constraint: {v.get('constraint', 'unknown')}")
                    if 'message' in v:
                        msg = v['message'][:80]
                        print(f"                 Message: {msg}")
            print()

    return True  # Return True if file was successfully validated (regardless of result)


def validate_directory(data_dir, shacl_graph, verbose=False, vocab_graph=None):
    """Validate all files in a directory and report results"""
    rdf_files = discover_rdf_files(data_dir)

    if not rdf_files:
        print(f"❌ No RDF files found in {data_dir}")
        return False

    print(f"Found {len(rdf_files)} file(s)\n")

    results, errors = validate_multiple_files(rdf_files, shacl_graph, extra_graph=vocab_graph)

    # Print errors first
    if errors:
        print("=" * 80)
        print("LOAD ERRORS")
        print("=" * 80)
        for error in errors:
            print(f"❌ {error}")
        print()

    # Group results by conformance
    valid = [r for r in results if r.conforms]
    invalid = [r for r in results if not r.conforms]

    # Show valid files
    if valid:
        print("=" * 80)
        print("VALID")
        print("=" * 80)
        for result in valid:
            rel_path = result.file_path.relative_to(data_dir)
            print(f"✓ {str(rel_path)}")
        print()

    # Show invalid files with violation details
    if invalid:
        print("=" * 80)
        print("INVALID")
        print("=" * 80)
        for result in invalid:
            rel_path = result.file_path.relative_to(data_dir)
            violations = result.get_violations()
            print(f"\n✗ {rel_path}")
            if violations:
                print(f"  Violations: {len(violations)}")
                if verbose:
                    for i, v in enumerate(violations, 1):
                        prop = v.get('property', 'unknown')
                        constraint = v.get('constraint', 'Unknown')
                        print(f"  [{i}] Property: {prop}")
                        print(f"      Constraint: {constraint}")
                        if 'message' in v:
                            msg = v['message'][:80]
                            print(f"      Message: {msg}")
                print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = len(results)
    valid_count = len(valid)
    invalid_count = len(invalid)
    error_count = len(errors)

    print(f"Total:     {total} file(s)")
    print(f"✓ Valid:   {valid_count}")
    print(f"✗ Invalid: {invalid_count}")
    if error_count:
        print(f"❌ Errors:  {error_count}")
    print("=" * 80)

    return error_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate RDF data against SHACL shapes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/validate.py --data my-data.ttl --shacl shacl/
  uv run scripts/validate.py --data data/ --shacl shacl/
  uv run scripts/validate.py --data data/ --shacl shacl/ --verbose
  uv run scripts/validate.py --data data/ --shacl shacl/ --vocab sample_data/vocabularies/
Supported formats: .ttl, .rdf, .xml, .nt, .n3, .jsonld, .json, .trig, .nq
        """
    )

    parser.add_argument(
        '--data',
        type=Path,
        default=Path('data'),
        help='Path to data file or directory (default: data/)'
    )

    parser.add_argument(
        '--shacl',
        type=Path,
        default=Path('shacl'),
        help='Path to SHACL file or directory (default: shacl/)'
    )

    parser.add_argument(
        '--vocab',
        type=Path,
        default=Path('sample_data/vocabularies'),
        help='Path to vocabulary stub directory (default: sample_data/vocabularies/)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed violation information'
    )

    args = parser.parse_args()

    # Load SHACL shapes
    print("Loading SHACL shapes...")
    try:
        shacl_graph, shacl_files = load_shacl(args.shacl)
        print(f"✓ Loaded {len(shacl_files)} SHACL file(s)\n")
    except Exception as e:
        print(f"❌ Error loading SHACL: {e}")
        exit(1)

    # Load vocabulary stubs
    vocab_graph = load_vocab_graph(args.vocab)

    # Validate
    success = False

    if args.data.is_file():
        success = validate_single_file(args.data, shacl_graph, args.verbose, vocab_graph)
    elif args.data.is_dir():
        success = validate_directory(args.data, shacl_graph, args.verbose, vocab_graph)
    else:
        print(f"❌ Data path not found: {args.data}")
        exit(1)

    exit(0 if success else 1)


if __name__ == "__main__":
    main()