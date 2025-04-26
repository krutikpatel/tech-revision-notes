# 1. 🔍 Project Reactor Filtering Operators Overview

Project Reactor's filtering operators help you control which elements flow through your reactive streams. They're essential tools for processing only the data you need and implementing business logic in your reactive applications.

Let's dive into the key filtering operators you need to know for your interviews!

---------

# 2. 🚫 Basic Filtering Operators

## 2.1 `filter` - Basic element filtering

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<Integer> evenNumbers = numbers.filter(n -> n % 2 == 0);
// Result: 2, 4, 6, 8, 10
```

📌 **Interview Insight**: Use filter early in your chains to reduce data volume downstream.

ASCII diagram:
```
filter:
   1  2  3  4  5  6  7  8  9  10
   |  |  |  |  |  |  |  |  |  |
   |  v  |  v  |  v  |  v  |  v
      2     4     6     8     10
```

❌ **Common Mistake**: Filter ordering in chains:
```java
// Less efficient - transforms all elements before filtering
Flux<UserDTO> activeUserDtos = userFlux
    .map(user -> convertToDTO(user))  // Converts ALL users
    .filter(dto -> dto.isActive());   // Then filters

// More efficient - filters first, then transforms only what's needed
Flux<UserDTO> activeUserDtos = userFlux
    .filter(user -> user.isActive())  // Filters first
    .map(user -> convertToDTO(user)); // Converts only active users
```

## 2.2 `filterWhen` - Async filtering

✅ **Usage**:
```java
Flux<User> premiumUsers = userFlux.filterWhen(user -> 
    subscriptionService.hasPremiumSubscription(user.getId())
);
```

📌 **Interview Insight**: Use when your filtering condition requires an asynchronous operation.

---------

# 3. 📈 Limiting Operators

## 3.1 `take` - Take N elements

✅ **Usage**:
```java
Flux<Integer> first5 = Flux.range(1, 100).take(5);
// Result: 1, 2, 3, 4, 5
```

📌 **Interview Insight**: Cancels the upstream publisher after receiving the specified number of elements.

## 3.2 `takeLast` - Take last N elements

✅ **Usage**:
```java
Flux<Integer> last3 = Flux.range(1, 10).takeLast(3);
// Result: 8, 9, 10
```

📌 **Interview Insight**: Must wait for the entire sequence to complete before emitting any elements.

❌ **Common Mistake**: Memory concerns with large streams:
```java
// Dangerous with large or infinite streams - must buffer all elements
Flux<LogEvent> lastLogs = logEventFlux.takeLast(100);

// Better for large streams - use take() with reversed ordering
Flux<LogEvent> lastLogs = logEventFlux
    .sort((a, b) -> b.getTimestamp().compareTo(a.getTimestamp()))
    .take(100);
```

## 3.3 `takeUntil` - Take until a condition is met

✅ **Usage**:
```java
Flux<Integer> untilBig = Flux.range(1, 100)
    .takeUntil(n -> n > 10);
// Result: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
```

📌 **Interview Insight**: The element that matches the predicate is INCLUDED in the output.

## 3.4 `takeWhile` - Take while a condition is true

✅ **Usage**:
```java
Flux<Integer> whileSmall = Flux.range(1, 100)
    .takeWhile(n -> n <= 5);
// Result: 1, 2, 3, 4, 5
```

📌 **Interview Insight**: The element that fails the predicate is NOT included in the output.

## 3.5 `limitRate` - Control request rate

✅ **Usage**:
```java
Flux<Data> rateLimitedData = dataFlux.limitRate(100);
```

📌 **Interview Insight**: Controls backpressure by limiting how many elements are requested at once.

---------

# 4. ⏭️ Skipping Operators

## 4.1 `skip` - Skip first N elements

✅ **Usage**:
```java
Flux<Integer> skipFirst5 = Flux.range(1, 10).skip(5);
// Result: 6, 7, 8, 9, 10
```

📌 **Interview Insight**: Great for pagination scenarios.

## 4.2 `skipLast` - Skip last N elements

✅ **Usage**:
```java
Flux<Integer> skipLast3 = Flux.range(1, 10).skipLast(3);
// Result: 1, 2, 3, 4, 5, 6, 7
```

📌 **Interview Insight**: Like `takeLast`, must buffer elements to know which ones to skip.

## 4.3 `skipUntil` - Skip until a condition is met

✅ **Usage**:
```java
Flux<Integer> skipUntilBig = Flux.range(1, 100)
    .skipUntil(n -> n > 95);
// Result: 96, 97, 98, 99, 100
```

📌 **Interview Insight**: The element that matches the predicate is INCLUDED in the output.

## 4.4 `skipWhile` - Skip while a condition is true

✅ **Usage**:
```java
Flux<Integer> skipWhileSmall = Flux.range(1, 10)
    .skipWhile(n -> n < 6);
// Result: 6, 7, 8, 9, 10
```

📌 **Interview Insight**: The element that fails the predicate is INCLUDED in the output.

---------

# 5. 🔄 Deduplication Operators

## 5.1 `distinct` - Remove all duplicates

✅ **Usage**:
```java
Flux<Integer> distinct = Flux.just(1, 2, 2, 3, 1, 3, 4)
    .distinct();
// Result: 1, 2, 3, 4
```

📌 **Interview Insight**: Uses a HashSet internally, so elements must implement proper equals/hashCode.

❌ **Common Mistake**: Memory issues with large streams:
```java
// Can cause memory issues with large streams - stores all seen elements
Flux<String> allDistinct = hugeFlux.distinct();

// Better for large streams - use time window or history size constraint
Flux<String> recentDistinct = hugeFlux.distinct(
    Object::hashCode,
    Queues.get(10000) // Limits history to last 10,000 elements
);
```

## 5.2 `distinctUntilChanged` - Remove consecutive duplicates

✅ **Usage**:
```java
Flux<Integer> noConsecutiveDupes = Flux.just(1, 1, 2, 2, 3, 1, 1)
    .distinctUntilChanged();
// Result: 1, 2, 3, 1
```

📌 **Interview Insight**: Only compares against the immediately preceding element. Much more memory efficient.

ASCII diagram:
```
distinctUntilChanged:
   1  1  2  2  3  1  1
   |  |  |  |  |  |  |
   v  |  v  |  v  v  |
   1     2     3  1
```

## 5.3 `distinct` with key extractor - Deduplication by property

✅ **Usage**:
```java
Flux<User> usersByEmail = userFlux
    .distinct(User::getEmail);
```

📌 **Interview Insight**: Allows deduplication based on a specific property rather than the whole object.

---------

# 6. 🧩 Element Inspection Operators

## 6.1 `elementAt` - Get element at specific index

✅ **Usage**:
```java
Mono<Integer> thirdElement = Flux.range(1, 10).elementAt(2); // Zero-based index
// Result: 3
```

📌 **Interview Insight**: Returns empty Mono if index is out of bounds.

## 6.2 `any` - Check if any element matches

✅ **Usage**:
```java
Mono<Boolean> hasEvenNumber = Flux.range(1, 10)
    .any(n -> n % 2 == 0);
// Result: true
```

📌 **Interview Insight**: Short-circuits once a matching element is found.

## 6.3 `all` - Check if all elements match

✅ **Usage**:
```java
Mono<Boolean> allPositive = Flux.range(1, 10)
    .all(n -> n > 0);
// Result: true
```

📌 **Interview Insight**: Short-circuits once a non-matching element is found.

## 6.4 `hasElements` - Check if sequence has any elements

✅ **Usage**:
```java
Mono<Boolean> hasAny = Flux.range(1, 10).hasElements();
// Result: true

Mono<Boolean> isEmpty = Flux.empty().hasElements();
// Result: false
```

📌 **Interview Insight**: More efficient than counting and checking if > 0.

---------

# 7. ⏰ Time-Based Filtering

## 7.1 `sample` - Sample at regular intervals

✅ **Usage**:
```java
Flux<Long> sampled = Flux.interval(Duration.ofMillis(10))
    .sample(Duration.ofMillis(100));
```

📌 **Interview Insight**: Emits the most recent element during each time window.

## 7.2 `sampleFirst` - Sample first element in interval

✅ **Usage**:
```java
Flux<Long> sampleFirst = Flux.interval(Duration.ofMillis(10))
    .sampleFirst(Duration.ofMillis(100));
```

📌 **Interview Insight**: Opposite of `sample` - takes the first element in each interval.

## 7.3 `timeout` - Filter out slow elements

✅ **Usage**:
```java
Flux<Data> withTimeout = dataFlux.timeout(Duration.ofSeconds(5));
```

📌 **Interview Insight**: Emits TimeoutException if emission/completion takes longer than specified.

## 7.4 `debounce` - Filter out rapid emissions

✅ **Usage**:
```java
// Only emit when there's a 300ms pause between elements
Flux<String> debounced = searchTerms.debounce(Duration.ofMillis(300));
```

📌 **Interview Insight**: Perfect for handling user input like search box typing.

ASCII diagram:
```
debounce:
   a a   b     c    d   d  d       e
   | |   |     |    |   |  |       |
   | |   |     |    |   |  |       v
       a       b    c           e
```

---------

# 8. 🔄 Conditional Filtering

## 8.1 `defaultIfEmpty` - Default value for empty sequence

✅ **Usage**:
```java
Mono<User> userOrDefault = userRepo.findById(id)
    .defaultIfEmpty(User.anonymous());
```

📌 **Interview Insight**: Only triggers if the sequence is empty, not if it errors.

## 8.2 `switchIfEmpty` - Fallback publisher for empty sequence

✅ **Usage**:
```java
Mono<User> user = primaryRepo.findById(id)
    .switchIfEmpty(backupRepo.findById(id));
```

📌 **Interview Insight**: More powerful than `defaultIfEmpty` as it can switch to another reactive sequence.

## 8.3 `ignoreElements` - Ignore all elements, preserve completion/error

✅ **Usage**:
```java
// Only care if the operation completes, not the actual elements
Mono<Void> completion = dataFlux.ignoreElements();
```

📌 **Interview Insight**: Useful when you only care about completion or error signals.

---------

# 9. 🧪 Error Filtering

## 9.1 `onErrorResume` - Replace errors with fallback publisher

✅ **Usage**:
```java
Flux<Data> withFallback = primarySource
    .onErrorResume(error -> fallbackSource);
```

📌 **Interview Insight**: Allows different fallbacks for different error types.

## 9.2 `onErrorReturn` - Replace errors with fallback value

✅ **Usage**:
```java
Mono<Integer> withDefault = riskyOperation()
    .onErrorReturn(0);
```

📌 **Interview Insight**: Simpler than `onErrorResume` when you just need a constant value.

## 9.3 `onErrorContinue` - Skip error-producing elements

✅ **Usage**:
```java
Flux<Integer> skipErrors = Flux.just(1, 0, 2, 0, 3)
    .map(i -> 10 / i)
    .onErrorContinue((error, value) -> {
        log.warn("Skipping division by zero for value: {}", value);
    });
// Result: 10, 5, 3.33
```

📌 **Interview Insight**: Allows processing to continue despite errors with specific elements.

❌ **Common Mistake**:
```java
// WRONG: onErrorContinue won't help here as the error is at the publisher level
Flux<Data> dataFlux = Flux.error(new RuntimeException("Failed to connect"))
    .onErrorContinue((e, o) -> log.error("Continuing after error"));

// CORRECT: Use onErrorResume for publisher-level errors
Flux<Data> dataFlux = Flux.error(new RuntimeException("Failed to connect"))
    .onErrorResume(e -> {
        log.error("Using fallback after error");
        return fallbackPublisher;
    });
```

---------

# 10. 🔍 Advanced Filtering Patterns

## 10.1 Combining Operators for Complex Filtering

✅ **Example**: First 5 even numbers
```java
Flux<Integer> first5Even = Flux.range(1, 100)
    .filter(n -> n % 2 == 0)
    .take(5);
// Result: 2, 4, 6, 8, 10
```

## 10.2 Custom Filtering with `handle`

✅ **Usage**:
```java
Flux<Integer> filtered = Flux.range(1, 10)
    .handle((value, sink) -> {
        if (value % 3 == 0) {
            sink.next(value * 10);
        } else if (value % 5 == 0) {
            sink.error(new RuntimeException("Found multiple of 5"));
        }
        // Other values are filtered out by not calling sink.next()
    });
// Result: 30, 60, 90
```

📌 **Interview Insight**: `handle` allows for both filtering and transformation in one step.

## 10.3 Dynamic Filtering with `doOnNext`

✅ **Usage**:
```java
Flux<Data> dynamicallyFiltered = dataFlux
    .doOnNext(data -> {
        if (!isValid(data)) {
            throw new ValidationException(data);
        }
    })
    .onErrorContinue(ValidationException.class, 
        (error, value) -> log.warn("Skipping invalid data: {}", value));
```

📌 **Interview Insight**: This pattern gives you fine-grained control over filtering logic.

---------

# 11. 📊 Interview Scenarios & Best Practices

## 11.1 Filtering Performance Considerations

✅ **Best Practice**: Filter early in the chain
```java
// Better - filter first, then transform
dataFlux.filter(this::needsProcessing)
       .flatMap(this::expensiveOperation);

// Worse - transform everything, then filter
dataFlux.flatMap(this::expensiveOperation)
       .filter(this::needsResult);
```

## 11.2 Memory-Efficient Filtering

✅ **Best Practice**: Avoid operators that buffer all elements
```java
// Better for large streams - constrained memory usage
Flux<String> recentDistinct = largeFlux
    .windowTimeout(1000, Duration.ofMinutes(5))
    .flatMap(window -> window.distinct());

// Worse - unbounded memory usage
Flux<String> allDistinct = largeFlux.distinct();
```

## 11.3 Error-Resilient Filtering

✅ **Best Practice**: Use appropriate error handling with filtering
```java
// Resilient filtering - continues despite errors
Flux<Integer> resilient = Flux.just(1, 2, "not a number", 3, 4)
    .handle((item, sink) -> {
        try {
            if (item instanceof Integer) {
                sink.next(item);
            } else {
                int parsed = Integer.parseInt(item.toString());
                sink.next(parsed);
            }
        } catch (Exception e) {
            log.warn("Skipping unparseable item: {}", item);
        }
    });
```

---------

# 12. 📝 Summary of Project Reactor Filtering Operators

✅ **Core Concepts**:
- Filtering operators let you selectively process only needed elements
- Apply filters early in processing chains for maximum efficiency
- Choose time-based filters for event streams
- Consider memory impact for large or infinite streams
- Combine error handling with filtering for resilient flows

✅ **Key Operators to Remember**:
- `filter` - Basic inclusion/exclusion using a predicate
- `take`/`skip` - Control how many elements to process
- `distinct` - Remove duplicates
- `timeout`/`sample`/`debounce` - Time-based filtering
- `defaultIfEmpty`/`switchIfEmpty` - Handle empty sequences

---------

# 13. 📊 Quick Reference Table

| Operator | Description | Memory Impact | Common Use Cases | Things to Watch For |
|----------|-------------|---------------|------------------|---------------------|
| `filter` | Keep elements matching predicate | Low | Basic filtering | Place early in chain |
| `filterWhen` | Async filtering | Low | DB/service lookups | Increased latency |
| `take(n)` | First n elements | Low | Pagination, limiting | Cancels upstream |
| `takeLast(n)` | Last n elements | High (buffers all) | Recent items | Memory with large streams |
| `takeUntil` | Elements until condition met | Low | Boundary conditions | Includes matching element |
| `takeWhile` | Elements while condition true | Low | Boundary conditions | Excludes failing element |
| `skip(n)` | Skip first n elements | Low | Pagination, offsetting | None |
| `skipLast(n)` | Skip last n elements | High (buffers all) | Trimming sequences | Memory with large streams |
| `distinct` | Remove all duplicates | High (keeps history) | Deduplication | Memory with large streams |
| `distinctUntilChanged` | Remove consecutive dupes | Low | Signal change detection | Only consecutive comparison |
| `elementAt` | Element at index | Low | Indexed access | Returns empty if out of bounds |
| `any` | Check if any match | Low | Existence check | Short-circuits on match |
| `all` | Check if all match | Low | Validation | Short-circuits on failure |
| `sample` | Periodic sampling | Low | Rate limiting | Takes most recent element |
| `debounce` | Wait for pause in signals | Medium | User input, throttling | Increases latency |
| `timeout` | Error if too slow | Low | Circuit breaking | Can cause streams to fail |
| `onErrorContinue` | Skip error elements | Low | Resilient processing | Only for element-level errors |
| `defaultIfEmpty` | Default for empty | Low | Fallback values | Only for empty, not errors |
| `switchIfEmpty` | Fallback for empty | Low | Fallback sources | Only for empty, not errors |

Remember - mastering filtering operators is key to writing efficient reactive applications. Focus on your interview preparation by understanding when to use each operator and how they affect performance and memory usage!