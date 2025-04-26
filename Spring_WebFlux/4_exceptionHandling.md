# Spring WebFlux Exception Handling Guide 🛡️

This guide will help you master exception handling in Spring WebFlux with practical examples for your upcoming interviews.

## 1. 🌐 Understanding Exception Handling in WebFlux
---------

Spring WebFlux handles exceptions differently than traditional Spring MVC due to its reactive nature. In WebFlux:

- Exceptions occur within reactive streams
- Traditional try-catch blocks often don't work
- Error signals propagate through the reactive chain
- Special operators handle these error signals

📌 **The Reactive Error Flow**:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  HTTP Request   │────►│  Reactive Flow  │────►│  HTTP Response  │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 │
                        ┌────────▼────────┐
                        │                 │
                        │      Error      │
                        │                 │
                        └────────┬────────┘
                                 │
                                 │
                        ┌────────▼────────┐
                        │                 │
                        │  Error Handling │
                        │  Operators      │
                        │                 │
                        └────────┬────────┘
                                 │
                                 │
                        ┌────────▼────────┐
                        │                 │
                        │ Error Response  │
                        │                 │
                        └─────────────────┘
```

✅ **Interview Insight**: In reactive programming, exceptions are converted to error signals and propagate through the reactive chain until handled or until they reach the subscriber.

## 2. 🔧 Important Classes & Interfaces
---------

Several key classes and interfaces are central to exception handling in WebFlux:

### Core Exception Classes:

1. **ResponseStatusException**: Base exception for HTTP status codes
2. **WebExchangeBindException**: Thrown during request binding failures
3. **ServerWebInputException**: For request body validation errors
4. **NotAcceptableStatusException**: When content type cannot be generated to satisfy request

### Handler Interfaces:

1. **WebExceptionHandler**: Interface for handling exceptions in WebFlux
2. **ErrorWebExceptionHandler**: Extended handler for global exception handling
3. **AbstractErrorWebExceptionHandler**: Base class for custom error handlers

### Support Classes:

1. **DefaultErrorAttributes**: Stores exception attributes for error responses
2. **ErrorResponse**: Interface describing error response structure
3. **ProblemDetail**: RFC 7807 Problem Details implementation

📌 **WebFlux Exception Hierarchy**:

```
ResponseStatusException
├── BadRequestException
├── NotFoundException
├── MethodNotAllowedException
├── NotAcceptableStatusException
├── UnsupportedMediaTypeStatusException
├── ServerErrorException
└── ServiceUnavailableException
```

✅ **Best Practice**: Use specific exception classes rather than generic ones to provide more meaningful error responses.

## 3. 📝 Controller-level Exception Handling
---------

Spring WebFlux allows you to handle exceptions at the controller level using the `@ExceptionHandler` annotation:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public Mono<User> getUserById(@PathVariable String id) {
        return userService.findById(id)
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleUserNotFoundException(UserNotFoundException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            Instant.now());
        
        return Mono.just(ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(errorResponse));
    }
}
```

✅ **Best Practice**: Return `Mono<ResponseEntity<>>` from exception handlers rather than just `ResponseEntity<>` to maintain the reactive flow.

❌ **Common Mistake**: Returning non-reactive types (like `ResponseEntity` directly) from `@ExceptionHandler` methods, which breaks the reactive chain.

## 4. 🌍 Global Exception Handling
---------

For application-wide exception handling, Spring WebFlux provides several approaches:

### Using @ControllerAdvice:

```java
@RestControllerAdvice
public class GlobalErrorWebExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleUserNotFoundException(UserNotFoundException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            Instant.now());
        
        return Mono.just(ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(errorResponse));
    }
    
    @ExceptionHandler(ValidationException.class)
    public Mono<ResponseEntity<ErrorResponse>> handleValidationException(ValidationException ex) {
        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            ex.getMessage(),
            Instant.now());
        
        return Mono.just(ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(errorResponse));
    }
    
    @ExceptionHandler(Exception.class)
    public Mono<ResponseEntity<ErrorResponse>> handleGenericException(Exception ex) {
        ErrorResponse errorResponse = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "An unexpected error occurred",
            Instant.now());
        
        return Mono.just(ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(errorResponse));
    }
}
```

### Using Custom ErrorWebExceptionHandler:

For more control, implement a custom `ErrorWebExceptionHandler`:

```java
@Component
@Order(-2) // Take precedence over DefaultErrorWebExceptionHandler
public class CustomErrorWebExceptionHandler extends AbstractErrorWebExceptionHandler {
    
    public CustomErrorWebExceptionHandler(
            ErrorAttributes errorAttributes,
            WebProperties.Resources resources,
            ApplicationContext applicationContext) {
        super(errorAttributes, resources, applicationContext);
    }
    
    @Override
    protected RouterFunction<ServerResponse> getRoutingFunction(ErrorAttributes errorAttributes) {
        return RouterFunctions.route(
            RequestPredicates.all(), this::renderErrorResponse);
    }
    
    private Mono<ServerResponse> renderErrorResponse(ServerRequest request) {
        Map<String, Object> errorPropertiesMap = getErrorAttributes(
            request, ErrorAttributeOptions.defaults());
        
        Throwable error = getError(request);
        HttpStatus status = determineHttpStatus(error);
        
        return ServerResponse.status(status)
            .contentType(MediaType.APPLICATION_JSON)
            .body(BodyInserters.fromValue(errorPropertiesMap));
    }
    
    private HttpStatus determineHttpStatus(Throwable error) {
        if (error instanceof UserNotFoundException) {
            return HttpStatus.NOT_FOUND;
        } else if (error instanceof ValidationException) {
            return HttpStatus.BAD_REQUEST;
        }
        return HttpStatus.INTERNAL_SERVER_ERROR;
    }
}
```

📌 **Key Insight**: `@ControllerAdvice` is simpler but `ErrorWebExceptionHandler` gives more control over the error response format and handling logic.

✅ **Interview Tip**: Be prepared to discuss the pros and cons of different exception handling approaches in WebFlux.

## 5. 🧩 Reactive Error Handling Operators
---------

Spring WebFlux relies on Project Reactor's error handling operators to manage exceptions within reactive streams:

### onErrorReturn:
Returns a fallback value when an error occurs.

```java
public Mono<User> getUserById(String id) {
    return userRepository.findById(id)
        .onErrorReturn(DatabaseException.class, User.defaultUser());
}
```

### onErrorResume:
Switches to an alternative publisher when an error occurs.

```java
public Mono<User> getUserById(String id) {
    return userRepository.findById(id)
        .onErrorResume(UserNotFoundException.class, ex -> {
            log.error("User not found: {}", id, ex);
            return userCacheRepository.findById(id);
        })
        .onErrorResume(DatabaseException.class, ex -> {
            log.error("Database error", ex);
            return Mono.empty();
        });
}
```

### onErrorMap:
Transforms an error into another error type.

```java
public Mono<User> getUserById(String id) {
    return userRepository.findById(id)
        .onErrorMap(DatabaseException.class, ex -> 
            new ServiceUnavailableException("Database service unavailable", ex))
        .onErrorMap(NotFoundException.class, ex -> 
            new UserNotFoundException("User with id " + id + " not found", ex));
}
```

### doOnError:
Executes a side-effect when an error occurs (like logging) without affecting the error flow.

```java
public Mono<User> getUserById(String id) {
    return userRepository.findById(id)
        .doOnError(ex -> log.error("Error fetching user: {}", id, ex))
        .onErrorMap(ex -> new UserNotFoundException(id));
}
```

❌ **Common Mistake**: Using `doOnError` to handle exceptions without a subsequent error operator, which doesn't actually handle the error.

✅ **Best Practice**: Choose the appropriate error operator based on what you want to do with the error:
- Use `onErrorReturn` for simple fallbacks
- Use `onErrorResume` for alternative flows
- Use `onErrorMap` to change error types
- Use `doOnError` for side effects like logging

## 6. 🛡️ Exception Handling for WebClient
---------

WebClient is Spring's reactive HTTP client, and it requires special exception handling approaches:

### Basic Error Handling:

```java
webClient.get()
    .uri("/api/users/{id}", id)
    .retrieve()
    .bodyToMono(User.class)
    .onErrorResume(WebClientResponseException.class, ex -> {
        if (ex.getStatusCode() == HttpStatus.NOT_FOUND) {
            return Mono.empty();
        }
        return Mono.error(ex);
    })
    .onErrorResume(WebClientRequestException.class, ex -> {
        log.error("Network error", ex);
        return Mono.error(new ServiceUnavailableException("External service unavailable"));
    });
```

### Using onStatus for HTTP Status Code Handling:

```java
webClient.get()
    .uri("/api/users/{id}", id)
    .retrieve()
    .onStatus(HttpStatus::is4xxClientError, response -> {
        if (response.statusCode() == HttpStatus.NOT_FOUND) {
            return Mono.error(new UserNotFoundException(id));
        }
        return response.bodyToMono(ErrorResponse.class)
            .flatMap(errorBody -> Mono.error(
                new ClientException(errorBody.getMessage())));
    })
    .onStatus(HttpStatus::is5xxServerError, response -> 
        Mono.error(new ServiceUnavailableException(
            "External service returned " + response.statusCode())))
    .bodyToMono(User.class);
```

### Using exchange() Method for More Control:

```java
webClient.get()
    .uri("/api/users/{id}", id)
    .exchange()
    .flatMap(response -> {
        if (response.statusCode().is4xxClientError()) {
            if (response.statusCode() == HttpStatus.NOT_FOUND) {
                return Mono.error(new UserNotFoundException(id));
            }
            return response.bodyToMono(ErrorResponse.class)
                .flatMap(errorBody -> Mono.error(
                    new ClientException(errorBody.getMessage())));
        }
        else if (response.statusCode().is5xxServerError()) {
            return Mono.error(new ServiceUnavailableException(
                "External service error: " + response.statusCode()));
        }
        return response.bodyToMono(User.class);
    });
```

### Timeout and Retry Handling:

```java
webClient.get()
    .uri("/api/users/{id}", id)
    .retrieve()
    .bodyToMono(User.class)
    .timeout(Duration.ofSeconds(3))
    .onErrorResume(TimeoutException.class, ex -> {
        log.warn("Request timed out for user id: {}", id);
        return Mono.error(new ServiceUnavailableException("Service timeout"));
    })
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
        .filter(ex -> ex instanceof IOException || 
                      ex instanceof TimeoutException));
```

### Error Handling With Circuit Breaker:

```java
// Define circuit breaker
CircuitBreaker circuitBreaker = CircuitBreaker.of("userService", CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofMillis(1000))
    .permittedNumberOfCallsInHalfOpenState(2)
    .slidingWindowSize(10)
    .build());

// Create reactive circuit breaker
ReactiveCircuitBreaker reactiveCircuitBreaker = 
    ReactiveCircuitBreakerFactory.create(circuitBreaker);

// Use with WebClient
webClient.get()
    .uri("/api/users/{id}", id)
    .retrieve()
    .bodyToMono(User.class)
    .transform(it -> reactiveCircuitBreaker.run(it, throwable -> {
        log.error("Circuit open, returning fallback", throwable);
        return Mono.just(User.defaultUser());
    }));
```

❌ **Common Mistakes**:
- Using `retrieve()` without proper error handling
- Not handling connection errors (like network issues or timeouts)
- Missing retry logic for transient failures

✅ **Best Practice**: Consider a layered approach to WebClient error handling:
1. HTTP status codes with `onStatus`
2. Timeouts with `timeout`
3. Retries with `retryWhen`
4. Circuit breaking for resilience

## 7. 🔍 Testing Exception Handling
---------

Testing exception handling in WebFlux is crucial to ensure your error flows work correctly:

### Unit Testing Controller Exception Handlers:

```java
@WebFluxTest(UserController.class)
class UserControllerTest {

    @Autowired
    private WebTestClient webTestClient;
    
    @MockBean
    private UserService userService;
    
    @Test
    void getUserById_WhenUserNotFound_ShouldReturnNotFound() {
        // Given
        String userId = "non-existent";
        when(userService.findById(userId))
            .thenReturn(Mono.error(new UserNotFoundException(userId)));
        
        // When & Then
        webTestClient.get()
            .uri("/api/users/{id}", userId)
            .exchange()
            .expectStatus().isNotFound()
            .expectBody()
            .jsonPath("$.status").isEqualTo(404)
            .jsonPath("$.message").isEqualTo("User with id " + userId + " not found")
            .jsonPath("$.timestamp").exists();
    }
    
    @Test
    void getUserById_WhenServiceFails_ShouldReturnInternalServerError() {
        // Given
        String userId = "123";
        when(userService.findById(userId))
            .thenReturn(Mono.error(new RuntimeException("Database failure")));
        
        // When & Then
        webTestClient.get()
            .uri("/api/users/{id}", userId)
            .exchange()
            .expectStatus().isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR)
            .expectBody()
            .jsonPath("$.status").isEqualTo(500)
            .jsonPath("$.message").isEqualTo("An unexpected error occurred");
    }
}
```

### Testing WebClient Error Handling:

```java
@SpringBootTest
class UserServiceTest {

    @Autowired
    private UserService userService;
    
    @MockBean
    private WebClient webClient;
    
    @MockBean
    private WebClient.RequestHeadersUriSpec requestHeadersUriSpec;
    
    @MockBean
    private WebClient.RequestHeadersSpec requestHeadersSpec;
    
    @MockBean
    private WebClient.ResponseSpec responseSpec;
    
    @BeforeEach
    void setup() {
        when(webClient.get()).thenReturn(requestHeadersUriSpec);
        when(requestHeadersUriSpec.uri(anyString(), anyString()))
            .thenReturn(requestHeadersSpec);
        when(requestHeadersSpec.retrieve()).thenReturn(responseSpec);
    }
    
    @Test
    void getExternalUser_WhenNotFound_ShouldReturnEmptyMono() {
        // Given
        String userId = "non-existent";
        
        when(responseSpec.onStatus(any(), any())).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(User.class))
            .thenReturn(Mono.error(
                new WebClientResponseException(404, "Not Found", null, null, null)));
        
        // When
        Mono<User> result = userService.getExternalUser(userId);
        
        // Then
        StepVerifier.create(result)
            .verifyComplete(); // Should complete empty without error
    }
    
    @Test
    void getExternalUser_WhenServerError_ShouldPropagateCustomException() {
        // Given
        String userId = "123";
        
        when(responseSpec.onStatus(any(), any())).thenReturn(responseSpec);
        when(responseSpec.bodyToMono(User.class))
            .thenReturn(Mono.error(
                new WebClientResponseException(500, "Server Error", null, null, null)));
        
        // When
        Mono<User> result = userService.getExternalUser(userId);
        
        // Then
        StepVerifier.create(result)
            .expectError(ServiceUnavailableException.class)
            .verify();
    }
}
```

✅ **Best Practice**: Use `StepVerifier` for testing reactive error flows - it helps verify both the success path and the error path.

## 8. 📋 Best Practices for WebFlux Error Handling
---------

### 1. Use Specific Exception Types:

```java
// Good
throw new UserNotFoundException(userId);

// Avoid
throw new RuntimeException("User not found: " + userId);
```

### 2. Create a Standardized Error Response Model:

```java
@Data
@AllArgsConstructor
public class ApiError {
    private int status;
    private String message;
    private String path;
    private Instant timestamp;
    private Map<String, String> validationErrors;
    
    // Constructors for different error scenarios
    public ApiError(int status, String message, String path) {
        this(status, message, path, Instant.now(), Collections.emptyMap());
    }
}
```

### 3. Layer Your Error Handling:

```java
// Service level error handling
public Mono<User> getUserById(String id) {
    return userRepository.findById(id)
        .switchIfEmpty(Mono.error(new UserNotFoundException(id)))
        .onErrorMap(DatabaseException.class, 
            ex -> new ServiceException("Database error", ex));
}

// Controller level error handling for specific exceptions
@ExceptionHandler(UserNotFoundException.class)
public Mono<ResponseEntity<ApiError>> handleUserNotFound(
        UserNotFoundException ex, ServerWebExchange exchange) {
    String path = exchange.getRequest().getPath().value();
    ApiError error = new ApiError(
        HttpStatus.NOT_FOUND.value(), 
        ex.getMessage(),
        path);
    
    return Mono.just(ResponseEntity
        .status(HttpStatus.NOT_FOUND)
        .body(error));
}

// Global error handling for generic exceptions
@ExceptionHandler(Exception.class)
public Mono<ResponseEntity<ApiError>> handleGenericException(
        Exception ex, ServerWebExchange exchange) {
    String path = exchange.getRequest().getPath().value();
    ApiError error = new ApiError(
        HttpStatus.INTERNAL_SERVER_ERROR.value(),
        "An unexpected error occurred",
        path);
    
    log.error("Unhandled exception", ex);
    
    return Mono.just(ResponseEntity
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .body(error));
}
```

### 4. Use RFC 7807 Problem Details for API Errors:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    public Mono<ResponseEntity<ProblemDetail>> handleUserNotFound(
            UserNotFoundException ex, ServerWebExchange exchange) {
        
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        
        problem.setTitle("User Not Found");
        problem.setType(URI.create("https://api.example.com/errors/not-found"));
        problem.setProperty("timestamp", Instant.now());
        problem.setProperty("errorCategory", "DATA_ACCESS");
        
        return Mono.just(ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(problem));
    }
}
```

✅ **Best Practice**: Use the RFC 7807 Problem Details format for API error responses - it's a standardized way to express errors that clients can parse consistently.

## 9. 📝 Summary
---------

Spring WebFlux exception handling requires a reactive approach due to its non-blocking nature. Key points:

1. **Reactive Error Flow**: Exceptions propagate as error signals through reactive chains
2. **Error Handling Approaches**:
   - Controller-level with `@ExceptionHandler`
   - Global with `@RestControllerAdvice`
   - Custom with `ErrorWebExceptionHandler`
3. **Reactor Operators**: `onErrorReturn`, `onErrorResume`, `onErrorMap`, and `doOnError`
4. **WebClient Error Handling**: `onStatus`, exception handling, and resilience patterns
5. **Testing**: Special approaches with `WebTestClient` and `StepVerifier`
6. **Best Practices**: Specific exceptions, standardized responses, and RFC 7807 Problem Details

## 10. 📊 Summary Table
---------

| Topic | Key Components | Best Practices | Common Mistakes |
|-------|----------------|----------------|-----------------|
| **Controller Exception Handling** | @ExceptionHandler, Mono<ResponseEntity> | Return reactive types, use specific handlers | Returning non-reactive types, generic handlers |
| **Global Exception Handling** | @RestControllerAdvice, AbstractErrorWebExceptionHandler | Order exception handlers from specific to general | Forgetting to handle generic Exception as a fallback |
| **Reactive Error Operators** | onErrorReturn, onErrorResume, onErrorMap, doOnError | Choose appropriate operator for the scenario | Using doOnError alone without handling the error |
| **WebClient Error Handling** | onStatus, retrieve vs exchange | Layer error handling (HTTP, timeout, retry) | Not handling connection errors, missing retry logic |
| **Resilience Patterns** | timeout, retry, circuit breaker | Combine patterns for complete resilience | Implementing just one pattern in isolation |
| **Error Response Design** | ApiError, ProblemDetail | Follow RFC 7807 for standardized errors | Inconsistent error formats, missing details |
| **Testing** | WebTestClient, StepVerifier | Test both success and error paths | Testing only happy paths, blocking tests |

✅ **Final Interview Tip**: When discussing WebFlux exception handling in interviews, emphasize how it differs from traditional MVC exception handling due to the reactive nature. Demonstrate your understanding of error flow in reactive streams and how to maintain the non-blocking paradigm throughout your error handling.