# mobilityDCAT-AP SHACL Validation

Validates RDF data against DCAT-AP 3.0 and mobilityDCAT-AP 1.1.0.

## Setup

```bash
git clone https://github.com/mobilityDCAT-AP/validation.git
cd validation
uv sync
```

## Run Validation

```bash
uv run scripts/validate.py
```

## Structure

```
validation/
├── scripts/validate.py    # Validation script
├── data/
│   ├── positive/          # Tests that should pass
│   └── negative/          # Tests that should fail
└── shacl/                 # SHACL shape files
```

## Add Tests

1. Put SHACL shapes in `shacl/`
2. Put test `.ttl` files in `data/positive/` or `data/negative/`
3. Run `uv run scripts/validate.py`