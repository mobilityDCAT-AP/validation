"""SHACL validation logic with detailed violation reporting"""

import signal
from pyshacl import validate
from rdflib import Namespace

SH = Namespace("http://www.w3.org/ns/shacl#")


class ValidationTimeoutError(Exception):
    """Raised when SHACL validation exceeds the configured timeout."""

class ValidationResult:
    """Holds validation results with violation details"""
    
    def __init__(self, conforms, results_graph, report_text, file_path=None):
        self.conforms = conforms
        self.results_graph = results_graph
        self.report_text = report_text
        self.file_path = file_path
        self._violations = None
    
    def passed(self):
        """Return validation result (conforms or not)"""
        return self.conforms
    
    def status(self):
        """Get status string based on conformance"""
        return "✓ Valid" if self.conforms else "✗ Invalid"
    
    def get_violations(self):
        """Extract violation details from results graph"""
        if self._violations is not None:
            return self._violations
        
        violations = []
        if not self.results_graph:
            return violations
        
        # Find all violation results
        for result in self.results_graph.subjects(predicate=SH.resultSeverity, object=SH.Violation):
            violation = {}
            
            # Get focus node
            focus = self.results_graph.value(result, SH.focusNode)
            if focus:
                violation['focus'] = str(focus).split('/')[-1]  # Get last part of URI
            
            # Get property path
            path = self.results_graph.value(result, SH.resultPath)
            if path:
                path_str = str(path).split('#')[-1].split('/')[-1]
                violation['property'] = path_str
            
            # Get constraint component
            component = self.results_graph.value(result, SH.sourceConstraintComponent)
            if component:
                comp_str = str(component).split('#')[-1]
                violation['constraint'] = comp_str
            
            # Get message
            message = self.results_graph.value(result, SH.resultMessage)
            if message:
                violation['message'] = str(message)
            
            violations.append(violation)
        
        self._violations = violations
        return violations

def validate_graph(data_graph, shacl_graph, inference='rdfs'):
    """Validate a data graph against SHACL shapes"""
    conforms, results_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference=inference,
        abort_on_first=False
    )
    
    return ValidationResult(conforms, results_graph, report_text)


def _validate_with_timeout(data_graph, shacl_graph, inference='rdfs', timeout_seconds=0):
    """Run pySHACL with optional Unix signal timeout."""
    if not timeout_seconds or timeout_seconds <= 0:
        return validate(
            data_graph,
            shacl_graph=shacl_graph,
            inference=inference,
            abort_on_first=False
        )

    if not hasattr(signal, 'SIGALRM'):
        return validate(
            data_graph,
            shacl_graph=shacl_graph,
            inference=inference,
            abort_on_first=False
        )

    def _handle_timeout(signum, frame):
        raise ValidationTimeoutError(f"Validation timed out after {timeout_seconds}s")

    previous_handler = signal.getsignal(signal.SIGALRM)
    try:
        signal.signal(signal.SIGALRM, _handle_timeout)
        signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
        return validate(
            data_graph,
            shacl_graph=shacl_graph,
            inference=inference,
            abort_on_first=False
        )
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)

def validate_file(file_path, shacl_graph, inference='rdfs', extra_graph=None, timeout_seconds=0):
    from graph_loader import load_graph_from_file, LoadError

    data_graph, load_error = load_graph_from_file(file_path)
    if load_error:
        return None, load_error

    # Merge vocabulary stubs into data graph
    if extra_graph:
        data_graph += extra_graph

    try:
        conforms, results_graph, report_text = _validate_with_timeout(
            data_graph,
            shacl_graph=shacl_graph,
            inference=inference,
            timeout_seconds=timeout_seconds,
        )
    except ValidationTimeoutError as e:
        return None, LoadError(file_path, str(e))

    return ValidationResult(conforms, results_graph, report_text, file_path), None


def validate_multiple_files(
    file_paths,
    shacl_graph,
    inference='rdfs',
    extra_graph=None,
    timeout_seconds=0,
    progress_callback=None,
):
    results = []
    errors = []
    total = len(file_paths)
    for index, file_path in enumerate(file_paths, 1):
        if progress_callback:
            progress_callback(file_path, index, total)
        result, error = validate_file(
            file_path,
            shacl_graph,
            inference,
            extra_graph,
            timeout_seconds,
        )
        if result:
            results.append(result)
        else:
            errors.append(error)
    return results, errors
