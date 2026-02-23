# DCAT-AP / mobilityDCAT-AP Test Suite

This test suite validates conformance against:
- DCAT-AP 3.0
- mobilityDCAT-AP 1.1.0

This repository contains a Python-based validation framework for testing SHACL shapes against DCAT-AP and mobilityDCAT-AP example datasets.

Validation is executed locally using **pySHACL** instead of SHACL Playground to ensure reliable resolution of multiple SHACL files and `owl:imports`. This guarantees consistent and reproducible validation behaviour across all test cases.

---

## Purpose

The goal of this repository is to:

- Validate DCAT-AP and mobilityDCAT-AP example data against SHACL constraints  
- Organise structured positive and negative test cases  
- Detect breaking changes through regression testing  
- Ensure stable constraint behaviour across specification updates  

---

## Project Structure

```text
testing_SHACL/
│
├── data/
│   ├── baseline-dcat-ap/
│   ├── mobility/
│   ├── multilingual/
│   ├── ranges/
│   ├── vocabularies/
│   ├── partial-graphs/
│   └── regression/
│
├── shacl/
│   ├── dcat-ap-3.0.shacl.ttl
│   └── mobilitydcat-ap-1.1.0.shacl.ttl
│  
│
└── validate_per_data_file.py

```

### `data/`

Contains all validation test cases, grouped by category.

Categories include:

- **baseline-dcat-ap** – Core DCAT-AP validation cases  
- **mobility** – mobilityDCAT-AP extension cases  
- **ranges** – Datatype and range validation tests  
- **multilingual** – Language tag and multilingual constraints  
- **vocabularies** – Controlled vocabulary enforcement  
- **partial-graphs** – Structural and edge-case tests  
- **regression** – Previously validated behaviour that must remain stable  

Each category may contain:

- `positive/` – Files that are expected to conform  
- `negative/` – Files that are expected to fail validation  

---

### `shacl/`

Contains all SHACL shape files used during validation.  
All files in this folder are loaded and merged into a single validation graph before execution.

---

### `validate_per_data_file.py`

Python script that:

1. Recursively scans the `data/` directory for Turtle (`.ttl`) files  
2. Loads and merges all SHACL files from the `shacl/` directory  
3. Validates each data file individually using pySHACL  
4. Prints validation results directly to the console  

No documents or reports are generated. Output is console-based to support automation and CI usage.

---

## ⚙️ How Validation Works

1. All `.ttl` files under `data/` are discovered recursively.
2. All SHACL files under `shacl/` are loaded into a single validation graph.
3. Each data file is validated using `pySHACL`.
4. Results are printed to the console.

Validation uses:
- RDFS inference
- Multiple SHACL files
- Console-only output (no documents generated)

---


## Running the Tests

### 1. Install Dependencies

Install the required Python packages:

- `pyshacl`  
- `rdflib`  

You can install them using:

```bash
pip install pyshacl rdflib
```

### 2. Execute the Validation Script

From the root directory of the repository, run:

```bash
python validate_per_data_file.py
```
The script will:

Print the number of discovered test files

List the loaded SHACL files

Display PASS/FAIL results per file

Optionally print detailed validation reports (if debug mode is enabled)

### 3. Example Output

**Passing case:**
PASS → baseline-dcat-ap/positive/B-P-01-minimal.ttl

**Failing case:**
FAIL → baseline-dcat-ap/negative/B-N-01-missing-title.ttl

### Regression Testing

The regression/ folder protects previously validated behaviour.

**regression/positive/** → must always pass

**regression/negative/** → must always fail

If a regression test changes status, this indicates:

A breaking change (previously valid data is now invalid)

A weakened constraint (previously invalid data now passes)

Regression tests safeguard specification stability.
