import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload
import openai
from tenacity import RetryError

# Add version number
__version__ = "1.0.0"

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
    return a + b

def get_test_quality_suggestions():
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

def display_results(code_analysis, test_analysis, project_type):
    st.header("Analysis Results")
    
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

def generate_fallback_tests(code_analysis, test_analysis, project_type):
    uncovered_functions = code_analysis['coverage']['uncovered_functions']
    
    unit_tests = []
    functional_tests = []
    
    for func in uncovered_functions:
        unit_test = f"// Fallback Unit Test for {func}\n// TODO: Implement unit test for {func}"
        functional_test = f"// Fallback Functional Test for {func}\n// TODO: Implement functional test for {func}"
        
        unit_tests.append(unit_test)
        functional_tests.append(functional_test)
    
    return "\n\n".join(unit_tests), "\n\n".join(functional_tests)

def main():
    st.set_page_config(page_title="Unit Test Analyzer", layout="wide")

    if 'unit_tests' not in st.session_state:
        st.session_state.unit_tests = None
    if 'functional_tests' not in st.session_state:
        st.session_state.functional_tests = None
    if 'usage_counter' not in st.session_state:
        st.session_state.usage_counter = 0

    st.title("Comprehensive Unit Test Analyzer")
    st.caption(f"Version: {__version__}")
    
    st.write(f"Total analyses performed: {st.session_state.usage_counter}")

    st.sidebar.header("Input Project Files")
    input_type = st.sidebar.radio("Select input type", ["File Upload", "File Path", "File Content"])

    default_file_content = """
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    """

    file_content = None

    if input_type == "File Upload":
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=['py', 'js', 'ts', 'java', 'cs'])
        if uploaded_file is not None:
            file_content = uploaded_file.getvalue().decode("utf-8")
    elif input_type == "File Path":
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
        file_content = st.sidebar.text_area("Paste file content here", value=default_file_content)

    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"])
    use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True)
    
    analyze_button = st.sidebar.button("Analyze Project")

    st.sidebar.write("Debug Info:")
    st.sidebar.write(f"Input Type: {input_type}")
    st.sidebar.write(f"File Content: {file_content[:50] if file_content else 'None'}...")
    st.sidebar.write(f"Project Type: {project_type}")
    st.sidebar.write(f"Analyze Button: {analyze_button}")

    if file_content and (analyze_button or input_type == "File Content"):
        st.session_state.usage_counter += 1
        
        # Prompt user for OpenAI API key
        user_api_key = st.text_input("Enter your OpenAI API key (optional):", type="password")
        
        with st.spinner("Analyzing project..."):
            try:
                processed_files = process_upload(file_content)
                st.write("Debug: Files processed successfully")
                
                code_analysis = analyze_code(processed_files, project_type)
                st.write("Debug: Code analysis completed")
                
                test_analysis = analyze_tests(processed_files, project_type)
                st.write("Debug: Test analysis completed")
                
                try:
                    unit_tests, functional_tests = generate_tests(code_analysis, test_analysis, project_type, api_key=user_api_key)
                    st.write("Debug: Test generation completed")
                except RetryError:
                    st.warning("OpenAI API rate limit exceeded. Using fallback test generation.")
                    unit_tests, functional_tests = generate_fallback_tests(code_analysis, test_analysis, project_type)
                except openai.error.AuthenticationError:
                    st.error("OpenAI API key is invalid. Please check your API key and try again.")
                    return
                except Exception as e:
                    st.error(f"An error occurred during test generation: {str(e)}")
                    st.write(f"Debug: Error details - {type(e).__name__}: {str(e)}")
                    return
                
                st.session_state.unit_tests = unit_tests
                st.session_state.functional_tests = functional_tests
                
                display_results(code_analysis, test_analysis, project_type)
                
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
                
                st.header("Suggestions for Improving Test Quality")
                suggestions = get_test_quality_suggestions()
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
                
            except Exception as e:
                st.error(f"An error occurred during the analysis: {str(e)}")
                st.write(f"Debug: Error details - {type(e).__name__}: {str(e)}")
    else:
        st.info("Please upload a file, enter a file path, or paste file content to begin analysis.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app analyzes JavaScript, Angular, React, Python, Java, and .NET projects for unit test coverage and quality, and generates new test cases.")

if __name__ == "__main__":
    main()