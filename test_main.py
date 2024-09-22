import unittest
from unittest.mock import patch
from main import add_numbers, main
import streamlit as st

class TestMain(unittest.TestCase):
    def setUp(self):
        # Setup method to initialize any common resources
        self.test_input = [2, 3, -1, 0]

    def tearDown(self):
        # Teardown method to clean up after tests
        pass

    def test_add_numbers(self):
        # Test the add_numbers function with multiple inputs
        test_cases = [
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (-5, -7, -12),
            (100, -100, 0)
        ]
        for a, b, expected in test_cases:
            with self.subTest(f"Testing add_numbers({a}, {b})"):
                self.assertEqual(add_numbers(a, b), expected)

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.text_input')
    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.sidebar.button')
    def test_main_file_path_input(self, mock_button, mock_selectbox, mock_text_input, mock_radio):
        # Test the main function with file path input
        mock_radio.return_value = "File Path"
        mock_text_input.return_value = "test_file.py"
        mock_selectbox.return_value = "Python"
        mock_button.return_value = True

        with patch('builtins.open', unittest.mock.mock_open(read_data="print('Hello, World!')")):
            with patch('streamlit.spinner'):
                main()

        # Add assertions to check if the main function behaves correctly
        # Note: Since streamlit runs in a separate thread, we can't directly assert its output
        # Instead, we can check if certain streamlit functions were called
        mock_radio.assert_called_once()
        mock_text_input.assert_called_once()
        mock_selectbox.assert_called_once()
        mock_button.assert_called_once()

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.text_area')
    @patch('streamlit.sidebar.selectbox')
    @patch('streamlit.sidebar.button')
    def test_main_file_content_input(self, mock_button, mock_selectbox, mock_text_area, mock_radio):
        # Test the main function with file content input
        mock_radio.return_value = "File Content"
        mock_text_area.return_value = "print('Hello, World!')"
        mock_selectbox.return_value = "Python"
        mock_button.return_value = True

        with patch('streamlit.spinner'):
            main()

        # Add assertions to check if the main function behaves correctly
        mock_radio.assert_called_once()
        mock_text_area.assert_called_once()
        mock_selectbox.assert_called_once()
        mock_button.assert_called_once()

if __name__ == '__main__':
    unittest.main()
