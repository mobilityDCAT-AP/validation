"""Load RDF graphs from files with multi-format support"""

from pathlib import Path
from rdflib import Graph

class LoadError:
    """Represents an error loading an RDF file"""
    
    def __init__(self, file_path, error_message):
        self.file_path = file_path
        self.error_message = error_message
    
    def __str__(self):
        return f"{self.file_path.name}: {self.error_message}"

# Supported RDF formats with file extensions
RDF_FORMATS = {
    '.ttl': 'turtle',
    '.rdf': 'xml',
    '.xml': 'xml',
    '.nt': 'nt',
    '.n3': 'n3',
    '.jsonld': 'json-ld',
    '.json': 'json-ld',
    '.trig': 'trig',
    '.nq': 'nquads'
}

def get_format_from_extension(file_path):
    """Determine RDF format from file extension"""
    suffix = file_path.suffix.lower()
    return RDF_FORMATS.get(suffix, 'turtle')  # Default to turtle

def load_graph_from_file(file_path):
    """
    Load RDF graph from file with auto-format detection
    
    Returns:
        tuple: (Graph or None, LoadError or None)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return None, LoadError(file_path, "File not found")
    
    graph = Graph()
    fmt = get_format_from_extension(file_path)
    
    try:
        graph.parse(file_path, format=fmt)
        return graph, None
    except Exception as e:
        return None, LoadError(file_path, str(e))

def discover_rdf_files(directory):
    """Find all RDF files in directory and subdirectories"""
    directory = Path(directory)
    
    if not directory.exists():
        return []
    
    rdf_files = []
    for ext in RDF_FORMATS.keys():
        rdf_files.extend(directory.rglob(f'*{ext}'))
    
    return sorted(rdf_files)
