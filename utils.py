from typing import List, Dict

def process_upload(file_contents: List[Dict]) -> List[Dict]:
    """
    Process the input file contents and return a list of dictionaries containing file information.
    """
    processed_files = []
    
    for file in file_contents:
        processed_files.append({
            'name': file['name'],
            'content': file['content']
        })
    
    return processed_files

def is_angular_file(file_name: str) -> bool:
    """
    Check if the file is an Angular-specific file.
    """
    angular_extensions = ['.ts', '.html', '.scss', '.css']
    return any(file_name.endswith(ext) for ext in angular_extensions)

def is_test_file(file_name: str) -> bool:
    """
    Check if the file is a test file.
    """
    return file_name.endswith('.spec.ts') or file_name.endswith('.test.js')
