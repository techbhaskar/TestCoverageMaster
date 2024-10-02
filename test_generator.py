import os
from typing import Dict, Tuple
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tests(code_analysis: Dict, test_analysis: Dict, project_type: str) -> Tuple[str, str]:
    """
    Generate both unit and integration test cases for uncovered functions using AI.
    """
    uncovered_functions = code_analysis['coverage']['uncovered_functions']
    
    unit_tests = []
    integration_tests = []
    
    for func in uncovered_functions:
        if project_type in ['Angular', 'React', 'JavaScript']:
            language = 'JavaScript' if project_type in ['JavaScript', 'React'] else 'TypeScript'
        elif project_type == 'Python':
            language = 'Python'
        elif project_type == 'Java':
            language = 'Java'
        elif project_type == '.NET':
            language = 'C#'
        else:
            language = 'JavaScript'
        
        unit_test = generate_ai_test_case(func, project_type, language, 'unit')
        integration_test = generate_ai_test_case(func, project_type, language, 'integration')
        
        unit_tests.append(unit_test)
        integration_tests.append(integration_test)
    
    return "\n\n".join(unit_tests), "\n\n".join(integration_tests)

def generate_ai_test_case(function_name: str, project_type: str, language: str, test_type: str) -> str:
    """
    Generate a test case for a given function using OpenAI's GPT-3.5-turbo.
    """
    if project_type in ['Angular', 'React', 'JavaScript']:
        framework = "Jest" if test_type == 'unit' else "Cypress"
    elif project_type == 'Python':
        framework = "unittest" if test_type == 'unit' else "pytest"
    elif project_type == 'Java':
        framework = "JUnit"
    elif project_type == '.NET':
        framework = "NUnit"
    else:
        framework = "Jest"

    prompt = f"""
    Generate a {test_type} test case using {framework} for the following {project_type} function in {language}:

    Function name: {function_name}

    The test case should:
    1. Include multiple assertions
    2. Test edge cases
    3. Use mocks or spies if appropriate
    4. Follow best practices for {framework} testing
    5. {"Focus on testing the function's behavior and output" if test_type == 'unit' else "Focus on testing the function's integration with other components, external services, and user interactions"}
    6. {"" if test_type == 'unit' else "Include setup and teardown steps for integration tests"}
    7. {"" if test_type == 'unit' else "Test different scenarios and workflows"}
    8. {"" if test_type == 'unit' else "Verify data persistence and retrieval if applicable"}
    9. {"" if test_type == 'unit' else "Test error handling and recovery in integrated environments"}

    Please provide only the code for the test case, without any explanations.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert test engineer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        generated_test = response.choices[0].message.content.strip()
        return f"// {test_type.capitalize()} Test for {function_name} using {framework}\n{generated_test}"
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
// Integration Test for {function_name} using Cypress
describe('{function_name} - Integration Test', () => {{
  beforeEach(() => {{
    // TODO: Set up any necessary test fixtures or visit the appropriate page
    cy.visit('/your-page');
  }});

  it('should perform expected actions', () => {{
    // TODO: Implement integration test steps
  }});

  it('should handle user interactions', () => {{
    // TODO: Implement user interaction tests
  }});

  it('should integrate with other components', () => {{
    // TODO: Implement integration tests with other components
  }});

  it('should persist and retrieve data correctly', () => {{
    // TODO: Implement data persistence and retrieval tests
  }});

  it('should handle errors and recover in integrated environments', () => {{
    // TODO: Implement error handling and recovery tests
  }});
}});
"""
    elif project_type == 'Python':
        if test_type == 'unit':
            return f"""
# Unit Test for {function_name}
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
# Integration Test for {function_name}
import pytest
from your_app import app, db

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield db
    db.drop_all()

def test_{function_name}_integration(test_client, init_database):
    # TODO: Implement integration test
    response = test_client.get('/your-endpoint')
    assert response.status_code == 200
    assert b'Expected content' in response.data

def test_{function_name}_user_interaction(test_client, init_database):
    # TODO: Implement user interaction test
    response = test_client.post('/your-endpoint', data={{'key': 'value'}})
    assert response.status_code == 200
    assert b'Expected result' in response.data

def test_{function_name}_error_handling(test_client, init_database):
    # TODO: Implement error handling test
    response = test_client.get('/nonexistent-endpoint')
    assert response.status_code == 404

def test_{function_name}_data_persistence(test_client, init_database):
    # TODO: Implement data persistence test
    test_client.post('/create-data', data={{'key': 'value'}})
    response = test_client.get('/retrieve-data')
    assert response.status_code == 200
    assert b'value' in response.data
"""
    elif project_type == 'Java':
        if test_type == 'unit':
            return f"""
// Unit Test for {function_name}
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class {function_name.capitalize()}Test {{

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

    @Test
    void test{function_name.capitalize()}WithMock() {{
        // TODO: Implement test with mock
        when(mockDependency.someMethod()).thenReturn("mocked_value");
        assertEquals("expected_result", classUnderTest.{function_name}());
    }}
}}
"""
        else:
            return f"""
// Integration Test for {function_name}
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.ResponseEntity;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class {function_name.capitalize()}IntegrationTest {{

    @LocalServerPort
    private int port;

    private TestRestTemplate restTemplate;
    private String baseUrl;

    @BeforeEach
    void setUp() {{
        restTemplate = new TestRestTemplate();
        baseUrl = "http://localhost:" + port;
    }}

    @Test
    void test{function_name.capitalize()}Integration() {{
        // TODO: Implement integration test
        ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/your-endpoint", String.class);
        assertEquals(200, response.getStatusCodeValue());
        assertTrue(response.getBody().contains("Expected content"));
    }}

    @Test
    void test{function_name.capitalize()}UserInteraction() {{
        // TODO: Implement user interaction test
        ResponseEntity<String> response = restTemplate.postForEntity(baseUrl + "/your-endpoint", "request body", String.class);
        assertEquals(200, response.getStatusCodeValue());
        assertTrue(response.getBody().contains("Expected result"));
    }}

    @Test
    void test{function_name.capitalize()}ErrorHandling() {{
        // TODO: Implement error handling test
        ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/nonexistent-endpoint", String.class);
        assertEquals(404, response.getStatusCodeValue());
    }}

    @Test
    void test{function_name.capitalize()}DataPersistence() {{
        // TODO: Implement data persistence test
        restTemplate.postForEntity(baseUrl + "/create-data", "{{\"key\": \"value\"}}", String.class);
        ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/retrieve-data", String.class);
        assertEquals(200, response.getStatusCodeValue());
        assertTrue(response.getBody().contains("value"));
    }}

    @AfterEach
    void tearDown() {{
        // TODO: Clean up any resources if needed
    }}
}}
"""
    elif project_type == '.NET':
        if test_type == 'unit':
            return f"""
// Unit Test for {function_name}
using NUnit.Framework;
using Moq;

[TestFixture]
public class {function_name.capitalize()}Tests
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

    [Test]
    public void {function_name}_WithMock()
    {{
        // TODO: Implement test with mock
        _mockDependency.Setup(m => m.SomeMethod()).Returns("mocked_value");
        Assert.AreEqual("expected_result", _classUnderTest.{function_name}());
    }}
}}
"""
        else:
            return f"""
// Integration Test for {function_name}
using NUnit.Framework;
using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;
using YourNamespace;

[TestFixture]
public class {function_name.capitalize()}IntegrationTests
{{
    private WebApplicationFactory<Startup> _factory;
    private HttpClient _client;

    [OneTimeSetUp]
    public void OneTimeSetUp()
    {{
        _factory = new WebApplicationFactory<Startup>();
        _client = _factory.CreateClient();
    }}

    [OneTimeTearDown]
    public void OneTimeTearDown()
    {{
        _client.Dispose();
        _factory.Dispose();
    }}

    [Test]
    public async Task {function_name}_Integration()
    {{
        // TODO: Implement integration test
        var response = await _client.GetAsync("/your-endpoint");
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("Expected content"));
    }}

    [Test]
    public async Task {function_name}_UserInteraction()
    {{
        // TODO: Implement user interaction test
        var requestContent = new StringContent("{{\"key\": \"value\"}}", System.Text.Encoding.UTF8, "application/json");
        var response = await _client.PostAsync("/your-endpoint", requestContent);
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("Expected result"));
    }}

    [Test]
    public async Task {function_name}_ErrorHandling()
    {{
        // TODO: Implement error handling test
        var response = await _client.GetAsync("/nonexistent-endpoint");
        Assert.That(response.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.NotFound));
    }}

    [Test]
    public async Task {function_name}_DataPersistence()
    {{
        // TODO: Implement data persistence test
        var createContent = new StringContent("{{\"key\": \"value\"}}", System.Text.Encoding.UTF8, "application/json");
        await _client.PostAsync("/create-data", createContent);

        var response = await _client.GetAsync("/retrieve-data");
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("value"));
    }}
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

  {{"" if test_type == 'unit' else "test('should handle user interactions', () => {{\n    // TODO: Implement user interaction tests\n  }});"}}

  {{"" if test_type == 'unit' else "test('should persist and retrieve data', () => {{\n    // TODO: Implement data persistence and retrieval tests\n  }});"}}

  {{"" if test_type == 'unit' else "test('should handle errors in integrated environments', () => {{\n    // TODO: Implement error handling and recovery tests\n  }});"}}
}});
"""
