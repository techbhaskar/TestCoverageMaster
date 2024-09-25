import os
from typing import Dict, Tuple
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_tests(code_analysis: Dict, test_analysis: Dict, project_type: str, api_key: str = None) -> Tuple[str, str]:
    """
    Generate both unit and functional test cases for uncovered functions using AI.
    """
    # Set up OpenAI API key
    openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    uncovered_functions = code_analysis['coverage']['uncovered_functions']
    
    unit_tests = []
    functional_tests = []
    
    for func in uncovered_functions:
        unit_test = generate_ai_test_case(func, project_type, 'unit')
        functional_test = generate_ai_test_case(func, project_type, 'functional')
        
        unit_tests.append(unit_test)
        functional_tests.append(functional_test)
    
    return "\n\n".join(unit_tests), "\n\n".join(functional_tests)

def generate_ai_test_case(function_name: str, project_type: str, test_type: str) -> str:
    """
    Generate a test case for a given function using OpenAI's GPT-3.
    """
    if project_type in ['Angular', 'React', 'JavaScript']:
        framework = "Jest" if project_type in ['JavaScript', 'React'] else "Jasmine"
        language = 'JavaScript' if project_type in ['JavaScript', 'React'] else 'TypeScript'
    elif project_type == 'Python':
        framework = "unittest"
        language = 'Python'
    elif project_type == 'Java':
        framework = "JUnit"
        language = 'Java'
    elif project_type == '.NET':
        framework = "NUnit"
        language = 'C#'
    else:
        framework = "Jest"
        language = 'JavaScript'

    prompt = f"""
    Generate a {test_type} test case using {framework} for the following {project_type} function in {language}:

    Function name: {function_name}

    The test case should:
    1. Include multiple assertions
    2. Test edge cases
    3. Use mocks or spies if appropriate
    4. Follow best practices for {framework} testing
    5. {"Focus on testing the function's behavior and output" if test_type == 'unit' else "Focus on testing the function's integration with other components and user interactions"}

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

        generated_test = response.choices[0].text.strip()
        return f"// {test_type.capitalize()} Test for {function_name} using {framework}\n{generated_test}"
    except openai.error.RateLimitError:
        print("OpenAI API rate limit exceeded. Retrying...")
        raise
    except Exception as e:
        print(f"Error generating AI test case: {str(e)}")
        return generate_fallback_test_case(function_name, project_type, test_type)

def generate_fallback_test_case(function_name: str, project_type: str, test_type: str) -> str:
    """
    Generate a basic test case when AI generation fails.
    """
    if project_type in ['Angular', 'React', 'JavaScript']:
        if test_type == 'unit':
            return f"""
// Unit Test for {function_name} using Jest
describe('{function_name}', () => {{
  test('should be defined', () => {{
    expect({function_name}).toBeDefined();
  }});

  test('should handle basic functionality', () => {{
    // TODO: Implement basic functionality test
  }});

  test('should handle edge cases', () => {{
    // TODO: Implement edge case tests
  }});

  test('should work with mocks', () => {{
    // TODO: Implement tests with mocks
  }});
}});
"""
        else:
            return f"""
// Functional Test for {function_name} using Cypress
describe('{function_name} - Functional Test', () => {{
  beforeEach(() => {{
    // TODO: Set up any necessary test fixtures or visit the appropriate page
    // cy.visit('/your-page');
  }});

  it('should perform expected actions', () => {{
    // TODO: Implement functional test steps
  }});

  it('should handle user interactions', () => {{
    // TODO: Implement user interaction tests
  }});

  it('should integrate with other components', () => {{
    // TODO: Implement integration tests
  }});
}});
"""
    elif project_type == 'Python':
        return f"""
# {test_type.capitalize()} Test for {function_name}
import unittest
from unittest.mock import patch

class Test{function_name.capitalize()}_{test_type.capitalize()}(unittest.TestCase):
    def setUp(self):
        # TODO: Set up any necessary test fixtures
        pass

    def test_{function_name}_basic(self):
        # TODO: Implement basic functionality test
        self.assertTrue({function_name}())

    def test_{function_name}_edge_cases(self):
        # TODO: Implement edge case tests
        pass

    {{"@patch('module.some_dependency')\n    def test_{function_name}_with_mock(self, mock_dependency):\n        # TODO: Implement test with mock\n        mock_dependency.return_value = 'mocked_value'\n        self.assertEqual({function_name}(), 'expected_result')" if test_type == 'unit' else f"def test_{function_name}_integration(self):\n        # TODO: Implement integration test\n        pass"}}

if __name__ == '__main__':
    unittest.main()
"""
    elif project_type == 'Java':
        return f"""
// {test_type.capitalize()} Test for {function_name}
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class {function_name.capitalize()}_{test_type.capitalize()}Test {{

    @Mock
    private SomeDependency mockDependency;

    @InjectMocks
    private YourClass classUnderTest;

    @BeforeEach
    void setUp() {{
        // TODO: Set up any necessary test fixtures
    }}

    @Test
    void test{function_name.capitalize()}Basic() {{
        // TODO: Implement basic functionality test
        assertTrue(classUnderTest.{function_name}());
    }}

    @Test
    void test{function_name.capitalize()}EdgeCases() {{
        // TODO: Implement edge case tests
    }}

    {{"@Test\n    void test{function_name.capitalize()}WithMock() {{\n        // TODO: Implement test with mock\n        when(mockDependency.someMethod()).thenReturn(\"mocked_value\");\n        assertEquals(\"expected_result\", classUnderTest.{function_name}());\n    }}" if test_type == 'unit' else f"@Test\n    void test{function_name.capitalize()}Integration() {{\n        // TODO: Implement integration test\n    }}"}}
}}
"""
    elif project_type == '.NET':
        return f"""
// {test_type.capitalize()} Test for {function_name}
using NUnit.Framework;
using Moq;

[TestFixture]
public class {function_name.capitalize()}_{test_type.capitalize()}Tests
{{
    private Mock<ISomeDependency> _mockDependency;
    private YourClass _classUnderTest;

    [SetUp]
    public void Setup()
    {{
        _mockDependency = new Mock<ISomeDependency>();
        _classUnderTest = new YourClass(_mockDependency.Object);
    }}

    [Test]
    public void {function_name}_Basic()
    {{
        // TODO: Implement basic functionality test
        Assert.IsTrue(_classUnderTest.{function_name}());
    }}

    [Test]
    public void {function_name}_EdgeCases()
    {{
        // TODO: Implement edge case tests
    }}

    {{"[Test]\n    public void {function_name}_WithMock()\n    {{\n        // TODO: Implement test with mock\n        _mockDependency.Setup(m => m.SomeMethod()).Returns(\"mocked_value\");\n        Assert.AreEqual(\"expected_result\", _classUnderTest.{function_name}());\n    }}" if test_type == 'unit' else f"[Test]\n    public void {function_name}_Integration()\n    {{\n        // TODO: Implement integration test\n    }}"}}
}}
"""
    else:
        return f"""
// {test_type.capitalize()} Test for {function_name}
describe('{function_name} - {test_type.capitalize()} Test', () => {{
  test('should be defined', () => {{
    expect({function_name}).toBeDefined();
  }});

  test('should handle edge cases', () => {{
    // TODO: Implement edge case tests
  }});

  {{"test('should work with mocks', () => {{\n    // TODO: Implement tests with mocks\n  }});" if test_type == 'unit' else "test('should integrate with other components', () => {{\n    // TODO: Implement integration tests\n  }});"}}
}});
"""