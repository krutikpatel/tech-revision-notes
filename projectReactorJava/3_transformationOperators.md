# 1. 🔄 Project Reactor Transformation Operators Overview

Project Reactor's transformation operators are powerful tools that allow you to modify, filter, and reshape reactive streams in Java. Understanding these operators is crucial for effective reactive programming and will be a key focus in interviews.

In this guide, we'll cover the essential transformation operators that you'll need to know for your interviews!

---------

# 2. 🛠️ Basic Transformation Operators

## 2.1 `map` - One-to-one transformation

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 5);
Flux<String> strings = numbers.map(n -> "Number: " + n);
// Result: "Number: 1", "Number: 2", "Number: 3", "Number: 4", "Number: 5"
```

📌 **Interview Insight**: `map` transforms each element synchronously, one-to-one.

❌ **Common Mistake**: Using `map` for asynchronous operations:
```java
// Wrong - blocks the thread with synchronous HTTP call
Flux<UserDto> userDtos = userFlux.map(user -> callExternalServiceForUserData(user));

// Correct - use flatMap for async operations
Flux<UserDto> userDtos = userFlux.flatMap(user -> 
    Mono.fromCallable(() -> callExternalServiceForUserData(user))
        .subscribeOn(Schedulers.boundedElastic())
);
```

## 2.2 `flatMap` - One-to-many transformation

✅ **Usage**:
```java
Flux<User> users = Flux.just(user1, user2);
Flux<Order> orders = users.flatMap(user -> 
    orderService.getOrdersForUser(user.getId())
);
```

📌 **Interview Insight**: `flatMap` is used when each input element maps to 0..N output elements. Great for async operations.

ASCII diagram:
```
flatMap:
    item1 -----> [A, B]
           \
            \---> result: A, B, C, D, E
           /
    item2 -----> [C, D, E]
```

## 2.3 `flatMapSequential` - Ordered flatMap

✅ **Usage**:
```java
Flux<Order> orders = users.flatMapSequential(user -> 
    orderService.getOrdersForUser(user.getId())
);
```

📌 **Interview Insight**: Like `flatMap` but preserves the order of the source elements in the output.

---------

# 3. 📊 Filtering Operators

## 3.1 `filter` - Keep elements matching a predicate

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<Integer> even = numbers.filter(n -> n % 2 == 0);
// Result: 2, 4, 6, 8, 10
```

📌 **Interview Insight**: Use filter early in your chain to reduce processing downstream.

## 3.2 `take` - Limit number of elements

✅ **Usage**:
```java
Flux<Integer> first5 = Flux.range(1, 100).take(5);
// Result: 1, 2, 3, 4, 5
```

📌 **Interview Insight**: `take` completes the sequence after emitting the specified number of elements.

## 3.3 `takeUntil` - Take until a condition is met

✅ **Usage**:
```java
Flux<Integer> untilBig = Flux.range(1, 100).takeUntil(n -> n > 10);
// Result: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
```

📌 **Interview Insight**: Remember that `takeUntil` includes the element that matched the predicate.

## 3.4 `skip` - Skip a number of elements

✅ **Usage**:
```java
Flux<Integer> skipFirst5 = Flux.range(1, 10).skip(5);
// Result: 6, 7, 8, 9, 10
```

📌 **Interview Insight**: Great for pagination and skipping known bad data.

## 3.5 `distinct` - Remove duplicates

✅ **Usage**:
```java
Flux<Integer> distinct = Flux.just(1, 2, 2, 3, 1, 4).distinct();
// Result: 1, 2, 3, 4
```

📌 **Interview Insight**: Uses `hashCode` and `equals` for comparison. For custom objects, implement these methods.

---------

# 4. 🧩 Combining Elements

## 4.1 `zipWith` - Combine elements from two publishers

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Jane");
Flux<String> lastNames = Flux.just("Doe", "Smith");
Flux<String> fullNames = names.zipWith(lastNames, (n, l) -> n + " " + l);
// Result: "John Doe", "Jane Smith"
```

📌 **Interview Insight**: Waits for both sources to produce an element before emitting combined result.

## 4.2 `zip` (static) - Combine elements from multiple publishers

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Jane");
Flux<String> lastNames = Flux.just("Doe", "Smith");
Flux<Integer> ages = Flux.just(30, 25);

Flux<User> users = Flux.zip(
    names, 
    lastNames, 
    ages, 
    (name, lastName, age) -> new User(name, lastName, age)
);
// Result: User("John", "Doe", 30), User("Jane", "Smith", 25)
```

📌 **Interview Insight**: Zips up to 8 sources. Use `zipWith` for more readability when combining just 2 sources.

## 4.3 `reduce` - Reduce to a single value

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 5);
Mono<Integer> sum = numbers.reduce(0, (acc, next) -> acc + next);
// Result: 15 (1+2+3+4+5)
```

📌 **Interview Insight**: Reduces a `Flux` to a `Mono` containing the final accumulated value.

## 4.4 `scan` - Show each reduction step

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 5);
Flux<Integer> runningSum = numbers.scan(0, (acc, next) -> acc + next);
// Result: 0, 1, 3, 6, 10, 15
```

📌 **Interview Insight**: Like `reduce` but emits each intermediate value.

---------

# 5. 🔀 Ordering and Batching

## 5.1 `buffer` - Collect elements into lists

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<List<Integer>> batches = numbers.buffer(3);
// Result: [1,2,3], [4,5,6], [7,8,9], [10]
```

📌 **Interview Insight**: Great for batching operations to improve performance.

## 5.2 `window` - Group elements into sub-fluxes

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<Flux<Integer>> windows = numbers.window(3);
// Result: Flux(1,2,3), Flux(4,5,6), Flux(7,8,9), Flux(10)
```

📌 **Interview Insight**: Unlike `buffer`, each window is a Flux that can be subscribed to independently.

## 5.3 `grouped` - Group by a key function

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<GroupedFlux<Boolean, Integer>> grouped = numbers.groupBy(n -> n % 2 == 0);
// Result: GroupedFlux(key=false, 1,3,5,7,9), GroupedFlux(key=true, 2,4,6,8,10)
```

📌 **Interview Insight**: Useful for partitioning data streams into logical groups.

---------

# 6. 🕒 Time-Based Transformations

## 6.1 `sample` - Sample at a regular rate

✅ **Usage**:
```java
Flux<Long> fastStream = Flux.interval(Duration.ofMillis(10));
Flux<Long> sampled = fastStream.sample(Duration.ofMillis(100));
```

📌 **Interview Insight**: Emits the most recent item during each sampling interval.

## 6.2 `timeout` - Apply a timeout

✅ **Usage**:
```java
Flux<Data> dataWithTimeout = service.getData()
    .timeout(Duration.ofSeconds(5), Flux.just(fallbackData));
```

📌 **Interview Insight**: Emits TimeoutException if an element doesn't arrive within the specified duration.

❌ **Common Mistake**: Not providing a fallback:
```java
// Wrong - throws TimeoutException after 5 seconds
Flux<Data> dataWithTimeout = service.getData()
    .timeout(Duration.ofSeconds(5));

// Correct - provides fallback if timeout occurs
Flux<Data> dataWithTimeout = service.getData()
    .timeout(Duration.ofSeconds(5), Flux.just(fallbackData));
```

---------

# 7. 🛑 Error Handling Transformations

## 7.1 `onErrorReturn` - Return a fallback value on error

✅ **Usage**:
```java
Mono<String> result = service.getData()
    .onErrorReturn("Default Value");
```

📌 **Interview Insight**: Simple fallback for all errors.

## 7.2 `onErrorResume` - Switch to a fallback publisher on error

✅ **Usage**:
```java
Mono<String> result = service.getPrimaryData()
    .onErrorResume(error -> {
        if (error instanceof TimeoutException) {
            return service.getBackupData();
        }
        return Mono.error(error); // rethrow other errors
    });
```

📌 **Interview Insight**: More powerful than `onErrorReturn` as it can handle different error types differently.

## 7.3 `onErrorContinue` - Continue processing on error

✅ **Usage**:
```java
Flux<Integer> result = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i) // Division by zero for third element
    .onErrorContinue((error, item) -> {
        log.error("Error processing item {}: {}", item, error.getMessage());
    });
// Result: 10, 5, 2.5 (skips the division by zero)
```

📌 **Interview Insight**: Useful for non-critical errors where you want to skip an element rather than fail the entire stream.

---------

# 8. 🔍 Debugging Operators

## 8.1 `log` - Log events in the stream

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 5)
    .log("MyFlux")
    .map(n -> n * 2);
```

📌 **Interview Insight**: Provides detailed logging of all Reactive Streams signals.

## 8.2 `doOnNext`/`doOnError`/`doOnComplete` - Side effects

✅ **Usage**:
```java
Flux<User> users = userService.getUsers()
    .doOnNext(user -> log.info("Processing user: {}", user.getName()))
    .doOnError(error -> log.error("Error occurred: {}", error.getMessage()))
    .doOnComplete(() -> log.info("Processing completed"));
```

📌 **Interview Insight**: These operators don't change the stream, they just allow you to perform side effects.

---------

# 9. 🔄 Advanced Transformations

## 9.1 `switchMap` - Switch to a new publisher

✅ **Usage**:
```java
Flux<String> searchResults = searchTerms
    .switchMap(term -> service.search(term));
```

📌 **Interview Insight**: Cancels the previous subscription when a new element arrives.

ASCII diagram:
```
switchMap:
    term1 ------> [searching...]
           \         
            \--X (cancelled)
           /
    term2 ------> [new search...] -> results
```

## 9.2 `concatMap` - Transform and concatenate

✅ **Usage**:
```java
Flux<Order> orders = users
    .concatMap(user -> orderService.getOrdersForUser(user.getId()));
```

📌 **Interview Insight**: Like `flatMap` but preserves order by waiting for each inner publisher to complete.

❌ **Common Mistake**: Using `concatMap` for high latency operations:
```java
// Wrong - later users must wait for all earlier users' orders
Flux<Order> orders = users
    .concatMap(user -> orderService.getOrdersForUser(user.getId()));

// Better - process in parallel but preserve order
Flux<Order> orders = users
    .flatMapSequential(user -> orderService.getOrdersForUser(user.getId()));
```

## 9.3 `expandDeep` - Recursively expand a tree structure

✅ **Usage**:
```java
Flux<Category> allCategories = rootCategoryMono
    .expandDeep(category -> categoryRepository.findChildCategories(category.getId()));
```

📌 **Interview Insight**: Depth-first traversal of tree structures.

---------

# 10. 🧪 Interview Scenarios & Best Practices

## 10.1 Optimizing Performance

✅ **Best Practice**: Use filtering early to reduce data volume
```java
// Better performance - filter early
userFlux.filter(user -> user.isActive())
       .flatMap(user -> loadUserDetails(user));

// Worse performance - filter late
userFlux.flatMap(user -> loadUserDetails(user))
       .filter(user -> user.isActive());
```

## 10.2 Choosing the Right Flatmap Variant

✅ **Best Practice**:
- Use `flatMap` for maximum throughput
- Use `concatMap` when strict ordering is required
- Use `flatMapSequential` for parallel execution with ordered results

## 10.3 Handling Backpressure

✅ **Best Practice**: Use operators like `buffer`, `window`, or `sample` to manage backpressure:
```java
// Batch incoming requests to prevent overwhelming downstream
requestFlux.buffer(100)
         .flatMap(batch -> processInBatch(batch));
```

---------

# 11. 📝 Summary of Project Reactor Transformation Operators

✅ **Core Concepts**:
- Transformation operators modify reactive streams without blocking
- Choose the right operator based on cardinality (one-to-one, one-to-many)
- Consider ordering requirements when choosing between flatMap variants
- Place filters early in the chain to reduce processing downstream
- Use debugging operators to troubleshoot complex reactive flows

✅ **Key Operators to Know**:
- `map` - One-to-one synchronous transformation
- `flatMap` - One-to-many asynchronous transformation
- `filter` - Keep elements matching a predicate
- `reduce` - Combine elements into a single result
- `zip` - Combine elements from multiple publishers
- `buffer`/`window` - Group elements for batch processing

---------

# 12. 📊 Quick Reference Table

| Operator | Type | Description | Use Case | Common Pitfalls |
|----------|------|-------------|----------|----------------|
| `map` | One-to-one | Synchronous transformation | Simple transformations | Using for async operations |
| `flatMap` | One-to-many | Async transformation with parallel execution | DB calls, network operations | Overloading downstream |
| `concatMap` | One-to-many | Sequential execution, preserves order | Operations needing strict ordering | High latency with many elements |
| `flatMapSequential` | One-to-many | Parallel execution, preserves order | Best of both worlds | Slightly higher overhead |
| `filter` | Filtering | Keep elements matching predicate | Reducing data volume | Applying too late in chain |
| `buffer` | Batching | Group elements into lists | Batch processing | Memory usage with large batches |
| `window` | Batching | Group elements into sub-fluxes | Complex batch processing | Added complexity |
| `reduce` | Aggregation | Combine elements into single result | Computing totals | Only emits final result |
| `scan` | Aggregation | Running accumulation | Running totals | Overhead for simple operations |
| `zip` | Combination | Combine elements from multiple sources | Joining related data | Slowest source limits throughput |
| `onErrorResume` | Error handling | Recover from errors with fallback | Graceful degradation | Not handling all error types |
| `switchMap` | Flow control | Cancel previous when new arrives | Search as you type | Cancelling important operations |

Remember - understanding how to effectively use these transformation operators is key to mastering Project Reactor! Use this guide as a quick reference for your interview preparation.