#!/usr/bin/env python3
"""
Test generator for GitHub Issue #160
Run from: data/issue-160/

Usage:
    python generate_tests.py
    
This will create:
    positive/*.ttl  (valid test cases)
    negative/*.ttl  (failing test cases)
"""

from pathlib import Path

# Test cases from issue #160
POSITIVE_TESTS = {
    "dataset-complete-valid.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Bus Schedule Dataset"@en ;
    dct:description "Complete bus schedule for city transport"@en ;
    dct:publisher <http://example.org/publisher/1> ;
    dct:spatial <http://example.org/spatial/bonn> ;
    dcat:distribution <http://example.org/distribution/1> ;
    dct:accrualPeriodicity <http://publications.europa.eu/resource/authority/frequency/DAILY> ;
    mobilitydcatap:mobilityTheme <https://w3id.org/mobilitydcat-ap/mobility-theme/road> .

<http://example.org/publisher/1> a foaf:Agent ;
    foaf:name "City Transport Authority" .

<http://example.org/spatial/bonn> a dct:Location .

<http://example.org/distribution/1> a dcat:Distribution ;
    dcat:accessURL <http://example.org/data/bus-schedule> ;
    dct:format <http://publications.europa.eu/resource/authority/file-type/JSON> ;
    dct:rights <http://example.org/rights/1> ;
    mobilitydcatap:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .

<http://example.org/rights/1> a dct:RightsStatement .
""",

    "catalogue-complete-valid.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/catalogue/1> a dcat:Catalog ;
    dct:title "Mobility Data Portal"@en ;
    dct:description "A portal providing datasets about mobility"@en ;
    foaf:homepage <http://example.org/> ;
    dct:spatial <http://example.org/spatial/germany> ;
    dct:identifier "cat-mobility-001" ;
    dcat:dataset <http://example.org/dataset/1> ;
    dcat:record <http://example.org/record/1> .

<http://example.org/record/1> a dcat:CatalogRecord ;
    foaf:primaryTopic <http://example.org/dataset/1> ;
    dct:language <http://publications.europa.eu/resource/authority/language/ENG> ;
    dct:created "2025-01-01"^^xsd:date .

<http://example.org/dataset/1> a dcat:Dataset .
<http://example.org/spatial/germany> a dct:Location .
""",
}

NEGATIVE_TESTS = {
    "dataset-missing-distribution.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .

# Issue #160 Case 1: Missing Distribution
<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Bus Schedule"@en ;
    dct:description "Bus schedule data"@en ;
    dct:publisher <http://example.org/publisher/1> ;
    dct:spatial <http://example.org/spatial/1> ;
    dct:accrualPeriodicity <http://publications.europa.eu/resource/authority/frequency/DAILY> ;
    mobilitydcatap:mobilityTheme <https://w3id.org/mobilitydcat-ap/mobility-theme/road> .
    # MISSING: dcat:distribution

<http://example.org/publisher/1> a foaf:Agent ;
    foaf:name "Publisher" .
<http://example.org/spatial/1> a dct:Location .
""",

    "catalogue-missing-language-tag.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Issue #160 Case 2: Missing Language Tag
<http://example.org/catalogue/1> a dcat:Catalog ;
    dct:title "Mobility Data Portal" ;
    # MISSING: @en language tag
    dct:description "A portal providing datasets about mobility"@en ;
    foaf:homepage <http://example.org/> ;
    dct:spatial <http://example.org/spatial/1> ;
    dct:identifier "cat-001" ;
    dcat:dataset <http://example.org/dataset/1> ;
    dcat:record <http://example.org/record/1> .

<http://example.org/record/1> a dcat:CatalogRecord ;
    foaf:primaryTopic <http://example.org/dataset/1> ;
    dct:language <http://publications.europa.eu/resource/authority/language/ENG> ;
    dct:created "2025-01-01"^^xsd:date .

<http://example.org/dataset/1> a dcat:Dataset .
<http://example.org/spatial/1> a dct:Location .
""",

    "catalogue-empty-description.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Issue #160 Case 4: Empty literal
<http://example.org/catalogue/1> a dcat:Catalog ;
    dct:title "Mobility Data Portal"@en ;
    dct:description ""@en ;
    # INVALID: Empty literal
    foaf:homepage <http://example.org/> ;
    dct:spatial <http://example.org/spatial/1> ;
    dct:identifier "cat-001" ;
    dcat:dataset <http://example.org/dataset/1> ;
    dcat:record <http://example.org/record/1> .

<http://example.org/record/1> a dcat:CatalogRecord ;
    foaf:primaryTopic <http://example.org/dataset/1> ;
    dct:language <http://publications.europa.eu/resource/authority/language/ENG> ;
    dct:created "2025-01-01"^^xsd:date .

<http://example.org/dataset/1> a dcat:Dataset .
<http://example.org/spatial/1> a dct:Location .
""",

    "catalogue-invalid-language-tag.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Issue #160 Case 5: Invalid language tag
<http://example.org/catalogue/1> a dcat:Catalog ;
    dct:title "Mobility Data Portal"@english ;
    # INVALID: @english instead of @en
    dct:description "A portal"@en ;
    foaf:homepage <http://example.org/> ;
    dct:spatial <http://example.org/spatial/1> ;
    dct:identifier "cat-001" ;
    dcat:dataset <http://example.org/dataset/1> ;
    dcat:record <http://example.org/record/1> .

<http://example.org/record/1> a dcat:CatalogRecord ;
    foaf:primaryTopic <http://example.org/dataset/1> ;
    dct:language <http://publications.europa.eu/resource/authority/language/ENG> ;
    dct:created "2025-01-01"^^xsd:date .

<http://example.org/dataset/1> a dcat:Dataset .
<http://example.org/spatial/1> a dct:Location .
""",

    "dataset-missing-mandatory-props.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .

# Issue #160 Case 6: Missing mandatory properties
<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Incomplete Dataset"@en .
    # MISSING: description, distribution, accrualPeriodicity, mobilityTheme, spatial, publisher
""",

    "distribution-invalid-format-uri.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .

# Issue #160 Case 9: Invalid format URI
<http://example.org/distribution/1> a dcat:Distribution ;
    dcat:accessURL <https://example.org/data/train_schedule.zip> ;
    dct:format <https://example.com/formats/ZIP> ;
    # INVALID: Not from http://publications.europa.eu/resource/authority/file-type/*
    dct:rights <http://publications.europa.eu/resource/authority/access-right/PUBLIC> ;
    mobilitydcatap:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .
""",

    "distribution-missing-access-url.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .

# Missing accessURL
<http://example.org/distribution/1> a dcat:Distribution ;
    dct:format <http://publications.europa.eu/resource/authority/file-type/JSON> ;
    dct:rights <http://example.org/rights/1> ;
    mobilitydcatap:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .
    # MISSING: dcat:accessURL

<http://example.org/rights/1> a dct:RightsStatement .
""",

    "catalogue-missing-homepage.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Missing homepage
<http://example.org/catalogue/1> a dcat:Catalog ;
    dct:title "Catalogue"@en ;
    dct:description "A catalogue"@en ;
    dct:spatial <http://example.org/spatial/1> ;
    dct:identifier "cat-001" ;
    dcat:dataset <http://example.org/dataset/1> ;
    dcat:record <http://example.org/record/1> .
    # MISSING: foaf:homepage

<http://example.org/record/1> a dcat:CatalogRecord ;
    foaf:primaryTopic <http://example.org/dataset/1> ;
    dct:language <http://publications.europa.eu/resource/authority/language/ENG> ;
    dct:created "2025-01-01"^^xsd:date .

<http://example.org/dataset/1> a dcat:Dataset .
<http://example.org/spatial/1> a dct:Location .
""",
}

def main():
    """Generate test files in current directory"""
    
    # Create positive tests
    pos_dir = Path("positive")
    pos_dir.mkdir(exist_ok=True)
    
    for filename, content in POSITIVE_TESTS.items():
        filepath = pos_dir / filename
        filepath.write_text(content)
        print(f"✓ {filepath}")
    
    # Create negative tests
    neg_dir = Path("negative")
    neg_dir.mkdir(exist_ok=True)
    
    for filename, content in NEGATIVE_TESTS.items():
        filepath = neg_dir / filename
        filepath.write_text(content)
        print(f"✓ {filepath}")
    
    print(f"\n✓ Generated {len(POSITIVE_TESTS)} positive and {len(NEGATIVE_TESTS)} negative tests")
    print("\nTo validate:")
    print("  cd ../..")
    print("  uv run scripts/validate.py --data data/issue-160/ --shacl shacl/ --verbose")

if __name__ == "__main__":
    main()
