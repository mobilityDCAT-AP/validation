# mobilityDCAT-AP SHACL Validation

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![SHACL](https://img.shields.io/badge/SHACL-W3C-orange.svg)](https://www.w3.org/TR/shacl/)
[![RDF](https://img.shields.io/badge/RDF-Turtle%20|%20JSON--LD%20|%20XML-green.svg)](https://www.w3.org/RDF/)
[![mobilityDCAT-AP](https://img.shields.io/badge/mobilityDCAT--AP-1.1.0-purple.svg)](https://w3id.org/mobilitydcat-ap/releases/1.1.0/)
[![DCAT-AP](https://img.shields.io/badge/DCAT--AP-3.0.1-blue.svg)](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)

SHACL validation toolkit for [mobilityDCAT-AP](https://github.com/mobilityDCAT-AP/mobilityDCAT-AP) metadata compliance.

## Documentation

**[Full Validation Guide](docs/README.md)** - Installation, Docker setup, usage examples, test categories, and Issue 

## Quick Install
```bash
git clone https://github.com/mobilityDCAT-AP/validation.git
cd validation
uv sync  # or: docker build -t mobilitydcat-validator .
```

## CLI Usage

Two separate workflows are available:
- Universal validation: `scripts/validate.py`
- Suite testing (positives/negatives expected outcomes): `scripts/validate_suite.py`

Run validator help:
```bash
uv run scripts/validate.py --help
```

Run suite tester help:
```bash
uv run scripts/validate_suite.py --help
```

Minimal default run:
```bash
uv run scripts/validate.py
```

Defaults used in minimal run:
- `--data data/`
- `--shacl shacl/`
- `--vocab sample_data/vocabularies/`
- `--report-file logs/validation-report.txt`

Example (directory validation):
```bash
uv run scripts/validate.py \
	--data sample_data/ \
	--shacl shacl/
```

Optional tuning example:
```bash
uv run scripts/validate.py \
	--data sample_data/ \
	--shacl shacl/ \
	--timeout 30 \
	--max-files-report 50
```

Report behavior:
- Terminal output is compact by default for large runs.
- Full violation details are always written to a report file.
- Default report path (if `--report-file` is omitted): `logs/validation-report.txt`.

Supported RDF serializations:
- The validator accepts multiple RDF serializations in one run, including `.ttl`, `.rdf`, `.xml`, `.nt`, `.n3`, `.jsonld`, `.json`, `.trig`, and `.nq`.
- You can point `--data` to a directory containing mixed formats; all supported files are discovered and validated.

Common options:
- `--data`: Input RDF file or directory
- `--shacl`: SHACL file or directory
- `--vocab`: Vocabulary stubs directory
- `--verbose` / `--no-verbose`: Show or hide detailed violations in terminal
- `--progress` / `--no-progress`: Per-file progress while validating directories
- `--timeout`: Per-file validation timeout in seconds (`0` disables timeout)
- `--max-files-report`: Safety option to cap VALID/INVALID terminal output on large runs (`50` default, `0` means unlimited)
- `--report-file`: Path for full detailed validation report

Suite testing workflow:
- Use `scripts/validate_suite.py` for `positives`/`negatives` test folders.
- Expected outcomes are inferred from directory names (`positives` => should conform, `negatives` => should violate).
- Files outside those folder patterns are reported as unclassified and fail the suite run.

Why `--vocab` is important:
- Some SHACL checks rely on external controlled vocabularies being available as RDF resources at validation time.
- Typical examples are EU File Type, EU Frequency, and mobility theme terms that are referenced by URI in datasets.
- The validator loads all `.ttl` files from the `--vocab` directory and merges them into each data graph before running SHACL.
- This prevents false violations caused by missing vocabulary resources during class/range checks.
- In most cases you can use the default path; override `--vocab` only when validating against a different vocabulary source.

## Structure
```
validation/
├── scripts/validate.py       # Validation script
├── shacl/                    # SHACL shapes
├── example_datagraphs/       # Test cases
└── docs/                     # Documentation
```

## Related Projects

- **[mobilityDCAT-AP](https://github.com/mobilityDCAT-AP/mobilityDCAT-AP)** - Main specification repository
- **[mobilityDCAT-AP 1.1.0](https://w3id.org/mobilitydcat-ap/releases/1.1.0/)** - Official specification
- **[DCAT-AP 3.0.1](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)** - Base DCAT-AP standard

## Technologies

- **Python 3.11+** - Core language
- **[pyshacl](https://github.com/RDFLib/pySHACL)** - SHACL validation engine
- **[rdflib](https://github.com/RDFLib/rdflib)** - RDF graph manipulation
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager
- **Docker** - Containerized validation

## Contributing

See [docs/README.md](docs/README.md) for test case documentation and validation guide.