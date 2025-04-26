# Java Spring WebClient Guide for Interview Preparation 🚀

Let's explore Spring WebClient thoroughly with practical examples and interview-focused insights to help you prepare efficiently.

## 1. 🌐 WebClient Introduction
---------

WebClient is Spring's modern, reactive HTTP client that replaces the traditional RestTemplate. It's part of the Spring WebFlux module and designed for non-blocking HTTP requests.

### Core Features:

- Non-blocking, reactive design
- Fluent API for request building
- Built on Project Reactor
- Streaming capabilities
- Support for reactive backpressure
- Support for multiple HTTP clients (Netty, Jetty, etc.)

📌 **Key Advantages:**

```
┌────────────────────┬────────────────────────────────────────┐
│ Feature            │ Benefit                                │
├────────────────────┼────────────────────────────────────────┤
│ Non-blocking       │ Better resource utilization            │
├────────────────────┼────────────────────────────────────────┤
│ Reactive streams   │ Efficient backpressure handling        │
├────────────────────┼────────────────────────────────────────┤
│ Functional API     │ More expressive request building       │
├────────────────────┼────────────────────────────────────────┤
│ Streaming support  │ Efficient handling of large responses  │
└────────────────────┴────────────────────────────────────────┘
```

✅ **Interview Insight:** WebClient is designed for environments where resource efficiency matters, like microservices architecture, and where traditional blocking RestTemplate might create bottlenecks.

## 2. 🧩 Important Classes & Components
---------

### Core Classes:

1. **WebClient** - Main entry point for creating requests
2. **WebClient.Builder** - For configuring and building WebClient instances
3. **ClientResponse** - Represents the HTTP response
4. **ExchangeStrategies** - For configuring HTTP message readers/writers
5. **WebClient.RequestBodySpec** - For configuring request body
6. **WebClient.ResponseSpec** - For handling response details

### Configuration Classes:

1. **ReactorClientHttpConnector** - For configuring the Reactor Netty client
2. **HttpClient** - Reactor Netty's client for HTTP requests
3. **ExchangeFilterFunction** - For filtering requests/responses

📌 **Class Hierarchy Diagram:**

```
WebClient
   └── Builder
       ├── baseUrl(String)
       ├── defaultHeader(String, String)
       ├── defaultCookie(String, String)
       ├── filter(ExchangeFilterFunction)
       └── build()
              └── get()/post()/put()/delete()/etc.
                     └── uri(String/Function)
                            └── retrieve() / exchange()
                                   └── bodyToMono(Class) / bodyToFlux(Class)
```

### Basic Usage Example:

```java
WebClient webClient = WebClient.builder()
    .baseUrl("https://api.example.com")
    .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
    .build();

Mono<User> userMono = webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(User.class);
```

✅ **Interview Tip:** Be prepared to discuss the key differences between `retrieve()` and `exchange()` methods. The former is simpler and handles errors automatically, while the latter gives you more control over the response.

## 3. ⚙️ WebClient Configuration
---------

### Basic Configuration:

```java
WebClient webClient = WebClient.builder()
    .baseUrl("https://api.example.com")
    .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
    .defaultCookie("session-id", "123456")
    .build();
```

### Advanced Configuration with Timeouts:

```java
// Configure HTTP client with timeouts
HttpClient httpClient = HttpClient.create()
    .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
    .responseTimeout(Duration.ofMillis(5000))
    .doOnConnected(conn -> 
        conn.addHandlerLast(new ReadTimeoutHandler(5000, TimeUnit.MILLISECONDS))
            .addHandlerLast(new WriteTimeoutHandler(5000, TimeUnit.MILLISECONDS)));

// Create WebClient with the custom HTTP client
WebClient webClient = WebClient.builder()
    .clientConnector(new ReactorClientHttpConnector(httpClient))
    .baseUrl("https://api.example.com")
    .build();
```

### Configuring Request/Response Size Limits:

```java
// Configure size limits for request/response
ExchangeStrategies strategies = ExchangeStrategies.builder()
    .codecs(configurer -> configurer
        .defaultCodecs()
        .maxInMemorySize(2 * 1024 * 1024)) // 2MB buffer limit
    .build();

WebClient webClient = WebClient.builder()
    .exchangeStrategies(strategies)
    .build();
```

❌ **Common Mistake:** Not configuring timeouts properly, which can lead to resource leaks in production systems when external services are slow to respond.

✅ **Best Practice:** Create a single WebClient bean for each external API you're connecting to, properly configured with timeouts and retry logic.

## 4. 📝 Common HTTP Operations
---------

### GET Request:

```java
Mono<User> result = webClient.get()
    .uri("/users/{id}", userId)
    .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
    .retrieve()
    .bodyToMono(User.class);
```

### POST Request:

```java
User newUser = new User("john", "john@example.com");

Mono<User> result = webClient.post()
    .uri("/users")
    .contentType(MediaType.APPLICATION_JSON)
    .bodyValue(newUser)
    .retrieve()
    .bodyToMono(User.class);
```

### PUT Request:

```java
Mono<Void> result = webClient.put()
    .uri("/users/{id}", userId)
    .contentType(MediaType.APPLICATION_JSON)
    .bodyValue(updatedUser)
    .retrieve()
    .bodyToMono(Void.class);
```

### DELETE Request:

```java
Mono<Void> result = webClient.delete()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(Void.class);
```

### Handling Query Parameters:

```java
Flux<User> users = webClient.get()
    .uri(uriBuilder -> uriBuilder
        .path("/users")
        .queryParam("page", page)
        .queryParam("size", size)
        .build())
    .retrieve()
    .bodyToFlux(User.class);
```

✅ **Interview Insight:** In interviews, demonstrate your understanding of reactive operations by explaining when to use `bodyToMono()` vs `bodyToFlux()` based on the expected response.

## 5. 🛡️ Error Handling
---------

### Basic Error Handling:

```java
webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .onStatus(HttpStatus::is4xxClientError, 
        response -> Mono.error(new ClientException("Client error: " + response.statusCode())))
    .onStatus(HttpStatus::is5xxServerError, 
        response -> Mono.error(new ServerException("Server error: " + response.statusCode())))
    .bodyToMono(User.class)
    .onErrorResume(ClientException.class, e -> {
        log.error("Client error occurred", e);
        return Mono.empty(); // Return fallback or empty
    })
    .onErrorResume(ServerException.class, e -> {
        log.error("Server error occurred", e);
        return Mono.just(new User("default", "default@example.com")); // Return fallback
    });
```

### Using exchange() for Custom Error Handling:

```java
webClient.get()
    .uri("/users/{id}", userId)
    .exchange()
    .flatMap(response -> {
        if (response.statusCode().is4xxClientError()) {
            return response.bodyToMono(ErrorResponse.class)
                .flatMap(errorBody -> Mono.error(
                    new CustomException(errorBody.getMessage())));
        }
        else if (response.statusCode().is5xxServerError()) {
            return Mono.error(new ServerException(
                "Server error: " + response.statusCode()));
        }
        return response.bodyToMono(User.class);
    });
```

### Handling Connection Errors:

```java
webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(User.class)
    .onErrorResume(WebClientResponseException.class, e -> {
        log.error("Error response status code: {}", e.getRawStatusCode(), e);
        return Mono.empty();
    })
    .onErrorResume(WebClientRequestException.class, e -> {
        log.error("Request error: {}", e.getMessage(), e);
        return Mono.empty();
    });
```

❌ **Common Mistakes:**
- Not differentiating between 4xx and 5xx errors
- Not handling connection errors (timeouts, network issues)
- Using `block()` inside error handlers, which makes them blocking

✅ **Best Practice:** Create custom exception classes for different types of errors and handle them specifically. Log meaningful error messages with correlation IDs for troubleshooting.

## 6. 🔄 Retry and Circuit Breaking
---------

### Basic Retry Logic:

```java
webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(User.class)
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
        .filter(e -> e instanceof WebClientResponseException &&
            ((WebClientResponseException) e).getStatusCode().is5xxServerError()));
```

### Advanced Retry with Custom Policies:

```java
// Define custom retry policy
Retry retrySpec = Retry.backoff(3, Duration.ofSeconds(1))
    .filter(throwable -> {
        return throwable instanceof WebClientResponseException &&
            ((WebClientResponseException) throwable).getStatusCode().is5xxServerError();
    })
    .onRetryExhaustedThrow((retryBackoffSpec, retrySignal) -> {
        throw new ServiceUnavailableException("External service failed after retries");
    });

// Use in WebClient
webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(User.class)
    .retryWhen(retrySpec);
```

### Circuit Breaker Integration with Resilience4j:

```java
// Define circuit breaker
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)
    .waitDurationInOpenState(Duration.ofMillis(1000))
    .permittedNumberOfCallsInHalfOpenState(2)
    .slidingWindowSize(10)
    .build();

CircuitBreaker circuitBreaker = CircuitBreaker.of("userService", config);
ReactiveCircuitBreaker reactiveCircuitBreaker = 
    ReactiveCircuitBreakerFactory.create(circuitBreaker);

// Use circuit breaker with WebClient
webClient.get()
    .uri("/users/{id}", userId)
    .retrieve()
    .bodyToMono(User.class)
    .transform(it -> reactiveCircuitBreaker.run(it, 
        throwable -> Mono.just(new User("fallback", "fallback@example.com"))));
```

✅ **Interview Insight:** Most interviewers look for candidates who understand resilience patterns beyond basic retry. Be prepared to discuss circuit breaker, bulkhead, and rate limiter patterns.

## 7. 📊 Metrics Collection
---------

### Basic Metrics with Micrometer:

```java
// Create metrics registry
MeterRegistry registry = new SimpleMeterRegistry();

// Create WebClient with filter for metrics
WebClient webClient = WebClient.builder()
    .filter((request, next) -> {
        long startTime = System.currentTimeMillis();
        
        return next.exchange(request)
            .doOnSuccess(response -> {
                String uri = request.url().toString();
                String method = request.method().name();
                int status = response.statusCode().value();
                
                Timer timer = Timer.builder("http.client.requests")
                    .tag("method", method)
                    .tag("uri", uri)
                    .tag("status", String.valueOf(status))
                    .register(registry);
                
                timer.record(System.currentTimeMillis() - startTime, TimeUnit.MILLISECONDS);
            });
    })
    .build();
```

### Comprehensive Metrics with Spring Boot Actuator:

```java
// In application.properties:
// management.metrics.web.client.request.autotime.enabled=true

// In your WebClient configuration
@Bean
public WebClient webClient(WebClient.Builder webClientBuilder, 
                         MeterRegistry meterRegistry) {
    return webClientBuilder
        .filter(WebClientFilterAdapter.create(
            WebClientExchangeTagsProvider.DEFAULT, 
            meterRegistry, 
            true))
        .build();
}
```

### Custom Metrics Implementation:

```java
@Configuration
public class WebClientConfig {

    @Bean
    public WebClient webClient(MeterRegistry meterRegistry) {
        return WebClient.builder()
            .filter((request, next) -> {
                String uri = request.url().getPath();
                String method = request.method().name();
                
                // Start timer
                Timer.Sample sample = Timer.start(meterRegistry);
                
                // Process request
                return next.exchange(request)
                    .doFinally(signalType -> {
                        // Record metrics when request completes
                        sample.stop(meterRegistry.timer("http.client.requests",
                            "method", method,
                            "uri", uri,
                            "status", signalType == SignalType.ON_ERROR ? "ERROR" : "SUCCESS"));
                    });
            })
            .build();
    }
}
```

✅ **Best Practice:** Always collect metrics in production for:
- Request duration
- Error rates by status code
- Circuit breaker state changes
- Response size

📌 **Interview Tip:** Demonstrate knowledge of observability triad: metrics, logging, and tracing. Mention distributed tracing tools like Spring Cloud Sleuth or OpenTelemetry integration.

## 8. 🔍 Advanced WebClient Usage
---------

### Client-Side Load Balancing:

```java
@Bean
public WebClient webClient(ReactorLoadBalancerExchangeFilterFunction lbFunction) {
    return WebClient.builder()
        .filter(lbFunction) // From Spring Cloud LoadBalancer
        .build();
}
```

### Streaming Response Handling:

```java
Flux<ServerSentEvent<String>> eventStream = webClient.get()
    .uri("/events")
    .accept(MediaType.TEXT_EVENT_STREAM)
    .retrieve()
    .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {});
    
eventStream.subscribe(
    event -> log.info("Event: {}", event.data()),
    error -> log.error("Error receiving SSE", error),
    () -> log.info("Completed!"));
```

### OAuth2 Integration:

```java
WebClient webClient = WebClient.builder()
    .filter(new OAuth2AuthorizedClientExchangeFilterFunction(
        authorizedClientManager))
    .build();

Mono<User> userMono = webClient.get()
    .uri("/users/{id}", userId)
    .attributes(oauth2AuthorizedClient(oAuth2AuthorizedClient))
    .retrieve()
    .bodyToMono(User.class);
```

### Multipart Form Data:

```java
MultipartBodyBuilder bodyBuilder = new MultipartBodyBuilder();
bodyBuilder.part("file", new FileSystemResource("path/to/file.txt"));
bodyBuilder.part("data", "{\"name\":\"test\"}", MediaType.APPLICATION_JSON);

webClient.post()
    .uri("/upload")
    .contentType(MediaType.MULTIPART_FORM_DATA)
    .body(BodyInserters.fromMultipartData(bodyBuilder.build()))
    .retrieve()
    .bodyToMono(String.class);
```

✅ **Interview Insight:** Being able to explain these advanced patterns shows depth of knowledge beyond basic API calls, which can set you apart in interviews.

## 9. 🧪 Testing WebClient
---------

### Unit Testing with MockWebServer:

```java
@Test
void testWebClientCall() {
    // Setup Mock Web Server
    MockWebServer mockWebServer = new MockWebServer();
    mockWebServer.enqueue(new MockResponse()
        .setResponseCode(200)
        .setHeader("Content-Type", "application/json")
        .setBody("{\"id\":1,\"name\":\"Test User\"}"));
    
    // Create WebClient pointing to Mock server
    WebClient webClient = WebClient.builder()
        .baseUrl(mockWebServer.url("/").toString())
        .build();
    
    // Test service using WebClient
    UserService userService = new UserService(webClient);
    User user = userService.getUserById("1").block();
    
    // Verify
    assertThat(user.getName()).isEqualTo("Test User");
    
    // Verify request was made correctly
    RecordedRequest recordedRequest = mockWebServer.takeRequest();
    assertThat(recordedRequest.getPath()).isEqualTo("/users/1");
    assertThat(recordedRequest.getMethod()).isEqualTo("GET");
}
```

### Testing with WebClient Mock:

```java
@Test
void testWithWebClientMock() {
    // Create mock WebClient
    WebClient webClientMock = mock(WebClient.class);
    WebClient.RequestHeadersUriSpec requestHeadersUriSpec = mock(WebClient.RequestHeadersUriSpec.class);
    WebClient.RequestHeadersSpec requestHeadersSpec = mock(WebClient.RequestHeadersSpec.class);
    WebClient.ResponseSpec responseSpec = mock(WebClient.ResponseSpec.class);
    
    // Setup mock behavior
    when(webClientMock.get()).thenReturn(requestHeadersUriSpec);
    when(requestHeadersUriSpec.uri("/users/{id}", "1")).thenReturn(requestHeadersSpec);
    when(requestHeadersSpec.retrieve()).thenReturn(responseSpec);
    when(responseSpec.bodyToMono(User.class)).thenReturn(Mono.just(new User("1", "Test User")));
    
    // Use mock to test service
    UserService userService = new UserService(webClientMock);
    User user = userService.getUserById("1").block();
    
    // Verify results
    assertThat(user.getName()).isEqualTo("Test User");
}
```

✅ **Best Practice:** Use MockWebServer for integration tests and mock WebClient for unit tests.

## 10. 📝 Summary
---------

Spring WebClient is a powerful reactive HTTP client for building non-blocking applications with Spring WebFlux. Key takeaways:

1. **Reactive Foundation**: Built on Project Reactor, uses Mono/Flux for processing
2. **Non-blocking I/O**: Efficient resource utilization with fewer threads
3. **Fluent API**: Expressive and chainable request building
4. **Resilience Patterns**: Built-in support for retry, timeout, and circuitbreaking
5. **Streaming Support**: Efficiently handles large responses and server-sent events
6. **Metrics Integration**: Observability with Micrometer and Spring Boot Actuator

## 11. 📊 Summary Table
---------

| Topic | Key Points | Interview Focus |
|-------|------------|-----------------|
| **WebClient Basics** | Non-blocking, fluent API, reactive | Compare with RestTemplate |
| **Important Classes** | WebClient, Builder, ClientResponse | Class hierarchy understanding |
| **Configuration** | Timeouts, filters, codecs | Performance implications |
| **Common Operations** | GET, POST, PUT, DELETE | Mono vs Flux usage |
| **Error Handling** | onStatus, onErrorResume | Custom error handling strategies |
| **Retry & Resilience** | retryWhen, circuit breaking | Fault tolerance knowledge |
| **Metrics** | Micrometer, custom metrics | Observability approaches |
| **Advanced Features** | Streaming, OAuth2, multipart | Depth of knowledge |
| **Testing** | MockWebServer, mocking | Test isolation strategies |

✅ **Final Interview Tip:** During interviews, emphasize not just how to use WebClient, but when and why to choose it over alternatives. Explain the performance implications of different configuration options and how they impact production systems.