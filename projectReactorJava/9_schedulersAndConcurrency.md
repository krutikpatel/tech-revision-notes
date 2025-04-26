# 1. 🌐 Project Reactor Schedulers and Concurrency Overview

Project Reactor provides sophisticated concurrency support through its Scheduler system. Schedulers in Reactor allow you to control which threads execute different parts of your reactive pipelines, without having to manually manage thread creation, pooling, or synchronization.

Understanding schedulers is crucial for building efficient reactive applications, especially when dealing with blocking operations or CPU-intensive tasks.

---------

# 2. 🧩 Reactor's Concurrency Model

## 2.1 Non-blocking by Default

✅ **Key Concept**: Project Reactor is non-blocking by default.

📌 **Interview Insight**: By default, operators in a reactive chain execute on the same thread that triggers the subscription, not creating new threads unless explicitly requested.

```java
// Simple example - all operations likely run on the main thread
Flux.range(1, 10)
    .map(i -> i * 2)
    .filter(i -> i > 5)
    .subscribe(System.out::println);
```

## 2.2 Schedulers vs. Java's ExecutorService

✅ **Key Difference**: Schedulers abstract over thread pools and provide specific scheduling strategies.

📌 **Interview Insight**: Unlike ExecutorService which just executes tasks, Schedulers are optimized for reactive workloads with specific characteristics.

```java
// ExecutorService approach (traditional)
ExecutorService executor = Executors.newFixedThreadPool(4);
executor.submit(() -> doWork());

// Reactor Scheduler approach (reactive)
Scheduler scheduler = Schedulers.parallel();
Mono.fromCallable(() -> doWork())
    .subscribeOn(scheduler)
    .subscribe();
```

---------

# 3. 🔍 Understanding Reactor Scheduler Types

## 3.1 `Schedulers.immediate()`

✅ **Purpose**: Execute on the current thread without scheduling.

```java
Flux.range(1, 10)
    .publishOn(Schedulers.immediate())
    .map(i -> {
        System.out.println("Thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .subscribe();
```

📌 **Interview Insight**: Useful for testing or when you explicitly want to avoid thread switching.

## 3.2 `Schedulers.single()`

✅ **Purpose**: Execute on a single, reusable thread.

```java
Flux.range(1, 10)
    .publishOn(Schedulers.single())
    .map(i -> {
        System.out.println("Thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .subscribe();
```

📌 **Interview Insight**: Good for simple, sequential tasks that benefit from being off the main thread.

## 3.3 `Schedulers.parallel()`

✅ **Purpose**: Execute on a fixed-size pool of workers (typically CPU core count).

```java
Flux.range(1, 10)
    .publishOn(Schedulers.parallel())
    .map(i -> {
        System.out.println("Thread: " + Thread.currentThread().getName());
        return computeIntensiveOperation(i);
    })
    .subscribe();
```

📌 **Interview Insight**: Ideal for CPU-intensive tasks; the pool size matches your CPU cores.

## 3.4 `Schedulers.boundedElastic()`

✅ **Purpose**: Execute on a pool that can grow and shrink, with a limit.

```java
Flux.range(1, 10)
    .publishOn(Schedulers.boundedElastic())
    .map(i -> {
        System.out.println("Thread: " + Thread.currentThread().getName());
        return blockingDatabaseCall(i);
    })
    .subscribe();
```

📌 **Interview Insight**: Best choice for I/O-bound or blocking operations; prevents thread starvation.

❌ **Common Mistake**: Using `parallel()` for I/O operations:
```java
// WRONG: Using parallel scheduler for blocking I/O
Flux.range(1, 100)
    .publishOn(Schedulers.parallel()) // Could exhaust all CPU threads
    .map(i -> blockingDatabaseCall(i))
    .subscribe();

// CORRECT: Using boundedElastic for blocking operations
Flux.range(1, 100)
    .publishOn(Schedulers.boundedElastic())
    .map(i -> blockingDatabaseCall(i))
    .subscribe();
```

## 3.5 Creating Custom Schedulers

✅ **Usage**: Create schedulers with custom thread pools.

```java
// Create a custom scheduler
Scheduler customScheduler = Schedulers.newParallel(
    "my-custom-pool", // Thread prefix name
    4,                // Number of threads
    true              // Daemon threads flag
);

Flux.range(1, 10)
    .publishOn(customScheduler)
    .map(i -> specializedOperation(i))
    .subscribe();
```

📌 **Interview Insight**: Useful for dedicated thread pools with specific threading requirements.

---------

# 4. 🔀 Switching Execution Context

## 4.1 `subscribeOn` Operator

✅ **Purpose**: Specifies which scheduler performs the subscription and affects the entire chain.

```java
Flux.range(1, 10)
    .map(i -> {
        System.out.println("Map1 thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .subscribeOn(Schedulers.boundedElastic()) // Affects entire chain
    .map(i -> {
        System.out.println("Map2 thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .subscribe();
```

📌 **Interview Insight**: The position of `subscribeOn()` in the chain doesn't matter - it affects the entire upstream chain.

ASCII diagram:
```
subscribeOn(scheduler) affects the ENTIRE chain:

[source] → [operator1] → [operator2] → [operator3] → [subscriber]
              ↑
              └── All executed on the specified scheduler
```

❌ **Common Mistake**: Adding multiple `subscribeOn` operators:

```java
// WRONG: Only the first subscribeOn has effect
Flux.range(1, 10)
    .subscribeOn(Schedulers.boundedElastic())
    .map(i -> compute(i))
    .subscribeOn(Schedulers.parallel()) // This has NO EFFECT!
    .subscribe();
```

## 4.2 `publishOn` Operator

✅ **Purpose**: Changes scheduler for subsequent operators in the chain.

```java
Flux.range(1, 10)
    .map(i -> {
        System.out.println("Map1 thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .publishOn(Schedulers.boundedElastic()) // Changes thread from here
    .map(i -> {
        System.out.println("Map2 thread: " + Thread.currentThread().getName());
        return i * 2;
    })
    .subscribe();
```

📌 **Interview Insight**: The position of `publishOn()` matters - it only affects operators after it in the chain.

ASCII diagram:
```
publishOn(scheduler) affects DOWNSTREAM operators:

[source] → [operator1] → [publishOn] → [operator2] → [subscriber]
                           ↓
                           └── Only these executed on the specified scheduler
```

## 4.3 Combining `subscribeOn` and `publishOn`

✅ **Usage**: Control both subscription and execution threads.

```java
Flux.range(1, 10)
    .subscribeOn(Schedulers.single()) // Controls subscription thread
    .map(i -> firstOperation(i))
    .publishOn(Schedulers.parallel()) // Switch to computation thread
    .map(i -> cpuIntensiveOperation(i))
    .publishOn(Schedulers.boundedElastic()) // Switch to I/O thread
    .map(i -> databaseOperation(i))
    .subscribe();
```

📌 **Interview Insight**: Common pattern is to use `subscribeOn` for overall source execution and `publishOn` to switch threads for specific operations.

---------

# 5. 🛠️ Advanced Concurrency Patterns

## 5.1 Parallel Processing with `parallel()`

✅ **Usage**: Split work across multiple threads.

```java
Flux.range(1, 100)
    .parallel(4) // Split into 4 "rails"
    .runOn(Schedulers.parallel()) // Assign each rail to parallel scheduler
    .map(i -> computeIntensiveOperation(i))
    .sequential() // Merge back to sequential flux
    .subscribe();
```

📌 **Interview Insight**: Returns a `ParallelFlux` that processes data in parallel "rails". `runOn()` is needed to actually assign threads.

ASCII diagram:
```
parallel() with runOn():

[1,2,3,4,5,6,7,8] → parallel(4) → runOn(scheduler)
                                   ↓
                       [1,5] [2,6] [3,7] [4,8]  (4 parallel rails)
                         ↓     ↓     ↓     ↓
                     process process process process
                         ↓     ↓     ↓     ↓
                       [R1,R5][R2,R6][R3,R7][R4,R8]
                                   ↓
                               sequential()
                                   ↓
                    [R1,R2,R3,R4,R5,R6,R7,R8]  (merged result)
```

❌ **Common Mistake**: Forgetting the `runOn()`:

```java
// WRONG: Missing runOn(), still runs on original thread
Flux.range(1, 100)
    .parallel(4)
    .map(i -> computeIntensiveOperation(i)) // Not actually parallel!
    .sequential()
    .subscribe();
```

## 5.2 FlatMap with Concurrency Control

✅ **Usage**: Process items concurrently with controlled parallelism.

```java
Flux.range(1, 100)
    .flatMap(
        i -> processAsync(i).subscribeOn(Schedulers.boundedElastic()),
        8 // concurrency limit
    )
    .subscribe();
```

📌 **Interview Insight**: The concurrency parameter limits how many inner publishers are subscribed to at once.

## 5.3 GroupBy for Parallel Processing

✅ **Usage**: Process different groups in parallel.

```java
Flux.range(1, 100)
    .groupBy(i -> i % 4) // Create 4 groups
    .flatMap(group -> 
        group.publishOn(Schedulers.parallel())
             .map(i -> computeForGroup(i))
    )
    .subscribe();
```

📌 **Interview Insight**: Useful for processing that naturally divides into independent groups.

---------

# 6. ⚠️ Handling Blocking Operations

## 6.1 Using `boundedElastic` for Blocking Calls

✅ **Usage**: Safely execute blocking code.

```java
Flux.range(1, 10)
    .flatMap(i -> 
        Mono.fromCallable(() -> blockingJdbcCall(i))
            .subscribeOn(Schedulers.boundedElastic())
    )
    .subscribe();
```

📌 **Interview Insight**: Wrap blocking calls in `Mono.fromCallable()` and use `boundedElastic` to prevent thread starvation.

## 6.2 Using `publishOn` vs `subscribeOn` for Blocking Operations

✅ **Best Practice**:

```java
// BETTER: Ensures publisher creation also happens on boundedElastic
Mono.fromCallable(() -> blockingOperation())
    .subscribeOn(Schedulers.boundedElastic());

// VS

// POTENTIALLY PROBLEMATIC: Only downstream operations run on boundedElastic
somePublisher
    .publishOn(Schedulers.boundedElastic())
    .map(data -> blockingOperation(data));
```

📌 **Interview Insight**: `subscribeOn` with `fromCallable` ensures even the callable execution runs on the non-blocking thread pool.

## 6.3 Project Reactor's `block()` Method

✅ **Usage**: Block until a result is available (usually for testing).

```java
// AVOID IN PRODUCTION CODE
Integer result = Flux.range(1, 10)
    .reduce(0, (a, b) -> a + b)
    .block(); // Blocks current thread until result available
```

❌ **Common Mistake**: Using `block()` in production code:

```java
// WRONG: Blocking in a reactive web application
@GetMapping("/data")
public List<Data> getData() {
    return dataService.fetchDataReactively()
        .collectList()
        .block(); // Defeats purpose of reactive programming!
}

// CORRECT: Stay reactive end-to-end
@GetMapping("/data")
public Flux<Data> getData() {
    return dataService.fetchDataReactively();
}
```

---------

# 7. 📊 Testing with Virtual Time

## 7.1 Using the `StepVerifier` with Virtual Time

✅ **Usage**: Test time-dependent operations without actual waiting.

```java
StepVerifier
    .withVirtualTime(() -> Flux.interval(Duration.ofSeconds(1)).take(3))
    .expectSubscription()
    .expectNoEvent(Duration.ofSeconds(1))
    .expectNext(0L)
    .thenAwait(Duration.ofSeconds(1))
    .expectNext(1L)
    .thenAwait(Duration.ofSeconds(1))
    .expectNext(2L)
    .verifyComplete();
```

📌 **Interview Insight**: Virtual time is crucial for testing time-based operators without slow tests.

## 7.2 `VirtualTimeScheduler` for Custom Testing

✅ **Usage**: Manually control virtual time progression.

```java
VirtualTimeScheduler scheduler = VirtualTimeScheduler.create();
Schedulers.setFactory(new Factory() {
    @Override
    public Scheduler createScheduler(ThreadFactory threadFactory) {
        return scheduler;
    }
});

Flux<Long> flux = Flux.interval(Duration.ofSeconds(1)).take(5);
flux.subscribe(System.out::println);

// Manually advance time
scheduler.advanceTimeBy(Duration.ofSeconds(6));

// Reset scheduler
Schedulers.resetFactory();
```

📌 **Interview Insight**: Useful for complex scenarios that StepVerifier doesn't handle elegantly.

---------

# 8. 🔍 Debugging Concurrency Issues

## 8.1 Using the `log()` Operator

✅ **Usage**: See which thread is executing each step.

```java
Flux.range(1, 5)
    .log("Source")
    .map(i -> i * 2)
    .publishOn(Schedulers.parallel())
    .log("After publishOn")
    .subscribe();
```

📌 **Interview Insight**: The `log()` operator shows detailed signal flow including thread information.

## 8.2 Adding `doOn...` Hooks with Thread Information

✅ **Usage**: Monitor thread transitions.

```java
Flux.range(1, 5)
    .doOnNext(i -> System.out.println("Source thread: " + 
        Thread.currentThread().getName()))
    .publishOn(Schedulers.parallel())
    .doOnNext(i -> System.out.println("After publishOn thread: " + 
        Thread.currentThread().getName()))
    .subscribe();
```

📌 **Interview Insight**: More targeted than `log()` when you only need thread information.

## 8.3 Using Reactor's Checkpoint Operators

✅ **Usage**: Add context for debugging stack traces.

```java
Flux.range(1, 10)
    .checkpoint("source-range")
    .map(i -> {
        if (i == 5) throw new RuntimeException("Boom!");
        return i;
    })
    .checkpoint("after-map")
    .publishOn(Schedulers.parallel())
    .subscribe();
```

📌 **Interview Insight**: Helps identify where errors occur in asynchronous code.

---------

# 9. 🔧 Performance Tuning

## 9.1 Controlling Prefetch Size

✅ **Usage**: Optimize memory usage and throughput.

```java
Flux.range(1, 1000)
    .publishOn(Schedulers.boundedElastic(), 32) // Prefetch 32 items
    .subscribe();
```

📌 **Interview Insight**: Default prefetch is often larger than needed; reducing it can lower memory usage.

## 9.2 Scheduler Tuning Parameters

✅ **Usage**: Customize thread pool behavior.

```java
Scheduler customScheduler = Schedulers.newBoundedElastic(
    10,     // Maximum number of threads
    1000,   // Maximum pending tasks
    "custom-pool", 
    60      // TTL in seconds for idle threads
);
```

📌 **Interview Insight**: Tuning scheduler parameters can significantly impact performance for specific workloads.

## 9.3 Avoiding Common Bottlenecks

✅ **Best Practices**:

```java
// GOOD: Proper CPU-intensive parallelization
Flux.range(1, 10000)
    .parallel()
    .runOn(Schedulers.parallel())
    .map(this::cpuIntensiveOperation)
    .sequential()
    .subscribe();

// GOOD: Proper I/O operation handling
Flux.range(1, 100)
    .flatMap(id -> 
        Mono.fromCallable(() -> blockingDbCall(id))
            .subscribeOn(Schedulers.boundedElastic()),
        10 // Concurrency limit
    )
    .subscribe();
```

❌ **Common Mistakes**:

```java
// BAD: Excessive parallelism
Flux.range(1, 100)
    .flatMap(id -> 
        processItem(id).subscribeOn(Schedulers.boundedElastic()),
        100 // Too much concurrency can overwhelm systems
    );

// BAD: Unbounded queue growth
Flux.create(sink -> {
    for (int i = 0; i < 1_000_000; i++) {
        sink.next(i); // No backpressure handling
    }
})
.publishOn(Schedulers.single())
.subscribe();
```

---------

# 10. 🏢 Real-world Applications

## 10.1 Web Applications with Spring WebFlux

✅ **Usage**: Non-blocking web services.

```java
@RestController
public class UserController {
    private final UserRepository userRepository;
    
    @GetMapping("/users")
    public Flux<User> getAllUsers() {
        return userRepository.findAll()
            // Use publishOn for CPU-intensive transformations
            .publishOn(Schedulers.parallel())
            .map(this::enrichUser);
    }
    
    @GetMapping("/users/{id}")
    public Mono<User> getUserById(@PathVariable String id) {
        return userRepository.findById(id)
            // Handle blocking operations properly
            .flatMap(user -> 
                Mono.fromCallable(() -> callLegacySystem(user))
                    .subscribeOn(Schedulers.boundedElastic())
            );
    }
}
```

📌 **Interview Insight**: Keep the entire pipeline reactive for best performance.

## 10.2 Reactive Database Access

✅ **Usage**: Optimizing database operations.

```java
public Flux<Order> getOrdersWithDetails(List<String> orderIds) {
    return Flux.fromIterable(orderIds)
        // Limit concurrent database calls
        .flatMap(id -> 
            orderRepository.findById(id)
                .flatMap(order ->
                    // Parallel fetch of order details
                    Flux.zip(
                        userRepository.findById(order.getUserId()),
                        itemRepository.findByOrderId(order.getId()).collectList()
                    )
                    .map(tuple -> {
                        User user = tuple.getT1();
                        List<Item> items = tuple.getT2();
                        order.setUser(user);
                        order.setItems(items);
                        return order;
                    })
                ),
            10 // Concurrency limit
        );
}
```

📌 **Interview Insight**: Combine `flatMap` with concurrency limits for controlled parallelism.

## 10.3 Event Processing Systems

✅ **Usage**: Efficient event pipeline processing.

```java
// Message consumption from Kafka/JMS
messageSource.receive()
    // Process messages in parallel but maintain ordering per key
    .groupBy(Message::getKey)
    .flatMap(group -> 
        group.publishOn(Schedulers.parallel())
             .flatMap(msg -> processMessage(msg))
    )
    // Use boundedElastic for database writes
    .publishOn(Schedulers.boundedElastic())
    .flatMap(result -> saveToDatabase(result))
    .subscribe();
```

📌 **Interview Insight**: Different stages of the pipeline may require different concurrency models.

---------

# 11. 📝 Summary of Schedulers and Concurrency in Project Reactor

✅ **Key Concepts**:
- Project Reactor is non-blocking by default
- Schedulers control which threads execute your reactive code
- Different scheduler types are optimized for different workloads
- `subscribeOn` affects the entire chain, regardless of position
- `publishOn` affects only downstream operators
- Use `boundedElastic` for blocking operations
- Parallel processing can be achieved with `parallel()`, `flatMap`, or `groupBy`

✅ **Best Practices**:
- Match scheduler type to workload characteristics
- Use `parallel()` with `runOn()` for CPU-bound parallel work
- Wrap blocking calls in `fromCallable().subscribeOn(boundedElastic())`
- Avoid `block()` in production code
- Control concurrency with flatMap's concurrency parameter
- Use virtual time for testing time-based operations

✅ **Common Pitfalls to Avoid**:
- Using multiple `subscribeOn` operators (only first one has effect)
- Using `parallel()` without `runOn()`
- Executing blocking operations on non-elastic schedulers
- Using excessive parallelism without considering resource limits
- Blocking the event loop thread in reactive applications

---------

# 12. 📊 Scheduler Types Quick Reference Table

| Scheduler Type | Created With | Thread Count | Use For | Avoid For | Example |
|----------------|--------------|--------------|---------|-----------|---------|
| `immediate()` | `Schedulers.immediate()` | 0 (current thread) | Testing, avoiding thread switches | Blocking operations | Unit tests |
| `single()` | `Schedulers.single()` | 1 | Simple sequential tasks | CPU-intensive work | Background tasks |
| `parallel()` | `Schedulers.parallel()` | CPU cores | CPU-intensive computation | Blocking I/O | Data processing |
| `boundedElastic()` | `Schedulers.boundedElastic()` | Dynamic (bounded) | I/O operations, blocking calls | CPU-intensive work | Database calls |
| Custom | `Schedulers.newParallel()`, `newBoundedElastic()`, etc. | Configurable | Specialized requirements | - | Domain-specific needs |

| Operator | Purpose | Affects | Example Use Case |
|----------|---------|---------|------------------|
| `subscribeOn()` | Set thread for subscription and source | Entire chain | Setting source execution thread |
| `publishOn()` | Set thread for downstream operators | Operators after it | Changing context mid-chain |
| `parallel().runOn()` | Split work across multiple threads | Parallel processing | CPU-intensive work |

Understanding Reactor's concurrency model and scheduler types is essential for building efficient reactive applications. The key is selecting the right scheduler for each type of work and properly handling transitions between blocking and non-blocking code.