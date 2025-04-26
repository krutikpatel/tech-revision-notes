# 1. 🔄 Project Reactor Combining Operators Overview

Project Reactor provides powerful operators to combine multiple reactive streams together. These combining operators are essential for handling complex data flows, coordinating multiple asynchronous operations, and creating sophisticated reactive pipelines.

Let's explore the key combining operators you should know for your interviews!

---------

# 2. 🧩 Merging Operators

## 2.1 `merge` - Combine Multiple Publishers

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B").delayElements(Duration.ofMillis(100));
Flux<String> flux2 = Flux.just("C", "D").delayElements(Duration.ofMillis(80));
Flux<String> merged = Flux.merge(flux1, flux2);
// Possible result: C, D, A, B (emissions interleaved based on timing)
```

📌 **Interview Insight**: `merge` combines publishers with potential interleaving. Subscribes to all sources eagerly.

ASCII diagram:
```
merge:
flux1: --A------B---->
flux2: ---C----D----->
result: ---C-A--D-B-->
```

❌ **Common Mistake**: Order is not preserved in `merge`. Items appear in the resulting Flux as they're emitted.

## 2.2 `mergeSequential` - Preserve Source Order

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B").delayElements(Duration.ofMillis(100));
Flux<String> flux2 = Flux.just("C", "D").delayElements(Duration.ofMillis(80));
Flux<String> merged = Flux.mergeSequential(flux1, flux2);
// Result: A, B, C, D (elements from each source stay together)
```

📌 **Interview Insight**: Unlike `merge`, this preserves the order of sources but still subscribes to all sources eagerly.

ASCII diagram:
```
mergeSequential:
flux1: --A------B---->
flux2: ---C----D----->
result: --A------B-C-D>
```

## 2.3 `mergeWith` - Instance Method Version

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B");
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> merged = flux1.mergeWith(flux2);
```

📌 **Interview Insight**: Functionally identical to `merge` but in a fluent API style.

## 2.4 `mergeDelayError` - Defer Errors Until Completion

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A").concatWith(Flux.error(new RuntimeException("Error")));
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> merged = Flux.mergeDelayError(1, flux1, flux2);
// Result: A, C, D, then error
```

📌 **Interview Insight**: Continues processing other sources even if one fails, delivering the error only at the end.

---------

# 3. 🔄 Concatenation Operators

## 3.1 `concat` - Sequential Combination

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B");
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> result = Flux.concat(flux1, flux2);
// Result: A, B, C, D
```

📌 **Interview Insight**: Subscribes to sources one after another, waiting for each to complete before moving to the next.

ASCII diagram:
```
concat:
flux1: --A--B--|
flux2:          --C--D--|
result: --A--B----C--D--|
```

## 3.2 `concatWith` - Instance Method Version

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B");
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> result = flux1.concatWith(flux2);
// Result: A, B, C, D
```

## 3.3 `concatDelayError` - Defer Errors Until Completion

✅ **Usage**:
```java
Flux<String> flux1 = Flux.just("A", "B").concatWith(Flux.error(new RuntimeException()));
Flux<String> flux2 = Flux.just("C", "D");
Flux<String> result = Flux.concatDelayError(flux1, flux2);
// Result: A, B, C, D, then error
```

📌 **Interview Insight**: If a source errors, continues with next sources and delivers error at the end.

## 3.4 `concatMap` - One-to-Many with Concatenation

✅ **Usage**:
```java
Flux<User> users = Flux.just(user1, user2);
Flux<Order> orders = users.concatMap(user -> 
    orderService.getOrdersForUser(user.getId())
);
```

📌 **Interview Insight**: Applies a function that returns a Publisher for each element, then concatenates results sequentially.

❌ **Common Mistake**: Using `concatMap` for high-latency operations can cause substantial delays:

```java
// WRONG: Later users must wait for earlier user operations to complete
Flux<Result> results = Flux.fromIterable(users)
    .concatMap(user -> highLatencyOperation(user));

// BETTER: Use flatMap or flatMapSequential if order isn't critical
Flux<Result> results = Flux.fromIterable(users)
    .flatMap(user -> highLatencyOperation(user));
```

---------

# 4. 🔀 Zipping Operators

## 4.1 `zip` - Combine Corresponding Elements

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Mary");
Flux<String> lastNames = Flux.just("Doe", "Smith");
Flux<Integer> ages = Flux.just(30, 25);

Flux<User> users = Flux.zip(
    names, 
    lastNames, 
    ages, 
    (name, lastName, age) -> new User(name, lastName, age)
);
// Result: User("John", "Doe", 30), User("Mary", "Smith", 25)
```

📌 **Interview Insight**: Waits for all sources to emit one element, then combines them. Limited by the shortest source.

ASCII diagram:
```
zip:
names:     --John------Mary----->
lastNames: -----Doe------Smith-->
ages:      --30---------25----->
result:    -----User1----User2-->
```

## 4.2 `zipWith` - Instance Method Version

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Mary");
Flux<String> lastNames = Flux.just("Doe", "Smith");
Flux<Tuple2<String, String>> combined = names.zipWith(lastNames);
// Result: Tuple2("John", "Doe"), Tuple2("Mary", "Smith")
```

📌 **Interview Insight**: Works with two publishers, returning tuples by default.

## 4.3 `zipWith` with BiFunction

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Mary");
Flux<String> lastNames = Flux.just("Doe", "Smith");
Flux<String> fullNames = names.zipWith(lastNames, 
    (name, lastName) -> name + " " + lastName
);
// Result: "John Doe", "Mary Smith"
```

---------

# 5. 🔗 Combining Latest Values

## 5.1 `combineLatest` - Combine Latest Elements

✅ **Usage**:
```java
Flux<String> names = Flux.just("John", "Mary").delayElements(Duration.ofMillis(100));
Flux<String> cities = Flux.just("New York", "Boston", "Chicago").delayElements(Duration.ofMillis(75));

Flux<String> combined = Flux.combineLatest(
    names, 
    cities, 
    (name, city) -> name + " from " + city
);
// Possible results include: "John from New York", "John from Boston", 
// "John from Chicago", "Mary from Chicago"
```

📌 **Interview Insight**: Emits when any source emits, combining with latest values from other sources.

ASCII diagram:
```
combineLatest:
names:    --John-------Mary---->
cities:   ----NY----Boston--Chicago-->
                    |    |      |
                    v    v      v
result:   ----"John from NY"
                "John from Boston"
                "Mary from Boston"
                "Mary from Chicago"
```

❌ **Common Mistake**: Forgetting that `combineLatest` needs at least one emission from each source before producing a result.

## 5.2 Real-World Example: Form Validation

✅ **Usage**:
```java
Flux<Boolean> emailValid = emailField.map(email -> 
    email.contains("@") && email.length() > 5
);
Flux<Boolean> passwordValid = passwordField.map(pass -> 
    pass.length() >= 8
);

Flux<Boolean> formValid = Flux.combineLatest(
    emailValid, 
    passwordValid, 
    (e, p) -> e && p
);
```

📌 **Interview Insight**: Perfect for UI validation and reactive form handling.

---------

# 6. 🧮 Sequential Composition

## 6.1 `then` - Execute Publishers in Sequence

✅ **Usage**:
```java
Mono<Void> sequence = saveUser(user)
    .then(sendEmail(user.getEmail()))
    .then(updateStats());
```

📌 **Interview Insight**: Executes the next publisher only after the previous completes, discarding its result.

## 6.2 `thenMany` - Switch to a Flux After Completion

✅ **Usage**:
```java
Flux<OrderItem> process = createOrder(order)
    .thenMany(fetchOrderItems(order.getId()));
```

📌 **Interview Insight**: Like `then`, but allows switching to a Flux for subsequent operations.

## 6.3 `thenReturn` - Return a Value After Completion

✅ **Usage**:
```java
Mono<String> result = saveUser(user)
    .thenReturn("User saved successfully");
```

📌 **Interview Insight**: Returns a constant value after the publisher completes.

## 6.4 `whenComplete` - Wait for Multiple Publishers

✅ **Usage**:
```java
Mono<Void> allDone = Mono.when(
    saveUser(user),
    updateInventory(),
    sendNotification()
);
```

📌 **Interview Insight**: Waits for all publishers to complete, ignoring their results.

---------

# 7. 📋 Batching and Windowing

## 7.1 `buffer` - Collect Elements Into Lists

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<List<Integer>> batches = numbers.buffer(3);
// Result: [1,2,3], [4,5,6], [7,8,9], [10]
```

📌 **Interview Insight**: Great for batching operations to improve performance.

## 7.2 `buffer` with Time

✅ **Usage**:
```java
Flux<Event> events = eventSource();
Flux<List<Event>> timeWindows = events.buffer(Duration.ofSeconds(1));
```

📌 **Interview Insight**: Useful for collecting time-based snapshots of data streams.

## 7.3 `window` - Collect Elements Into Sub-fluxes

✅ **Usage**:
```java
Flux<Integer> numbers = Flux.range(1, 10);
Flux<Flux<Integer>> windows = numbers.window(3);
// Result: Flux(1,2,3), Flux(4,5,6), Flux(7,8,9), Flux(10)
```

📌 **Interview Insight**: Similar to buffer but emits Flux instead of Lists.

## 7.4 Real-World Example: Batch Processing

✅ **Usage**:
```java
Flux<Order> orders = orderService.getNewOrders();
Flux<List<Order>> batches = orders.buffer(10);
Flux<BatchResult> results = batches.flatMap(batch -> 
    processBatch(batch)
);
```

---------

# 8. 🔍 Combining for Filtering and Selection

## 8.1 `and` - Logical AND of Two Publishers

✅ **Usage**:
```java
Mono<Boolean> userExists = userRepository.existsById(userId);
Mono<Boolean> hasPermissions = permissionService.hasAccess(userId, resource);

Mono<Boolean> canAccess = userExists.and(hasPermissions);
```

📌 **Interview Insight**: Returns a new Mono that completes when both source Monos complete.

## 8.2 `or` - First to Complete

✅ **Usage**:
```java
Mono<Data> primaryData = primaryDataSource.getData().timeout(Duration.ofSeconds(5));
Mono<Data> fallbackData = fallbackDataSource.getData();

Mono<Data> result = primaryData.or(fallbackData);
```

📌 **Interview Insight**: Returns the result of whichever publisher emits first.

❌ **Common Mistake**: Misunderstanding `or` behavior:
```java
// WRONG: This doesn't implement a fallback as expected
Mono<Data> primary = primarySource.getData(); 
Mono<Data> fallback = fallbackSource.getData();
Mono<Data> result = primary.or(fallback);
// If primary emits first, fallback is ignored

// CORRECT: For fallback on error
Mono<Data> result = primarySource.getData()
    .onErrorResume(e -> fallbackSource.getData());
```

## 8.3 `firstWithSignal` - First to Emit Any Signal

✅ **Usage**:
```java
Mono<Data> fastest = Mono.firstWithSignal(
    source1.getData().subscribeOn(Schedulers.parallel()),
    source2.getData().subscribeOn(Schedulers.parallel()),
    source3.getData().subscribeOn(Schedulers.parallel())
);
```

📌 **Interview Insight**: Returns whichever publisher first emits any signal (next, error, or complete).

---------

# 9. 🗺️ Advanced Combining Patterns

## 9.1 Fan-Out / Fan-In Pattern

✅ **Usage**:
```java
Flux<Integer> source = Flux.range(1, 10);

// Fan-out: Split processing across multiple streams
Flux<Integer> doubledValues = source.map(i -> i * 2);
Flux<Integer> squaredValues = source.map(i -> i * i);
Flux<String> textValues = source.map(i -> "Number: " + i);

// Fan-in: Combine results back together
Flux<Object> results = Flux.merge(
    doubledValues, 
    squaredValues, 
    textValues
);
```

📌 **Interview Insight**: This pattern allows for parallel processing of the same source data in different ways.

## 9.2 Scatter-Gather Pattern

✅ **Usage**:
```java
Mono<Price> bestPrice = Flux.fromIterable(suppliers)
    .flatMap(supplier -> 
        supplier.getPrice(productId)
            .timeout(Duration.ofSeconds(1))
            .onErrorResume(e -> Mono.empty())
    )
    .reduce((p1, p2) -> p1.getAmount() < p2.getAmount() ? p1 : p2)
    .switchIfEmpty(Mono.error(new PriceNotFoundException()));
```

📌 **Interview Insight**: Sends the same request to multiple sources and aggregates responses.

## 9.3 Dynamic Pipelines with groupBy and flatMap

✅ **Usage**:
```java
Flux<Transaction> transactions = transactionSource();

Flux<ProcessedTransaction> processed = transactions
    .groupBy(Transaction::getType)
    .flatMap(group -> {
        String type = group.key();
        if ("PAYMENT".equals(type)) {
            return group.flatMap(paymentProcessor::process);
        } else if ("REFUND".equals(type)) {
            return group.flatMap(refundProcessor::process);
        } else {
            return group.flatMap(defaultProcessor::process);
        }
    });
```

📌 **Interview Insight**: Creates dynamic processing pipelines based on data characteristics.

---------

# 10. 🚀 Performance Considerations

## 10.1 Parallelization with Prefetch

✅ **Usage**:
```java
Flux<Data> optimized = Flux.merge(
    source1.getData(),
    source2.getData(),
    source3.getData()
).take(5, 32); // prefetch 32 elements
```

📌 **Interview Insight**: Prefetching can improve performance for bursty sources.

## 10.2 Backpressure with combiners

✅ **Best Practice**:
```java
// Uses unbounded queue - can lead to OutOfMemoryError
Flux<Data> risky = Flux.zip(
    fastSource,
    slowSource
);

// Better - limit buffer size
Flux<Data> safe = Flux.zip(
    options -> new ZipCoordinator(options, 32), // buffer size of 32
    fastSource,
    slowSource
);
```

📌 **Interview Insight**: Consider buffer sizes when combining sources with different emission rates.

## 10.3 Operator Choice Impact

✅ **Usage Comparison**:
```java
// High memory usage - collects all elements in memory
Flux<List<Integer>> buffer = source.buffer();

// Lower memory - processes windows as they emit
Flux<Integer> processed = source.window()
    .flatMap(window -> window.reduce(0, Integer::sum));
```

---------

# 11. 📋 Interview Q&A and Best Practices

## 11.1 Common Interview Questions

✅ **Q: When would you use `merge` vs `concat`?**
- Use `merge` when order doesn't matter and you want parallel processing
- Use `concat` when you need to preserve the exact order of sources

✅ **Q: How does `zip` differ from `combineLatest`?**
- `zip` waits for all sources to emit before combining (1-to-1 matching)
- `combineLatest` emits when any source emits, using latest values from others

✅ **Q: How do you handle errors in combined streams?**
- Use `mergeDelayError` or `concatDelayError` to defer errors until all sources are processed
- Error in `zip` immediately terminates the combined flux
- Consider each operator's error propagation behavior

## 11.2 Best Practices

✅ **Choosing the Right Operator**:
- Performance considerations: `merge` (parallel) vs `concat` (sequential)
- Order requirements: `concat`/`concatMap` (preserves order) vs `merge`/`flatMap` (interleaved)
- Coordination needs: `zip` (corresponding elements) vs `combineLatest` (latest values)

✅ **Production Code Best Practices**:
- Add timeouts to prevent stuck operations
- Consider bounded buffers to control memory usage
- Use `retry`/`onErrorResume` with combiners for resilience
- Monitor backpressure with metrics
- Use `doOn` callbacks for debugging combined flows

❌ **Common Mistakes**:
- Using `concatMap` for high-latency operations (use `flatMap` instead)
- Forgetting that `zip` is limited by the shortest source
- Not handling errors properly in combined streams
- Creating overly complex combining chains that are hard to debug

---------

# 12. 📝 Summary of Project Reactor Combining Operators

✅ **Merging Operators**:
- `merge` - Combines multiple publishers with interleaving
- `mergeSequential` - Preserves source order but subscribes eagerly
- `mergeDelayError` - Defers errors until all sources complete

✅ **Concatenation Operators**:
- `concat` - Sequential combination, one source after another
- `concatMap` - Applies a function and concatenates results sequentially
- `concatDelayError` - Continues to next source even if a source errors

✅ **Zipping Operators**:
- `zip` - Combines corresponding elements from multiple sources
- `zipWith` - Instance method version of zip

✅ **Combining Latest Operators**:
- `combineLatest` - Combines latest values whenever any source emits

✅ **Sequential Composition**:
- `then`/`thenMany`/`thenReturn` - Execute publishers in sequence

✅ **Batching and Windowing**:
- `buffer` - Collect elements into lists
- `window` - Collect elements into sub-fluxes

---------

# 13. 📊 Quick Reference Table

| Operator | Purpose | Ordering | Subscription Model | Use When | Watch Out For |
|----------|---------|----------|-------------------|----------|---------------|
| `merge` | Combine multiple sources | Interleaved (as items arrive) | Eager (all at once) | Order doesn't matter, parallel processing | Memory usage with many sources |
| `mergeSequential` | Combine preserving source order | Sequential by source | Eager (all at once) | Need source grouping with parallel subscription | Complexity compared to concat |
| `concat` | Combine in strict sequence | Sequential | Lazy (one at a time) | Strict ordering is required | Head-of-line blocking |
| `zip` | Match corresponding elements | Paired by index | Eager | Need to combine related elements | Limited by shortest source |
| `combineLatest` | Combine latest values | Based on emission timing | Eager | Reactive UIs, form validation | Initial wait for all sources to emit once |
| `buffer` | Group elements into lists | Preserved within groups | N/A | Batching for efficiency | Memory usage with large buffers |
| `window` | Group into sub-sequences | Preserved within windows | N/A | Complex processing of groups | More complex than buffer |
| `then`/`thenMany` | Sequential execution | Sequential | Sequential | Workflow steps, ignoring interim results | Discards results of previous steps |
| `and` | Combine two publishers | N/A | Eager | Checking multiple conditions | Both must complete successfully |
| `or` | First to complete | First to emit | Eager | Race between sources | Complexity of behavior |

Remember - mastering these combining operators is crucial for handling complex data flows in Project Reactor. They're frequently asked about in interviews as they demonstrate your understanding of reactive stream composition!

-------

# Understanding zipWhen() in Project Reactor

`zipWhen()` is an operator in Project Reactor that combines the current Mono/Flux with another publisher that depends on the value of the first one. It's a powerful operator for creating dependent data flows in reactive applications.

## Basic Functionality

`zipWhen()` takes a function that receives the value from the source publisher and returns a second publisher. It then "zips" (combines) the original value with the result from the second publisher.

```java
Mono<User> userMono = userRepository.findById(userId);

Mono<Tuple2<User, List<Order>>> userWithOrders = userMono.zipWhen(
    user -> orderRepository.findByUserId(user.getId())
);
```

## Key Characteristics

1. **Dependent Publishers**: Unlike regular `zip()` which works with independent publishers, `zipWhen()` creates a dependent relationship - the second publisher depends on the value from the first.

2. **Result Format**: By default, returns a `Tuple2` containing both values, but can be customized with a combinator function.

3. **Sequential Execution**: The second publisher is only subscribed to after the first one emits a value.

4. **Error Handling**: If either publisher errors, the resulting Mono/Flux will also error.

## Using with a Combinator Function

You can provide a BiFunction combinator to transform the results into a custom format:

```java
Mono<UserWithOrders> combined = userMono.zipWhen(
    user -> orderRepository.findByUserId(user.getId()),
    (user, orders) -> new UserWithOrders(user, orders)
);
```

## Common Use Cases

1. **Fetching Related Data**:
```java
Mono<Product> productMono = productRepository.findById(productId);
Mono<ProductDetails> details = productMono.zipWhen(
    product -> reviewRepository.findByProductId(product.getId()),
    (product, reviews) -> new ProductDetails(product, reviews)
);
```

2. **Conditional Operations**:
```java
Mono<User> userMono = userRepository.findById(userId);
Mono<AuthResult> authResult = userMono.zipWhen(
    user -> user.isActive() ? 
            tokenService.generateToken(user) : 
            Mono.error(new AccountInactiveException())
);
```

3. **Multi-step Validation**:
```java
Mono<Order> orderMono = orderService.createOrder(orderRequest);
Mono<Order> validatedOrder = orderMono.zipWhen(
    order -> inventoryService.checkAvailability(order.getItems()),
    (order, available) -> {
        if (!available) throw new InsufficientInventoryException();
        return order;
    }
);
```

## zipWhen() vs flatMap()

While both can be used for dependent operations, they differ in how they handle the results:

- `flatMap()` discards the original value, keeping only the result from the inner publisher
- `zipWhen()` preserves both values, combining them into a tuple or custom object

## Best Practices

1. Use `zipWhen()` when you need both the original value and the result of the dependent operation.

2. Consider using the version with a combinator function for cleaner code.

3. For complex transformations with multiple dependent calls, consider chaining multiple operators instead of nesting `zipWhen()` calls.

4. Add appropriate error handling for cases where the dependent publisher might fail.