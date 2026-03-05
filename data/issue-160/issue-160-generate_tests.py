#!/usr/bin/env python3
"""Precise test generator for Issue #160"""
from pathlib import Path

POSITIVE_TESTS = {
    "dataset-valid.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix mdcat: <https://w3id.org/mobilitydcat-ap#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Bus Schedule"@en ;
    dct:description "Complete bus schedule"@en ;
    dct:publisher <http://example.org/publisher/1> ;
    dct:spatial <http://publications.europa.eu/resource/authority/country/DEU> ;
    dct:accrualPeriodicity <http://publications.europa.eu/resource/authority/frequency/DAILY> ;
    mdcat:mobilityTheme <https://w3id.org/mobilitydcat-ap/mobility-theme/road> ;
    dcat:distribution <http://example.org/dist/1> .

<http://example.org/publisher/1> a foaf:Agent ;
    foaf:name "Transport Authority" .

<http://example.org/dist/1> a dcat:Distribution ;
    dcat:accessURL <http://example.org/data> ;
    dct:format <http://publications.europa.eu/resource/authority/file-type/JSON> ;
    mdcat:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .

<http://publications.europa.eu/resource/authority/frequency/DAILY> a dct:Frequency .
<https://w3id.org/mobilitydcat-ap/mobility-theme/road> a skos:Concept .
<http://publications.europa.eu/resource/authority/file-type/JSON> a dct:MediaTypeOrExtent .
""",

    "catalogue-valid.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.org/cat/1> a dcat:Catalog ;
    dct:title "Mobility Portal"@en ;
    dct:description "Mobility data portal"@en ;
    foaf:homepage <http://example.org/> .
""",
}

NEGATIVE_TESTS = {
    "dataset-missing-distribution.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix mdcat: <https://w3id.org/mobilitydcat-ap#> .

<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Dataset"@en ;
    dct:description "Description"@en ;
    dct:publisher <http://example.org/pub/1> ;
    dct:spatial <http://publications.europa.eu/resource/authority/country/DEU> ;
    dct:accrualPeriodicity <http://publications.europa.eu/resource/authority/frequency/DAILY> ;
    mdcat:mobilityTheme <https://w3id.org/mobilitydcat-ap/mobility-theme/road> .

<http://example.org/pub/1> a foaf:Agent ; foaf:name "Publisher" .
""",

    "catalogue-no-language-tag.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.org/cat/1> a dcat:Catalog ;
    dct:title "Portal" ;
    dct:description "Description"@en ;
    foaf:homepage <http://example.org/> .
""",

    "catalogue-empty-description.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.org/cat/1> a dcat:Catalog ;
    dct:title "Portal"@en ;
    dct:description ""@en ;
    foaf:homepage <http://example.org/> .
""",

    "catalogue-invalid-language.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://example.org/cat/1> a dcat:Catalog ;
    dct:title "Portal"@english ;
    dct:description "Description"@en ;
    foaf:homepage <http://example.org/> .
""",

    "dataset-missing-properties.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://example.org/dataset/1> a dcat:Dataset ;
    dct:title "Dataset"@en .
""",

    "distribution-invalid-format.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mdcat: <https://w3id.org/mobilitydcat-ap#> .

<http://example.org/dist/1> a dcat:Distribution ;
    dcat:accessURL <http://example.org/data> ;
    dct:format <https://invalid.com/ZIP> ;
    mdcat:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .
""",

    "distribution-no-access-url.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mdcat: <https://w3id.org/mobilitydcat-ap#> .

<http://example.org/dist/1> a dcat:Distribution ;
    dct:format <http://publications.europa.eu/resource/authority/file-type/JSON> ;
    mdcat:mobilityDataStandard <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .
""",

    "catalogue-no-homepage.ttl": """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://example.org/cat/1> a dcat:Catalog ;
    dct:title "Portal"@en ;
    dct:description "Description"@en .
""",
}

def main():
    pos_dir = Path("positive")
    neg_dir = Path("negative")
    pos_dir.mkdir(exist_ok=True)
    neg_dir.mkdir(exist_ok=True)
    
    for name, content in POSITIVE_TESTS.items():
        (pos_dir / name).write_text(content)
        print(f"✓ positive/{name}")
    
    for name, content in NEGATIVE_TESTS.items():
        (neg_dir / name).write_text(content)
        print(f"✓ negative/{name}")
    
    print(f"\n✓ {len(POSITIVE_TESTS)} positive, {len(NEGATIVE_TESTS)} negative")

if __name__ == "__main__":
    main()