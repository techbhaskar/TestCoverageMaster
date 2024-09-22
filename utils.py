from typing import List, Dict

def process_upload(uploaded_files) -> List[Dict]:
    """
    Process uploaded files and return a list of dictionaries containing file information.
    """
    processed_files = []
    
    for file in uploaded_files:
        content = file.read().decode('utf-8')
        processed_files.append({
            'name': file.name,
            'content': content
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
