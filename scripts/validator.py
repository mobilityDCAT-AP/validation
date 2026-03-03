"""SHACL validation logic"""

from pyshacl import validate

class ValidationResult:
    """Holds validation results"""
    
    def __init__(self, conforms, results_graph, report_text, file_path=None):
        self.conforms = conforms
        self.results_graph = results_graph
        self.report_text = report_text
        self.file_path = file_path
    
    def is_positive_test(self):
        """Check if this is a positive test case"""
        if self.file_path:
            return "positive" in str(self.file_path)
        return False
    
    def is_negative_test(self):
        """Check if this is a negative test case"""
        if self.file_path:
            return "negative" in str(self.file_path)
        return False
    
    def passed(self):
        """Check if test passed based on expected outcome"""
        if self.is_positive_test():
            return self.conforms
        elif self.is_negative_test():
            return not self.conforms
        else:
            return self.conforms
    
    def status(self):
        """Get status string"""
        return "✓ PASS" if self.passed() else "✗ FAIL"

def validate_graph(data_graph, shacl_graph, inference='rdfs'):
    """Validate a data graph against SHACL shapes"""
    conforms, results_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference=inference,
        abort_on_first=False
    )
    
    return ValidationResult(conforms, results_graph, report_text)

def validate_file(file_path, shacl_graph, inference='rdfs'):
    """
    Validate a file against SHACL shapes
    
    Returns:
        tuple: (ValidationResult or None, LoadError or None)
    """
    from .graph_loader import load_graph_from_file
    
    data_graph, load_error = load_graph_from_file(file_path)
    
    if load_error:
        return None, load_error
    
    conforms, results_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference=inference,
        abort_on_first=False
    )
    
    return ValidationResult(conforms, results_graph, report_text, file_path), None

def validate_multiple_files(file_paths, shacl_graph, inference='rdfs'):
    """
    Validate multiple files
    
    Returns:
        tuple: (list of ValidationResults, list of LoadErrors)
    """
    results = []
    errors = []
    
    for file_path in file_paths:
        result, error = validate_file(file_path, shacl_graph, inference)
        if result:
            results.append(result)
        else:
            errors.append(error)
    
    return results, errors
