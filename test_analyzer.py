from typing import List, Dict
import re
import ast

def analyze_tests(files: List[Dict], project_type: str) -> Dict:
    """
    Analyze the test files and return test quality and functional coverage information.
    """
    test_files = [f for f in files if f['name'].endswith('.test.js') or f['name'].endswith('.spec.ts') or f['name'].endswith('_test.py')]
    
    quality = analyze_test_quality(test_files, project_type)
    functional_coverage = analyze_functional_coverage(files, test_files, project_type)
    
    return {
        'quality': quality,
        'functional_coverage': functional_coverage
    }

def analyze_test_quality(test_files: List[Dict], project_type: str) -> Dict:
    """
    Analyze the quality of test files.
    """
    quality = {
        'total_tests': 0,
        'assertions': 0,
        'mocks': 0,
        'test_depth': 0
    }
    
    for file in test_files:
        content = file['content']
        if project_type == 'Angular':
            quality['total_tests'] += content.count('it(')
            quality['assertions'] += content.count('expect(')
            quality['mocks'] += content.count('jasmine.createSpy') + content.count('jasmine.createSpyObj')
            quality['test_depth'] += content.count('describe(')
        elif project_type == 'Python':
            quality['total_tests'] += content.count('def test_')
            quality['assertions'] += content.count('assert')
            quality['mocks'] += content.count('mock.patch')
            quality['test_depth'] += content.count('class Test')
        else:
            quality['total_tests'] += content.count('test(')
            quality['assertions'] += content.count('expect(')
            quality['mocks'] += content.count('jest.mock(')
            quality['test_depth'] += content.count('describe(')
    
    return quality

def analyze_functional_coverage(files: List[Dict], test_files: List[Dict], project_type: str) -> Dict:
    """
    Analyze the functional coverage of tests.
    """
    coverage = {
        'total_functions': 0,
        'tested_functions': 0,
        'coverage_percentage': 0
    }
    
    all_functions = set()
    tested_functions = set()
    
    for file in files:
        if project_type == "JavaScript":
            file_functions = extract_js_functions(file['content'])
        elif project_type == "Angular":
            file_functions = extract_angular_functions(file['content'])
        elif project_type == "React":
            file_functions = extract_react_functions(file['content'])
        elif project_type == "Python":
            file_functions = extract_python_functions(file['content'])
        
        all_functions.update(file_functions)
    
    for test_file in test_files:
        tested_functions.update(extract_tested_functions(test_file['content'], project_type))
    
    coverage['total_functions'] = len(all_functions)
    coverage['tested_functions'] = len(tested_functions)
    
    if coverage['total_functions'] > 0:
        coverage['coverage_percentage'] = (coverage['tested_functions'] / coverage['total_functions']) * 100
    
    return coverage

def extract_js_functions(content: str) -> List[str]:
    """
    Extract function names from JavaScript code.
    """
    return re.findall(r'function\s+(\w+)', content)

def extract_angular_functions(content: str) -> List[str]:
    """
    Extract function and property names from Angular code.
    """
    functions = re.findall(r'(public|private)?\s*(\w+)\s*\([^)]*\)\s*{', content)
    functions = [f[1] for f in functions]  # Extract function names
    
    properties = re.findall(r'(\w+)\s*:\s*(\w+)\s*;', content)
    properties = [p[0] for p in properties]  # Extract property names
    
    return functions + properties

def extract_react_functions(content: str) -> List[str]:
    """
    Extract function names from React code.
    """
    # This should be implemented with a JSX parser
    return extract_js_functions(content)  # Placeholder implementation

def extract_python_functions(content: str) -> List[str]:
    """
    Extract function names from Python code.
    """
    tree = ast.parse(content)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def extract_tested_functions(content: str, project_type: str) -> List[str]:
    """
    Extract names of functions being tested.
    """
    if project_type == 'Angular':
        return re.findall(r'it\([\'"](.+?)[\'"]', content)
    elif project_type == 'Python':
        return re.findall(r'def\s+test_(\w+)', content)
    else:
        return re.findall(r'test\([\'"](.+?)[\'"]', content)
