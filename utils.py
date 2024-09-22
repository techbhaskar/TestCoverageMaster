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
