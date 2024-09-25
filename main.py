import streamlit as st
import pandas as pd
import os
from code_analyzer import analyze_code
from test_analyzer import analyze_tests
from test_generator import generate_tests
from visualization import display_coverage, display_test_quality, display_functional_coverage
from utils import process_upload

# Add version number
__version__ = "1.0.0"

# ... rest of the file content ...

if __name__ == "__main__":
    main()
