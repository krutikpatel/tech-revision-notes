# Java Stream API: Interview-Ready Guide 🚀

I'll help you master the Java Stream API with a comprehensive yet concise guide perfect for interview preparation. Let's dive in!

---------

## 1. 🌊 Stream API Basics

The Stream API was introduced in Java 8 to process collections of objects in a functional programming style. Streams don't store data - they operate on a source and produce a result.

```java
// Main components of a stream operation
collection.stream()           // 1. Create a stream
         .filter(e -> e > 10) // 2. Add intermediate operations (can be multiple)
         .forEach(System.out::println); // 3. Apply a terminal operation (only one)
```

Key characteristics of streams:
- Not a data structure - they don't store elements
- Designed for lambdas - functional-style operations
- Lazy evaluation - processing only happens when terminal operation is invoked
- Consumable - can be traversed only once

📌 **Interview Insight**: Streams support internal iteration (unlike collections that use external iteration with for loops), making them more optimized for parallel processing.

---------

## 2. 🛠️ Stream Creation Methods

There are several ways to create streams:

### From Collections

```java
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream = list.stream();
```

### From Arrays

```java
String[] array = {"a", "b", "c"};
Stream<String> stream = Arrays.stream(array);
```

### Using Stream.of

```java
Stream<String> stream = Stream.of("a", "b", "c");
```

### Using Stream.iterate (Infinite Stream)

```java
// Generate infinite stream of sequential integers starting from 0
Stream<Integer> infiniteStream = Stream.iterate(0, n -> n + 1);
// Use limit() to make it finite
Stream<Integer> first10Numbers = Stream.iterate(0, n -> n + 1).limit(10);
```

### Using Stream.generate (Infinite Stream)

```java
// Generate infinite stream of random numbers
Stream<Double> randomNumbers = Stream.generate(Math::random);
// Use limit() to make it finite
Stream<Double> tenRandomNumbers = Stream.generate(Math::random).limit(10);
```

### Empty Stream

```java
Stream<String> emptyStream = Stream.empty();
```

### From Files (Lines)

```java
try (Stream<String> lines = Files.lines(Paths.get("file.txt"))) {
    lines.forEach(System.out::println);
}
```

### Primitive Streams

```java
// IntStream, LongStream, DoubleStream
IntStream intStream = IntStream.range(1, 5); // 1, 2, 3, 4
IntStream closedRangeStream = IntStream.rangeClosed(1, 5); // 1, 2, 3, 4, 5
```

✅ **Best Practice**: For large ranges of numbers, use specialized primitive streams instead of boxed streams for better performance.

❌ **Common Mistake**: Trying to reuse a stream after it's been consumed.

```java
Stream<String> stream = Stream.of("a", "b", "c");
stream.forEach(System.out::println);
// This will throw IllegalStateException: stream has already been operated upon or closed
stream.forEach(System.out::println);
```

---------

## 3. 🔄 Intermediate Operations

Intermediate operations transform a stream into another stream. They are lazy - execution doesn't start until a terminal operation is invoked.

### map

Transforms each element using the provided function.

```java
List<String> words = Arrays.asList("hello", "world");
List<Integer> lengths = words.stream()
                            .map(String::length)
                            .collect(Collectors.toList()); // [5, 5]
```

### flatMap

Transforms each element into a stream and then flattens them into a single stream.

```java
// Without flatMap
List<List<Integer>> nestedNumbers = Arrays.asList(
    Arrays.asList(1, 2, 3),
    Arrays.asList(4, 5, 6)
);

// With flatMap - flattens nested lists
List<Integer> flattenedNumbers = nestedNumbers.stream()
                                             .flatMap(Collection::stream)
                                             .collect(Collectors.toList()); // [1, 2, 3, 4, 5, 6]
```

📌 **Interview Insight**: `flatMap` is used to flatten a stream of collections into a stream of elements.

```
// ASCII Diagram: map vs flatMap
map:      [List1, List2] -> [Stream1, Stream2]
flatMap:  [List1, List2] -> [a, b, c, d, e, f]
```

### filter

Retains elements that match the given predicate.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
List<Integer> evenNumbers = numbers.stream()
                                  .filter(n -> n % 2 == 0)
                                  .collect(Collectors.toList()); // [2, 4, 6]
```

### distinct

Removes duplicate elements based on `equals()`.

```java
List<Integer> numbers = Arrays.asList(1, 2, 2, 3, 3, 3, 4);
List<Integer> distinctNumbers = numbers.stream()
                                      .distinct()
                                      .collect(Collectors.toList()); // [1, 2, 3, 4]
```

### sorted

Sorts elements based on their natural order or a provided Comparator.

```java
// Natural order
List<Integer> sortedNumbers = numbers.stream()
                                    .sorted()
                                    .collect(Collectors.toList());

// Custom comparator (descending)
List<Integer> reverseSorted = numbers.stream()
                                    .sorted(Comparator.reverseOrder())
                                    .collect(Collectors.toList());

// Sorting objects by a property
List<Person> sortedByAge = persons.stream()
                                 .sorted(Comparator.comparing(Person::getAge))
                                 .collect(Collectors.toList());
```

### peek

Performs an action on each element while preserving the stream for further processing. Useful for debugging.

```java
List<Integer> result = numbers.stream()
                             .peek(n -> System.out.println("Processing: " + n))
                             .map(n -> n * 2)
                             .peek(n -> System.out.println("Mapped to: " + n))
                             .collect(Collectors.toList());
```

❌ **Common Mistake**: Using `peek()` for side effects in production code instead of just for debugging.

### limit

Restricts the stream to a specified number of elements.

```java
List<Integer> first3Numbers = numbers.stream()
                                    .limit(3)
                                    .collect(Collectors.toList()); // [1, 2, 3]
```

### skip

Discards the first n elements.

```java
List<Integer> skipFirst2 = numbers.stream()
                                 .skip(2)
                                 .collect(Collectors.toList()); // [3, 4, 5, 6]
```

✅ **Best Practice**: Use `limit()` and `skip()` for pagination of large datasets.

📌 **Interview Insight**: Intermediate operations are lazy - they set up the pipeline but don't execute until a terminal operation is called.

---------

## 4. 🎯 Terminal Operations

Terminal operations produce a result from a stream pipeline. After the terminal operation is performed, the stream is considered consumed and cannot be reused.

### forEach

Performs an action for each element.

```java
numbers.stream().forEach(System.out::println);
```

### collect

Accumulates elements into a collection or other result container.

```java
// Collect into a List
List<Integer> list = numbers.stream()
                           .filter(n -> n > 3)
                           .collect(Collectors.toList());

// Collect into a Set
Set<Integer> set = numbers.stream()
                         .filter(n -> n > 3)
                         .collect(Collectors.toSet());

// Collect into a Map
Map<Integer, String> map = numbers.stream()
                                 .collect(Collectors.toMap(
                                     n -> n,            // Key mapper
                                     n -> "Number " + n // Value mapper
                                 ));
```

#### Advanced Collectors

```java
// Joining strings
String joined = words.stream()
                    .collect(Collectors.joining(", ")); // "hello, world"

// Grouping
Map<Integer, List<String>> groupedByLength = words.stream()
                                                 .collect(Collectors.groupingBy(String::length));

// Partitioning
Map<Boolean, List<Integer>> partitioned = numbers.stream()
                                                .collect(Collectors.partitioningBy(n -> n % 2 == 0));
// Result: {false=[1, 3, 5], true=[2, 4, 6]}

// Statistics
IntSummaryStatistics stats = numbers.stream()
                                   .collect(Collectors.summarizingInt(Integer::intValue));
// Access stats.getSum(), stats.getAverage(), stats.getMax(), etc.
```

📌 **Interview Insight**: Collectors are extremely versatile for transforming streams into collections with various characteristics.

### reduce

Combines elements into a single result.

```java
// Sum with an identity value (0)
Optional<Integer> sum = numbers.stream()
                              .reduce((a, b) -> a + b);
// Or more concisely:
Integer sum2 = numbers.stream().reduce(0, Integer::sum);

// Finding max value
Optional<Integer> max = numbers.stream()
                              .reduce(Integer::max);

// Custom reduction (concatenate strings)
String concatenated = words.stream()
                          .reduce("", (a, b) -> a + b);
```

### count, min, max

Short-hand terminal operations for common reductions.

```java
long count = numbers.stream().count();
Optional<Integer> min = numbers.stream().min(Comparator.naturalOrder());
Optional<Integer> max = numbers.stream().max(Comparator.naturalOrder());
```

### anyMatch, allMatch, noneMatch

Return boolean result based on predicates.

```java
boolean anyEven = numbers.stream().anyMatch(n -> n % 2 == 0); // true if any even
boolean allEven = numbers.stream().allMatch(n -> n % 2 == 0); // true if all even
boolean noneEven = numbers.stream().noneMatch(n -> n % 2 == 0); // true if none even
```

### findFirst, findAny

Return an element from the stream.

```java
Optional<Integer> first = numbers.stream().findFirst(); // First element
Optional<Integer> any = numbers.stream().findAny(); // Any element (useful in parallel)
```

✅ **Best Practice**: When you just need any matching element and are using parallel streams, prefer `findAny()` over `findFirst()` for better performance.

❌ **Common Mistake**: Not handling empty Optional results from operations like `findFirst()`, `min()`, or `reduce()`.

---------

## 5. 🚀 Short-Circuiting Operations

Short-circuiting operations allow processing of infinite streams in finite time by terminating the processing early.

### Intermediate Short-Circuiting Operations

- `limit(n)`: Restricts stream to n elements
- `skip(n)`: Skips first n elements

### Terminal Short-Circuiting Operations

- `anyMatch()`: Returns as soon as a matching element is found
- `allMatch()`: Returns as soon as a non-matching element is found
- `noneMatch()`: Returns as soon as a matching element is found
- `findFirst()`: Returns the first element
- `findAny()`: Returns any element (often the first in sequential streams)

Example with infinite stream:

```java
// Process an infinite stream safely with short-circuiting
boolean hasMultipleOf10 = Stream.iterate(1, n -> n + 1) // Infinite stream
                               .limit(1000)             // Short-circuit to first 1000
                               .anyMatch(n -> n % 10 == 0); // Short-circuits at first match
```

📌 **Interview Insight**: Without short-circuiting operations, infinite streams would cause your program to hang indefinitely.

---------

## 6. ⚡ Parallel Streams and Performance

Parallel streams leverage multi-core processors to process elements concurrently, potentially improving performance for large datasets.

### Creating Parallel Streams

```java
// From a collection
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Stream<Integer> parallelStream = numbers.parallelStream();

// From an existing stream
Stream<Integer> parallel = numbers.stream().parallel();
```

### Checking if a Stream is Parallel

```java
boolean isParallel = stream.isParallel();
```

### Converting Back to Sequential

```java
Stream<Integer> sequential = parallelStream.sequential();
```

### Performance Considerations

✅ **When to Use Parallel Streams**:
- Large data sets (tens of thousands of elements or more)
- Operations that are computationally intensive
- When you have enough cores available
- When the data source supports efficient concurrent access
- When operations are stateless and independent

❌ **When to Avoid Parallel Streams**:
- Small data sets (overhead may exceed benefits)
- When order is important (maintaining encounter order adds overhead)
- With operations that involve side effects
- When using shared mutable state
- When using sources that don't support efficient splitting (like LinkedList)

Example of incorrect parallel stream usage:

```java
// BAD: Side effects in parallel stream
List<String> results = new ArrayList<>();
words.parallelStream().map(String::toUpperCase).forEach(results::add);
// Results will be unpredictable due to race conditions

// GOOD: Use proper collectors instead
List<String> results = words.parallelStream()
                          .map(String::toUpperCase)
                          .collect(Collectors.toList());
```

### Measuring Performance

```java
long start = System.currentTimeMillis();
// Sequential operation
long sequential = IntStream.range(0, 10_000_000)
                          .filter(n -> n % 2 == 0)
                          .count();
long seqTime = System.currentTimeMillis() - start;

start = System.currentTimeMillis();
// Parallel operation
long parallel = IntStream.range(0, 10_000_000)
                        .parallel()
                        .filter(n -> n % 2 == 0)
                        .count();
long parTime = System.currentTimeMillis() - start;

System.out.println("Sequential: " + seqTime + "ms, Parallel: " + parTime + "ms");
```

📌 **Interview Insight**: Using parallel streams doesn't guarantee better performance. Always measure and benchmark to confirm improvements.

❌ **Common Mistake**: Using parallel streams for IO-bound operations instead of CPU-bound operations.

---------

## 7. 🧩 Common Stream Patterns and Examples

### Filtering and Mapping

```java
List<Employee> highEarners = employees.stream()
                                     .filter(e -> e.getSalary() > 100000)
                                     .collect(Collectors.toList());

List<String> employeeNames = employees.stream()
                                     .map(Employee::getName)
                                     .collect(Collectors.toList());
```

### Finding Elements

```java
Optional<Employee> first = employees.stream()
                                   .filter(e -> e.getDepartment().equals("IT"))
                                   .findFirst();

boolean hasManager = employees.stream()
                             .anyMatch(e -> e.getRole().equals("Manager"));
```

### Statistical Operations

```java
double averageSalary = employees.stream()
                               .mapToDouble(Employee::getSalary)
                               .average()
                               .orElse(0.0);

Employee highestPaid = employees.stream()
                               .max(Comparator.comparing(Employee::getSalary))
                               .orElseThrow(NoSuchElementException::new);
```

### Grouping and Partitioning

```java
// Group employees by department
Map<String, List<Employee>> byDepartment = employees.stream()
                                                  .collect(Collectors.groupingBy(Employee::getDepartment));

// Count employees in each department
Map<String, Long> departmentSize = employees.stream()
                                          .collect(Collectors.groupingBy(
                                              Employee::getDepartment,
                                              Collectors.counting()));

// Partition by salary threshold
Map<Boolean, List<Employee>> bySalaryBracket = employees.stream()
                                                      .collect(Collectors.partitioningBy(
                                                          e -> e.getSalary() > 75000));
```

### String Processing

```java
// Split a string into words, count occurrences
Map<String, Long> wordFrequency = Pattern.compile("\\s+")
                                        .splitAsStream(text)
                                        .map(String::toLowerCase)
                                        .collect(Collectors.groupingBy(
                                            w -> w,
                                            Collectors.counting()));
```

### Combining Multiple Sources

```java
// Merge and process two lists
List<String> combined = Stream.concat(
                             list1.stream(),
                             list2.stream())
                          .distinct()
                          .sorted()
                          .collect(Collectors.toList());
```

---------

## 8. ❌ Common Mistakes and Traps

### 1. Reusing Streams

```java
Stream<String> stream = list.stream();
long count = stream.count();
// Error: stream has already been operated upon or closed
List<String> collected = stream.collect(Collectors.toList());
```

Fix: Create a new stream for each terminal operation.

### 2. Side Effects in Stream Operations

```java
// BAD - mutable state with side effects
List<String> collected = new ArrayList<>();
stream.forEach(collected::add);

// GOOD - use proper terminal collector
List<String> collected = stream.collect(Collectors.toList());
```

### 3. Parallel Stream with Non-Thread-Safe Operations

```java
// BAD - shared mutable state in parallel
Map<String, Integer> counts = new HashMap<>();
words.parallelStream().forEach(w -> {
    counts.put(w, counts.getOrDefault(w, 0) + 1); // Race condition!
});

// GOOD - use proper collectors
Map<String, Long> counts = words.parallelStream()
                              .collect(Collectors.groupingBy(
                                  w -> w,
                                  Collectors.counting()));
```

### 4. Breaking the Laziness

```java
// BAD - breaking the laziness chain
Stream<String> stream = list.stream();
stream.filter(s -> {
    System.out.println("filtering: " + s); // Side effect
    return s.startsWith("A");
}); // No terminal operation, nothing happens!

// GOOD - complete chain with terminal operation
list.stream()
    .filter(s -> {
        System.out.println("filtering: " + s); // Side effect for debugging
        return s.startsWith("A");
    })
    .count(); // Terminal operation triggers execution
```

### 5. Excessive Boxing/Unboxing with Primitive Streams

```java
// BAD - unnecessary boxing/unboxing
Stream<Integer> boxed = IntStream.range(1, 1000)
                               .boxed() // Boxing
                               .map(i -> i * 2) // Operating on boxed values
                               .filter(i -> i % 2 == 0);

// GOOD - stay primitive when possible
IntStream efficient = IntStream.range(1, 1000)
                             .map(i -> i * 2) // Still using primitive
                             .filter(i -> i % 2 == 0);
```

### 6. Neglecting Resource Management

```java
// BAD - resource leak
Stream<String> lines = Files.lines(Paths.get("file.txt"));
lines.forEach(System.out::println);
// Stream not closed!

// GOOD - use try-with-resources
try (Stream<String> lines = Files.lines(Paths.get("file.txt"))) {
    lines.forEach(System.out::println);
} // Stream automatically closed
```

---------

## 9. ✅ Best Practices

1. **Favor Method References Over Lambdas** when they're clearer
   ```java
   // Instead of:
   stream.map(s -> s.toLowerCase())
   // Use:
   stream.map(String::toLowerCase)
   ```

2. **Avoid Side Effects** in stream operations
   ```java
   // Don't modify external state in stream operations
   // Use collectors to gather results instead
   ```

3. **Use Specialized Streams** for primitives when possible
   ```java
   // Instead of:
   Stream<Integer> stream = // ...
   // Use:
   IntStream stream = // ...
   ```

4. **Limit Intermediate Operations** for better readability
   ```java
   // Break complex stream pipelines into smaller ones
   // with meaningful variable names
   ```

5. **Close Streams** that are backed by IO resources
   ```java
   try (Stream<String> lines = Files.lines(path)) {
       // Process stream
   }
   ```

6. **Test Performance** before assuming parallel is better
   ```java
   // Always benchmark to ensure parallel streams actually improve performance
   ```

7. **Use Collectors** for complex reductions
   ```java
   // Leverage built-in collectors for common operations:
   Collectors.groupingBy(), Collectors.partitioningBy(), etc.
   ```

8. **Consider Ordering** when using parallel streams
   ```java
   // Use unordered() when order doesn't matter
   stream.unordered().parallel()...
   ```

9. **Avoid Infinite Streams** without short-circuiting operations
   ```java
   // Always use limit() or a matching operation with infinite streams
   ```

10. **Provide Meaningful Comparators** for sorted operations
    ```java
    // Be explicit about sort order with custom objects
    stream.sorted(Comparator.comparing(Person::getLastName)
                           .thenComparing(Person::getFirstName))
    ```

---------

## 10. 📊 Summary (Super Quick Revision)

Java Stream API provides a functional approach to process sequences of elements. Streams have three parts: creation, intermediate operations (map, filter, etc.), and terminal operations (collect, reduce, etc.). Intermediate operations are lazy and return a new stream, while terminal operations trigger the execution and produce a result. Short-circuiting operations enable processing infinite streams in finite time. Parallel streams can improve performance for large, CPU-intensive operations but should be used carefully. Avoid common mistakes like reusing streams, side effects, and shared mutable state.

---------

## 11. 📑 Summary Table

| Category | Operation | Description | Example |
|----------|-----------|-------------|---------|
| **Creation** | Collection.stream() | Create from Collection | `list.stream()` |
|  | Arrays.stream() | Create from array | `Arrays.stream(array)` |
|  | Stream.of() | Create from elements | `Stream.of("a", "b")` |
|  | Stream.iterate() | Create infinite sequence | `Stream.iterate(0, n -> n + 1)` |
|  | Stream.generate() | Create from Supplier | `Stream.generate(Math::random)` |
| **Intermediate** | map() | Transform elements | `stream.map(String::length)` |
|  | flatMap() | Transform and flatten | `stream.flatMap(Collection::stream)` |
|  | filter() | Keep elements matching | `stream.filter(n -> n > 3)` |
|  | distinct() | Remove duplicates | `stream.distinct()` |
|  | sorted() | Sort elements | `stream.sorted()` |
|  | peek() | Observe elements | `stream.peek(System.out::println)` |
|  | limit() | Truncate stream | `stream.limit(10)` |
|  | skip() | Skip elements | `stream.skip(5)` |
| **Terminal** | forEach() | Process each element | `stream.forEach(System.out::println)` |
|  | collect() | Gather into collection | `stream.collect(Collectors.toList())` |
|  | reduce() | Combine elements | `stream.reduce(0, Integer::sum)` |
|  | count() | Count elements | `stream.count()` |
|  | min()/max() | Find extremes | `stream.min(Comparator.naturalOrder())` |
|  | anyMatch() | Check if any match | `stream.anyMatch(s -> s.isEmpty())` |
|  | allMatch() | Check if all match | `stream.allMatch(n -> n > 0)` |
|  | noneMatch() | Check if none match | `stream.noneMatch(n -> n < 0)` |
|  | findFirst() | Get first element | `stream.findFirst()` |
|  | findAny() | Get any element | `stream.findAny()` |
| **Short-Circuit** | limit(), skip() | Limit processing | `stream.limit(5)` |
|  | anyMatch(), allMatch(), noneMatch() | Early termination | `stream.anyMatch(predicate)` |
|  | findFirst(), findAny() | Early termination | `stream.findFirst()` |
| **Parallel** | parallelStream() | From collection | `collection.parallelStream()` |
|  | parallel() | From stream | `stream.parallel()` |
|  | sequential() | To sequential | `parallelStream.sequential()` |

### Common Collectors

| Collector | Description | Example |
|-----------|-------------|---------|
| toList() | Collect to List | `Collectors.toList()` |
| toSet() | Collect to Set | `Collectors.toSet()` |
| toMap() | Collect to Map | `Collectors.toMap(Person::getId, Person::getName)` |
| joining() | Join strings | `Collectors.joining(", ")` |
| groupingBy() | Group by key | `Collectors.groupingBy(Person::getDepartment)` |
| partitioningBy() | Split by predicate | `Collectors.partitioningBy(n -> n % 2 == 0)` |
| counting() | Count elements | `Collectors.counting()` |
| summarizingInt() | Stats on ints | `Collectors.summarizingInt(Person::getAge)` |
| reducing() | Custom reduction | `Collectors.reducing(0, Person::getSalary, Integer::sum)` |

I hope this guide helps you prepare effectively for your Java interviews! Good luck! 🍀