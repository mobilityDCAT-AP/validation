#!/usr/bin/env python3
"""Validation suite runner for positives/negatives expected outcomes."""
import argparse
from datetime import datetime
from pathlib import Path

from graph_loader import discover_rdf_files
from shacl_loader import load_shacl
from validate import load_vocab_graph
from validator import validate_multiple_files


def expected_conforms_for_path(file_path: Path):
    """Infer expected conformance from path names."""
    lowered_parts = {part.lower() for part in file_path.parts}
    if 'negatives' in lowered_parts or 'negative' in lowered_parts:
        return False
    if 'positives' in lowered_parts or 'positive' in lowered_parts:
        return True
    return None


def write_suite_report(report_file, data_root, entries, errors):
    """Write a full suite report including expectations and mismatches."""
    report_file.parent.mkdir(parents=True, exist_ok=True)

    passes = [e for e in entries if e['passed']]
    fails = [e for e in entries if not e['passed']]
    unclassified = [e for e in entries if e['expected'] is None]

    lines = []
    lines.append("MOBILITYDCAT-AP VALIDATION SUITE REPORT")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Data root: {data_root}")
    lines.append(
        f"Total: {len(entries)}  Pass: {len(passes)}  Fail: {len(fails)}  Unclassified: {len(unclassified)}  Errors: {len(errors)}"
    )
    lines.append("")

    lines.append("LOAD ERRORS")
    lines.append("-" * 80)
    if errors:
        for error in errors:
            lines.append(str(error))
    else:
        lines.append("None")
    lines.append("")

    lines.append("FAIL DETAILS")
    lines.append("-" * 80)
    if fails:
        for entry in fails:
            rel_path = entry['result'].file_path.relative_to(data_root)
            expected_label = 'conforms' if entry['expected'] else 'violates'
            actual_label = 'conforms' if entry['result'].conforms else 'violates'
            lines.append(f"FILE: {rel_path}")
            lines.append(f"EXPECTED: {expected_label}")
            lines.append(f"ACTUAL: {actual_label}")
            violations = entry['result'].get_violations()
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

    lines.append("UNCLASSIFIED FILES")
    lines.append("-" * 80)
    if unclassified:
        for entry in unclassified:
            rel_path = entry['result'].file_path.relative_to(data_root)
            lines.append(str(rel_path))
    else:
        lines.append("None")

    report_file.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Run validation suites using positives/negatives expected outcomes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/validate_suite.py --data sample_data/mobility --shacl shacl/
  uv run scripts/validate_suite.py --data sample_data --shacl shacl/ --max-files-report 100
        """,
    )

    parser.add_argument('--data', type=Path, required=True, help='Suite data file or directory')
    parser.add_argument('--shacl', type=Path, default=Path('shacl'), help='Path to SHACL file or directory')
    parser.add_argument(
        '--vocab',
        type=Path,
        default=Path('sample_data/vocabularies'),
        help='Path to vocabulary stub directory (default: sample_data/vocabularies/)'
    )
    parser.add_argument('--timeout', type=float, default=0, help='Per-file validation timeout in seconds (0 disables timeout)')
    parser.add_argument('--progress', action='store_true', default=False, help='Enable per-file progress output')
    parser.add_argument(
        '--max-files-report',
        type=int,
        default=50,
        help='Maximum number of pass/fail files to print per section (0 means unlimited)'
    )
    parser.add_argument(
        '--report-file',
        type=Path,
        default=Path('logs/validation-suite-report.txt'),
        help='Path to write full suite report'
    )

    args = parser.parse_args()

    print("Loading SHACL shapes...")
    try:
        shacl_graph, shacl_files = load_shacl(args.shacl)
        print(f"✓ Loaded {len(shacl_files)} SHACL file(s)\n")
    except Exception as exc:
        print(f"❌ Error loading SHACL: {exc}")
        raise SystemExit(1)

    vocab_graph = load_vocab_graph(args.vocab)

    if args.data.is_file():
        rdf_files = [args.data]
        data_root = args.data.parent
    elif args.data.is_dir():
        rdf_files = discover_rdf_files(args.data)
        data_root = args.data
    else:
        print(f"❌ Data path not found: {args.data}")
        raise SystemExit(1)

    if not rdf_files:
        print(f"❌ No RDF files found in {args.data}")
        raise SystemExit(1)

    print(f"Found {len(rdf_files)} file(s)\n")

    def progress_printer(file_path, index, total):
        if args.progress:
            rel_path = file_path.relative_to(data_root)
            print(f"[{index:>3}/{total}] Validating {rel_path}")

    results, errors = validate_multiple_files(
        rdf_files,
        shacl_graph,
        extra_graph=vocab_graph,
        timeout_seconds=args.timeout,
        progress_callback=progress_printer if args.progress else None,
    )

    entries = []
    for result in results:
        expected = expected_conforms_for_path(result.file_path)
        passed = expected is not None and result.conforms == expected
        entries.append({'result': result, 'expected': expected, 'passed': passed})

    passes = [e for e in entries if e['passed']]
    fails = [e for e in entries if not e['passed'] and e['expected'] is not None]
    unclassified = [e for e in entries if e['expected'] is None]

    if passes:
        print("=" * 80)
        print("PASS")
        print("=" * 80)
        to_print = passes[:args.max_files_report] if args.max_files_report and args.max_files_report > 0 else passes
        for entry in to_print:
            rel_path = entry['result'].file_path.relative_to(data_root)
            print(f"✓ {rel_path}")
        if len(passes) > len(to_print):
            print(f"... omitted {len(passes) - len(to_print)} additional pass file(s). Use --max-files-report to adjust.")
        print()

    if fails:
        print("=" * 80)
        print("FAIL")
        print("=" * 80)
        to_print = fails[:args.max_files_report] if args.max_files_report and args.max_files_report > 0 else fails
        for entry in to_print:
            rel_path = entry['result'].file_path.relative_to(data_root)
            expected_label = 'conforms' if entry['expected'] else 'violates'
            actual_label = 'conforms' if entry['result'].conforms else 'violates'
            print(f"✗ {rel_path} (expected: {expected_label}, actual: {actual_label})")
        if len(fails) > len(to_print):
            print(f"... omitted {len(fails) - len(to_print)} additional fail file(s). Use --max-files-report to adjust.")
        print()

    if unclassified:
        print("=" * 80)
        print("UNCLASSIFIED")
        print("=" * 80)
        to_print = unclassified[:args.max_files_report] if args.max_files_report and args.max_files_report > 0 else unclassified
        for entry in to_print:
            rel_path = entry['result'].file_path.relative_to(data_root)
            print(f"! {rel_path} (expected outcome not inferable; use positives/negatives folder names)")
        if len(unclassified) > len(to_print):
            print(f"... omitted {len(unclassified) - len(to_print)} additional unclassified file(s). Use --max-files-report to adjust.")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total:        {len(entries)} file(s)")
    print(f"✓ Pass:       {len(passes)}")
    print(f"✗ Fail:       {len(fails)}")
    print(f"! Unclassified: {len(unclassified)}")
    if errors:
        print(f"❌ Errors:     {len(errors)}")
    print("=" * 80)

    write_suite_report(args.report_file, data_root, entries, errors)
    print(f"Detailed report: {args.report_file}\n")

    success = len(fails) == 0 and len(unclassified) == 0 and len(errors) == 0
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    main()
