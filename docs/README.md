# mobilityDCAT-AP SHACL Validation

Validation suite for mobilityDCAT-AP 1.1.0 compliance using SHACL shapes.

## Quick Start
```bash
# Install dependencies
uv sync

# Validate single file
uv run scripts/validate.py --data example_datagraphs/baseline-dcat-ap/negatives/B-N-01-missing-catalog-title.ttl --shacl shacl/

# Validate with verbose output
uv run scripts/validate.py --data example_datagraphs/mobility/negatives/M-N-01-missing-mandatory-properties-dataset.ttl --shacl shacl/ -v
```

## Run All Test Suites
```bash
# All baseline DCAT-AP tests
uv run scripts/validate.py --data example_datagraphs/baseline-dcat-ap/ --shacl shacl/

# All mobility-specific tests
uv run scripts/validate.py --data example_datagraphs/mobility/ --shacl shacl/

# All multilingual tests
uv run scripts/validate.py --data example_datagraphs/multilingual/ --shacl shacl/

# All partial graph tests
uv run scripts/validate.py --data example_datagraphs/partial_graphs/ --shacl shacl/

# All range constraint tests
uv run scripts/validate.py --data example_datagraphs/ranges/ --shacl shacl/

# All vocabulary tests
uv run scripts/validate.py --data example_datagraphs/vocabularies/ --shacl shacl/

# Run everything
uv run scripts/validate.py --data example_datagraphs/ --shacl shacl/
```

## Docker Usage

### Build Image
```bash
docker build -t mobilitydcat-validator .
```

### Validate Files
```bash
# Single file
docker run -v %cd%/example_datagraphs:/data mobilitydcat-validator \
  --data /data/baseline-dcat-ap/negatives/B-N-01-missing-catalog-title.ttl \
  --shacl /validation/shacl/

# Directory
docker run -v %cd%/example_datagraphs:/data mobilitydcat-validator \
  --data /data/baseline-dcat-ap/ \
  --shacl /validation/shacl/

# Verbose output
docker run -v %cd%/example_datagraphs:/data mobilitydcat-validator \
  --data /data/mobility/ \
  --shacl /validation/shacl/ \
  -v
```

### Using Docker Compose
```bash
# Run validation
docker-compose run validator --data /data/baseline-dcat-ap/ --shacl /validation/shacl/

# Run mobility tests
docker-compose run validator --data /data/mobility/ --shacl /validation/shacl/
```

### Platform-Specific Commands

**Linux/Mac:**
```bash
docker run -v $(pwd)/example_datagraphs:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

**Windows (CMD):**
```cmd
docker run -v %cd%/example_datagraphs:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

**Windows (PowerShell):**
```powershell
docker run -v ${PWD}/example_datagraphs:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

---

## Run Issue #160 Tests

Validate specific test cases from Issue #160:
```bash
# Test Case 1: Missing language tag detection
uv run scripts/validate.py --data example_datagraphs/multilingual/negatives/L-N-01-missing-language-tag.ttl --shacl shacl/ -v

# Test Case 2: Language mismatch (NOT YET DETECTED)
uv run scripts/validate.py --data example_datagraphs/multilingual/negatives/L-N-02-mismatched-language-tags.ttl --shacl shacl/ -v

# Test Case 3: Empty multilingual field detection
uv run scripts/validate.py --data example_datagraphs/multilingual/negatives/L-N-03-empty-multilingual-field.ttl --shacl shacl/ -v

# Test Case 4: Invalid language tag detection
uv run scripts/validate.py --data example_datagraphs/multilingual/negatives/L-N-04-invalid-language-tag.ttl --shacl shacl/ -v

# Distribution without accessURL
uv run scripts/validate.py --data example_datagraphs/partial_graphs/negatives/P-N-02-distribution-without-access-url.ttl --shacl shacl/ -v
```

## Expected Results

✓ **Negative tests (N-*)**: Should detect violations  
⚠️ **Positive tests (P-*)**: Currently incomplete - missing mandatory properties  
✗ **Baseline DCAT-AP positives (B-P-*)**: Expected to fail (missing mobilityDCAT-AP mandatory properties like mobilityTheme, spatial, accrualPeriodicity)

## Test Categories

- **baseline-dcat-ap/** - Tests base DCAT-AP compliance (7 negative, 4 positive)
- **mobility/** - Tests mobility-specific properties (5 negative, 4 positive)
- **multilingual/** - Tests language tag validation (4 negative, 2 positive)
- **partial_graphs/** - Tests individual class validation
- **ranges/** - Tests type/class constraints
- **vocabularies/** - Tests controlled vocabulary URIs
- **regression/** - Tests previously fixed bugs

## Issue #160 Status

### ✓ Solved
- Language tag presence validation
- Empty field detection
- Invalid language tag detection (e.g., @english instead of @en)
- Distribution mandatory property validation
- mobilityDataStandard validation
- No duplicate error messages for Distribution properties

### ✗ Remaining
- **Language mismatch detection** (title@en vs description@es) - Current shapes detect OTHER violations but NOT the specific language inconsistency. Requires SPARQL constraint.

## SHACL Files

- `shacl/mobilitydcat-ap-shacl.ttl` - Main validation rules (cardinality, datatypes, mandatory properties)
- `shacl/mobilitydcat-ap-shacl-ranges.ttl` - Type/class constraints (sh:class validations)

## Specification Alignment

Shapes are aligned with:
- mobilityDCAT-AP 1.1.0 (https://w3id.org/mobilitydcat-ap/releases/1.1.0/)
- DCAT-AP 3.0.1 (https://semiceu.github.io/DCAT-AP/releases/3.0.1/)

### Recent Fixes
- Fixed Catalog `dct:identifier` cardinality: changed from mandatory (1..*) to optional (0..1) per spec §4.4.3