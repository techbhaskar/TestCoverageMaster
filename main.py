import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload
import glob

# Add version number
__version__ = "1.5.0"

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
    """Provide suggestions for improving test quality based on best practices with specific examples and real-world scenarios."""
    suggestions = [
        "Improve test coverage by adding more test cases, especially for edge cases and different scenarios. For example, if you have a function that processes user input, test it with valid input, empty input, extremely long input, and input containing special characters.",
        "Implement parameterized tests to test multiple inputs efficiently. For instance, use @pytest.mark.parametrize in Python to test a sorting function with various input lists: sorted, reverse sorted, empty, and lists with duplicate elements.",
        "Use setup and teardown methods for better test organization and resource management. In a real-world scenario, you might use setUp() to create a test database connection and tearDown() to close it, ensuring each test starts with a clean slate.",
        "Group related tests into test classes for better structure and readability. For example, create separate test classes for UserAuthentication, OrderProcessing, and PaymentGateway in an e-commerce application.",
        "Utilize mocking to isolate units of code and test them independently. In a weather app, you could mock the API call to a weather service to test how your app handles different weather conditions without making actual API requests.",
        "Add integration tests to verify the interaction between different components. For instance, test the entire user registration process in a web application, from form submission to database entry creation and email notification.",
        "Adopt test-driven development (TDD) by writing tests before implementing new features. When adding a new 'forgot password' feature, write tests for successful password reset, invalid token handling, and email sending before implementing the feature.",
        "Use specific assertions to check expected outcomes more accurately. Instead of using assertEqual(True, user.is_active), use assertTrue(user.is_active) for better readability and more informative error messages.",
        "Implement continuous integration to run tests automatically on each code change. Set up a CI/CD pipeline using tools like Jenkins or GitHub Actions to run your test suite on every push to the repository.",
        "Regularly review and refactor tests to maintain their quality and relevance. As your codebase evolves, some tests may become obsolete or redundant. Schedule monthly test code reviews to keep your test suite efficient and up-to-date.",
        "Use code coverage tools to identify areas of the codebase that lack test coverage. Tools like coverage.py for Python or Istanbul for JavaScript can help you visualize which parts of your code are not covered by tests.",
        "Write both positive and negative test cases to ensure proper error handling. For a user registration function, test both successful registration with valid data and failed registration attempts with invalid email formats or weak passwords.",
        "Keep tests independent and avoid dependencies between test cases. Each test should be able to run in isolation. For example, don't rely on the state created by one test for another test to function correctly.",
        "Use meaningful test names that describe the behavior being tested. Instead of test_login(), use test_login_with_valid_credentials_succeeds() or test_login_with_invalid_password_fails() to clearly indicate the test's purpose.",
        "Implement performance tests for critical parts of the application. For an e-commerce site, create tests to ensure the product search function returns results within acceptable time limits, even with a large product database."
    ]
    return suggestions

def display_results(code_analysis, test_analysis, project_type, show_coverage_quality, show_functional_coverage):
    st.header("Analysis Results")
    
    if show_coverage_quality:
        if code_analysis and 'coverage' in code_analysis:
            coverage = code_analysis['coverage']
            if coverage['total_lines'] > 0:
                st.subheader("Code Coverage")
                try:
                    display_coverage(coverage)
                    st.write(f"Total Lines: {coverage['total_lines']}")
                    st.write(f"Covered Lines: {coverage['covered_lines']}")
                    st.write(f"Coverage Percentage: {coverage['coverage_percentage']:.2f}%")
                except Exception as e:
                    st.error(f"Error displaying code coverage: {str(e)}")
            else:
                st.warning("No code coverage data available.")
        else:
            st.warning("Code coverage analysis not available.")
        
        if test_analysis and 'quality' in test_analysis:
            quality = test_analysis['quality']
            if any(quality.values()):
                st.subheader("Test Quality")
                try:
                    display_test_quality(quality)
                    st.write(f"Total Tests: {quality['total_tests']}")
                    st.write(f"Assertions: {quality['assertions']}")
                    st.write(f"Mocks: {quality['mocks']}")
                    st.write(f"Test Depth: {quality['test_depth']}")
                except Exception as e:
                    st.error(f"Error displaying test quality: {str(e)}")
            else:
                st.warning("No test quality data available.")
        else:
            st.warning("Test quality analysis not available.")
    
    if show_functional_coverage:
        if test_analysis and 'functional_coverage' in test_analysis:
            functional_coverage = test_analysis['functional_coverage']
            if functional_coverage['total_functions'] > 0:
                st.subheader("Functional Coverage")
                try:
                    display_functional_coverage(functional_coverage)
                except Exception as e:
                    st.error(f"Error displaying functional coverage: {str(e)}")
            else:
                st.warning("No functional coverage data available.")
        else:
            st.warning("Functional coverage analysis not available.")

def scan_directory(directory_path, project_type):
    """Recursively scan directory and return file contents."""
    file_contents = []
    extensions = ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.cs']
    
    for ext in extensions:
        for file_path in glob.glob(f"{directory_path}/**/*{ext}", recursive=True):
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    file_contents.append({
                        'name': os.path.relpath(file_path, directory_path),
                        'content': content
                    })
            except Exception as e:
                st.warning(f"Error reading file {file_path}: {str(e)}")
    
    return file_contents

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
    input_type = st.sidebar.radio("Select input type", ["Project Directory", "Multiple Files Input"], key="input_type_radio")

    file_contents = []

    if input_type == "Multiple Files Input":
        st.sidebar.markdown("### Paste Multiple Files")
        st.sidebar.markdown("Format: ```\nFilename: example.js\n[Content here]\n---```")
        content = st.sidebar.text_area("Paste files here", height=300, key="multi_file_content_input")
        
        if content:
            files = content.split('---')
            for file_block in files:
                if not file_block.strip():
                    continue
                try:
                    file_lines = file_block.strip().split('\n')
                    if file_lines[0].startswith('Filename:'):
                        filename = file_lines[0].replace('Filename:', '').strip()
                        file_content = '\n'.join(file_lines[1:])
                        file_contents.append({
                            'name': filename,
                            'content': file_content
                        })
                except Exception as e:
                    st.sidebar.error(f"Error parsing file block: {str(e)}")
    else:  # Project Directory
        directory_path = st.sidebar.text_input("Enter directory path", key="directory_path_input")
        if directory_path:
            if os.path.isdir(directory_path):
                project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"], key="project_type_directory")
                file_contents = scan_directory(directory_path, project_type)
                if not file_contents:
                    st.sidebar.warning("No relevant files found in the directory.")
            else:
                st.sidebar.error("Invalid directory path.")

    project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"], key="project_type_main")
    use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True, key="use_ai_checkbox")
    
    # Add checkboxes for toggling different sections
    show_coverage_quality = st.sidebar.checkbox("Show Code Coverage and Test Quality", value=False, key="show_coverage_quality_checkbox")
    show_functional_coverage = st.sidebar.checkbox("Show Functional Coverage", value=False, key="show_functional_coverage_checkbox")
    
    analyze_button = st.sidebar.button("Analyze Project")

    if file_contents and analyze_button:
        with st.spinner("Analyzing project..."):
            try:
                # Process input
                processed_files = process_upload(file_contents)
                
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
                display_results(code_analysis, test_analysis, project_type, show_coverage_quality, show_functional_coverage)
                
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
                        mime="text/plain",
                        key="download_unit_tests_button"
                    )
                if st.session_state.functional_tests:
                    st.download_button(
                        label="Download Functional Tests",
                        data=st.session_state.functional_tests,
                        file_name=f"generated_functional_tests.{get_file_extension(project_type)}",
                        mime="text/plain",
                        key="download_functional_tests_button"
                    )
                
                # Display test quality suggestions
                st.header("Suggestions for Improving Test Quality")
                suggestions = get_test_quality_suggestions()
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
                
            except Exception as e:
                st.error(f"An error occurred during the analysis: {str(e)}")
    else:
        st.info("Please enter a file path, paste file content, or provide a directory path and click 'Analyze Project' to begin analysis.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app analyzes JavaScript, Angular, React, Python, Java, and .NET projects for unit test coverage and quality, and generates new test cases.")

if __name__ == "__main__":
    main()