# Java Spring Framework: Spring WebFlux Guide for Interview Preparation 🚀

I'll help you understand Spring WebFlux concepts with practical examples and interview-focused insights. This guide is structured for efficient review in under 30 minutes.

## 1. 🔄 Reactive vs Servlet Stack
---------

Spring offers two web application stacks:

### Traditional Servlet Stack:
- Uses Spring MVC built on the Servlet API
- Blocking & synchronous processing model
- One thread per request architecture

### Reactive Stack:
- Uses Spring WebFlux built on Reactive Streams
- Non-blocking & asynchronous processing model
- Fewer threads handling more requests

📌 **Key Differences:**

```
┌─────────────────┬─────────────────────────┬─────────────────────────┐
│                 │ Spring MVC (Servlet)    │ Spring WebFlux          │
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ Programming     │ Imperative              │ Reactive                │
│ Model           │                         │                         │
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ Thread Model    │ One thread per request  │ Event loop (few threads)│
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ Concurrency     │ Thread pools           │ Event loops             │
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ I/O Model       │ Blocking               │ Non-blocking            │
├─────────────────┼─────────────────────────┼─────────────────────────┤
│ Back Pressure   │ No built-in support    │ Built-in support        │
└─────────────────┴─────────────────────────┴─────────────────────────┘
```

✅ **Interview Insight:** WebFlux is designed for applications that need to handle high concurrency with fewer threads, especially in microservices architecture with high throughput requirements.

❌ **Common Mistake:** Choosing WebFlux just because it's newer without evaluating if your use case benefits from reactive programming.

## 2. 📊 WebFlux Controllers
---------

Spring WebFlux offers an annotation-based programming model similar to Spring MVC but returns reactive types.

### Basic Controller Example:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserRepository userRepository;
    
    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @GetMapping("/{id}")
    public Mono<User> getUserById(@PathVariable String id) {
        return userRepository.findById(id);
    }
    
    @GetMapping
    public Flux<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    @PostMapping
    public Mono<User> createUser(@RequestBody Mono<User> userMono) {
        return userMono.flatMap(userRepository::save);
    }
}
```

### Key Reactive Types:
- `Mono<T>`: Returns 0 or 1 elements (similar to Optional/CompletableFuture)
- `Flux<T>`: Returns 0..N elements (similar to Stream/CompletableFuture<List>)

✅ **Best Practices:**
- Never block in controller methods
- Use proper error handling with `onErrorResume()`, `onErrorMap()`
- Understand when to use `map()` vs `flatMap()` operations

❌ **Interview Traps:**
- Using `block()` or `blockFirst()` in a WebFlux controller (defeats the purpose of reactive)
- Not handling errors properly in reactive chains
- Mixing blocking and non-blocking operations

📌 **Real-world Example:** Handling a streaming API response:

```java
@GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> streamEvents() {
    return Flux.interval(Duration.ofSeconds(1))
               .map(sequence -> ServerSentEvent.<String>builder()
                       .id(String.valueOf(sequence))
                       .event("periodic-event")
                       .data("SSE - " + LocalTime.now().toString())
                       .build());
}
```

## 3. 🧩 Functional Endpoints
---------

Spring WebFlux offers a functional programming model alternative to annotations for more explicit and declarative request handling.

### Basic Structure:

```java
@Configuration
public class UserRouterConfig {

    @Bean
    public RouterFunction<ServerResponse> userRoutes(UserHandler userHandler) {
        return RouterFunctions
            .route(GET("/api/users").and(accept(APPLICATION_JSON)), 
                   userHandler::getAllUsers)
            .andRoute(GET("/api/users/{id}").and(accept(APPLICATION_JSON)), 
                    userHandler::getUserById)
            .andRoute(POST("/api/users").and(contentType(APPLICATION_JSON)), 
                    userHandler::createUser);
    }
}
```

### Handler Class:

```java
@Component
public class UserHandler {
    private final UserRepository userRepository;
    
    public UserHandler(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public Mono<ServerResponse> getUserById(ServerRequest request) {
        String userId = request.pathVariable("id");
        return userRepository.findById(userId)
                .flatMap(user -> ServerResponse.ok()
                        .contentType(APPLICATION_JSON)
                        .bodyValue(user))
                .switchIfEmpty(ServerResponse.notFound().build());
    }
    
    public Mono<ServerResponse> getAllUsers(ServerRequest request) {
        return ServerResponse.ok()
                .contentType(APPLICATION_JSON)
                .body(userRepository.findAll(), User.class);
    }
    
    public Mono<ServerResponse> createUser(ServerRequest request) {
        return request.bodyToMono(User.class)
                .flatMap(userRepository::save)
                .flatMap(savedUser -> ServerResponse.created(
                        URI.create("/api/users/" + savedUser.getId()))
                        .bodyValue(savedUser));
    }
}
```

✅ **Interview Insight:** Functional endpoints provide more control over request handling logic and are often preferred for microservices that need fine-grained control over HTTP behavior.

📌 **Key Differences from Annotated Controllers:**
- More explicit request handling
- Easier testing in isolation
- More functional programming style
- Better separation of routing and handling logic

❌ **Common Mistakes:**
- Not properly handling the `ServerRequest` and `ServerResponse` types
- Forgetting content type or status code in responses
- Not handling empty results with `switchIfEmpty`

## 4. 🛠️ Advanced WebFlux Concepts
---------

### Error Handling:

```java
@GetMapping("/{id}")
public Mono<ResponseEntity<User>> getUserById(@PathVariable String id) {
    return userRepository.findById(id)
        .map(user -> ResponseEntity.ok(user))
        .defaultIfEmpty(ResponseEntity.notFound().build())
        .onErrorResume(e -> {
            log.error("Error fetching user", e);
            return Mono.just(ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .build());
        });
}
```

### WebClient for HTTP Requests:

```java
WebClient webClient = WebClient.create("https://api.example.com");

Mono<ResponseData> result = webClient.get()
    .uri("/data/{id}", id)
    .retrieve()
    .bodyToMono(ResponseData.class)
    .timeout(Duration.ofSeconds(5))
    .onErrorResume(WebClientResponseException.class, e -> {
        if (e.getStatusCode() == HttpStatus.NOT_FOUND) {
            return Mono.empty();
        }
        return Mono.error(e);
    });
```

### Testing WebFlux Controllers:

```java
@Test
public void testGetUserById() {
    Mono<User> userMono = Mono.just(new User("1", "Test User"));
    when(userRepository.findById("1")).thenReturn(userMono);
    
    webTestClient.get().uri("/api/users/1")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus().isOk()
        .expectBody(User.class)
        .value(user -> assertThat(user.getName()).isEqualTo("Test User"));
}
```

✅ **Best Practices:**
- Use `WebTestClient` for efficient endpoint testing
- Implement proper backpressure handling for streaming data
- Use `flatMap` for operations that return another publisher
- Use `map` for simple transformations

## 5. 🎯 Interview Focus Points
---------

### Performance Considerations:
- WebFlux is not always faster than Spring MVC - it depends on the use case
- Benefits most when dealing with I/O-bound applications (DB, network calls)
- Can handle more concurrent connections with fewer resources

### When to Choose WebFlux:
- Microservices with high concurrency requirements
- Applications with streaming data needs
- Systems that interact with reactive data sources/sinks

### When to Avoid WebFlux:
- CRUD applications with simple workflows
- Teams unfamiliar with reactive programming
- Applications where blocking libraries are heavily used

## 6. 📝 Summary
---------

Spring WebFlux is Spring's reactive web framework designed for non-blocking applications with high concurrency needs. It provides:

1. **Non-blocking I/O model** - efficient resource utilization
2. **Two programming models**:
   - Annotation-based controllers (similar to Spring MVC)
   - Functional endpoints (router functions + handler functions)
3. **Reactive types**:
   - `Mono<T>` - for 0..1 elements
   - `Flux<T>` - for 0..N elements
4. **Built-in backpressure** support
5. **Integration with reactive data repositories** (R2DBC, Reactive MongoDB, etc.)

## 7. 📊 Summary Table
---------

| Concept | Spring MVC | Spring WebFlux | Interview Focus |
|---------|------------|----------------|-----------------|
| Programming Model | Imperative | Reactive | Understanding reactive patterns |
| I/O Model | Blocking | Non-blocking | Resource efficiency |
| Controller Types | Annotated controllers | Annotated + Functional | Know both approaches |
| Return Types | Objects, Collections | Mono<T>, Flux<T> | Proper handling of reactive types |
| Error Handling | Try/catch, @ExceptionHandler | onErrorResume, onErrorMap | Reactive error flows |
| Client | RestTemplate | WebClient | WebClient API familiarity |
| Testing | MockMvc | WebTestClient | Reactive test methodology |
| Ideal Use Cases | Traditional CRUD apps | High-concurrency, streaming | When to choose each |

✅ **Interview Closing Tip:** Be prepared to discuss real-world scenarios where you'd choose WebFlux over MVC or vice versa. Don't present WebFlux as universally superior - it's a tool with specific strengths for specific use cases!