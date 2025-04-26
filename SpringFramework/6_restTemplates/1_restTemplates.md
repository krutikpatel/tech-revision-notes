# Spring REST Templates for HTTP Calls 🌐

This guide will help you understand how to make HTTP calls in Spring using RestTemplate, with practical examples and interview-focused insights.

## 1. 🔍 Introduction to REST Templates
---------

RestTemplate is Spring's central class for synchronous client-side HTTP communication. It simplifies the process of making HTTP requests to REST APIs by handling details like:

- Connection management
- Request/response marshalling
- HTTP headers and methods
- Error handling

### Where RestTemplate Fits in Spring:

```
┌─────────────────────────────────────────┐
│           Spring Application            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐        ┌────────────┐  │
│  │   Service   │───────►│RestTemplate│──┼──► External APIs
│  │    Layer    │        └────────────┘  │
│  └─────────────┘                        │
│                                         │
└─────────────────────────────────────────┘
```

📌 **Key Insight**: While RestTemplate has been the standard for many years, it's now in maintenance mode. Spring recommends WebClient (reactive approach) for new applications, but RestTemplate is still widely used.

✅ **Interview Tip**: Mention that you're aware RestTemplate is in maintenance mode, but it's still important to understand as it's used in many existing Spring applications.

## 2. 📊 Important Classes & Components
---------

RestTemplate is built on several key classes that work together to provide HTTP functionality:

### Core Classes:

1. **RestTemplate**: Main class that provides methods for HTTP operations
2. **HttpMessageConverter**: Converts HTTP requests/responses to/from Java objects
3. **ClientHttpRequestFactory**: Creates ClientHttpRequest objects
4. **ClientHttpRequest**: Represents an HTTP request
5. **ClientHttpResponse**: Represents an HTTP response
6. **ResponseErrorHandler**: Handles errors in HTTP responses
7. **ResponseExtractor**: Extracts data from HTTP responses

### Class Relationships:

```
RestTemplate
    │
    ├── HttpMessageConverters
    │       (JSON, XML, Form, etc.)
    │
    ├── ClientHttpRequestFactory
    │       (SimpleClientHttpRequestFactory, 
    │        HttpComponentsClientHttpRequestFactory, etc.)
    │
    ├── ResponseErrorHandler
    │       (DefaultResponseErrorHandler)
    │
    └── ResponseExtractor
```

📌 **Important Class Hierarchy**:

- RestTemplate delegates to HttpMessageConverters for marshalling/unmarshalling
- RestTemplate uses ClientHttpRequestFactory to create actual HTTP requests
- Different RequestFactory implementations provide different capabilities:
  - SimpleClientHttpRequestFactory: JDK HttpURLConnection
  - HttpComponentsClientHttpRequestFactory: Apache HttpComponents
  - OkHttp3ClientHttpRequestFactory: OkHttp

✅ **Interview Insight**: Understanding these components shows depth of knowledge beyond just using the RestTemplate API.

## 3. ⚙️ Setting Up RestTemplate
---------

### Basic Configuration:

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

### Advanced Configuration with Timeouts:

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        // Create a custom HttpClient with timeouts
        HttpComponentsClientHttpRequestFactory factory = 
            new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(5000); // 5 seconds
        factory.setReadTimeout(5000);   // 5 seconds
        
        // Create RestTemplate with custom request factory
        RestTemplate restTemplate = new RestTemplate(factory);
        
        // Add message converters if needed
        restTemplate.getMessageConverters().add(
            new MappingJackson2HttpMessageConverter());
        
        // Set custom error handler if needed
        restTemplate.setErrorHandler(new CustomResponseErrorHandler());
        
        return restTemplate;
    }
}
```

### Adding Interceptors for Authentication:

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        
        // Add interceptor for authentication headers
        restTemplate.getInterceptors().add((request, body, execution) -> {
            request.getHeaders().add("Authorization", "Bearer " + getToken());
            return execution.execute(request, body);
        });
        
        return restTemplate;
    }
    
    private String getToken() {
        // Implementation to get your auth token
        return "your-auth-token";
    }
}
```

❌ **Common Mistake**: Not configuring timeouts, which can lead to resource leaks if external services are slow or unresponsive.

✅ **Best Practice**: Configure appropriate timeouts and create a bean to reuse the RestTemplate across your application.

## 4. 📝 Basic HTTP Operations
---------

RestTemplate provides numerous methods for different HTTP operations:

### GET Request:

```java
// Simple GET for an object
User user = restTemplate.getForObject(
    "https://api.example.com/users/{id}", 
    User.class, 
    123);  // Path variable

// GET with ResponseEntity to access headers and status code
ResponseEntity<User> response = restTemplate.getForEntity(
    "https://api.example.com/users/{id}", 
    User.class, 
    123);
User user = response.getBody();
HttpStatus status = response.getStatusCode();
HttpHeaders headers = response.getHeaders();

// GET with query parameters
String url = "https://api.example.com/users?name={name}&active={active}";
Map<String, String> params = new HashMap<>();
params.put("name", "John");
params.put("active", "true");
User[] users = restTemplate.getForObject(url, User[].class, params);
```

### POST Request:

```java
// Simple POST
User newUser = new User("John", "john@example.com");
User createdUser = restTemplate.postForObject(
    "https://api.example.com/users", 
    newUser,  // Request body
    User.class);

// POST with response headers (to get Location header)
URI location = restTemplate.postForLocation(
    "https://api.example.com/users", 
    newUser);

// POST with full response
ResponseEntity<User> response = restTemplate.postForEntity(
    "https://api.example.com/users", 
    newUser, 
    User.class);
```

### PUT Request:

```java
User updatedUser = new User("John", "john_updated@example.com");
// PUT doesn't return a response body by default
restTemplate.put(
    "https://api.example.com/users/{id}", 
    updatedUser, 
    123);
```

### DELETE Request:

```java
// Simple DELETE
restTemplate.delete("https://api.example.com/users/{id}", 123);
```

### PATCH Request:

```java
// PATCH (using exchange)
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);

// Only include fields to update
Map<String, Object> patchFields = new HashMap<>();
patchFields.put("email", "john_updated@example.com");

HttpEntity<Map<String, Object>> requestEntity = 
    new HttpEntity<>(patchFields, headers);

ResponseEntity<User> response = restTemplate.exchange(
    "https://api.example.com/users/{id}",
    HttpMethod.PATCH,
    requestEntity,
    User.class,
    123);
```

✅ **Interview Tip**: Know the different response handling methods (getForObject vs. getForEntity) and when to use each one.

## 5. 🛡️ Error Handling
---------

RestTemplate provides mechanisms for handling HTTP errors:

### Default Error Handling:

By default, RestTemplate throws exceptions for 4xx and 5xx responses:

- **HttpClientErrorException**: For 4xx client errors (404, 400, etc.)
- **HttpServerErrorException**: For 5xx server errors (500, 503, etc.)
- **UnknownHttpStatusCodeException**: For undefined status codes

### Custom Error Handler:

```java
public class CustomResponseErrorHandler implements ResponseErrorHandler {

    @Override
    public boolean hasError(ClientHttpResponse response) throws IOException {
        return response.getStatusCode().series() == 
               HttpStatus.Series.CLIENT_ERROR || 
               response.getStatusCode().series() == 
               HttpStatus.Series.SERVER_ERROR;
    }

    @Override
    public void handleError(ClientHttpResponse response) throws IOException {
        if (response.getStatusCode().series() == HttpStatus.Series.SERVER_ERROR) {
            // Handle 5xx errors
            throw new ServerApiException(
                "Server error: " + response.getStatusCode(), 
                response.getStatusCode());
        } else if (response.getStatusCode().series() == HttpStatus.Series.CLIENT_ERROR) {
            // Handle 4xx errors
            if (response.getStatusCode() == HttpStatus.NOT_FOUND) {
                throw new ResourceNotFoundException("Resource not found");
            } else if (response.getStatusCode() == HttpStatus.UNAUTHORIZED) {
                throw new UnauthorizedException("Authentication failed");
            }
            throw new ClientApiException(
                "Client error: " + response.getStatusCode(), 
                response.getStatusCode());
        }
    }
}
```

### Using the Custom Error Handler:

```java
RestTemplate restTemplate = new RestTemplate();
restTemplate.setErrorHandler(new CustomResponseErrorHandler());

try {
    User user = restTemplate.getForObject(
        "https://api.example.com/users/{id}", 
        User.class, 
        999);  // Non-existent ID
} catch (ResourceNotFoundException ex) {
    log.error("User not found", ex);
    // Handle 404 specifically
} catch (UnauthorizedException ex) {
    log.error("Authentication failed", ex);
    // Handle 401 specifically
} catch (ClientApiException ex) {
    log.error("Client error: {}", ex.getStatusCode(), ex);
    // Handle other 4xx errors
} catch (ServerApiException ex) {
    log.error("Server error: {}", ex.getStatusCode(), ex);
    // Handle 5xx errors
}
```

❌ **Common Mistake**: Not handling specific HTTP status codes appropriately, leading to poor error messages or incorrect recovery logic.

✅ **Best Practice**: Create custom exceptions for different error scenarios to make error handling more meaningful.

## 6. 🔄 Advanced Usage
---------

### Exchange Method for Full Control:

The `exchange()` method provides the most flexibility for complex HTTP requests:

```java
// Set headers
HttpHeaders headers = new HttpHeaders();
headers.set("Accept", MediaType.APPLICATION_JSON_VALUE);
headers.set("Custom-Header", "value");

// Create request entity with body and headers
HttpEntity<User> requestEntity = new HttpEntity<>(user, headers);

// Execute request with full control
ResponseEntity<User> response = restTemplate.exchange(
    "https://api.example.com/users/{id}",
    HttpMethod.PUT,
    requestEntity,
    User.class,
    123);

// Access response
HttpStatus status = response.getStatusCode();
HttpHeaders responseHeaders = response.getHeaders();
User updatedUser = response.getBody();
```

### Using UriComponentsBuilder for Complex URLs:

```java
// Build complex URLs with UriComponentsBuilder
UriComponentsBuilder builder = UriComponentsBuilder
    .fromHttpUrl("https://api.example.com/users")
    .queryParam("name", "John")
    .queryParam("active", true)
    .queryParam("department", "IT");

// Execute request with built URL
User[] users = restTemplate.getForObject(
    builder.toUriString(), 
    User[].class);
```

### Handling Generic Types (e.g., List<User>):

```java
// Create a ParameterizedTypeReference for generic types
ParameterizedTypeReference<List<User>> responseType = 
    new ParameterizedTypeReference<List<User>>() {};

// Use exchange method with the type reference
ResponseEntity<List<User>> response = restTemplate.exchange(
    "https://api.example.com/users",
    HttpMethod.GET,
    null,  // No request body
    responseType);

List<User> users = response.getBody();
```

✅ **Interview Insight**: Using exchange() with ParameterizedTypeReference is a key technique for working with generic types, which is a common interview topic.

## 7. 🧪 Testing with RestTemplate
---------

### Mocking RestTemplate in Unit Tests:

```java
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @Mock
    private RestTemplate restTemplate;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    public void testGetUserById() {
        // Setup mock response
        User mockUser = new User(1L, "Test User", "test@example.com");
        when(restTemplate.getForObject(
            anyString(), 
            eq(User.class), 
            eq(1L))).thenReturn(mockUser);
        
        // Call service method
        User result = userService.getUserById(1L);
        
        // Verify
        assertNotNull(result);
        assertEquals("Test User", result.getName());
        assertEquals("test@example.com", result.getEmail());
        
        // Verify RestTemplate was called correctly
        verify(restTemplate).getForObject(
            eq("https://api.example.com/users/{id}"), 
            eq(User.class), 
            eq(1L));
    }
    
    @Test
    public void testGetUserById_NotFound() {
        // Setup mock to throw exception
        when(restTemplate.getForObject(
            anyString(), 
            eq(User.class), 
            eq(999L))).thenThrow(
                new HttpClientErrorException(HttpStatus.NOT_FOUND));
        
        // Verify exception is thrown
        assertThrows(ResourceNotFoundException.class, () -> {
            userService.getUserById(999L);
        });
    }
}
```

### Integration Testing with MockRestServiceServer:

```java
@SpringBootTest
public class UserServiceIntegrationTest {

    @Autowired
    private RestTemplate restTemplate;
    
    @Autowired
    private UserService userService;
    
    private MockRestServiceServer mockServer;
    
    @BeforeEach
    public void setup() {
        mockServer = MockRestServiceServer.createServer(restTemplate);
    }
    
    @Test
    public void testGetUserById() {
        // Setup mock server expectations
        mockServer.expect(requestTo("https://api.example.com/users/1"))
                 .andExpect(method(HttpMethod.GET))
                 .andRespond(withStatus(HttpStatus.OK)
                     .contentType(MediaType.APPLICATION_JSON)
                     .body("{\"id\":1,\"name\":\"Test User\",\"email\":\"test@example.com\"}"));
        
        // Call service method
        User result = userService.getUserById(1L);
        
        // Verify
        assertEquals("Test User", result.getName());
        
        // Verify all expectations were met
        mockServer.verify();
    }
    
    @Test
    public void testCreateUser() {
        // Setup mock server expectations
        mockServer.expect(requestTo("https://api.example.com/users"))
                 .andExpect(method(HttpMethod.POST))
                 .andExpect(content().json("{\"name\":\"New User\",\"email\":\"new@example.com\"}"))
                 .andRespond(withStatus(HttpStatus.CREATED)
                     .contentType(MediaType.APPLICATION_JSON)
                     .body("{\"id\":2,\"name\":\"New User\",\"email\":\"new@example.com\"}"));
        
        // Create user object
        User newUser = new User(null, "New User", "new@example.com");
        
        // Call service method
        User result = userService.createUser(newUser);
        
        // Verify
        assertEquals(2L, result.getId());
        assertEquals("New User", result.getName());
        
        // Verify all expectations were met
        mockServer.verify();
    }
}
```

✅ **Best Practice**: Use MockRestServiceServer for testing classes that use RestTemplate without making actual HTTP calls.

## 8. 🔧 RestTemplate Customization
---------

### Adding Custom HttpMessageConverters:

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        
        // Get the existing converters
        List<HttpMessageConverter<?>> converters = 
            restTemplate.getMessageConverters();
            
        // Add a custom XML converter
        converters.add(new MarshallingHttpMessageConverter(jaxbMarshaller()));
        
        // Add a custom JSON converter with specific ObjectMapper
        converters.add(new MappingJackson2HttpMessageConverter(customObjectMapper()));
        
        return restTemplate;
    }
    
    @Bean
    public Jaxb2Marshaller jaxbMarshaller() {
        Jaxb2Marshaller marshaller = new Jaxb2Marshaller();
        marshaller.setPackagesToScan("com.example.model");
        return marshaller;
    }
    
    @Bean
    public ObjectMapper customObjectMapper() {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return objectMapper;
    }
}
```

### Adding Logging Interceptor:

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        
        // Add logging interceptor
        restTemplate.getInterceptors().add(new LoggingInterceptor());
        
        return restTemplate;
    }
}

public class LoggingInterceptor implements ClientHttpRequestInterceptor {

    private static final Logger log = LoggerFactory.getLogger(LoggingInterceptor.class);

    @Override
    public ClientHttpResponse intercept(
            HttpRequest request, 
            byte[] body, 
            ClientHttpRequestExecution execution) throws IOException {
        
        // Log request
        log.info("Request: {} {}", request.getMethod(), request.getURI());
        log.debug("Request Headers: {}", request.getHeaders());
        
        if (body.length > 0) {
            log.debug("Request Body: {}", new String(body, StandardCharsets.UTF_8));
        }
        
        // Execute request
        long startTime = System.currentTimeMillis();
        ClientHttpResponse response = execution.execute(request, body);
        long duration = System.currentTimeMillis() - startTime;
        
        // Log response
        log.info("Response: {} {} - {} ms", 
            request.getMethod(), 
            request.getURI(), 
            duration);
        log.debug("Response Status: {}", response.getStatusCode());
        log.debug("Response Headers: {}", response.getHeaders());
        
        return response;
    }
}
```

✅ **Interview Insight**: Knowing how to add custom converters and interceptors shows advanced understanding of RestTemplate.

## 9. 📱 RestTemplate vs. WebClient
---------

RestTemplate is being phased out in favor of WebClient. Here's how they compare:

```
┌─────────────────────────────┬─────────────────────────────┐
│ RestTemplate                │ WebClient                   │
├─────────────────────────────┼─────────────────────────────┤
│ Synchronous                 │ Asynchronous                │
├─────────────────────────────┼─────────────────────────────┤
│ Blocking I/O                │ Non-blocking I/O            │
├─────────────────────────────┼─────────────────────────────┤
│ Java Servlet Stack          │ Spring WebFlux Stack        │
├─────────────────────────────┼─────────────────────────────┤
│ Returns direct objects      │ Returns Mono/Flux           │
├─────────────────────────────┼─────────────────────────────┤
│ No streaming support        │ Streaming support           │
├─────────────────────────────┼─────────────────────────────┤
│ Limited exception handling  │ Rich error handling         │
└─────────────────────────────┴─────────────────────────────┘
```

### When to Use RestTemplate vs. WebClient:

- **Use RestTemplate when**:
  - Working with existing Spring MVC applications
  - Simple HTTP client needs
  - Team is more familiar with synchronous programming

- **Use WebClient when**:
  - Building new reactive applications
  - Need for non-blocking I/O
  - Higher concurrency requirements
  - Streaming responses

✅ **Interview Tip**: Mentioning the transition to WebClient shows you're up-to-date with Spring's direction.

## 10. 📝 Summary
---------

RestTemplate is Spring's synchronous HTTP client for making REST calls from your applications. Key points:

1. **Core Functionality**: Simplifies HTTP operations (GET, POST, PUT, DELETE)
2. **Key Components**: HttpMessageConverter, ClientHttpRequestFactory, ResponseErrorHandler
3. **Configuration**: Customize with timeouts, error handlers, and message converters
4. **Advanced Usage**: exchange() method for complex requests, UriComponentsBuilder for URLs
5. **Error Handling**: Default and custom error handlers for different status codes
6. **Testing**: MockRestServiceServer for integration testing
7. **Customization**: Interceptors for logging, authentication; custom converters for serialization
8. **Future**: Being replaced by WebClient for reactive applications

## 11. 📊 Summary Table
---------

| Topic | Key Points | Interview Focus |
|-------|------------|-----------------|
| **Basic Operations** | getForObject, postForObject, put, delete | Different return types and parameters |
| **ResponseEntity** | getForEntity, postForEntity, exchange | Working with status codes and headers |
| **URL Handling** | Path variables, query parameters, UriComponentsBuilder | Building complex URLs properly |
| **Error Handling** | HttpClientErrorException, HttpServerErrorException, custom handlers | Differentiating between 4xx and 5xx errors |
| **Message Converters** | Jackson for JSON, JAXB for XML | Adding custom converters |
| **Request Factories** | SimpleClientHttpRequestFactory, HttpComponentsClientHttpRequestFactory | Setting timeouts, connection pooling |
| **Interceptors** | Authentication, logging, custom headers | Modifying requests/responses |
| **Testing** | Mockito for unit tests, MockRestServiceServer for integration tests | Verifying correct requests |
| **RestTemplate vs WebClient** | Synchronous vs asynchronous, blocking vs non-blocking | When to use each approach |

✅ **Final Interview Tip**: When discussing RestTemplate in interviews, mention both its strengths (simplicity, wide adoption) and limitations (blocking nature). This balanced view shows you understand the tool's place in the Spring ecosystem.