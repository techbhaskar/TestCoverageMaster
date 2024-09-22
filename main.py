import streamlit as st
import pandas as pd
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload

st.set_page_config(page_title="Unit Test Analyzer", layout="wide")

st.title("Comprehensive Unit Test Analyzer")

st.sidebar.header("Upload Project Files")
uploaded_files = st.sidebar.file_uploader("Choose project files", accept_multiple_files=True, type=['js', 'jsx', 'ts', 'tsx'])

if uploaded_files:
    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React"])
    
    if st.sidebar.button("Analyze Project"):
        with st.spinner("Analyzing project..."):
            # Process uploaded files
            processed_files = process_upload(uploaded_files)
            
            # Analyze code
            code_analysis = analyze_code(processed_files, project_type)
            
            # Analyze existing tests
            test_analysis = analyze_tests(processed_files, project_type)
            
            # Generate new tests
            new_tests = generate_tests(code_analysis, test_analysis)
            
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
            st.code(new_tests, language='javascript')
            
            st.download_button(
                label="Download Generated Tests",
                data=new_tests,
                file_name="generated_tests.js",
                mime="text/javascript"
            )
else:
    st.info("Please upload your project files to begin analysis.")

st.sidebar.markdown("---")
st.sidebar.info("This app analyzes JavaScript, Angular, and React projects for unit test coverage and quality, and generates new test cases.")
