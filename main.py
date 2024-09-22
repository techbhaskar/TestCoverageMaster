import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload

st.set_page_config(page_title="Unit Test Analyzer", layout="wide")

st.title("Comprehensive Unit Test Analyzer")

st.sidebar.header("Input Project Files")
input_type = st.sidebar.radio("Select input type", ["File Path", "File Content"])

file_content = None

if input_type == "File Path":
    file_path = st.sidebar.text_input("Enter file path")
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            st.sidebar.error(f"File not found: {file_path}")
        except IOError:
            st.sidebar.error(f"Error reading file: {file_path}")
else:
    file_content = st.sidebar.text_area("Paste file content here")

if file_content:
    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python"])
    use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True)
    
    if st.sidebar.button("Analyze Project"):
        with st.spinner("Analyzing project..."):
            # Process input
            processed_files = process_upload(file_content)
            
            # Analyze code
            code_analysis = analyze_code(processed_files, project_type)
            
            # Analyze existing tests
            test_analysis = analyze_tests(processed_files, project_type)
            
            # Generate new tests
            if use_ai and os.getenv("OPENAI_API_KEY"):
                new_tests = generate_tests(code_analysis, test_analysis, project_type)
            else:
                new_tests = "AI-powered test generation is disabled or OpenAI API key is missing."
            
            # Display results
            st.header("Analysis Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Code Coverage")
                display_coverage(code_analysis['coverage'])
                
                st.subheader("Test Quality")
                display_test_quality(test_analysis['quality'])
            
            with col2:
                st.subheader("Functional Test Coverage")
                display_functional_coverage(test_analysis['functional_coverage'])
            
            st.header("Generated Test Cases")
            st.code(new_tests, language='python' if project_type == 'Python' else 'typescript' if project_type == 'Angular' else 'javascript')
            
            st.download_button(
                label="Download Generated Tests",
                data=new_tests,
                file_name=f"generated_tests.{'py' if project_type == 'Python' else 'spec.ts' if project_type == 'Angular' else 'test.js'}",
                mime="text/plain"
            )
else:
    st.info("Please enter a file path or paste file content to begin analysis.")

st.sidebar.markdown("---")
st.sidebar.info("This app analyzes JavaScript, Angular, React, and Python projects for unit test coverage and quality, and generates new test cases.")
