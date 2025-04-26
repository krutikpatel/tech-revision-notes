# 1. 📚 Project Reactor Creation Operators Overview

Project Reactor is a reactive programming library for building non-blocking applications on the JVM. Creation operators are the starting point of any reactive chain, allowing you to create various types of publishers that emit data.

Let's dive into the key creation operators you should know for your interviews!

---------

# 2. 🏭 Core Creation Operators

## 2.1 `just` - Creating a Mono from a single value

✅ **Usage**:
```java
Mono<String> mono = Mono.just("Hello Reactor");
```

📌 **Interview Insight**: `just` is eager - it captures the value immediately, not when subscribed to.

❌ **Common Mistake**: Passing `null` directly to `just` causes `NullPointerException`
```java
// Wrong - causes NullPointerException
Mono<String> mono = Mono.just(null);

// Correct - use Mono.empty() instead
Mono<String> mono = Mono.empty();
```

## 2.2 `fromSupplier` - Creating a Mono lazily

✅ **Usage**:
```java
Mono<String> mono = Mono.fromSupplier(() -> generateExpensiveString());
```

📌 **Interview Insight**: Evaluation happens only upon subscription, great for expensive operations.

## 2.3 `empty` - Creating an empty Mono

✅ **Usage**:
```java
Mono<String> emptyMono = Mono.empty();
```

📌 **Interview Insight**: Use for representing absence of value without errors.

## 2.4 `error` - Creating a failing Mono

✅ **Usage**:
```java
Mono<String> errorMono = Mono.error(new RuntimeException("Failed"));
```

📌 **Interview Insight**: Creates a publisher that immediately fails with the specified error.

---------

# 3. 🔄 Creating Flux Objects

## 3.1 `just` - Creating a Flux from known values

✅ **Usage**:
```java
Flux<String> flux = Flux.just("One", "Two", "Three");
```

📌 **Interview Insight**: All values are eagerly captured at creation time.

## 3.2 `fromIterable` - Creating a Flux from a collection

✅ **Usage**:
```java
List<String> list = Arrays.asList("One", "Two", "Three");
Flux<String> flux = Flux.fromIterable(list);
```

📌 **Interview Insight**: Great for working with existing collections.

## 3.3 `fromArray` - Creating a Flux from an array

✅ **Usage**:
```java
String[] array = {"One", "Two", "Three"};
Flux<String> flux = Flux.fromArray(array);
```

## 3.4 `range` - Creating numeric sequences

✅ **Usage**:
```java
// Creates a Flux that emits integers 1 through 5
Flux<Integer> flux = Flux.range(1, 5);
```

📌 **Interview Insight**: Useful for generating test data or pagination.

---------

# 4. ⏱️ Time-Based Creation Operators

## 4.1 `interval` - Creating timed emissions

✅ **Usage**:
```java
// Emits Long values 0, 1, 2... every second
Flux<Long> flux = Flux.interval(Duration.ofSeconds(1));
```

📌 **Interview Insight**: Creates an infinite sequence! Always use with `take()` or similar operators.

❌ **Common Mistake**: Forgetting to limit the sequence
```java
// Wrong - infinite sequence
Flux<Long> flux = Flux.interval(Duration.ofSeconds(1));

// Correct - limited to 5 elements
Flux<Long> flux = Flux.interval(Duration.ofSeconds(1)).take(5);
```

## 4.2 `delayElements` - Delaying emissions

✅ **Usage**:
```java
Flux<Integer> flux = Flux.range(1, 5)
                         .delayElements(Duration.ofMillis(100));
```

📌 **Interview Insight**: Great for rate limiting or simulating slow processes.

---------

# 5. 🧩 Advanced Creation Operators

## 5.1 `defer` - Deferring Mono/Flux creation

✅ **Usage**:
```java
Mono<Instant> mono = Mono.defer(() -> Mono.just(Instant.now()));
```

📌 **Interview Insight**: Creation is deferred until subscription. Each subscriber gets a fresh publisher.

❌ **Common Mistake**: Using `just` instead of `defer` for dynamic values:
```java
// Wrong - all subscribers get same timestamp
Mono<Instant> wrongMono = Mono.just(Instant.now());

// Correct - each subscriber gets current timestamp
Mono<Instant> correctMono = Mono.defer(() -> Mono.just(Instant.now()));
```

## 5.2 `create` - Programmatic creation with emitter

✅ **Usage**:
```java
Flux<String> flux = Flux.create(emitter -> {
    emitter.next("One");
    emitter.next("Two");
    emitter.complete();
});
```

📌 **Interview Insight**: Provides fine control over emissions. Great for bridging non-reactive APIs.

## 5.3 `generate` - Stateful generation

✅ **Usage**:
```java
Flux<Integer> flux = Flux.generate(
    () -> 0, // initial state
    (state, sink) -> {
        sink.next(state); // emit current state
        if (state == 10) {
            sink.complete(); // stop at 10
        }
        return state + 1; // update state for next iteration
    }
);
```

📌 **Interview Insight**: Great for stateful generation. State passed between iterations.

---------

# 6. 🔗 Combining Creation Operators

## 6.1 `concat` - Sequential combination

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B");
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> combined = Flux.concat(flux1, flux2); // A, B, C, D
```

📌 **Interview Insight**: Subscribes to publishers sequentially, waiting for each to complete.

## 6.2 `merge` - Parallel combination

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B").delayElements(Duration.ofMillis(100));
Flux<String> flux2 = Flux.just("C", "D").delayElements(Duration.ofMillis(50));
Flux<String> merged = Flux.merge(flux1, flux2); // May be C, D, A, B (interleaved)
```

📌 **Interview Insight**: Subscribes to all publishers at once, emissions may interleave.

## 6.3 `zip` - Combining corresponding elements

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B");
Flux<String> flux2 = Flux.just("1", "2");
Flux<Tuple2<String, String>> zipped = Flux.zip(flux1, flux2);
// Results in: (A,1), (B,2)
```

📌 **Interview Insight**: Waits for corresponding elements from all sources.

---------

# 7. 🚨 Error Handling Creation Operators

## 7.1 `onErrorReturn` - Fallback value on error

✅ **Usage**:
```java
Mono<String> mono = service.getData()
    .onErrorReturn("Fallback Value");
```

## 7.2 `onErrorResume` - Fallback publisher on error

✅ **Usage**:
```java
Mono<String> mono = service.getData()
    .onErrorResume(error -> Mono.just("Fallback Value"));
```

📌 **Interview Insight**: More powerful than `onErrorReturn` as it can choose fallback based on error type.

## 7.3 `onErrorContinue` - Continue on error

✅ **Usage**:
```java
Flux<Integer> flux = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i) // Division by zero for third element
    .onErrorContinue((error, item) -> {
        log.error("Error for item {}: {}", item, error.getMessage());
    });
```

📌 **Interview Insight**: Continues processing subsequent elements after an error.

---------

# 8. 🔄 Common Interview Scenarios & Best Practices

## 8.1 Choosing Between Mono vs Flux

✅ **Best Practice**: 
- Use `Mono` when expecting 0 or 1 result
- Use `Flux` when expecting multiple results or streams

## 8.2 Eager vs Lazy Creation

✅ **Best Practice**:
- Use `just` for immediately available values
- Use `fromSupplier`/`defer` for expensive computations

## 8.3 When to Use `create` vs Other Operators

✅ **Best Practice**:
- Use `create` for bridging non-reactive APIs
- Use standard operators for most other cases

## 8.4 Avoid Blocking in Creation

❌ **Common Mistake**:
```java
// Wrong - blocks thread
Mono<Data> mono = Mono.just(blockingOperation());

// Correct - offloads blocking call
Mono<Data> mono = Mono.fromCallable(() -> blockingOperation())
                    .subscribeOn(Schedulers.boundedElastic());
```

---------

# 9. 📊 Summary of Project Reactor Creation Operators

✅ **Core Concepts**:
- Creation operators are the starting point for reactive chains
- Choose between eager (`just`) and lazy evaluation (`defer`, `fromSupplier`)
- Select appropriate operator based on source data (collection, array, etc.)
- Consider performance implications in high-throughput scenarios

✅ **Most Common Operators**:
- `Mono.just()` - Single value
- `Flux.just()` - Multiple values
- `Flux.fromIterable()` - From collections
- `Mono/Flux.defer()` - Lazy creation
- `Mono/Flux.create()` - Programmatic creation

---------

# 10. 📈 Quick Reference Table

| Operator | Type | Description | Eager/Lazy | Use Case |
|----------|------|-------------|------------|----------|
| `just` | Mono/Flux | Create from known values | Eager | When values are immediately available |
| `empty` | Mono/Flux | Create empty publisher | Eager | Representing absence of values |
| `error` | Mono/Flux | Create failing publisher | Eager | When you want to signal failure |
| `fromSupplier` | Mono | Create from supplier function | Lazy | For expensive computations |
| `defer` | Mono/Flux | Defer creation until subscription | Lazy | For dynamic values, fresh instance per subscriber |
| `fromIterable` | Flux | Create from collections | Lazy | For working with existing collections |
| `fromArray` | Flux | Create from arrays | Lazy | For working with arrays |
| `range` | Flux | Create numeric sequence | Lazy | For generating sequences |
| `interval` | Flux | Create timed emissions | Lazy | For periodic tasks |
| `create` | Mono/Flux | Programmatic creation | Lazy | For bridging non-reactive APIs |
| `generate` | Flux | Stateful generation | Lazy | For state-based sequences |

Remember that understanding creation operators is fundamental to mastering Project Reactor. They're often asked about in interviews since they form the foundation of your reactive chains!