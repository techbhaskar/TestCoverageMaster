import os
from typing import Dict, Tuple
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        response = client.chat.completions.create(
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
  let mockDependency;

  beforeEach(() => {{
    mockDependency = jest.fn();
  }});

  test('should be defined', () => {{
    expect({function_name}).toBeDefined();
  }});

  test('should handle basic functionality', () => {{
    const result = {function_name}('test input');
    expect(result).toBe('expected output');
  }});

  test('should handle edge cases', () => {{
    expect({function_name}('')).toBe('empty input handled');
    expect({function_name}(null)).toBe('null input handled');
  }});

  test('should work with mocks', () => {{
    mockDependency.mockReturnValue('mocked value');
    const result = {function_name}(mockDependency);
    expect(mockDependency).toHaveBeenCalled();
    expect(result).toBe('expected output with mock');
  }});
}});
"""
        else:
            return f"""
// Integration Test for {function_name} using Cypress
describe('{function_name} - Integration Test', () => {{
  beforeEach(() => {{
    cy.visit('/test-page');
    cy.intercept('GET', '/api/data', {{ fixture: 'testData.json' }}).as('getData');
  }});

  it('should perform expected actions', () => {{
    cy.get('#inputField').type('test input');
    cy.get('#submitButton').click();
    cy.wait('@getData');
    cy.get('#result').should('contain', 'Expected output');
  }});

  it('should handle user interactions', () => {{
    cy.get('#dropdown').select('option1');
    cy.get('#checkbox').check();
    cy.get('#submitForm').click();
    cy.get('#formResult').should('contain', 'Form submitted successfully');
  }});

  it('should integrate with other components', () => {{
    cy.get('#componentA').should('be.visible');
    cy.get('#triggerIntegration').click();
    cy.get('#componentB').should('contain', 'Integration successful');
  }});

  it('should persist and retrieve data correctly', () => {{
    const testData = {{ key: 'value' }};
    cy.window().then((win) => {{
      win.localStorage.setItem('testData', JSON.stringify(testData));
    }});
    cy.reload();
    cy.window().its('localStorage.testData').should('eq', JSON.stringify(testData));
  }});

  it('should handle errors and recover in integrated environments', () => {{
    cy.intercept('GET', '/api/data', {{ statusCode: 500 }}).as('getDataError');
    cy.get('#fetchData').click();
    cy.get('#errorMessage').should('be.visible');
    cy.get('#retryButton').click();
    cy.wait('@getData');
    cy.get('#result').should('contain', 'Data fetched successfully');
  }});
}});
"""
    elif project_type == 'Python':
        if test_type == 'unit':
            return f"""
# Unit Test for {function_name}
import unittest
from unittest.mock import patch, MagicMock

class Test{function_name.capitalize()}(unittest.TestCase):
    def setUp(self):
        self.mock_dependency = MagicMock()

    def test_{function_name}_basic(self):
        result = {function_name}('test input')
        self.assertEqual(result, 'expected output')

    def test_{function_name}_edge_cases(self):
        self.assertEqual({function_name}(''), 'empty input handled')
        self.assertEqual({function_name}(None), 'null input handled')

    @patch('module.some_dependency')
    def test_{function_name}_with_mock(self, mock_dependency):
        mock_dependency.return_value = 'mocked value'
        result = {function_name}(mock_dependency)
        mock_dependency.assert_called_once()
        self.assertEqual(result, 'expected output with mock')

if __name__ == '__main__':
    unittest.main()
"""
        else:
            return f"""
# Integration Test for {function_name}
import pytest
from your_app import app, db
from your_app.models import User, Product

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='module')
def init_database(test_client):
    user = User(username='testuser', email='test@example.com')
    product = Product(name='Test Product', price=9.99)
    db.session.add(user)
    db.session.add(product)
    db.session.commit()
    yield

def test_{function_name}_integration(test_client, init_database):
    response = test_client.get('/api/{function_name}')
    assert response.status_code == 200
    assert b'Expected content' in response.data

def test_{function_name}_user_interaction(test_client, init_database):
    response = test_client.post('/api/{function_name}', json={{'key': 'value'}})
    assert response.status_code == 200
    assert b'Success' in response.data

def test_{function_name}_data_persistence(test_client, init_database):
    response = test_client.post('/api/create_product', json={{'name': 'New Product', 'price': 19.99}})
    assert response.status_code == 201
    
    response = test_client.get('/api/products')
    assert response.status_code == 200
    assert b'New Product' in response.data

def test_{function_name}_error_handling(test_client, init_database):
    response = test_client.get('/api/nonexistent')
    assert response.status_code == 404
    
    response = test_client.post('/api/{function_name}', json={{'invalid': 'data'}})
    assert response.status_code == 400
    assert b'Error' in response.data

def test_{function_name}_integration_workflow(test_client, init_database):
    # Step 1: Create a new user
    response = test_client.post('/api/register', json={{'username': 'newuser', 'email': 'new@example.com', 'password': 'password123'}})
    assert response.status_code == 201
    
    # Step 2: Log in
    response = test_client.post('/api/login', json={{'username': 'newuser', 'password': 'password123'}})
    assert response.status_code == 200
    token = response.json['token']
    
    # Step 3: Create a new product (authenticated)
    headers = {{'Authorization': f'Bearer {{token}}'}}
    response = test_client.post('/api/create_product', json={{'name': 'User Product', 'price': 29.99}}, headers=headers)
    assert response.status_code == 201
    
    # Step 4: Verify the product was created
    response = test_client.get('/api/products')
    assert response.status_code == 200
    assert b'User Product' in response.data
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
        mockDependency = mock(SomeDependency.class);
        classUnderTest = new YourClass(mockDependency);
    }}

    @Test
    void test{function_name.capitalize()}Basic() {{
        String result = classUnderTest.{function_name}("test input");
        assertEquals("expected output", result);
    }}

    @Test
    void test{function_name.capitalize()}EdgeCases() {{
        assertEquals("empty input handled", classUnderTest.{function_name}(""));
        assertEquals("null input handled", classUnderTest.{function_name}(null));
    }}

    @Test
    void test{function_name.capitalize()}WithMock() {{
        when(mockDependency.someMethod()).thenReturn("mocked value");
        String result = classUnderTest.{function_name}("test input");
        verify(mockDependency).someMethod();
        assertEquals("expected output with mock", result);
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
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
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
        ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/api/{function_name}", String.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(response.getBody().contains("Expected content"));
    }}

    @Test
    void test{function_name.capitalize()}UserInteraction() {{
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");
        HttpEntity<String> request = new HttpEntity<>("{{\"key\": \"value\"}}", headers);
        
        ResponseEntity<String> response = restTemplate.postForEntity(baseUrl + "/api/{function_name}", request, String.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertTrue(response.getBody().contains("Success"));
    }}

    @Test
    void test{function_name.capitalize()}DataPersistence() {{
        // Create a new product
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");
        HttpEntity<String> request = new HttpEntity<>("{{\"name\": \"New Product\", \"price\": 19.99}}", headers);
        
        ResponseEntity<String> createResponse = restTemplate.postForEntity(baseUrl + "/api/create_product", request, String.class);
        assertEquals(HttpStatus.CREATED, createResponse.getStatusCode());
        
        // Verify the product was created
        ResponseEntity<String> getResponse = restTemplate.getForEntity(baseUrl + "/api/products", String.class);
        assertEquals(HttpStatus.OK, getResponse.getStatusCode());
        assertTrue(getResponse.getBody().contains("New Product"));
    }}

    @Test
    void test{function_name.capitalize()}ErrorHandling() {{
        ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/api/nonexistent", String.class);
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");
        HttpEntity<String> request = new HttpEntity<>("{{\"invalid\": \"data\"}}", headers);
        
        ResponseEntity<String> errorResponse = restTemplate.postForEntity(baseUrl + "/api/{function_name}", request, String.class);
        assertEquals(HttpStatus.BAD_REQUEST, errorResponse.getStatusCode());
        assertTrue(errorResponse.getBody().contains("Error"));
    }}

    @Test
    void test{function_name.capitalize()}IntegrationWorkflow() {{
        // Step 1: Register a new user
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");
        HttpEntity<String> registerRequest = new HttpEntity<>("{{\"username\": \"newuser\", \"email\": \"new@example.com\", \"password\": \"password123\"}}", headers);
        
        ResponseEntity<String> registerResponse = restTemplate.postForEntity(baseUrl + "/api/register", registerRequest, String.class);
        assertEquals(HttpStatus.CREATED, registerResponse.getStatusCode());
        
        // Step 2: Log in
        HttpEntity<String> loginRequest = new HttpEntity<>("{{\"username\": \"newuser\", \"password\": \"password123\"}}", headers);
        ResponseEntity<String> loginResponse = restTemplate.postForEntity(baseUrl + "/api/login", loginRequest, String.class);
        assertEquals(HttpStatus.OK, loginResponse.getStatusCode());
        String token = loginResponse.getBody(); // Assume the body contains the token
        
        // Step 3: Create a new product (authenticated)
        headers.set("Authorization", "Bearer " + token);
        HttpEntity<String> createProductRequest = new HttpEntity<>("{{\"name\": \"User Product\", \"price\": 29.99}}", headers);
        ResponseEntity<String> createProductResponse = restTemplate.postForEntity(baseUrl + "/api/create_product", createProductRequest, String.class);
        assertEquals(HttpStatus.CREATED, createProductResponse.getStatusCode());
        
        // Step 4: Verify the product was created
        ResponseEntity<String> getProductsResponse = restTemplate.getForEntity(baseUrl + "/api/products", String.class);
        assertEquals(HttpStatus.OK, getProductsResponse.getStatusCode());
        assertTrue(getProductsResponse.getBody().contains("User Product"));
    }}

    @AfterEach
    void tearDown() {{
        // Clean up test data if needed
    }}
}}
"""
    elif project_type == '.NET':
        if test_type == 'unit':
            return f"""
// Unit Test for {function_name}
using NUnit.Framework;
using Moq;
using YourNamespace;

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
        var result = _classUnderTest.{function_name}("test input");
        Assert.AreEqual("expected output", result);
    }}

    [Test]
    public void {function_name}_EdgeCases()
    {{
        Assert.AreEqual("empty input handled", _classUnderTest.{function_name}(""));
        Assert.AreEqual("null input handled", _classUnderTest.{function_name}(null));
    }}

    [Test]
    public void {function_name}_WithMock()
    {{
        _mockDependency.Setup(m => m.SomeMethod()).Returns("mocked value");
        var result = _classUnderTest.{function_name}("test input");
        _mockDependency.Verify(m => m.SomeMethod(), Times.Once);
        Assert.AreEqual("expected output with mock", result);
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
using System.Text;

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
        var response = await _client.GetAsync("/api/{function_name}");
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("Expected content"));
    }}

    [Test]
    public async Task {function_name}_UserInteraction()
    {{
        var requestContent = new StringContent("{{\"key\": \"value\"}}", Encoding.UTF8, "application/json");
        var response = await _client.PostAsync("/api/{function_name}", requestContent);
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("Success"));
    }}

    [Test]
    public async Task {function_name}_DataPersistence()
    {{
        // Create a new product
        var createContent = new StringContent("{{\"name\": \"New Product\", \"price\": 19.99}}", Encoding.UTF8, "application/json");
        var createResponse = await _client.PostAsync("/api/create_product", createContent);
        createResponse.EnsureSuccessStatusCode();

        // Verify the product was created
        var getResponse = await _client.GetAsync("/api/products");
        getResponse.EnsureSuccessStatusCode();
        var content = await getResponse.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("New Product"));
    }}

    [Test]
    public async Task {function_name}_ErrorHandling()
    {{
        var response = await _client.GetAsync("/api/nonexistent");
        Assert.That(response.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.NotFound));

        var errorContent = new StringContent("{{\"invalid\": \"data\"}}", Encoding.UTF8, "application/json");
        var errorResponse = await _client.PostAsync("/api/{function_name}", errorContent);
        Assert.That(errorResponse.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.BadRequest));
        var content = await errorResponse.Content.ReadAsStringAsync();
        Assert.That(content, Does.Contain("Error"));
    }}

    [Test]
    public async Task {function_name}_IntegrationWorkflow()
    {{
        // Step 1: Register a new user
        var registerContent = new StringContent("{{\"username\": \"newuser\", \"email\": \"new@example.com\", \"password\": \"password123\"}}", Encoding.UTF8, "application/json");
        var registerResponse = await _client.PostAsync("/api/register", registerContent);
        Assert.That(registerResponse.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.Created));

        // Step 2: Log in
        var loginContent = new StringContent("{{\"username\": \"newuser\", \"password\": \"password123\"}}", Encoding.UTF8, "application/json");
        var loginResponse = await _client.PostAsync("/api/login", loginContent);
        Assert.That(loginResponse.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.OK));
        var loginResult = await loginResponse.Content.ReadAsStringAsync();
        var token = JsonConvert.DeserializeObject<dynamic>(loginResult).token.ToString();

        // Step 3: Create a new product (authenticated)
        var createProductContent = new StringContent("{{\"name\": \"User Product\", \"price\": 29.99}}", Encoding.UTF8, "application/json");
        _client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
        var createProductResponse = await _client.PostAsync("/api/create_product", createProductContent);
        Assert.That(createProductResponse.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.Created));

        // Step 4: Verify the product was created
        var getProductsResponse = await _client.GetAsync("/api/products");
        Assert.That(getProductsResponse.StatusCode, Is.EqualTo(System.Net.HttpStatusCode.OK));
        var productsContent = await getProductsResponse.Content.ReadAsStringAsync();
        Assert.That(productsContent, Does.Contain("User Product"));
    }}
}}
"""
    else:
        return f"""
// {test_type.capitalize()} Test for {function_name}
describe('{function_name} - {test_type.capitalize()} Test', () => {{
  let mockDependency;

  beforeEach(() => {{
    mockDependency = jest.fn();
  }});

  test('should be defined', () => {{
    expect({function_name}).toBeDefined();
  }});

  test('should handle basic functionality', () => {{
    const result = {function_name}('test input');
    expect(result).toBe('expected output');
  }});

  test('should handle edge cases', () => {{
    expect({function_name}('')).toBe('empty input handled');
    expect({function_name}(null)).toBe('null input handled');
  }});

  test('should work with mocks', () => {{
    mockDependency.mockReturnValue('mocked value');
    const result = {function_name}(mockDependency);
    expect(mockDependency).toHaveBeenCalled();
    expect(result).toBe('expected output with mock');
  }});

  test('should integrate with other components', () => {{
    // Setup mock API
    jest.spyOn(global, 'fetch').mockResolvedValue({{
      json: jest.fn().mockResolvedValue({{ data: 'test data' }}),
    }});

    // Test integration
    return {function_name}()
      .then(result => {{
        expect(result).toBe('integrated result');
        expect(fetch).toHaveBeenCalledWith('/api/data');
      }});
  }});

  test('should handle user interactions', () => {{
    const mockCallback = jest.fn();
    const wrapper = mount(<YourComponent onAction={{mockCallback}} />);
    wrapper.find('button').simulate('click');
    expect(mockCallback).toHaveBeenCalled();
  }});

  test('should persist and retrieve data', () => {{
    const testData = {{ key: 'value' }};
    localStorage.setItem('testData', JSON.stringify(testData));
    const result = {function_name}();
    expect(result).toEqual(testData);
  }});

  test('should handle errors in integrated environments', () => {{
    jest.spyOn(global, 'fetch').mockRejectedValue(new Error('API Error'));
    return {function_name}()
      .catch(error => {{
        expect(error.message).toBe('API Error');
      }});
  }});
}});
"""
