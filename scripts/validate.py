#!/usr/bin/env python3
"""Main validation script - orchestrates all layers"""

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
        print("\n--- Validation Report ---")
        print(result.report_text)
        print("--- End Report ---\n")
    
    return result.passed()

def validate_directory(data_dir, shacl_graph, verbose=False):
    """Validate all files in a directory"""
    rdf_files = discover_rdf_files(data_dir)
    
    if not rdf_files:
        print(f"❌ No RDF files found in {data_dir}")
        return False
    
    print(f"Found {len(rdf_files)} file(s)\n")
    
    results, errors = validate_multiple_files(rdf_files, shacl_graph)
    
    # Show loading errors first
    if errors:
        print("❌ Loading Errors:")
        for error in errors:
            print(f"  {error}")
        print()
    
    # Show validation results
    passed = 0
    failed = 0
    
    for result in results:
        rel_path = result.file_path.relative_to(data_dir)
        print(f"{result.status():8} {rel_path}")
        
        if result.passed():
            passed += 1
        else:
            failed += 1
        
        if verbose and not result.conforms:
            print("\n--- Validation Report ---")
            print(result.report_text)
            print("--- End Report ---\n")
    
    print(f"\n✓ Passed: {passed}  ✗ Failed: {failed}")
    if errors:
        print(f"⚠ Load errors: {len(errors)}")
    
    return failed == 0 and len(errors) == 0

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

  # Show validation details
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
        help='Show detailed validation reports'
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
