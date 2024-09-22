import re
import ast
from typing import List, Dict

def analyze_code(files: List[Dict], project_type: str) -> Dict:
    """
    Analyze the code files and return code coverage information.
    """
    coverage = {
        'total_lines': 0,
        'covered_lines': 0,
        'coverage_percentage': 0,
        'uncovered_functions': []
    }
    
    for file in files:
        if project_type == "JavaScript":
            file_coverage = analyze_javascript(file['content'])
        elif project_type == "Angular":
            file_coverage = analyze_angular(file['content'])
        elif project_type == "React":
            file_coverage = analyze_react(file['content'])
        
        coverage['total_lines'] += file_coverage['total_lines']
        coverage['covered_lines'] += file_coverage['covered_lines']
        coverage['uncovered_functions'].extend(file_coverage['uncovered_functions'])
    
    if coverage['total_lines'] > 0:
        coverage['coverage_percentage'] = (coverage['covered_lines'] / coverage['total_lines']) * 100
    
    return {'coverage': coverage}

def analyze_javascript(content: str) -> Dict:
    """
    Analyze JavaScript code for coverage.
    """
    # This is a simplified analysis and should be replaced with a proper JS parser
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
    
    functions = re.findall(r'function\s+(\w+)', content)
    uncovered_functions = [f for f in functions if f"test_{f}" not in content]
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions
    }

def analyze_angular(content: str) -> Dict:
    """
    Analyze Angular code for coverage.
    """
    # This should be implemented with a TypeScript parser
    return analyze_javascript(content)  # Placeholder implementation

def analyze_react(content: str) -> Dict:
    """
    Analyze React code for coverage.
    """
    # This should be implemented with a JSX parser
    return analyze_javascript(content)  # Placeholder implementation
