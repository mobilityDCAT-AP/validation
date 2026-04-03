#!/usr/bin/env python3
"""One-time script to fix vocabulary stubs and test file"""
from pathlib import Path

vocab_dir = Path("sample_data/vocabularies")
vocab_dir.mkdir(parents=True, exist_ok=True)

files = {
    "mobility-theme.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

<https://w3id.org/mobilitydcat-ap/mobility-theme>
  a skos:ConceptScheme ;
  dct:title "Mobility Theme"@en .

<https://w3id.org/mobilitydcat-ap/mobility-theme/passenger-transport>
  a skos:Concept ;
  skos:prefLabel "Passenger transport"@en ;
  skos:inScheme <https://w3id.org/mobilitydcat-ap/mobility-theme> .
""",

    "mobility-data-standard.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .

<https://w3id.org/mobilitydcat-ap/mobility-data-standard>
  a skos:ConceptScheme ;
  dct:title "Mobility Data Standard"@en .

<https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs>
  a skos:Concept ;
  a mobilitydcatap:MobilityDataStandard ;
  skos:prefLabel "GTFS"@en ;
  skos:inScheme <https://w3id.org/mobilitydcat-ap/mobility-data-standard> .
""",

    "conditions-for-access-and-usage.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

<https://w3id.org/mobilitydcat-ap/conditions-for-access-and-usage>
  a skos:ConceptScheme ;
  dct:title "Conditions for access and usage"@en .

<https://w3id.org/mobilitydcat-ap/conditions-for-access-and-usage/free-of-charge>
  a skos:Concept ;
  skos:prefLabel "Free of charge"@en ;
  skos:inScheme <https://w3id.org/mobilitydcat-ap/conditions-for-access-and-usage> .
""",

    "eu-frequency.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://publications.europa.eu/resource/authority/frequency>
  a skos:ConceptScheme ;
  dct:title "Frequency"@en .

<http://publications.europa.eu/resource/authority/frequency/DAILY>
  a skos:Concept ;
  a dct:Frequency ;
  skos:prefLabel "Daily"@en ;
  skos:inScheme <http://publications.europa.eu/resource/authority/frequency> .
""",

    "eu-file-type.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://publications.europa.eu/resource/authority/file-type>
  a skos:ConceptScheme ;
  dct:title "File Type"@en .

<http://publications.europa.eu/resource/authority/file-type/ZIP>
  a skos:Concept ;
  a dct:MediaTypeOrExtent ;
  skos:prefLabel "ZIP"@en ;
  skos:inScheme <http://publications.europa.eu/resource/authority/file-type> .

<http://publications.europa.eu/resource/authority/file-type/JSON>
  a skos:Concept ;
  a dct:MediaTypeOrExtent ;
  skos:prefLabel "JSON"@en ;
  skos:inScheme <http://publications.europa.eu/resource/authority/file-type> .
""",

    "eu-country.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://publications.europa.eu/resource/authority/country>
  a skos:ConceptScheme ;
  dct:title "Countries"@en .

<http://publications.europa.eu/resource/authority/country/DEU>
  a skos:Concept ;
  a dct:Location ;
  skos:prefLabel "Germany"@en ;
  skos:inScheme <http://publications.europa.eu/resource/authority/country> .
""",

    "eu-corporate-body.ttl": """\
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://publications.europa.eu/resource/authority/corporate-body>
  a skos:ConceptScheme ;
  dct:title "Corporate body"@en .

<http://publications.europa.eu/resource/authority/corporate-body/AGENTEXA>
  a skos:Concept ;
  a foaf:Agent ;
  skos:prefLabel "Example Transport Agency"@en ;
  foaf:name "Example Transport Agency"@en ;
  skos:inScheme <http://publications.europa.eu/resource/authority/corporate-body> .
""",
}

test_file = Path("sample_data/mobility/positives/M-P-03-valid-mobility-distribution.ttl")
test_content = """\
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ex: <https://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix mobilitydcatap: <https://w3id.org/mobilitydcat-ap#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:dataset1
  a dcat:Dataset ;
  dct:title "GTFS Schedules"@en ;
  dct:description "Public transport schedules in GTFS format."@en ;
  dct:accrualPeriodicity <http://publications.europa.eu/resource/authority/frequency/DAILY> ;
  mobilitydcatap:mobilityTheme <https://w3id.org/mobilitydcat-ap/mobility-theme/passenger-transport> ;
  dct:spatial <http://publications.europa.eu/resource/authority/country/DEU> ;
  dct:publisher <http://publications.europa.eu/resource/authority/corporate-body/AGENTEXA> ;
  dcat:distribution ex:distribution1 .

ex:distribution1
  a dcat:Distribution ;
  dcat:accessURL <https://example.org/downloads/gtfs.zip> ;
  dct:format <http://publications.europa.eu/resource/authority/file-type/ZIP> ;
  dct:rights ex:rights1 ;
  mobilitydcatap:mobilityDataStandard
    <https://w3id.org/mobilitydcat-ap/mobility-data-standard/gtfs> .

ex:rights1
  a dct:RightsStatement ;
  dct:type <https://w3id.org/mobilitydcat-ap/conditions-for-access-and-usage/free-of-charge> .
"""

# Write vocab stubs
for filename, content in files.items():
    path = vocab_dir / filename
    path.write_text(content, encoding="utf-8")
    print(f"✓ Written {path}")

# Write test file
test_file.write_text(test_content, encoding="utf-8")
print(f"✓ Written {test_file}")

print("\nDone. Now run:")
print("uv run scripts/validate.py --data sample_data/mobility/positives/M-P-03-valid-mobility-distribution.ttl --shacl shacl/ -v")