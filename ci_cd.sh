#!/bin/bash

echo "Starting CI/CD pipeline..."

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m unittest discover -v

# Run linter (assuming we're using flake8)
echo "Running linter..."
flake8 .

# Run the application (this will restart the Streamlit app)
echo "Restarting the application..."
pkill streamlit
streamlit run main.py --server.port 5000 &

echo "CI/CD pipeline completed."
