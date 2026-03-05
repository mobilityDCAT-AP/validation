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