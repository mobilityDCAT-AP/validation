# mobilityDCAT-AP SHACL Validation

Validates RDF data against DCAT-AP 3.0.1 and mobilityDCAT-AP 1.1.0 specifications.

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

## Documentation

📖 **[Full Validation Guide](docs/README.md)** - Detailed instructions, test categories, and Issue #160 status

## Structure
```
validation/
├── scripts/
│   └── validate.py           # Validation script
├── shacl/
│   ├── mobilitydcat-ap-shacl.ttl        # Main validation rules
│   └── mobilitydcat-ap-shacl-ranges.ttl # Type constraints
├── example_datagraphs/
│   ├── baseline-dcat-ap/     # Base DCAT-AP tests
│   ├── mobility/             # Mobility-specific tests
│   ├── multilingual/         # Language validation tests
│   ├── partial_graphs/       # Individual class tests
│   ├── ranges/               # Type constraint tests
│   ├── vocabularies/         # Controlled vocabulary tests
│   └── regression/           # Bug regression tests
└── docs/                     # Detailed documentation
```

## Test Naming Convention

- `B-*` - Baseline DCAT-AP tests
- `M-*` - Mobility-specific tests
- `L-*` - Language/multilingual tests
- `P-*` - Partial graph tests
- `R-*` - Range constraint tests
- `V-*` - Vocabulary tests
- `RG-*` - Regression tests

Each category has:
- `*-N-*` - Negative tests (should detect violations)
- `*-P-*` - Positive tests (should pass validation)

## Specification Alignment

- [mobilityDCAT-AP 1.1.0](https://w3id.org/mobilitydcat-ap/releases/1.1.0/)
- [DCAT-AP 3.0.1](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)

## Contributing

See [docs/README.md](docs/README.md) for detailed test case documentation and Issue #160 status.