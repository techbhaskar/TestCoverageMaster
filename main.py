import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload
from streamlit_oauth import OAuth2Component
from oauth_config import google_oauth, facebook_oauth, github_oauth, REDIRECT_URI

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

def login_button(name, oauth_client):
    return OAuth2Component(
        name=f"{name}_oauth",
        client_id=oauth_client.client_id,
        client_secret=oauth_client.client_secret,
        authorize_endpoint=oauth_client.authorize_endpoint,
        token_endpoint=oauth_client.token_endpoint,
        refresh_token_endpoint=oauth_client.refresh_token_endpoint,
        revoke_token_endpoint=oauth_client.revoke_token_endpoint,
        redirect_uri=REDIRECT_URI,
    )

def main():
    st.set_page_config(page_title="Unit Test Analyzer", layout="wide")

    # Initialize session state for storing generated tests and user info
    if 'unit_tests' not in st.session_state:
        st.session_state.unit_tests = None
    if 'functional_tests' not in st.session_state:
        st.session_state.functional_tests = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'show_login' not in st.session_state:
        st.session_state.show_login = False

    st.title("Comprehensive Unit Test Analyzer")
    st.caption(f"Version: {__version__}")

    # Header with login button or user info
    header = st.container()
    with header:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("Welcome to the Unit Test Analyzer")
        with col2:
            if st.session_state.user:
                st.write(f"Logged in as: {st.session_state.user['name']}")
                if st.button("Logout"):
                    st.session_state.user = None
            else:
                if st.button("Login"):
                    st.session_state.show_login = True

    # Login popup
    if st.session_state.show_login and not st.session_state.user:
        login_container = st.empty()
        with login_container.container():
            st.subheader("Login Options")
            google_button = login_button("Google", google_oauth)
            facebook_button = login_button("Facebook", facebook_oauth)
            github_button = login_button("GitHub", github_oauth)

            if google_button.authorize_button("Login with Google"):
                st.session_state.user = google_button.get_user_info()
                st.session_state.show_login = False
                login_container.empty()
            elif facebook_button.authorize_button("Login with Facebook"):
                st.session_state.user = facebook_button.get_user_info()
                st.session_state.show_login = False
                login_container.empty()
            elif github_button.authorize_button("Login with GitHub"):
                st.session_state.user = github_button.get_user_info()
                st.session_state.show_login = False
                login_container.empty()

    # Main application content
    if st.session_state.user:
        st.sidebar.header("Input Project Files")
        input_type = st.sidebar.radio("Select input type", ["File Path", "File Content"])

        # Default file content for testing
        default_file_content = """
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    """

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
            file_content = st.sidebar.text_area("Paste file content here", value=default_file_content)

        project_type = st.sidebar.selectbox("Select Project Type", ["JavaScript", "Angular", "React", "Python", "Java", ".NET"])
        use_ai = st.sidebar.checkbox("Use AI-powered test generation", value=True)
        
        analyze_button = st.sidebar.button("Analyze Project")

        # Debug information
        st.sidebar.write("Debug Info:")
        st.sidebar.write(f"Input Type: {input_type}")
        st.sidebar.write(f"File Content: {file_content[:50] if file_content else 'None'}...")
        st.sidebar.write(f"Project Type: {project_type}")
        st.sidebar.write(f"Analyze Button: {analyze_button}")

        if file_content and (analyze_button or input_type == "File Content"):
            with st.spinner("Analyzing project..."):
                try:
                    # Process input
                    processed_files = process_upload(file_content)
                    st.write("Debug: Files processed successfully")
                    
                    # Analyze code
                    code_analysis = analyze_code(processed_files, project_type)
                    st.write("Debug: Code analysis completed")
                    
                    # Analyze existing tests
                    test_analysis = analyze_tests(processed_files, project_type)
                    st.write("Debug: Test analysis completed")
                    
                    # Generate new tests
                    unit_tests, functional_tests = generate_tests(code_analysis, test_analysis, project_type)
                    st.write("Debug: Test generation completed")
                    
                    # Store generated tests in session state
                    st.session_state.unit_tests = unit_tests
                    st.session_state.functional_tests = functional_tests
                    
                    # Display results
                    display_results(code_analysis, test_analysis, project_type)
                    
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
                    st.write(f"Debug: Error details - {type(e).__name__}: {str(e)}")
        else:
            st.info("Please enter a file path or paste file content to begin analysis.")

    else:
        st.info("Please log in to use the Unit Test Analyzer.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app analyzes JavaScript, Angular, React, Python, Java, and .NET projects for unit test coverage and quality, and generates new test cases.")

if __name__ == "__main__":
    main()
