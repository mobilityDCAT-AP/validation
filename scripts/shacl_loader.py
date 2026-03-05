"""Load SHACL shapes from files or directories"""

from pathlib import Path
from rdflib import Graph

def load_shacl_from_file(file_path):
    """Load SHACL shapes from a single file"""
    shacl_graph = Graph()
    shacl_graph.parse(file_path, format="turtle")
    return shacl_graph

def load_shacl_from_directory(directory_path):
    """Load and merge all SHACL files from a directory"""
    if not directory_path.is_dir():
        raise ValueError(f"Not a directory: {directory_path}")
    
    shacl_graph = Graph()
    shacl_files = list(directory_path.glob("*.ttl"))
    
    if not shacl_files:
        raise ValueError(f"No .ttl files found in {directory_path}")
    
    for shacl_file in shacl_files:
        shacl_graph.parse(shacl_file, format="turtle")
    
    return shacl_graph, shacl_files

def load_shacl(path):
    """Load SHACL shapes from file or directory"""
    path = Path(path)
    
    if path.is_file():
        return load_shacl_from_file(path), [path]
    elif path.is_dir():
        return load_shacl_from_directory(path)
    else:
        raise ValueError(f"Path not found: {path}")
