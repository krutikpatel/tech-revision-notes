# 1. 🚨 Project Reactor Error Handling Overview

Error handling is a critical aspect of reactive programming with Project Reactor. Unlike traditional try-catch blocks, reactive streams require a different approach to handle errors effectively. This guide will help you understand Project Reactor's error handling operators and strategies for interviews.

---------

# 2. 🌊 Understanding Error Flow in Reactive Streams

## 2.1 The Error Signal

📌 **Interview Insight**: In Reactor, errors are first-class citizens in the reactive streams specification.

✅ **How Errors Propagate**:
```java
Flux<Integer> numbers = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i); // Will throw ArithmeticException (division by zero)
    
numbers.subscribe(
    value -> System.out.println("Value: " + value),
    error -> System.out.println("Error: " + error.getMessage()),
    () -> System.out.println("Completed!")
);
```

ASCII diagram:
```
Error propagation:
   [1] [2] [0] [4]
    |   |   |   |
    v   v   v   v
   [10] [5] [X] [?]
                |
               Error: / by zero
```

📌 **Interview Insight**: Once an error occurs, the stream is terminated - no more elements will be processed.

❌ **Common Mistake**: Forgetting that errors terminate the stream:
```java
// WRONG expectation: All values get processed
Flux.just(1, 2, 0, 4)
    .map(i -> {
        try {
            return 10 / i;
        } catch (Exception e) {
            return 0; // This will handle the error locally, but...
        }
    })
    .map(i -> {
        if (i == 0) {
            throw new RuntimeException("Zero result detected"); // This still terminates the stream
        }
        return i;
    });
// The 4 never gets processed after the exception!
```

---------

# 3. 📦 Basic Error Handling Operators

## 3.1 `onErrorReturn` - Fallback to a Default Value

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i)
    .onErrorReturn(999); // Return 999 on any error
```

📌 **Interview Insight**: Simple error recovery with a static value.

## 3.2 `onErrorReturn` with Predicate - Conditional Fallback

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i)
    .onErrorReturn(
        e -> e instanceof ArithmeticException, // Only for ArithmeticException
        999
    );
```

📌 **Interview Insight**: This provides more control by handling only specific error types.

## 3.3 `onErrorResume` - Switch to Fallback Publisher

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i)
    .onErrorResume(e -> {
        log.error("Calculation error", e);
        return Flux.just(100, 200, 300); // Fallback sequence
    });
```

📌 **Interview Insight**: More powerful than `onErrorReturn` as it can switch to a different publisher.

## 3.4 `onErrorResume` with Error Type - Conditional Fallback Publisher

✅ **Usage**:
```java
Flux<Data> result = service.getData()
    .onErrorResume(TimeoutException.class, e -> 
        backupService.getData())
    .onErrorResume(DataCorruptionException.class, e -> 
        repairService.recoverData())
    .onErrorResume(e -> {
        // Catch-all for other errors
        log.error("Unhandled error", e);
        return Flux.empty();
    });
```

📌 **Interview Insight**: Allows different fallback strategies for different error types.

---------

# 4. 🔄 Error Recovery Strategies

## 4.1 `retry` - Simple Retry

✅ **Usage**:
```java
Flux<Data> resilientRequest = service.getData()
    .retry(3); // Retry up to 3 times (4 total attempts)
```

📌 **Interview Insight**: Retries immediately on failure, which may not be suitable for all failures.

❌ **Common Mistake**: Infinite retries with permanent failures:
```java
// WRONG: Infinite retry can lead to resource exhaustion
Flux<Data> infiniteRetry = service.getData()
    .retry(); // No argument means infinite retries

// Better: Limit retries
Flux<Data> limitedRetry = service.getData()
    .retry(3);
```

## 4.2 `retryWhen` - Advanced Retry

✅ **Usage**:
```java
Flux<Data> backoffRetry = service.getData()
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))
        .maxBackoff(Duration.ofSeconds(10))
        .filter(e -> e instanceof NetworkException)
    );
```

📌 **Interview Insight**: Provides exponential backoff and conditional retries.

## 4.3 Custom Retry Strategies with `retryWhen`

✅ **Usage**:
```java
Flux<Data> customRetry = service.getData()
    .retryWhen(Retry.from(companion -> companion
        .map(signal -> {
            if (signal.totalRetries() < 3) {
                return signal.totalRetries();
            } else {
                throw Exceptions.propagate(signal.failure());
            }
        })
        .flatMap(attempt -> {
            long delay = (long) Math.pow(2, attempt) * 100; // Exponential backoff
            return Mono.delay(Duration.ofMillis(delay));
        })
    ));
```

📌 **Interview Insight**: For complex retry requirements, `retryWhen` offers complete control.

---------

# 5. 🧩 Continuing Despite Errors

## 5.1 `onErrorContinue` - Recover and Continue

✅ **Usage**:
```java
Flux<Integer> results = Flux.just(1, 2, 0, 4)
    .map(i -> {
        try {
            return 10 / i;
        } catch (Exception e) {
            throw new CustomException("Error processing: " + i, e);
        }
    })
    .onErrorContinue((error, originalValue) -> {
        log.warn("Skipping error for value {}: {}", originalValue, error.getMessage());
    });
```

📌 **Interview Insight**: Unlike other error operators, this allows the stream to continue processing after an error.

ASCII diagram:
```
onErrorContinue:
   [1] [2] [0] [4]
    |   |   |   |
    v   v   v   v
   [10] [5] [X] [2.5]
              |
              Log warning, continue to next element
```

❌ **Common Mistake**: Misunderstanding where `onErrorContinue` works:
```java
// WRONG: onErrorContinue doesn't work for errors from publishers
Flux<Integer> numbers = Flux.error(new RuntimeException("Publisher error"))
    .onErrorContinue((error, value) -> {
        log.warn("This won't be called!");
    });

// WRONG: onErrorContinue doesn't work for errors in subscribe()
Flux<Integer> numbers = Flux.just(1, 2, 3)
    .onErrorContinue((error, value) -> {
        log.warn("This won't be called!");
    })
    .subscribe(
        value -> {
            throw new RuntimeException("Error in subscriber"); // Won't be caught by onErrorContinue
        }
    );
```

## 5.2 `onErrorContinue` with Type Predicate

✅ **Usage**:
```java
Flux<Integer> results = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i)
    .onErrorContinue(
        ArithmeticException.class, 
        (error, value) -> log.warn("Skipping division by zero for: {}", value)
    );
```

📌 **Interview Insight**: This variant allows you to handle only specific error types.

---------

# 6. 🧪 Testing Error Scenarios

## 6.1 StepVerifier for Error Testing

✅ **Usage**:
```java
Flux<Integer> flux = Flux.just(1, 2, 0)
    .map(i -> 10 / i);

StepVerifier.create(flux)
    .expectNext(10)
    .expectNext(5)
    .expectError(ArithmeticException.class)
    .verify();
```

📌 **Interview Insight**: StepVerifier makes error testing explicit and readable.

## 6.2 Testing Error Recovery

✅ **Usage**:
```java
Flux<Integer> flux = Flux.just(1, 2, 0)
    .map(i -> 10 / i)
    .onErrorReturn(999);

StepVerifier.create(flux)
    .expectNext(10)
    .expectNext(5)
    .expectNext(999)
    .expectComplete()
    .verify();
```

---------

# 7. 🏗️ Composing Error Handlers

## 7.1 Building Resilient Chains

✅ **Usage**:
```java
Flux<Data> resilientFlow = service.getData()
    .onErrorResume(TimeoutException.class, e -> backupService.getData())
    .timeout(Duration.ofSeconds(10))
    .onErrorMap(e -> new ServiceException("Service timed out", e))
    .retry(3)
    .onErrorReturn(new EmptyData());
```

📌 **Interview Insight**: You can chain multiple error handlers for layered resilience strategies.

## 7.2 `doOnError` - Side Effects Without Recovery

✅ **Usage**:
```java
Flux<Data> loggedFlow = service.getData()
    .doOnError(e -> {
        log.error("Error in data service", e);
        metrics.incrementErrorCount();
    })
    .onErrorResume(e -> backupService.getData());
```

📌 **Interview Insight**: `doOnError` performs side effects without changing the error flow.

---------

# 8. 🔄 Error Transformation

## 8.1 `onErrorMap` - Transform Error Type

✅ **Usage**:
```java
Flux<User> users = userService.getUsers()
    .onErrorMap(e -> {
        if (e instanceof TimeoutException) {
            return new ServiceUnavailableException("User service timed out", e);
        }
        return new UnknownServiceException("Unknown error in user service", e);
    });
```

📌 **Interview Insight**: Standardize error types or add context while preserving the error flow.

## 8.2 Using `Exceptions.propagate` and `Exceptions.unwrap`

✅ **Usage**:
```java
try {
    // Some code that throws checked exceptions
    riskyOperation();
} catch (IOException e) {
    // Convert to runtime exception while preserving stack trace
    throw Exceptions.propagate(e);
}

// Later, unwrap to handle specific types
.onErrorResume(e -> {
    Throwable original = Exceptions.unwrap(e);
    if (original instanceof IOException) {
        return fallbackForIO();
    }
    return Mono.error(e);
})
```

📌 **Interview Insight**: Reactor provides utilities to work with checked exceptions in a reactive context.

---------

# 9. 🛡️ Advanced Error Handling Patterns

## 9.1 Circuit Breaker Pattern

✅ **Usage with Resilience4j**:
```java
CircuitBreaker circuitBreaker = CircuitBreaker.ofDefaults("service");

Flux<Data> protected = Mono.fromCallable(() -> service.getData())
    .transformDeferred(CircuitBreakerOperator.of(circuitBreaker))
    .onErrorResume(CallNotPermittedException.class, e -> 
        Mono.just(fallbackData));
```

📌 **Interview Insight**: Circuit breakers prevent cascading failures in distributed systems.

## 9.2 Fallback Hierarchy

✅ **Usage**:
```java
Flux<Data> withFallbacks = primaryService.getData()
    .onErrorResume(e -> secondaryService.getData()
        .onErrorResume(e2 -> tertiaryService.getData()
            .onErrorReturn(lastResortData)));
```

📌 **Interview Insight**: Create a hierarchy of increasingly reliable (but potentially less feature-rich) fallbacks.

## 9.3 Error Streaming with `materialize`/`dematerialize`

✅ **Usage**:
```java
Flux<Data> dataWithErrorInfo = sourceFlux
    .materialize()
    .map(signal -> {
        if (signal.isOnNext()) {
            return Signal.next(signal.get());
        } else if (signal.isOnError()) {
            log.error("Error occurred", signal.getThrowable());
            return Signal.next(fallbackData); // Replace error with fallback
        } else {
            return signal; // Pass through completion
        }
    })
    .dematerialize();
```

📌 **Interview Insight**: Materialize/dematerialize allows treating errors as regular data for advanced handling.

---------

# 10. 🚫 Common Anti-Patterns to Avoid

## 10.1 Swallowing Errors Without Logging

❌ **Anti-Pattern**:
```java
// BAD: Errors disappear without a trace
Flux<Data> silent = service.getData()
    .onErrorResume(e -> Flux.empty());
```

✅ **Better Practice**:
```java
// GOOD: At least log the error before moving on
Flux<Data> logged = service.getData()
    .doOnError(e -> log.error("Error fetching data", e))
    .onErrorResume(e -> Flux.empty());
```

## 10.2 Mixing Try-Catch with Reactive Error Handling

❌ **Anti-Pattern**:
```java
// BAD: Mixing paradigms
Flux<Integer> mixed = Flux.just(1, 2, 0, 4)
    .map(i -> {
        try {
            return 10 / i;
        } catch (Exception e) {
            return -1; // Try-catch hides the error from reactive chains
        }
    });
```

✅ **Better Practice**:
```java
// GOOD: Stay within reactive paradigm
Flux<Integer> reactive = Flux.just(1, 2, 0, 4)
    .map(i -> 10 / i)
    .onErrorReturn(-1);
```

## 10.3 Ignoring Context in Error Handling

❌ **Anti-Pattern**:
```java
// BAD: Error lacks context of what caused it
Flux<Data> noContext = Flux.fromIterable(items)
    .flatMap(item -> processItem(item));
```

✅ **Better Practice**:
```java
// GOOD: Preserve context in errors
Flux<Data> withContext = Flux.fromIterable(items)
    .flatMap(item -> processItem(item)
        .onErrorMap(e -> new ItemProcessingException("Error processing item " + item.getId(), e))
    );
```

---------

# 11. 🏆 Best Practices for Interviews

## 11.1 Choose the Right Error Operator

✅ **Decision Guide**:
- Use `onErrorReturn` for simple static fallbacks
- Use `onErrorResume` for dynamic fallback publishers
- Use `onErrorContinue` when you need to continue processing other elements
- Use `retry`/`retryWhen` for transient failures
- Use `onErrorMap` to provide context or standardize error types

## 11.2 Error Handling Strategy by Component Type

✅ **Best Practices**:
- **Data Access Layer**: Use retries for transient failures, specific error mapping
- **Service Layer**: Provide fallbacks, circuit breakers
- **API Layer**: Standardize error responses, add context
- **UI Layer**: Show user-friendly messages, retry with backoff

## 11.3 Global Error Handlers

✅ **Using Hooks**:
```java
// Set up global error handler
Hooks.onOperatorError((error, value) -> {
    log.error("Global error handler caught: {}", error.getMessage());
    return new ApplicationException("Something went wrong", error);
});
```

📌 **Interview Insight**: Global handlers can provide a safety net, but specific local handlers are preferred.

---------

# 12. 📝 Summary of Project Reactor Error Handling

✅ **Core Concepts**:
- Errors in reactive streams are signals that terminate the sequence
- Error handling operators allow recovery from errors
- Different operators serve different recovery strategies
- Error handling should be tailored to the error type and context
- Layered error handling provides defense in depth

✅ **Key Points to Remember**:
- Use `onErrorReturn` for simple fallbacks
- Use `onErrorResume` for switching to alternative publishers
- Use `onErrorContinue` to keep processing despite element-level errors
- Use `retry`/`retryWhen` for transient failures
- Always log errors for troubleshooting
- Consider context when handling errors

---------

# 13. 📊 Quick Reference Table

| Operator | Purpose | Returns | Best For | Limitations |
|----------|---------|---------|----------|-------------|
| `onErrorReturn` | Static fallback value | Original stream type | Simple recovery | Single fallback value |
| `onErrorResume` | Dynamic fallback publisher | Original stream type | Complex recovery logic | - |
| `onErrorMap` | Transform error | Original stream type with new error | Adding context to errors | Doesn't recover, just transforms |
| `onErrorContinue` | Skip error and continue | Original stream type | Element-level errors | Doesn't work for source errors |
| `retry` | Resubscribe on error | Original stream type | Transient failures | Can cause infinite loops |
| `retryWhen` | Advanced retry logic | Original stream type | Backoff strategies | Complex to implement |
| `doOnError` | Side effects on error | Original stream | Logging, metrics | Doesn't modify error flow |
| `timeout` | Error after duration | Original stream with timeout error | Ensuring SLAs | Needs error handling itself |
| `Exceptions.propagate` | Convert checked to unchecked | RuntimeException | Working with checked exceptions | - |
| `materialize` | Convert signals to values | Flux<Signal<T>> | Advanced error handling | Breaks reactive flow |

Remember that effective error handling is a key differentiator between junior and senior reactive programmers. Show your expertise in interviews by demonstrating an understanding of how to build resilient reactive systems!