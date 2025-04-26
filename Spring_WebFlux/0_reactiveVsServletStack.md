# Reactive vs Servlet Stack in Spring: Interview Preparation Guide 🚀

This guide will help you understand the key differences between Spring's Reactive and Servlet stacks for your upcoming interviews, with practical examples and insights.

## 1. 🌐 Understanding the Two Stacks
---------

Spring Framework offers two distinct web application stacks:

### Servlet Stack:
- Built on Java Servlet API
- Uses Spring MVC
- Synchronous and blocking by nature
- One-thread-per-request model

### Reactive Stack:
- Built on Reactive Streams specification
- Uses Spring WebFlux
- Asynchronous and non-blocking by design
- Event-loop concurrency model

📌 **Key Insight**: Both stacks serve different purposes and choosing between them depends on your application's requirements rather than one being inherently "better" than the other.

```
                    ┌─────────────────────────┐
                    │     Spring Framework    │
                    └───────────┬─────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
    ┌───────────▼────────────┐      ┌──────────▼─────────────┐
    │      Servlet Stack     │      │     Reactive Stack     │
    │     (Spring MVC)       │      │     (Spring WebFlux)   │
    └───────────┬────────────┘      └──────────┬─────────────┘
                │                               │
    ┌───────────▼────────────┐      ┌──────────▼─────────────┐
    │    Java Servlet API    │      │     Reactive Streams   │
    └────────────────────────┘      └────────────────────────┘
```

✅ **Interview Tip**: Don't present WebFlux as an "upgrade" to Spring MVC. They're different tools for different scenarios.

## 2. 🧩 Core Architecture Comparison
---------

### Thread Model:

**Servlet Stack (Spring MVC):**
- One thread per request model
- Thread remains blocked until response is complete
- Relies on thread pool to handle concurrent requests

**Reactive Stack (WebFlux):**
- Event-loop with small number of threads
- Non-blocking operations
- Can handle many concurrent connections with fewer threads

📊 **Visual Comparison**:

```
Servlet Stack (MVC):
┌────────┐     ┌─────────────┐     ┌────────────┐
│Request ├────►│Servlet Thread├────►│   Response │
└────────┘     │  (blocked)   │     └────────────┘
               └─────────────┘
               
Reactive Stack (WebFlux):
┌────────┐     ┌─────────────┐     ┌────────────┐
│Request ├────►│ Event Loop  ├────►│   Response │
└────────┘     │(non-blocking)│     └────────────┘
               └──────┬──────┘
                      │        ┌────────────────┐
                      └────────┤Other operations│
                               └────────────────┘
```

✅ **Best Practice**: Choose Servlet Stack for CPU-bound applications and Reactive Stack for I/O-bound applications with high concurrency requirements.

## 3. 📝 Programming Model
---------

### Servlet Stack (Spring MVC):

```java
@RestController
@RequestMapping("/users")
public class UserController {
    
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return userService.findById(id); // Blocking call
    }
    
    @GetMapping
    public List<User> getAllUsers() {
        return userService.findAll(); // Returns entire collection
    }
}
```

### Reactive Stack (WebFlux):

```java
@RestController
@RequestMapping("/users")
public class UserController {
    
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public Mono<User> getUserById(@PathVariable Long id) {
        return userService.findById(id); // Returns a Mono (0-1 elements)
    }
    
    @GetMapping
    public Flux<User> getAllUsers() {
        return userService.findAll(); // Returns a Flux (0-N elements)
    }
}
```

📌 **Key Differences**:
- Return types: Objects/Collections vs Mono/Flux
- Processing model: Imperative vs Reactive
- Error handling approach: Try/catch vs operators

❌ **Common Mistake**: Returning Mono/Flux but still using blocking operations inside service methods, negating the benefits of the reactive stack.

## 4. ⚡ Performance Characteristics
---------

### Memory Utilization:

**Servlet Stack:**
- Consumes memory for each thread (typically 1MB+ per thread)
- Thread pool size is a limiting factor for concurrent requests
- Memory usage scales linearly with concurrent connections

**Reactive Stack:**
- Uses fewer threads (typically # of CPU cores)
- Much lower memory footprint per connection
- Better memory utilization with high concurrency

### Response Time:

**Servlet Stack:**
- Good for simple, quick operations
- Predictable performance under normal load
- Degrades rapidly under heavy load

**Reactive Stack:**
- Slightly higher overhead for simple operations
- Maintains consistent performance under heavy load
- Excels when there are slow I/O operations

📊 **Performance Comparison**:

```
                  Low Traffic │ Medium Traffic │ High Traffic
                 ─────────────┼────────────────┼──────────────
Servlet Stack    Excellent    │     Good       │   Poor
                 ─────────────┼────────────────┼──────────────
Reactive Stack   Good         │   Excellent    │   Excellent
```

✅ **Interview Insight**: In interviews, mention that reactive programming doesn't always yield better performance - it depends on the workload and resource constraints.

## 5. 🔄 Use Cases & Selection Criteria
---------

### When to Choose Servlet Stack (MVC):

1. **CRUD applications** with simple workflows
2. **Synchronous processing** requirements
3. **Teams familiar** with imperative programming
4. **Short-lived requests** with immediate responses
5. **Integration with blocking libraries** without reactive alternatives

### When to Choose Reactive Stack (WebFlux):

1. **High concurrency** requirements with limited resources
2. **Streaming** data applications (real-time feeds, SSE)
3. **Asynchronous workflows** with complex operations
4. **Microservices** calling other microservices
5. **Long-lived connections** where thread-per-request would be inefficient

❌ **Interview Trap**: Don't say "always use WebFlux because it's newer and better." Explain that it's about selecting the right tool for specific use cases.

## 6. 📊 API Comparison
---------

### Data Access:

**Spring MVC (with Spring Data JPA):**
```java
@Service
public class UserService {
    
    private final UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

**WebFlux (with Spring Data Reactive):**
```java
@Service
public class UserService {
    
    private final ReactiveUserRepository userRepository;
    
    public UserService(ReactiveUserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public Mono<User> findById(Long id) {
        return userRepository.findById(id)
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }
}
```

### REST Client:

**Spring MVC (RestTemplate):**
```java
RestTemplate restTemplate = new RestTemplate();
User user = restTemplate.getForObject("https://api.example.com/users/1", User.class);
```

**WebFlux (WebClient):**
```java
WebClient webClient = WebClient.create("https://api.example.com");
Mono<User> userMono = webClient.get()
                              .uri("/users/{id}", 1)
                              .retrieve()
                              .bodyToMono(User.class);
```

✅ **Best Practice**: Even in a WebFlux application, you can use traditional repositories for some operations if reactive alternatives aren't available, but be careful not to block in reactive code.

## 7. 🚨 Error Handling
---------

### Spring MVC (Servlet Stack):

```java
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        try {
            User user = userService.findById(id);
            return ResponseEntity.ok(user);
        } catch (UserNotFoundException ex) {
            return ResponseEntity.notFound().build();
        } catch (Exception ex) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UserNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                           .body("User not found: " + ex.getMessage());
    }
}
```

### Spring WebFlux (Reactive Stack):

```java
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    public Mono<ResponseEntity<User>> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(user -> ResponseEntity.ok(user))
            .onErrorResume(UserNotFoundException.class, ex -> 
                Mono.just(ResponseEntity.notFound().build()))
            .onErrorResume(ex -> 
                Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build()));
    }
}
```

### Global Exception Handler:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    // Spring MVC
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UserNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                           .body("User not found: " + ex.getMessage());
    }
    
    // Spring WebFlux
    @ExceptionHandler
    public Mono<ResponseEntity<String>> handleUserNotFound(UserNotFoundException ex) {
        return Mono.just(ResponseEntity.status(HttpStatus.NOT_FOUND)
                       .body("User not found: " + ex.getMessage()));
    }
}
```

❌ **Common Mistake**: Using blocking exception handling methods in reactive code or forgetting to handle errors in reactive chains.

## 8. 🧪 Testing Approaches
---------

### Testing Servlet Stack (MVC):

```java
@WebMvcTest(UserController.class)
public class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    public void shouldReturnUser() throws Exception {
        User user = new User(1L, "John");
        when(userService.findById(1L)).thenReturn(user);
        
        mockMvc.perform(get("/users/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.id").value(1))
               .andExpect(jsonPath("$.name").value("John"));
    }
}
```

### Testing Reactive Stack (WebFlux):

```java
@WebFluxTest(UserController.class)
public class UserControllerTest {
    
    @Autowired
    private WebTestClient webTestClient;
    
    @MockBean
    private UserService userService;
    
    @Test
    public void shouldReturnUser() {
        User user = new User(1L, "John");
        when(userService.findById(1L)).thenReturn(Mono.just(user));
        
        webTestClient.get().uri("/users/1")
                   .exchange()
                   .expectStatus().isOk()
                   .expectBody()
                   .jsonPath("$.id").isEqualTo(1)
                   .jsonPath("$.name").isEqualTo("John");
    }
}
```

✅ **Interview Insight**: Be ready to explain the testing tools specific to each stack and how they differ in approaches to verification.

## 9. 🔨 Infrastructure & Deployment Considerations
---------

### Servlet Stack:

- Compatible with all servlet containers (Tomcat, Jetty, etc.)
- Well-established monitoring and management tools
- Mature ecosystem for deployment and operations
- Straightforward performance tuning (thread pool size)

### Reactive Stack:

- Can run on servlet containers or Netty (preferred)
- Different monitoring approach (focus on backpressure, event loop)
- Requires different performance tuning approaches
- May need updated operational procedures

📌 **Deployment Comparison**:

```
                  Servlet Stack     │     Reactive Stack
                 ───────────────────┼────────────────────────
Containers        Any servlet       │  Netty (preferred)
                  container         │  or servlet containers
                 ───────────────────┼────────────────────────
Memory Required   Higher            │  Lower
                 ───────────────────┼────────────────────────
Scaling Model     Scale up threads  │  Scale connections per
                  per server        │  thread
                 ───────────────────┼────────────────────────
Monitoring        Thread pools,     │  Event loops, 
Focus             queue size        │  backpressure
```

✅ **Best Practice**: When deploying reactive applications, avoid tuning based on thread pool metrics (like you would with servlet applications). Focus instead on event loop utilization and backpressure indicators.

## 10. 📝 Summary
---------

Spring provides two distinct web stacks to suit different application needs:

- **Servlet Stack (Spring MVC)**: Traditional, synchronous and blocking, one thread per request model. Ideal for simple CRUD applications with straightforward workflows.

- **Reactive Stack (Spring WebFlux)**: Modern, asynchronous and non-blocking, event-loop concurrency model. Designed for applications with high concurrency needs or streaming data requirements.

The choice between them should be based on:
1. Application workload (I/O-bound vs CPU-bound)
2. Concurrency requirements
3. Team familiarity with reactive programming
4. Integration with other systems and libraries

✅ **Interview Tip**: Emphasize that the decision isn't about which is "better" but which is more appropriate for specific use cases. Being able to articulate when to use each stack demonstrates mature engineering judgment.

## 11. 📊 Summary Table
---------

| Aspect | Servlet Stack (MVC) | Reactive Stack (WebFlux) |
|--------|---------------------|--------------------------|
| **Programming Model** | Imperative, synchronous | Declarative, asynchronous |
| **Concurrency** | Thread per request | Event loop, non-blocking |
| **Return Types** | Objects, Collections | Mono<T>, Flux<T> |
| **Memory Usage** | Higher (1MB+ per thread) | Lower (fewer threads) |
| **Performance Under Load** | Degrades with increasing load | Maintains better under high load |
| **I/O Operations** | Blocking | Non-blocking |
| **Learning Curve** | Lower, familiar | Higher, reactive paradigm |
| **Best For** | CRUD, simple workflows | High concurrency, streaming |
| **Web Server** | Any servlet container | Netty (preferred) |
| **Libraries** | All Java libraries | Reactive libraries |

✅ **Final Interview Advice**: In interviews, demonstrate that you understand the core principles and trade-offs rather than just implementation details. Being able to explain when and why to choose one stack over the other shows practical engineering judgment that interviewers value.