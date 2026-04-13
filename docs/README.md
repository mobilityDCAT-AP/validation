# mobilityDCAT-AP SHACL Validation

Validation suite for mobilityDCAT-AP 1.1.0 compliance using SHACL shapes.

## Quick Start
```bash
# Install dependencies
uv sync

# Validate single file
uv run scripts/validate.py --data sample_data/baseline-dcat-ap/negatives/B-N-01-missing-catalog-title.ttl --shacl shacl/

# Validate with verbose output
uv run scripts/validate.py --data sample_data/mobility/negatives/M-N-01-missing-mandatory-properties-dataset.ttl --shacl shacl/ -v
```

## CLI Options

Show all options:
```bash
uv run scripts/validate.py --help
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

Current key options:
- `--data`: Path to RDF file or directory
- `--shacl`: Path to SHACL file or directory
- `--vocab`: Path to vocabulary stubs directory (default: `sample_data/vocabularies`)
- `--verbose` / `--no-verbose`: Toggle detailed violation output in terminal
- `--progress` / `--no-progress`: Toggle per-file progress output for directory validation
- `--timeout`: Per-file timeout in seconds (`0` disables timeout)
- `--max-files-report`: Safety option to cap VALID/INVALID terminal output and keep VS Code responsive on large runs (`0` means unlimited)
- `--report-file`: Write full detailed report (default: `logs/validation-report.txt`)

Why `--vocab` is important:
- Several shapes expect terms from external controlled vocabularies to be present as RDF resources.
- Common examples include EU file types, EU frequency values, and mobility theme concepts.
- The validator reads all `.ttl` files from the `--vocab` folder and merges them into each input graph before validation.
- This helps avoid false negatives/positives caused by unresolved vocabulary resources in class/range constraints.
- Keep the default in normal runs; set a custom `--vocab` path when you need to validate against another vocabulary snapshot.

Notes:
- Terminal output is intentionally compact by default for stability on large runs.
- Full violation details are written to the report file.

Supported RDF serializations:
- Validation supports multiple RDF serializations: `.ttl`, `.rdf`, `.xml`, `.nt`, `.n3`, `.jsonld`, `.json`, `.trig`, and `.nq`.
- A single directory run can include mixed serializations; all supported files are discovered automatically.

Example with explicit report file:
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
  --max-files-report 50 \
  --report-file logs/validation-report-latest.txt
```

## Run All Test Suites
```bash
# All baseline DCAT-AP tests
uv run scripts/validate.py --data sample_data/baseline-dcat-ap/ --shacl shacl/

# All mobility-specific tests
uv run scripts/validate.py --data sample_data/mobility/ --shacl shacl/

# All multilingual tests
uv run scripts/validate.py --data sample_data/multilingual/ --shacl shacl/

# All partial graph tests
uv run scripts/validate.py --data sample_data/partial_graphs/ --shacl shacl/

# All range constraint tests
uv run scripts/validate.py --data sample_data/ranges/ --shacl shacl/

# All vocabulary tests
uv run scripts/validate.py --data sample_data/vocabularies/ --shacl shacl/

# Run everything
uv run scripts/validate.py --data sample_data/ --shacl shacl/
```

## Docker Usage

### Build Image
```bash
docker build -t mobilitydcat-validator .
```

### Validate Files
```bash
# Single file
docker run -v %cd%/sample_data:/data mobilitydcat-validator \
  --data /data/baseline-dcat-ap/negatives/B-N-01-missing-catalog-title.ttl \
  --shacl /validation/shacl/

# Directory
docker run -v %cd%/sample_data:/data mobilitydcat-validator \
  --data /data/baseline-dcat-ap/ \
  --shacl /validation/shacl/

# Verbose output
docker run -v %cd%/sample_data:/data mobilitydcat-validator \
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
docker run -v $(pwd)/sample_data:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

**Windows (CMD):**
```cmd
docker run -v %cd%/sample_data:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

**Windows (PowerShell):**
```powershell
docker run -v ${PWD}/sample_data:/data mobilitydcat-validator --data /data/ --shacl /validation/shacl/
```

---

## Run Issue #160 Tests

Validate specific test cases from Issue #160:
```bash
# Test Case 1: Missing language tag detection
uv run scripts/validate.py --data sample_data/multilingual/negatives/L-N-01-missing-language-tag.ttl --shacl shacl/ -v

# Test Case 2: Language mismatch (NOT YET DETECTED)
uv run scripts/validate.py --data sample_data/multilingual/negatives/L-N-02-mismatched-language-tags.ttl --shacl shacl/ -v

# Test Case 3: Empty multilingual field detection
uv run scripts/validate.py --data sample_data/multilingual/negatives/L-N-03-empty-multilingual-field.ttl --shacl shacl/ -v

# Test Case 4: Invalid language tag detection
uv run scripts/validate.py --data sample_data/multilingual/negatives/L-N-04-invalid-language-tag.ttl --shacl shacl/ -v

# Distribution without accessURL
uv run scripts/validate.py --data sample_data/partial_graphs/negatives/P-N-02-distribution-without-access-url.ttl --shacl shacl/ -v
```

## Expected Results

✓ **Negative tests (N-*)**: Should detect violations
⚠️ **Positive tests (P-*)**: Currently incomplete - missing mandatory properties
✗ **Baseline DCAT-AP positives (B-P-*)**: Expected to fail (missing mobilityDCAT-AP mandatory properties like mobilityTheme, spatial, accrualPeriodicity)

## Test Categories

- **baseline-dcat-ap/** - Tests base DCAT-AP compliance 
- **mobility/** - Tests mobility-specific properties
- **multilingual/** - Tests language tag validation 
- **partial_graphs/** - Tests individual class validation
- **ranges/** - Tests type/class constraints
- **vocabularies/** - Tests controlled vocabulary URIs
- **regression/** - Tests previously fixed bugs

### Remaining

- **Language mismatch detection**- Current shapes detect OTHER violations but NOT the specific language inconsistency. Requires SPARQL constraint.

## SHACL Files

> **Note:** Example test cases and documentation are being updated to align
> with the new three-file SHACL structure (shapes + ranges + MDR vocabularies).
> Updated examples will be available once
> [PR #178](https://github.com/mobilityDCAT-AP/mobilityDCAT-AP/pull/178)
> is merged in the main repository.

- `shacl/mobilitydcat-ap_1.1.0_shacl_shapes.ttl` — Basic validation (cardinality, datatypes, mandatory properties)
- `shacl/mobilitydcat-ap_1.1.0_shacl_range.ttl` — Range constraints (sh:class validations)
- `shacl/mobilitydcat-ap_1.1.0_shacl_mdr-vocabularies.shape.ttl` — Controlled vocabulary validation

## Specification Alignment

Shapes are aligned with:

- mobilityDCAT-AP 1.1.0 (https://w3id.org/mobilitydcat-ap/releases/1.1.0/)
- DCAT-AP 2.0.1 (https://semiceu.github.io/DCAT-AP/releases/2.0.1/)

### Recent Fixes

- Fixed Catalog `dct:identifier` cardinality: changed from mandatory (1..*) to optional (0..1) per spec §4.4.3