import coverage
import os
import subprocess
from typing import List, Dict

def analyze_code(files: List[Dict], project_type: str) -> Dict:
    """
    Analyze the code files and return code coverage information using actual unit tests.
    """
    coverage_data = {
        'total_lines': 0,
        'covered_lines': 0,
        'coverage_percentage': 0,
        'uncovered_functions': []
    }

    # Create a coverage object
    cov = coverage.Coverage()

    # Start coverage measurement
    cov.start()

    # Run unit tests
    test_files = [f['name'] for f in files if f['name'].startswith('test_') or f['name'].endswith('_test.py')]
    for test_file in test_files:
        subprocess.run(['python', '-m', 'unittest', test_file], capture_output=True)

    # Stop coverage measurement
    cov.stop()

    # Save coverage results
    cov.save()

    # Analyze coverage data
    cov.load()
    total_lines = 0
    covered_lines = 0

    for file in files:
        if not file['name'].startswith('test_') and not file['name'].endswith('_test.py'):
            file_coverage = cov.analysis(file['name'])
            total_lines += len(file_coverage[1] + file_coverage[2])
            covered_lines += len(file_coverage[1])
            uncovered_lines = file_coverage[2]
            
            # Extract uncovered functions
            with open(file['name'], 'r') as f:
                content = f.readlines()
                for i, line in enumerate(content):
                    if 'def ' in line and i+1 in uncovered_lines:
                        function_name = line.split('def ')[1].split('(')[0].strip()
                        coverage_data['uncovered_functions'].append(function_name)

    coverage_data['total_lines'] = total_lines
    coverage_data['covered_lines'] = covered_lines
    
    if total_lines > 0:
        coverage_data['coverage_percentage'] = (covered_lines / total_lines) * 100

    # Generate HTML report
    cov.html_report(directory='coverage_report')

    return {'coverage': coverage_data}

# Keep other functions (analyze_javascript, analyze_angular, etc.) as they are,
# they might be useful for more detailed analysis in the future.
