# mobilityDCAT-AP SHACL Validation

Validates RDF data against DCAT-AP 3.0 and mobilityDCAT-AP 1.1.0 shapes.

## Quick Start

```bash
# Clone
git clone https://github.com/mobilityDCAT-AP/validation.git
cd validation

# Install dependencies (using uv)
uv sync

# Run validation
uv python run validate_per_data_file.py
```

## Structure

```
validation/
├── data/           # Test cases (.ttl files)
│   ├── positive/   # Should pass validation
│   └── negative/   # Should fail validation
├── shacl/          # SHACL shape files
└── validate_per_data_file.py
```

## Adding Tests

1. Put SHACL shapes in `shacl/`
2. Put test files in `data/positive/` or `data/negative/`
3. Run `uv run validate_per_data_file.py`

## Requirements

- Python 3.11+
- pyshacl
- rdflib