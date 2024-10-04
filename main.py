import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload

# Add version number
__version__ = "1.2.0"

def get_file_extension(project_type):
    if project_type in ["JavaScript", "React"]:
        return "js"
    elif project_type == "Angular":
        return "ts"
    elif project_type == "Python":
        return "py"
    elif project_type == "Java":
        return "java"
    elif project_type == ".NET":
        return "cs"
    else:
        return "txt"

def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def get_test_quality_suggestions():
    """Provide suggestions for improving test quality based on best practices."""
    suggestions = [
        "Improve test coverage by adding more test cases, especially for edge cases and different scenarios.",
        "Implement parameterized tests to test multiple inputs efficiently.",
        "Use setup and teardown methods for better test organization and resource management.",
        "Group related tests into test classes for better structure and readability.",
        "Utilize mocking to isolate units of code and test them independently.",
        "Add integration tests to verify the interaction between different components.",
        "Adopt test-driven development (TDD) by writing tests before implementing new features.",
        "Use specific assertions to check expected outcomes more accurately.",
        "Implement continuous integration to run tests automatically on each code change.",
        "Regularly review and refactor tests to maintain their quality and relevance.",
        "Use code coverage tools to identify areas of the codebase that lack test coverage.",
        "Write both positive and negative test cases to ensure proper error handling.",
        "Keep tests independent and avoid dependencies between test cases.",
        "Use meaningful test names that describe the behavior being tested.",
        "Implement performance tests for critical parts of the application."
    ]
    return suggestions

def display_results(code_analysis, test_analysis, project_type, show_coverage_quality):
    st.header("Analysis Results")
    
    if show_coverage_quality:
        if code_analysis and 'coverage' in code_analysis:
            st.subheader("Code Coverage")
            try:
                display_coverage(code_analysis['coverage'])
            except Exception as e:
                st.error(f"Error displaying code coverage: {str(e)}")
        else:
            st.warning("Code coverage data is not available.")
        
        if test_analysis and 'quality' in test_analysis:
            st.subheader("Test Quality")
            try:
                display_test_quality(test_analysis['quality'])
            except Exception as e:
                st.error(f"Error displaying test quality: {str(e)}")
        else:
            st.warning("Test quality data is not available.")
    
    if test_analysis and 'functional_coverage' in test_analysis:
        st.subheader("Functional Coverage")
        try:
            display_functional_coverage(test_analysis['functional_coverage'])
        except Exception as e:
            st.error(f"Error displaying functional coverage: {str(e)}")
    else:
        st.warning("Functional coverage data is not available.")

def main():
    st.set_page_config(page_title="Unit Test Analyzer", layout="wide")

    # Initialize session state for storing generated tests
    if 'unit_tests' not in st.session_state:
        st.session_state.unit_tests = None
    if 'functional_tests' not in st.session_state:
        st.session_state.functional_tests = None

    st.title("Comprehensive Unit Test Analyzer")
    st.caption(f"Version: {__version__}")

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

    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"])
    use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True)
    
    # Add checkbox for toggling Code Coverage and Test Quality sections
    show_coverage_quality = st.sidebar.checkbox("Show Code Coverage and Test Quality", value=False)
    
    analyze_button = st.sidebar.button("Analyze Project")

    if file_content and analyze_button:
        with st.spinner("Analyzing project..."):
            try:
                # Process input
                processed_files = process_upload(file_content)
                
                # Analyze code
                code_analysis = analyze_code(processed_files, project_type)
                
                # Analyze existing tests
                test_analysis = analyze_tests(processed_files, project_type)
                
                # Generate new tests
                unit_tests, functional_tests = generate_tests(code_analysis, test_analysis, project_type)
                
                # Store generated tests in session state
                st.session_state.unit_tests = unit_tests
                st.session_state.functional_tests = functional_tests
                
                # Display results
                display_results(code_analysis, test_analysis, project_type, show_coverage_quality)
                
                # Display generated tests
                st.header("Generated Test Cases")
                if unit_tests:
                    st.subheader("Unit Tests")
                    st.code(unit_tests)
                else:
                    st.warning("No unit tests were generated.")
                
                if functional_tests:
                    st.subheader("Functional Tests")
                    st.code(functional_tests)
                else:
                    st.warning("No functional tests were generated.")
                
                # Add download buttons for unit tests and functional tests
                if st.session_state.unit_tests:
                    st.download_button(
                        label="Download Unit Tests",
                        data=st.session_state.unit_tests,
                        file_name=f"generated_unit_tests.{get_file_extension(project_type)}",
                        mime="text/plain"
                    )
                if st.session_state.functional_tests:
                    st.download_button(
                        label="Download Functional Tests",
                        data=st.session_state.functional_tests,
                        file_name=f"generated_functional_tests.{get_file_extension(project_type)}",
                        mime="text/plain"
                    )
                
                # Display test quality suggestions
                st.header("Suggestions for Improving Test Quality")
                suggestions = get_test_quality_suggestions()
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
                
            except Exception as e:
                st.error(f"An error occurred during the analysis: {str(e)}")
    else:
        st.info("Please enter a file path or paste file content and click 'Analyze Project' to begin analysis.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app analyzes JavaScript, Angular, React, Python, Java, and .NET projects for unit test coverage and quality, and generates new test cases.")

if __name__ == "__main__":
    main()
