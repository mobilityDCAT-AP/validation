# mobilityDCAT-AP SHACL Validation

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-enabled-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![SHACL](https://img.shields.io/badge/SHACL-W3C-orange.svg)](https://www.w3.org/TR/shacl/)
[![RDF](https://img.shields.io/badge/RDF-Turtle%20|%20JSON--LD%20|%20XML-green.svg)](https://www.w3.org/RDF/)
[![mobilityDCAT-AP](https://img.shields.io/badge/mobilityDCAT--AP-1.1.0-purple.svg)](https://w3id.org/mobilitydcat-ap/releases/1.1.0/)


Validates RDF data against mobilityDCAT-AP 1.1.0 and DCAT-AP 3.0.1 specifications.

## Quick Setup
```bash
git clone https://github.com/mobilityDCAT-AP/validation.git
cd validation
uv sync
```

## Quick Start
```bash
# Validate a file
uv run scripts/validate.py --data example_datagraphs/baseline-dcat-ap/negatives/B-N-01-missing-catalog-title.ttl --shacl shacl/

# Run all tests
uv run scripts/validate.py --data example_datagraphs/ --shacl shacl/
```

## Docker
```bash
docker build -t mobilitydcat-validator .
docker run -v %cd%/example_datagraphs:/data mobilitydcat-validator --data /data/baseline-dcat-ap/ --shacl /validation/shacl/
```

**See [docs/README.md](docs/README.md) for full Docker guide**

## Documentation

**[Full Validation Guide](docs/README.md)** - Detailed instructions, Docker guide, test categories, and Issue #160 status

## Structure
```
validation/
├── scripts/validate.py       # Validation script
├── shacl/                    # SHACL shapes
├── example_datagraphs/       # Test cases
└── docs/                     # Documentation
```

## Related Projects

- **[mobilityDCAT-AP Specification](https://github.com/mobilityDCAT-AP/mobilityDCAT-AP)** - Main specification repository
- **[mobilityDCAT-AP 1.1.0](https://w3id.org/mobilitydcat-ap/releases/1.1.0/)** - Official specification
- **[DCAT-AP 3.0.1](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)** - Base DCAT-AP standard

## Technologies

- **Python 3.11+** - Core language
- **[pyshacl](https://github.com/RDFLib/pySHACL)** - SHACL validation engine
- **[rdflib](https://github.com/RDFLib/rdflib)** - RDF graph manipulation
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager
- **Docker** - Containerized validation

## Contributing

See [docs/README.md](docs/README.md) for detailed test case documentation and Issue #160 status.