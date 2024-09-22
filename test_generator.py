import os
from typing import Dict, List
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tests(code_analysis: Dict, test_analysis: Dict, project_type: str) -> str:
    """
    Generate test cases for uncovered functions using AI.
    """
    uncovered_functions = code_analysis['coverage']['uncovered_functions']
    
    generated_tests = []
    
    for func in uncovered_functions:
        if project_type == 'Angular':
            test_case = generate_ai_test_case(func, project_type, 'TypeScript')
        elif project_type == 'React':
            test_case = generate_ai_test_case(func, project_type, 'JavaScript')
        elif project_type == 'Python':
            test_case = generate_ai_test_case(func, project_type, 'Python')
        else:
            test_case = generate_ai_test_case(func, project_type, 'JavaScript')
        generated_tests.append(test_case)
    
    return '\n\n'.join(generated_tests)

def generate_ai_test_case(function_name: str, project_type: str, language: str) -> str:
    """
    Generate a test case for a given function using OpenAI's GPT-3.
    """
    prompt = f"""
    Generate a complex test case for the following {project_type} function in {language}:

    Function name: {function_name}

    The test case should:
    1. Include multiple assertions
    2. Test edge cases
    3. Use mocks or spies if appropriate
    4. Follow best practices for {project_type} testing

    Please provide only the code for the test case, without any explanations.
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating AI test case: {str(e)}")
        return generate_fallback_test_case(function_name, project_type)

def generate_fallback_test_case(function_name: str, project_type: str) -> str:
    """
    Generate a basic test case when AI generation fails.
    """
    if project_type == 'Angular':
        return f"""
describe('{function_name}', () => {{
  let component: YourComponentName;
  let fixture: ComponentFixture<YourComponentName>;

  beforeEach(async () => {{
    await TestBed.configureTestingModule({{
      declarations: [ YourComponentName ]
    }})
    .compileComponents();
  }});

  beforeEach(() => {{
    fixture = TestBed.createComponent(YourComponentName);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }});

  it('should be defined', () => {{
    expect(component.{function_name}).toBeDefined();
  }});

  it('should handle edge cases', () => {{
    // TODO: Implement edge case tests
  }});

  it('should work with mocks', () => {{
    // TODO: Implement tests with mocks
  }});
}});
"""
    elif project_type == 'Python':
        return f"""
import unittest
from unittest.mock import patch

class Test{function_name.capitalize()}(unittest.TestCase):
    def setUp(self):
        # TODO: Set up any necessary test fixtures
        pass

    def test_{function_name}_basic(self):
        # TODO: Implement basic functionality test
        self.assertTrue({function_name}())

    def test_{function_name}_edge_cases(self):
        # TODO: Implement edge case tests
        pass

    @patch('module.some_dependency')
    def test_{function_name}_with_mock(self, mock_dependency):
        # TODO: Implement test with mock
        mock_dependency.return_value = 'mocked_value'
        self.assertEqual({function_name}(), 'expected_result')

if __name__ == '__main__':
    unittest.main()
"""
    else:
        return f"""
describe('{function_name}', () => {{
  test('should be defined', () => {{
    expect({function_name}).toBeDefined();
  }});

  test('should handle edge cases', () => {{
    // TODO: Implement edge case tests
  }});

  test('should work with mocks', () => {{
    // TODO: Implement tests with mocks
  }});
}});
"""
