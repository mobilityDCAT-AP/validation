"""Generic RDF data loader with format detection and error handling"""

from pathlib import Path
from rdflib import Graph
from rdflib.util import guess_format

# Supported RDF formats and their extensions
RDF_FORMATS = {
    '.ttl': 'turtle',
    '.n3': 'n3',
    '.nt': 'nt',
    '.nq': 'nquads',
    '.rdf': 'xml',
    '.xml': 'xml',
    '.jsonld': 'json-ld',
    '.json': 'json-ld',
    '.trig': 'trig',
}

class LoadError:
    """Represents a file loading error"""
    
    def __init__(self, file_path, error):
        self.file_path = file_path
        self.error = error
    
    def __str__(self):
        return f"{self.file_path}: {self.error}"

def detect_format(file_path):
    """Detect RDF format from file extension"""
    suffix = file_path.suffix.lower()
    
    if suffix in RDF_FORMATS:
        return RDF_FORMATS[suffix]
    
    # Try rdflib's guess_format as fallback
    guessed = guess_format(str(file_path))
    if guessed:
        return guessed
    
    return None

def load_graph_from_file(file_path, format=None):
    """
    Load a single RDF file into a graph
    
    Args:
        file_path: Path to RDF file
        format: RDF format (auto-detected if None)
    
    Returns:
        tuple: (Graph or None, LoadError or None)
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return None, LoadError(file_path, "File not found")
    
    if not file_path.is_file():
        return None, LoadError(file_path, "Not a file")
    
    # Detect format if not provided
    if format is None:
        format = detect_format(file_path)
        if format is None:
            return None, LoadError(file_path, f"Unknown format: {file_path.suffix}")
    
    # Try to parse
    try:
        graph = Graph()
        graph.parse(file_path, format=format)
        return graph, None
    except Exception as e:
        return None, LoadError(file_path, f"Parse error: {str(e)}")

def discover_rdf_files(directory_path):
    """
    Find all RDF files in a directory
    
    Returns:
        list: List of file paths
    """
    if not directory_path.is_dir():
        raise ValueError(f"Not a directory: {directory_path}")
    
    rdf_files = []
    for ext in RDF_FORMATS.keys():
        rdf_files.extend(directory_path.rglob(f"*{ext}"))
    
    return sorted(rdf_files)

def load_graphs_from_directory(directory_path):
    """
    Load all RDF files from a directory
    
    Returns:
        tuple: (dict of graphs, list of LoadErrors)
    """
    files = discover_rdf_files(directory_path)
    graphs = {}
    errors = []
    
    for file_path in files:
        graph, error = load_graph_from_file(file_path)
        if graph:
            graphs[file_path] = graph
        else:
            errors.append(error)
    
    return graphs, errors
