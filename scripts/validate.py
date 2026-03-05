#!/usr/bin/env python3
"""Main validation script - clean, detailed output"""

import argparse
from pathlib import Path

from graph_loader import discover_rdf_files
from shacl_loader import load_shacl
from validator import validate_file, validate_multiple_files

def validate_single_file(data_file, shacl_graph, verbose=False):
    """Validate a single file"""
    result, error = validate_file(data_file, shacl_graph)
    
    if error:
        print(f"❌ ERROR {error}")
        return False
    
    print(f"{result.status():8} {data_file.name}")
    
    if verbose and not result.conforms:
        violations = result.get_violations()
        if violations:
            print(f"\n  Violations found: {len(violations)}")
            for i, v in enumerate(violations, 1):
                print(f"  [{i}] Property: {v.get('property', 'unknown')}")
                print(f"      Constraint: {v.get('constraint', 'unknown')}")
                if 'message' in v:
                    print(f"      Message: {v['message'][:100]}")
            print()
    
    return result.passed()

def validate_directory(data_dir, shacl_graph, verbose=False):
    """Validate all files in a directory"""
    rdf_files = discover_rdf_files(data_dir)
    
    if not rdf_files:
        print(f"❌ No RDF files found in {data_dir}")
        return False
    
    print(f"Found {len(rdf_files)} file(s)\n")
    
    results, errors = validate_multiple_files(rdf_files, shacl_graph)
    
    # Print errors first
    if errors:
        print("=" * 80)
        print("LOAD ERRORS")
        print("=" * 80)
        for error in errors:
            print(f"❌ {error}")
        print()
    
    # Group results
    passed = [r for r in results if r.passed()]
    failed = [r for r in results if not r.passed()]
    
    # Show passed tests
    if passed:
        print("=" * 80)
        print("PASSED")
        print("=" * 80)
        for result in passed:
            rel_path = result.file_path.relative_to(data_dir)
            violations = result.get_violations()
            if violations:
                print(f"✓ {str(rel_path):<45} Detected {len(violations)} violation(s)")
            else:
                print(f"✓ {str(rel_path):<45} Valid")
        print()
    
    # Show failed tests with details
    if failed:
        print("=" * 80)
        print("FAILED")
        print("=" * 80)
        for result in failed:
            rel_path = result.file_path.relative_to(data_dir)
            print(f"\n✗ {rel_path}")
            
            if result.is_positive_test():
                violations = result.get_violations()
                if violations:
                    print(f"  Expected: Valid")
                    print(f"  Got:      {len(violations)} violation(s) found\n")
                    for i, v in enumerate(violations, 1):
                        prop = v.get('property', 'unknown')
                        constraint = v.get('constraint', 'Unknown')
                        print(f"  [{i}] Property: {prop}")
                        print(f"      Constraint: {constraint}")
                        if 'message' in v:
                            msg = v['message'][:80]  # Truncate long messages
                            print(f"      Message: {msg}")
                        print()
            else:
                print(f"  Expected: Invalid (should have violations)")
                print(f"  Got:      Valid (no violations detected)\n")
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total = len(results)
    passed_count = len(passed)
    failed_count = len(failed)
    error_count = len(errors)
    
    print(f"Total:    {total} file(s)")
    print(f"✓ Passed: {passed_count}")
    print(f"✗ Failed: {failed_count}")
    if error_count:
        print(f"❌ Errors: {error_count}")
    print("=" * 80)
    
    return failed_count == 0 and error_count == 0

def main():
    parser = argparse.ArgumentParser(
        description="Validate RDF data against SHACL shapes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file (any RDF format)
  uv run scripts/validate.py --data my-data.ttl --shacl shacl/
  uv run scripts/validate.py --data my-data.rdf --shacl shacl/
  uv run scripts/validate.py --data my-data.jsonld --shacl shacl/

  # Validate directory
  uv run scripts/validate.py --data data/ --shacl shacl/

  # Show verbose details
  uv run scripts/validate.py --data data/ --shacl shacl/ --verbose

  # Use defaults
  uv run scripts/validate.py

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
    
    # Validate
    success = False
    
    if args.data.is_file():
        # Single file
        success = validate_single_file(args.data, shacl_graph, args.verbose)
    elif args.data.is_dir():
        # Directory
        success = validate_directory(args.data, shacl_graph, args.verbose)
    else:
        print(f"❌ Data path not found: {args.data}")
        exit(1)
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
