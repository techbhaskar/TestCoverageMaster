# Comprehensive Unit Test Analyzer

This Streamlit-based app provides comprehensive unit test analysis, code coverage, and test case generation for JavaScript, Angular, React, Python, Java, and .NET projects. It now includes OAuth authentication support for Google, Facebook, and GitHub.

## Setup

1. Fork this Replit project to your account.
2. Create a new GitHub repository and connect it to your Replit project:
   - In Replit, go to "Version Control" in the left sidebar.
   - Click on "Create a Git repo" and follow the instructions to connect to your GitHub repository.

3. Set up the Replit token secret in your GitHub repository:
   - Go to your GitHub repository settings.
   - Navigate to "Secrets and variables" > "Actions".
   - Click on "New repository secret".
   - Name: REPLIT_TOKEN
   - Value: Your Replit token (You can find this in your Replit account settings)

4. Set up OAuth API keys:
   - Create OAuth applications in the Google, Facebook, and GitHub developer consoles.
   - In your Replit project, go to the "Secrets" tab in the left sidebar.
   - Add the following secrets with their respective values:
     - GOOGLE_CLIENT_ID
     - GOOGLE_CLIENT_SECRET
     - FACEBOOK_CLIENT_ID
     - FACEBOOK_CLIENT_SECRET
     - GITHUB_CLIENT_ID
     - GITHUB_CLIENT_SECRET

5. Update the REDIRECT_URI in oauth_config.py with your Replit app URL.

6. Push your code to the GitHub repository:
   - In Replit, commit your changes and push them to the connected GitHub repository.

Now, whenever you push changes to the main branch of your GitHub repository, the GitHub Actions workflow will automatically run tests, perform linting, and deploy the updated app to Replit.

## Usage

1. Open the Streamlit app in Replit.
2. Log in using your Google, Facebook, or GitHub account.
3. Choose between entering a file path or pasting file content.
4. Select the project type (JavaScript, Angular, React, Python, Java, or .NET).
5. Click "Analyze Project" to run the analysis.
6. View the results, including code coverage, test quality, and generated test cases.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License.
