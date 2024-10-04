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
        'unit_coverage': 0,
        'functional_coverage': 0,
        'uncovered_functions': []
    }
    
    js_ts_files = [f for f in files if f['name'].endswith(('.js', '.ts', '.jsx', '.tsx'))]
    html_files = [f for f in files if f['name'].endswith('.html')]
    
    for file in files:
        if project_type == "JavaScript":
            file_coverage = analyze_javascript(file['content'], js_ts_files, html_files)
        elif project_type == "Angular":
            file_coverage = analyze_angular(file['content'], js_ts_files, html_files)
        elif project_type == "React":
            file_coverage = analyze_react(file['content'], js_ts_files, html_files)
        elif project_type == "Python":
            file_coverage = analyze_python(file['content'])
        elif project_type == "Java":
            file_coverage = analyze_java(file['content'])
        elif project_type == ".NET":
            file_coverage = analyze_dotnet(file['content'])
        
        coverage['total_lines'] += file_coverage['total_lines']
        coverage['covered_lines'] += file_coverage['covered_lines']
        coverage['uncovered_functions'].extend(file_coverage['uncovered_functions'])
        
        if 'unit_coverage' in file_coverage:
            coverage['unit_coverage'] += file_coverage['unit_coverage']
        if 'functional_coverage' in file_coverage:
            coverage['functional_coverage'] += file_coverage['functional_coverage']
    
    if coverage['total_lines'] > 0:
        coverage['coverage_percentage'] = (coverage['covered_lines'] / coverage['total_lines']) * 100
    
    if len(js_ts_files) > 0:
        coverage['unit_coverage'] /= len(js_ts_files)
        coverage['functional_coverage'] /= len(js_ts_files)
    
    return {'coverage': coverage}

def analyze_javascript(content: str, js_ts_files: List[Dict], html_files: List[Dict]) -> Dict:
    """
    Analyze JavaScript code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
    
    functions = re.findall(r'function\s+(\w+)', content)
    uncovered_functions = [f for f in functions if f"test_{f}" not in content]
    
    unit_coverage = calculate_unit_coverage(content)
    functional_coverage = calculate_functional_coverage(js_ts_files, html_files)
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions,
        'unit_coverage': unit_coverage,
        'functional_coverage': functional_coverage
    }

def analyze_angular(content: str, js_ts_files: List[Dict], html_files: List[Dict]) -> Dict:
    """
    Analyze Angular code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
    
    # Find TypeScript/Angular functions and methods
    functions = re.findall(r'(public|private)?\s*(\w+)\s*\([^)]*\)\s*{', content)
    functions = [f[1] for f in functions]  # Extract function names
    
    # Find component properties
    properties = re.findall(r'(\w+)\s*:\s*(\w+)\s*;', content)
    properties = [p[0] for p in properties]  # Extract property names
    
    all_functions = functions + properties
    uncovered_functions = [f for f in all_functions if f"test_{f}" not in content]
    
    unit_coverage = calculate_unit_coverage(content)
    functional_coverage = calculate_functional_coverage(js_ts_files, html_files)
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions,
        'unit_coverage': unit_coverage,
        'functional_coverage': functional_coverage
    }

def analyze_react(content: str, js_ts_files: List[Dict], html_files: List[Dict]) -> Dict:
    """
    Analyze React code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('//'))
    
    # Find React component functions and methods
    functions = re.findall(r'(function|const)\s+(\w+)\s*[=]?\s*(\([^)]*\)|)\s*[=]?\s*[{(]', content)
    functions = [f[1] for f in functions]  # Extract function names
    
    uncovered_functions = [f for f in functions if f"test_{f}" not in content]
    
    unit_coverage = calculate_unit_coverage(content)
    functional_coverage = calculate_functional_coverage(js_ts_files, html_files)
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions,
        'unit_coverage': unit_coverage,
        'functional_coverage': functional_coverage
    }

def calculate_unit_coverage(content: str) -> float:
    """
    Calculate unit test coverage based on the presence of test functions.
    """
    total_functions = len(re.findall(r'(function|const)\s+(\w+)\s*[=]?\s*(\([^)]*\)|)\s*[=]?\s*[{(]', content))
    test_functions = len(re.findall(r'(describe|it|test)\s*\(', content))
    
    if total_functions == 0:
        return 0
    return (test_functions / total_functions) * 100

def calculate_functional_coverage(js_ts_files: List[Dict], html_files: List[Dict]) -> float:
    """
    Calculate functional coverage based on the presence of UI elements and corresponding event handlers.
    """
    ui_elements = 0
    event_handlers = 0
    
    for html_file in html_files:
        ui_elements += len(re.findall(r'<(\w+)[^>]*>', html_file['content']))
    
    for js_ts_file in js_ts_files:
        event_handlers += len(re.findall(r'(onClick|onSubmit|onChange|addEventListener)', js_ts_file['content']))
    
    if ui_elements == 0:
        return 0
    return min((event_handlers / ui_elements) * 100, 100)

def analyze_python(content: str) -> Dict:
    """
    Analyze Python code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
    
    tree = ast.parse(content)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    uncovered_functions = [f for f in functions if f"test_{f}" not in content]
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions
    }

def analyze_java(content: str) -> Dict:
    """
    Analyze Java code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))
    
    # Find Java methods
    methods = re.findall(r'(public|private|protected)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{', content)
    methods = [m[1] for m in methods]  # Extract method names
    
    uncovered_functions = [m for m in methods if f"test{m.capitalize()}" not in content]
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions
    }

def analyze_dotnet(content: str) -> Dict:
    """
    Analyze .NET (C#) code for coverage.
    """
    lines = content.split('\n')
    total_lines = len(lines)
    covered_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))
    
    # Find C# methods
    methods = re.findall(r'(public|private|protected)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{', content)
    methods = [m[1] for m in methods]  # Extract method names
    
    uncovered_functions = [m for m in methods if f"Test{m}" not in content]
    
    return {
        'total_lines': total_lines,
        'covered_lines': covered_lines,
        'uncovered_functions': uncovered_functions
    }
