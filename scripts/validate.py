#!/usr/bin/env python3
"""Main validation script - clean, detailed output"""
import argparse
from datetime import datetime
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


def write_detailed_report(report_file, data_root, results, errors):
    """Write full validation errors and violations to a report file."""
    report_file.parent.mkdir(parents=True, exist_ok=True)

    valid = [r for r in results if r.conforms]
    invalid = [r for r in results if not r.conforms]

    lines = []
    lines.append("MOBILITYDCAT-AP VALIDATION REPORT")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Data root: {data_root}")
    lines.append(f"Total: {len(results)}  Valid: {len(valid)}  Invalid: {len(invalid)}  Errors: {len(errors)}")
    lines.append("")

    lines.append("LOAD ERRORS")
    lines.append("-" * 80)
    if errors:
        for error in errors:
            lines.append(str(error))
    else:
        lines.append("None")
    lines.append("")

    lines.append("INVALID FILE DETAILS")
    lines.append("-" * 80)
    if invalid:
        for result in invalid:
            rel_path = result.file_path.relative_to(data_root)
            violations = result.get_violations()
            lines.append(f"FILE: {rel_path}")
            lines.append(f"VIOLATIONS: {len(violations)}")

            for i, violation in enumerate(violations, 1):
                lines.append(f"  [{i}] Property: {violation.get('property', 'unknown')}")
                lines.append(f"      Constraint: {violation.get('constraint', 'Unknown')}")
                if 'focus' in violation:
                    lines.append(f"      Focus: {violation['focus']}")
                if 'message' in violation:
                    lines.append(f"      Message: {violation['message']}")

            lines.append("")
    else:
        lines.append("None")
        lines.append("")

    report_file.write_text("\n".join(lines), encoding="utf-8")


def validate_single_file(
    data_file,
    shacl_graph,
    verbose=False,
    vocab_graph=None,
    timeout=0,
    return_details=False,
):
    """Validate a single file and report results"""
    result, error = validate_file(
        data_file,
        shacl_graph,
        extra_graph=vocab_graph,
        timeout_seconds=timeout,
    )

    if error:
        print(f"❌ {error}")
        if return_details:
            return False, None, error
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

    if return_details:
        return result.conforms, result, None

    return result.conforms


def validate_directory(
    data_dir,
    shacl_graph,
    verbose=False,
    vocab_graph=None,
    timeout=0,
    progress=False,
    max_files_report=50,
    report_file=Path('logs/validation-report.txt'),
):
    """Validate all files in a directory and report results"""
    rdf_files = discover_rdf_files(data_dir)

    if not rdf_files:
        print(f"❌ No RDF files found in {data_dir}")
        return False

    print(f"Found {len(rdf_files)} file(s)\n")

    def progress_printer(file_path, index, total):
        if progress:
            rel_path = file_path.relative_to(data_dir)
            print(f"[{index:>3}/{total}] Validating {rel_path}")

    results, errors = validate_multiple_files(
        rdf_files,
        shacl_graph,
        extra_graph=vocab_graph,
        timeout_seconds=timeout,
        progress_callback=progress_printer if progress else None,
    )

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
        valid_to_print = valid[:max_files_report] if max_files_report and max_files_report > 0 else valid
        for result in valid_to_print:
            rel_path = result.file_path.relative_to(data_dir)
            print(f"✓ {str(rel_path)}")
        if len(valid) > len(valid_to_print):
            omitted = len(valid) - len(valid_to_print)
            print(f"... omitted {omitted} additional valid file(s). Use --max-files-report to adjust.")
        print()

    # Show invalid files with violation details
    if invalid:
        print("=" * 80)
        print("INVALID")
        print("=" * 80)
        invalid_to_print = invalid[:max_files_report] if max_files_report and max_files_report > 0 else invalid
        for result in invalid_to_print:
            rel_path = result.file_path.relative_to(data_dir)
            violations = result.get_violations()
            violation_count = len(violations) if violations else 0
            print(f"✗ {rel_path} (violations: {violation_count})")
            if verbose and violations:
                for i, v in enumerate(violations, 1):
                    prop = v.get('property', 'unknown')
                    constraint = v.get('constraint', 'Unknown')
                    print(f"  [{i}] Property: {prop}")
                    print(f"      Constraint: {constraint}")
                    if 'message' in v:
                        msg = v['message'][:80]
                        print(f"      Message: {msg}")
                print()
        if len(invalid) > len(invalid_to_print):
            omitted = len(invalid) - len(invalid_to_print)
            print(f"... omitted {omitted} additional invalid file(s). Use --max-files-report to adjust.")
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

    write_detailed_report(report_file, data_dir, results, errors)
    print(f"Detailed report: {report_file}\n")

    return invalid_count == 0 and error_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate RDF data against SHACL shapes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/validate.py --data my-data.ttl --shacl shacl/
  uv run scripts/validate.py --data data/ --shacl shacl/
    uv run scripts/validate.py --data data/ --shacl shacl/ --verbose --progress
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
        default=False,
        help='Show detailed violation information (off by default for large runs)'
    )

    parser.add_argument(
        '--no-verbose',
        dest='verbose',
        action='store_false',
        help='Disable detailed violation information'
    )

    parser.add_argument(
        '--progress',
        dest='progress',
        action='store_true',
        default=False,
        help='Enable per-file progress output while validating directories'
    )

    parser.add_argument(
        '--timeout',
        type=float,
        default=0,
        help='Per-file validation timeout in seconds (0 disables timeout)'
    )

    parser.add_argument(
        '--no-progress',
        dest='progress',
        action='store_false',
        help='Disable per-file progress output while validating directories'
    )

    parser.add_argument(
        '--max-files-report',
        type=int,
        default=50,
        help='Maximum number of valid/invalid files to print per section (0 means unlimited)'
    )

    parser.add_argument(
        '--report-file',
        type=Path,
        default=Path('logs/validation-report.txt'),
        help='Path to write full error and violation details'
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
        success, single_result, single_error = validate_single_file(
            args.data,
            shacl_graph,
            args.verbose,
            vocab_graph,
            args.timeout,
            return_details=True,
        )
        # Single-file runs write a report with full details as well.
        write_detailed_report(
            args.report_file,
            args.data.parent,
            [single_result] if single_result else [],
            [single_error] if single_error else [],
        )
        print(f"Detailed report: {args.report_file}\n")
    elif args.data.is_dir():
        success = validate_directory(
            args.data,
            shacl_graph,
            args.verbose,
            vocab_graph,
            args.timeout,
            args.progress,
            args.max_files_report,
            args.report_file,
        )
    else:
        print(f"❌ Data path not found: {args.data}")
        exit(1)

    exit(0 if success else 1)


if __name__ == "__main__":
    main()