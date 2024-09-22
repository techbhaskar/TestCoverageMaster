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
    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"])
    use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True)
    
    if st.sidebar.button("Analyze Project"):
        with st.spinner("Analyzing project..."):
            try:
                # Process input
                processed_files = process_upload(file_content)
                st.write("Debug: Input files processed successfully.")
                
                # Analyze code
                code_analysis = analyze_code(processed_files, project_type)
                st.write("Debug: Code analysis completed.")
                
                # Analyze existing tests
                test_analysis = analyze_tests(processed_files, project_type)
                st.write("Debug: Test analysis completed.")
                
                # Generate new tests
                st.write("Debug: Starting test generation.")
                if use_ai and os.getenv("OPENAI_API_KEY"):
                    unit_tests, functional_tests = generate_tests(code_analysis, test_analysis, project_type)
                    st.write("Debug: AI-powered test generation completed.")
                else:
                    unit_tests = "AI-powered test generation is disabled or OpenAI API key is missing."
                    functional_tests = "AI-powered test generation is disabled or OpenAI API key is missing."
                    st.write("Debug: AI-powered test generation skipped.")
                
                st.write("Debug: Preparing to display results.")
                
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
                
                # Display generated test cases
                st.header("Generated Test Cases")
                
                if project_type == 'Python':
                    language = 'python'
                    file_extension = '_test.py'
                elif project_type == 'Angular':
                    language = 'typescript'
                    file_extension = '.spec.ts'
                elif project_type == '.NET':
                    language = 'csharp'
                    file_extension = 'Tests.cs'
                elif project_type == 'Java':
                    language = 'java'
                    file_extension = 'Test.java'
                elif project_type == 'React':
                    language = 'javascript'
                    file_extension = '.test.js'
                else:
                    language = 'javascript'
                    file_extension = '.test.js'
                
                st.subheader("Unit Tests")
                st.code(unit_tests, language=language)
                
                st.subheader("Functional Tests")
                st.code(functional_tests, language=language)
                
                # Download buttons for generated tests
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Unit Tests",
                        data=unit_tests,
                        file_name=f"generated_unit_tests{file_extension}",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        label="Download Functional Tests",
                        data=functional_tests,
                        file_name=f"generated_functional_tests{file_extension}",
                        mime="text/plain"
                    )
                
                st.write("Debug: Analysis and result display completed successfully.")
            except Exception as e:
                st.error(f"An error occurred during the analysis: {str(e)}")
                st.write(f"Debug: Error details - {type(e).__name__}: {str(e)}")
else:
    st.info("Please enter a file path or paste file content to begin analysis.")

st.sidebar.markdown("---")
st.sidebar.info("This app analyzes JavaScript, Angular, React, Python, Java, and .NET projects for unit test coverage and quality, and generates new test cases.")
