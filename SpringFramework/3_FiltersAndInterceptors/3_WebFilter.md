# 🌊 WebFilter Tutorial: Spring WebFlux Filtering

## 1. 🔍 Introduction to WebFilter
---------

WebFilter is a core component in Spring WebFlux applications that enables you to intercept and process HTTP requests and responses before they reach your controllers and after your controllers have generated responses. WebFilter is the reactive counterpart to traditional Servlet Filters.

### 📌 What is WebFilter?

WebFilter is an interface in Spring WebFlux that allows you to perform cross-cutting tasks such as:

- Authentication and authorization
- Request/response logging
- Request transformation
- Response modification
- Metrics collection
- Rate limiting
- CORS handling

```
┌───────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────┐
│  Client   │ ──▶ │WebFilter│ ──▶ │WebFilter│ ──▶ │ Controllers │
│  Request  │     │    1    │     │    2    │     │             │
└───────────┘     └─────────┘     └─────────┘     └─────────────┘
                      │                │                │
                      │                │                │
┌───────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────┐
│  Client   │ ◀── │WebFilter│ ◀── │WebFilter│ ◀── │  Response   │
│  Browser  │     │    1    │     │    2    │     │  Generated  │
└───────────┘     └─────────┘     └─────────┘     └─────────────┘
```

### 📌 WebFilter vs. Servlet Filter

✅ **WebFilter**:
- Reactive/non-blocking
- Works with `Mono<Void>` return type
- Uses `ServerWebExchange` for request/response
- Appropriate for reactive applications

❌ **Servlet Filter**:
- Blocking
- Void return type
- Uses `HttpServletRequest/Response`
- Used in traditional Spring MVC

## 2. 🛠️ Creating Your First WebFilter
---------

### 📌 Basic WebFilter Implementation

Here's a simple logging WebFilter:

```java
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component
public class LoggingWebFilter implements WebFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(LoggingWebFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Pre-processing: Log the incoming request
        logger.info("Incoming request: {} {}",
                exchange.getRequest().getMethod(),
                exchange.getRequest().getURI());
        
        // Continue the filter chain and perform post-processing after
        return chain.filter(exchange)
                .doFinally(signalType -> {
                    // Post-processing: Log the response status
                    logger.info("Response status: {}", 
                            exchange.getResponse().getStatusCode());
                });
    }
}
```

### 📌 Key Components

1. **WebFilter Interface**: Defines the `filter` method that you must implement
2. **ServerWebExchange**: Contains both request and response
3. **WebFilterChain**: Enables invocation of the next filter in the chain
4. **Mono\<Void\>**: Reactive return type indicating completion

### 📌 Filter Registration

The simplest way to register a WebFilter is by declaring it as a Spring component:

```java
@Component
public class MyWebFilter implements WebFilter {
    // Implementation
}
```

Spring Boot will automatically detect and register WebFilter beans.

## 3. 🎯 Controlling Filter Order
---------

When you have multiple filters, controlling their execution order becomes important. Spring provides several ways to do this:

### 📌 Using @Order Annotation

```java
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(1) // Lower values have higher priority
public class SecurityWebFilter implements WebFilter {
    // Implementation
}

@Component
@Order(2) // Will execute after SecurityWebFilter
public class LoggingWebFilter implements WebFilter {
    // Implementation
}
```

### 📌 Implementing Ordered Interface

```java
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;

@Component
public class SecurityWebFilter implements WebFilter, Ordered {
    
    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE;
    }
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Implementation
    }
}
```

### 📌 Programmatic Registration with WebFluxConfigurer

For more complex registration scenarios:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.config.WebFluxConfigurer;
import org.springframework.core.annotation.Order;

@Configuration
public class WebFluxConfig implements WebFluxConfigurer {
    
    @Bean
    @Order(1)
    public WebFilter securityWebFilter() {
        return (exchange, chain) -> {
            // Security filter logic
            return chain.filter(exchange);
        };
    }
    
    @Bean
    @Order(2)
    public WebFilter loggingWebFilter() {
        return (exchange, chain) -> {
            // Logging filter logic
            return chain.filter(exchange);
        };
    }
}
```

## 4. 💡 Common WebFilter Use Cases
---------

### 📌 Logging Filter

A logging filter records details about requests and responses:

```java
@Component
@Order(1)
public class RequestLoggingFilter implements WebFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(RequestLoggingFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        long startTime = System.currentTimeMillis();
        String path = exchange.getRequest().getURI().getPath();
        String method = exchange.getRequest().getMethod().name();
        
        logger.info("Request started: {} {}", method, path);
        
        return chain.filter(exchange)
                .doFinally(signalType -> {
                    long duration = System.currentTimeMillis() - startTime;
                    logger.info("Request completed: {} {} - Status: {} - Duration: {}ms", 
                            method, 
                            path, 
                            exchange.getResponse().getStatusCode(), 
                            duration);
                });
    }
}
```

### 📌 Authentication Filter

This filter checks for authentication tokens:

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class AuthenticationFilter implements WebFilter {
    
    private final AuthenticationManager authManager;
    
    public AuthenticationFilter(AuthenticationManager authManager) {
        this.authManager = authManager;
    }
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String path = exchange.getRequest().getPath().value();
        
        // Skip authentication for public paths
        if (isPublicPath(path)) {
            return chain.filter(exchange);
        }
        
        String token = extractTokenFromRequest(exchange.getRequest());
        
        if (token == null) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }
        
        // Validate token
        return authManager.authenticate(token)
                .flatMap(user -> {
                    // Store authenticated user in exchange attributes
                    exchange.getAttributes().put("USER", user);
                    return chain.filter(exchange);
                })
                .onErrorResume(AuthenticationException.class, error -> {
                    exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
                    return exchange.getResponse().setComplete();
                });
    }
    
    private boolean isPublicPath(String path) {
        return path.startsWith("/public") || 
               path.equals("/login") || 
               path.equals("/signup");
    }
    
    private String extractTokenFromRequest(ServerHttpRequest request) {
        List<String> authHeader = request.getHeaders().get("Authorization");
        
        if (authHeader != null && !authHeader.isEmpty()) {
            String auth = authHeader.get(0);
            if (auth.startsWith("Bearer ")) {
                return auth.substring(7);
            }
        }
        
        return null;
    }
}
```

### 📌 CORS Filter

Spring provides a built-in CORS filter that you can configure:

```java
@Configuration
public class CorsConfig {
    
    @Bean
    public CorsWebFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        
        config.setAllowCredentials(true);
        config.addAllowedOrigin("https://example.com");
        config.addAllowedHeader("*");
        config.addAllowedMethod("*");
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        
        return new CorsWebFilter(source);
    }
}
```

### 📌 Rate Limiting Filter

This filter implements basic rate limiting:

```java
@Component
public class RateLimitingFilter implements WebFilter {
    
    private final Map<String, RateLimiter> limiters = new ConcurrentHashMap<>();
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String ip = exchange.getRequest().getRemoteAddress().getAddress().getHostAddress();
        
        // Get or create rate limiter for this IP
        RateLimiter limiter = limiters.computeIfAbsent(ip, 
                k -> RateLimiter.create(10.0)); // 10 requests per second
        
        if (limiter.tryAcquire()) {
            // Request is within rate limits
            return chain.filter(exchange);
        } else {
            // Too many requests
            exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
            return exchange.getResponse().writeWith(
                    Mono.just(exchange.getResponse().bufferFactory()
                            .wrap("Too many requests".getBytes())));
        }
    }
}
```

## 5. 🔧 Advanced WebFilter Techniques
---------

### 📌 Modifying Request and Response

WebFilters can modify request or response objects:

```java
@Component
public class RequestTransformationFilter implements WebFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Create a mutated exchange with an additional header
        ServerWebExchange mutatedExchange = exchange.mutate()
                .request(builder -> builder.header("X-Custom-Header", "CustomValue"))
                .build();
        
        return chain.filter(mutatedExchange);
    }
}
```

### 📌 Handling Request Body

Working with the request body in a filter requires special handling:

```java
@Component
public class RequestBodyModificationFilter implements WebFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        
        // Only process JSON content
        if (request.getHeaders().getContentType() != null && 
                request.getHeaders().getContentType().includes(MediaType.APPLICATION_JSON)) {
            
            return DataBufferUtils.join(request.getBody())
                    .flatMap(dataBuffer -> {
                        // Read the original body
                        byte[] bytes = new byte[dataBuffer.readableByteCount()];
                        dataBuffer.read(bytes);
                        DataBufferUtils.release(dataBuffer);
                        
                        // Process the body content
                        String bodyString = new String(bytes, StandardCharsets.UTF_8);
                        
                        // Perform modifications (e.g., adding a timestamp)
                        try {
                            ObjectMapper mapper = new ObjectMapper();
                            JsonNode node = mapper.readTree(bodyString);
                            ((ObjectNode) node).put("timestamp", System.currentTimeMillis());
                            
                            bodyString = mapper.writeValueAsString(node);
                        } catch (IOException e) {
                            return Mono.error(e);
                        }
                        
                        // Create a new request with the modified body
                        byte[] modifiedBytes = bodyString.getBytes(StandardCharsets.UTF_8);
                        Flux<DataBuffer> modifiedBody = Flux.just(
                                exchange.getResponse().bufferFactory().wrap(modifiedBytes));
                        
                        ServerHttpRequest modifiedRequest = request.mutate()
                                .body(modifiedBody)
                                .build();
                        
                        return chain.filter(exchange.mutate().request(modifiedRequest).build());
                    });
        }
        
        // For non-JSON requests, proceed unchanged
        return chain.filter(exchange);
    }
}
```

### 📌 Response Modification

Modifying the response requires wrapping the response body:

```java
@Component
public class ResponseHeaderFilter implements WebFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpResponse response = exchange.getResponse();
        
        // Add headers to all responses
        response.getHeaders().add("X-App-Version", "1.0.0");
        
        return chain.filter(exchange);
    }
}
```

For more complex response modifications:

```java
@Component
public class ResponseModificationFilter implements WebFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Get original response
        ServerHttpResponse originalResponse = exchange.getResponse();
        
        // Create response decorator
        ServerHttpResponseDecorator decoratedResponse = new ServerHttpResponseDecorator(originalResponse) {
            @Override
            public Mono<Void> writeWith(Publisher<? extends DataBuffer> body) {
                if (body instanceof Flux) {
                    Flux<? extends DataBuffer> fluxBody = (Flux<? extends DataBuffer>) body;
                    
                    return super.writeWith(fluxBody.buffer().map(dataBuffers -> {
                        DataBufferFactory factory = originalResponse.bufferFactory();
                        
                        // Join all data buffers
                        DataBuffer joinedBuffer = factory.join(dataBuffers);
                        byte[] content = new byte[joinedBuffer.readableByteCount()];
                        joinedBuffer.read(content);
                        DataBufferUtils.release(joinedBuffer);
                        
                        // Convert to string for manipulation
                        String responseBody = new String(content, StandardCharsets.UTF_8);
                        
                        // Modify response body (example: add a timestamp)
                        try {
                            MediaType contentType = originalResponse.getHeaders().getContentType();
                            
                            // Only modify JSON responses
                            if (contentType != null && contentType.includes(MediaType.APPLICATION_JSON)) {
                                ObjectMapper mapper = new ObjectMapper();
                                JsonNode node = mapper.readTree(responseBody);
                                
                                // Add field to response
                                ((ObjectNode) node).put("processedAt", System.currentTimeMillis());
                                
                                responseBody = mapper.writeValueAsString(node);
                            }
                        } catch (IOException e) {
                            // Log error but continue with original response
                            System.err.println("Error modifying response: " + e.getMessage());
                        }
                        
                        // Create a new buffer with the modified content
                        byte[] modifiedContent = responseBody.getBytes(StandardCharsets.UTF_8);
                        originalResponse.getHeaders().setContentLength(modifiedContent.length);
                        
                        return factory.wrap(modifiedContent);
                    }).flatMap(dataBuffer -> Flux.just(dataBuffer)));
                }
                
                // If not a Flux, return body without modification
                return super.writeWith(body);
            }
        };
        
        // Replace response in exchange with decorator and continue
        return chain.filter(exchange.mutate().response(decoratedResponse).build());
    }
}
```

## 6. ⚠️ Common Pitfalls & Best Practices
---------

### ❌ Common Pitfalls

1. **Forgetting to continue the filter chain**
   ```java
   // BAD: This will stop request processing
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       logger.info("Request received");
       // Missing chain.filter(exchange)
       return Mono.empty();
   }
   ```

2. **Blocking operations in filter**
   ```java
   // BAD: Blocking calls in reactive code
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       // Blocking call!
       Thread.sleep(100);
       return chain.filter(exchange);
   }
   ```

3. **Not handling errors properly**
   ```java
   // BAD: No error handling
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       return doSomethingRisky()
               .then(chain.filter(exchange));  // If doSomethingRisky() fails, chain won't be called
   }
   ```

4. **Consuming the request body without replacing it**
   ```java
   // BAD: Consuming the body without making it available again
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       return exchange.getRequest().getBody()
               .doOnNext(buffer -> {
                   // Read the buffer
                   byte[] bytes = new byte[buffer.readableByteCount()];
                   buffer.read(bytes);
               })
               .then(chain.filter(exchange));  // Body is now consumed and unavailable!
   }
   ```

### ✅ Best Practices

1. **Always continue the filter chain**
   ```java
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       logger.info("Request received");
       return chain.filter(exchange)
               .doFinally(signalType -> logger.info("Request completed"));
   }
   ```

2. **Use reactive patterns consistently**
   ```java
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       return Mono.fromCallable(() -> {
           // Compute something
           return computeSomething();
       })
       .subscribeOn(Schedulers.boundedElastic())  // Move blocking work off event loop
       .flatMap(result -> {
           exchange.getAttributes().put("computed", result);
           return chain.filter(exchange);
       });
   }
   ```

3. **Proper error handling**
   ```java
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       return doSomethingRisky()
               .flatMap(result -> {
                   exchange.getAttributes().put("result", result);
                   return chain.filter(exchange);
               })
               .onErrorResume(error -> {
                   logger.error("Error in filter", error);
                   exchange.getResponse().setStatusCode(HttpStatus.INTERNAL_SERVER_ERROR);
                   return exchange.getResponse().setComplete();
               });
   }
   ```

4. **Preserve or replace request body**
   ```java
   @Override
   public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
       return DataBufferUtils.join(exchange.getRequest().getBody())
               .map(dataBuffer -> {
                   // Create a copy for the filter to use
                   byte[] bytes = new byte[dataBuffer.readableByteCount()];
                   dataBuffer.read(bytes);
                   DataBufferUtils.release(dataBuffer);
                   
                   // Do something with bytes
                   processBytes(bytes);
                   
                   // Create a new buffer for downstream consumers
                   return exchange.getResponse().bufferFactory().wrap(bytes);
               })
               .flatMap(dataBuffer -> {
                   // Create a new request with the same body content
                   Flux<DataBuffer> body = Flux.just(dataBuffer);
                   ServerHttpRequest request = exchange.getRequest().mutate()
                           .body(body)
                           .build();
                   
                   return chain.filter(exchange.mutate().request(request).build());
               });
   }
   ```

5. **Graceful filter order management**
   ```java
   @Component
   @Order(Ordered.HIGHEST_PRECEDENCE + 10)  // Relative ordering
   public class SecurityFilter implements WebFilter {
       // Implementation
   }
   ```

## 7. 📊 Testing WebFilters
---------

### 📌 Unit Testing

Test WebFilters in isolation:

```java
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.mock.web.reactive.function.server.MockServerRequest;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilterChain;
import org.springframework.mock.http.server.reactive.MockServerHttpRequest;
import org.springframework.mock.web.server.MockServerWebExchange;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

public class LoggingWebFilterTests {
    
    @Test
    public void testLoggingWebFilter() {
        // Create a mock WebFilterChain
        WebFilterChain chain = Mockito.mock(WebFilterChain.class);
        Mockito.when(chain.filter(Mockito.any(ServerWebExchange.class)))
                .thenReturn(Mono.empty());
        
        // Create a mock request
        MockServerHttpRequest request = MockServerHttpRequest
                .get("/test")
                .build();
        
        // Create a mock exchange
        ServerWebExchange exchange = MockServerWebExchange.from(request);
        
        // Create filter
        LoggingWebFilter filter = new LoggingWebFilter();
        
        // Execute and verify
        StepVerifier.create(filter.filter(exchange, chain))
                .verifyComplete();
        
        // Verify filter chain was called
        Mockito.verify(chain).filter(exchange);
    }
}
```

### 📌 Integration Testing

Test WebFilters integrated with your application:

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.reactive.server.WebTestClient;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class WebFilterIntegrationTests {
    
    @Autowired
    private WebTestClient webTestClient;
    
    @Test
    public void testEndpointWithFilters() {
        webTestClient.get()
                .uri("/api/test")
                .exchange()
                .expectStatus().isOk()
                .expectHeader().exists("X-App-Version")  // Check header added by filter
                .expectBody(String.class)
                .isEqualTo("Test response");
    }
    
    @Test
    public void testSecurityFilter() {
        // Test without auth token
        webTestClient.get()
                .uri("/api/secured")
                .exchange()
                .expectStatus().isUnauthorized();
        
        // Test with auth token
        webTestClient.get()
                .uri("/api/secured")
                .header("Authorization", "Bearer valid-token")
                .exchange()
                .expectStatus().isOk();
    }
}
```

## 8. 🌐 Real-world Examples
---------

### 📌 Global Exception Handling Filter

Catch and process exceptions from all routes:

```java
@Component
@Order(-2)  // Run before other filters
public class GlobalExceptionFilter implements WebFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        return chain.filter(exchange)
                .onErrorResume(e -> {
                    logger.error("Unhandled exception in request processing", e);
                    
                    ServerHttpResponse response = exchange.getResponse();
                    response.setStatusCode(HttpStatus.INTERNAL_SERVER_ERROR);
                    response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
                    
                    // Create error response
                    Map<String, Object> errorDetails = new HashMap<>();
                    errorDetails.put("timestamp", new Date());
                    errorDetails.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
                    errorDetails.put("error", HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase());
                    errorDetails.put("message", e.getMessage());
                    errorDetails.put("path", exchange.getRequest().getURI().getPath());
                    
                    try {
                        String json = new ObjectMapper().writeValueAsString(errorDetails);
                        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
                        
                        DataBuffer buffer = response.bufferFactory().wrap(bytes);
                        return response.writeWith(Mono.just(buffer));
                    } catch (JsonProcessingException jsonException) {
                        return Mono.error(jsonException);
                    }
                });
    }
}
```

### 📌 Request Tracing Filter

Add request tracing capability:

```java
@Component
@Order(1)
public class RequestTracingFilter implements WebFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(RequestTracingFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        // Generate or extract trace ID
        String traceId = extractTraceId(exchange.getRequest());
        
        // Add trace ID to MDC for logging
        return Mono.fromRunnable(() -> MDC.put("traceId", traceId))
                .then(Mono.defer(() -> {
                    // Add trace ID to response headers
                    exchange.getResponse().getHeaders().add("X-Trace-ID", traceId);
                    
                    // Add trace ID to exchange attributes
                    exchange.getAttributes().put("traceId", traceId);
                    
                    logger.info("Request started: {} {}", 
                            exchange.getRequest().getMethod(),
                            exchange.getRequest().getURI());
                    
                    return chain.filter(exchange)
                            .doFinally(signalType -> {
                                logger.info("Request completed with status: {}", 
                                        exchange.getResponse().getStatusCode());
                                MDC.remove("traceId");
                            });
                }));
    }
    
    private String extractTraceId(ServerHttpRequest request) {
        List<String> existingTraceHeaders = request.getHeaders().get("X-Trace-ID");
        
        if (existingTraceHeaders != null && !existingTraceHeaders.isEmpty()) {
            return existingTraceHeaders.get(0);
        }
        
        // Generate new trace ID
        return UUID.randomUUID().toString();
    }
}
```

### 📌 API Key Validation Filter

Validate API keys for secure endpoints:

```java
@Component
public class ApiKeyFilter implements WebFilter {
    
    private final Set<String> validApiKeys;
    
    public ApiKeyFilter(@Value("${api.keys}") String[] configuredApiKeys) {
        this.validApiKeys = new HashSet<>(Arrays.asList(configuredApiKeys));
    }
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getURI().getPath();
        
        // Only check API endpoints
        if (path.startsWith("/api/")) {
            List<String> apiKeyHeader = request.getHeaders().get("X-API-Key");
            
            if (apiKeyHeader == null || apiKeyHeader.isEmpty()) {
                return unauthorizedResponse(exchange, "Missing API key");
            }
            
            String apiKey = apiKeyHeader.get(0);
            
            if (!validApiKeys.contains(apiKey)) {
                return unauthorizedResponse(exchange, "Invalid API key");
            }
        }
        
        return chain.filter(exchange);
    }
    
    private Mono<Void> unauthorizedResponse(ServerWebExchange exchange, String message) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.UNAUTHORIZED);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        Map<String, Object> errorDetails = new HashMap<>();
        errorDetails.put("error", "Unauthorized");
        errorDetails.put("message", message);
        
        try {
            String json = new ObjectMapper().writeValueAsString(errorDetails);
            byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
            
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (JsonProcessingException e) {
            return Mono.error(e);
        }
    }
}
```

## 9. 📝 Summary
---------

### 📌 Key Takeaways

1. **WebFilter Basics**
   - Interface for intercepting and processing requests/responses
   - Reactive, non-blocking design
   - Part of the Spring WebFlux stack

2. **Implementation Steps**
   - Implement WebFilter interface
   - Configure with @Component and @Order
   - Control filter order for proper sequencing

3. **Common Use Cases**
   - Logging and monitoring
   - Authentication and security
   - Request/response transformation
   - Rate limiting and throttling

4. **Best Practices**
   - Maintain reactive context
   - Properly handle the filter chain
   - Use proper error handling
   - Be careful with request/response body consumption

5. **Advanced Techniques**
   - Request/response body modification
   - Exchange attribute manipulation
   - Reactive composition with other operations

### 📌 Reference Table

| Topic | Key Points |
|-------|------------|
| WebFilter Interface | - `filter(ServerWebExchange, WebFilterChain)` method<br>- Returns `Mono<Void>` |
| ServerWebExchange | - Contains request and response<br>- Has attributes for storing data<br>- Can be mutated to create modified exchanges |
| WebFilterChain | - Continues filter processing<br>- Must be called to proceed<br>- Returns `Mono<Void>` |
| Filter Order | - Use `@Order` annotation<br>- Implement `Ordered` interface<br>- Lower values = higher priority |
| Common Filters | - Security/Authentication<br>- Logging<br>- CORS<br>- Rate limiting |
| Best Practices | - Maintain reactive flow<br>- Proper error handling<br>- Careful body handling<br>- Clear responsibility separation |

---

By following this guide, you should now have a solid understanding of WebFilters in Spring WebFlux and be able to implement them effectively in your applications. Remember to keep your filters focused, maintain proper ordering, and adhere to reactive programming patterns for optimal performance.