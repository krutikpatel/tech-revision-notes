# Java Functional Programming Collectors: Interview-Ready Guide 🚀

I'll help you master Java Collectors with a comprehensive yet concise guide perfect for interview preparation. Let's dive in!

---------

## 1. 📋 Collectors Basics

Collectors in Java are a powerful tool for gathering elements processed in a stream pipeline into a final collection or value. They're implemented through the `Collectors` utility class in the `java.util.stream` package.

```java
import java.util.stream.Collectors;
```

The basic pattern for using collectors is:

```java
List<Person> result = persons.stream()
    .filter(person -> person.getAge() > 18)
    .collect(Collectors.toList()); // Collector is applied here
```

📌 **Interview Insight**: Collectors transform a stream into various data structures and perform aggregate operations using a mutable reduction operation.

✅ **Key Point**: Collectors are primarily used with the `collect()` terminal operation on streams. They provide a way to accumulate stream elements into collections, strings, summaries, or other data structures.

---------

## 2. 🧩 Basic Collectors: toList(), toSet(), toMap()

These are the most commonly used collectors for transforming streams into standard collections.

### toList()

Collects stream elements into an ArrayList:

```java
List<String> names = people.stream()
    .map(Person::getName)
    .collect(Collectors.toList());
```

### toSet()

Collects stream elements into a HashSet, automatically eliminating duplicates:

```java
Set<String> uniqueNames = people.stream()
    .map(Person::getName)
    .collect(Collectors.toSet());
```

### toMap()

Creates a HashMap from a stream by defining key and value mapper functions:

```java
// Basic usage - people's IDs as keys, Person objects as values
Map<Integer, Person> peopleById = people.stream()
    .collect(Collectors.toMap(
        Person::getId,     // Key mapper
        person -> person   // Value mapper (identity function)
    ));

// Using name as key and age as value
Map<String, Integer> nameToAge = people.stream()
    .collect(Collectors.toMap(
        Person::getName,   // Key mapper
        Person::getAge     // Value mapper
    ));
```

#### Handling Duplicate Keys

When duplicate keys occur, `toMap()` will throw an `IllegalStateException`. You can provide a merge function to handle duplicates:

```java
// Keep the older person when names conflict
Map<String, Person> nameToPersonMap = people.stream()
    .collect(Collectors.toMap(
        Person::getName,               // Key mapper
        person -> person,              // Value mapper
        (existing, replacement) -> existing.getAge() > replacement.getAge() 
            ? existing : replacement   // Merge function - keep older person
    ));
```

#### Specifying the Map Implementation

You can also specify which Map implementation to use:

```java
// Collect into a TreeMap for sorted keys
Map<String, Person> sortedByName = people.stream()
    .collect(Collectors.toMap(
        Person::getName,
        person -> person,
        (p1, p2) -> p1,                // Merge function (keep first)
        TreeMap::new                   // Map supplier
    ));
```

❌ **Common Mistake**: Forgetting to handle duplicate keys with `toMap()`.

📌 **Interview Insight**: Know when to use which implementation. `toList()` preserves order and allows duplicates, `toSet()` eliminates duplicates, and `toMap()` transforms elements into key-value pairs.

---------

## 3. 🔄 String Operations: joining()

The `joining()` collector combines stream elements into a single string.

### Basic joining

```java
List<String> names = List.of("Alice", "Bob", "Charlie");
String result = names.stream()
    .collect(Collectors.joining());
// Result: "AliceBobCharlie"
```

### With delimiter

```java
String result = names.stream()
    .collect(Collectors.joining(", "));
// Result: "Alice, Bob, Charlie"
```

### With prefix and suffix

```java
String result = names.stream()
    .collect(Collectors.joining(", ", "[", "]"));
// Result: "[Alice, Bob, Charlie]"
```

✅ **Best Practice**: Use `joining()` instead of concatenating strings in a loop or using `reduce()` for better performance.

📌 **Interview Insight**: `joining()` internally uses a `StringBuilder` for efficient string concatenation.

---------

## 4. 📊 Aggregation Collectors: counting(), summingInt(), etc.

These collectors perform common reduction operations on streams.

### counting()

Counts the number of elements in a stream:

```java
Long count = people.stream()
    .collect(Collectors.counting());

// Alternative (simpler) approach
long count = people.stream().count();
```

### summingInt(), summingLong(), summingDouble()

Calculate the sum of numeric properties:

```java
// Total age of all people
Integer totalAge = people.stream()
    .collect(Collectors.summingInt(Person::getAge));

// Total salary
Double totalSalary = people.stream()
    .collect(Collectors.summingDouble(Person::getSalary));
```

### averagingInt(), averagingLong(), averagingDouble()

Calculate the average of numeric properties:

```java
// Average age
Double averageAge = people.stream()
    .collect(Collectors.averagingInt(Person::getAge));
```

### maxBy(), minBy()

Find maximum or minimum values based on a comparator:

```java
// Person with maximum age
Optional<Person> oldest = people.stream()
    .collect(Collectors.maxBy(Comparator.comparing(Person::getAge)));

// Person with minimum salary
Optional<Person> lowestPaid = people.stream()
    .collect(Collectors.minBy(Comparator.comparing(Person::getSalary)));
```

### summarizingInt(), summarizingLong(), summarizingDouble()

Get comprehensive statistics in one operation:

```java
IntSummaryStatistics ageStats = people.stream()
    .collect(Collectors.summarizingInt(Person::getAge));

// Now you can access multiple statistics
long count = ageStats.getCount();
long sum = ageStats.getSum();
double average = ageStats.getAverage();
int min = ageStats.getMin();
int max = ageStats.getMax();
```

📌 **Interview Insight**: `summarizingInt()` is more efficient than calculating individual statistics separately, as it processes the stream only once.

❌ **Common Mistake**: Using separate stream operations for different statistics when a summary collector would be more efficient.

---------

## 5. 🧮 Grouping Operations: groupingBy()

The `groupingBy()` collector categorizes stream elements into groups according to a classification function.

### Basic groupingBy()

```java
// Group people by their department
Map<String, List<Person>> byDepartment = people.stream()
    .collect(Collectors.groupingBy(Person::getDepartment));
```

### With downstream collector

You can specify a secondary collector to process each group:

```java
// Group by department, but collect only names in each group
Map<String, List<String>> namesByDepartment = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.mapping(Person::getName, Collectors.toList())
    ));

// Count number of people in each department
Map<String, Long> countByDepartment = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.counting()
    ));

// Find highest salary in each department
Map<String, Optional<Person>> highestPaidByDept = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.maxBy(Comparator.comparing(Person::getSalary))
    ));
```

### Multi-level grouping

```java
// Group by department, then by job title
Map<String, Map<String, List<Person>>> byDeptAndTitle = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.groupingBy(Person::getJobTitle)
    ));
```

### Controlling the Map implementation

```java
// Group by department using TreeMap (sorted keys)
Map<String, List<Person>> sortedByDepartment = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        TreeMap::new,
        Collectors.toList()
    ));
```

📌 **Interview Insight**: `groupingBy()` is similar to SQL's `GROUP BY` clause and is extremely versatile when combined with downstream collectors.

✅ **Best Practice**: For complex grouping operations, consider breaking down the logic into smaller, more readable steps with intermediate variables.

---------

## 6. 🔍 Partitioning Operations: partitioningBy()

The `partitioningBy()` collector divides stream elements into exactly two groups - those that satisfy a predicate and those that don't.

### Basic partitioningBy()

```java
// Partition people by age (adults vs minors)
Map<Boolean, List<Person>> adultVsMinors = people.stream()
    .collect(Collectors.partitioningBy(p -> p.getAge() >= 18));

// Access the partitioned groups
List<Person> adults = adultVsMinors.get(true);
List<Person> minors = adultVsMinors.get(false);
```

### With downstream collector

```java
// Partition by gender and count
Map<Boolean, Long> countByGender = people.stream()
    .collect(Collectors.partitioningBy(
        p -> p.getGender() == Gender.MALE,
        Collectors.counting()
    ));

// Partition by salary threshold and get names
Map<Boolean, List<String>> namesByHighSalary = people.stream()
    .collect(Collectors.partitioningBy(
        p -> p.getSalary() > 100000,
        Collectors.mapping(Person::getName, Collectors.toList())
    ));
```

📌 **Interview Insight**: `partitioningBy()` is more efficient than `groupingBy()` for boolean classifications because it always creates exactly two groups and optimizes for this case.

```
// ASCII diagram: partitioningBy vs groupingBy
partitioningBy: [all elements] --> {true: [...], false: [...]}
groupingBy:     [all elements] --> {value1: [...], value2: [...], value3: [...], ...}
```

✅ **Best Practice**: Use `partitioningBy()` instead of `groupingBy()` when you're grouping by a boolean condition.

---------

## 7. 🛠️ Custom Collectors

Sometimes the built-in collectors aren't enough. Java allows you to create custom collectors using the `Collector.of()` factory method.

### Anatomy of a Collector

A custom collector requires four components:
1. **Supplier**: Creates a new result container
2. **Accumulator**: Adds an element to the result container
3. **Combiner**: Merges two result containers
4. **Finisher**: Performs final transformation on the container

```java
// Custom collector that joins strings with a delimiter and converts to uppercase
Collector<String, StringBuilder, String> customJoiner = Collector.of(
    StringBuilder::new,                                       // Supplier
    (builder, str) -> {                                       // Accumulator
        if (builder.length() > 0) builder.append(", ");
        builder.append(str);
    },
    (b1, b2) -> {                                             // Combiner
        if (b2.length() > 0) {
            if (b1.length() > 0) b1.append(", ");
            b1.append(b2);
        }
        return b1;
    },
    builder -> builder.toString().toUpperCase()               // Finisher
);

// Usage
String result = names.stream().collect(customJoiner);
```

### Creating a Simplified Custom Collector

Here's a more practical example - a custom collector that builds a comma-separated string with a count:

```java
public class CustomCollectors {
    public static <T> Collector<T, ?, String> toCountedString() {
        return Collector.of(
            // Supplier - create a container to hold count and elements
            () -> new Object[] { 0, new StringBuilder() },
            
            // Accumulator - add element to the result
            (result, element) -> {
                Object[] arr = (Object[]) result;
                int count = (int) arr[0];
                StringBuilder sb = (StringBuilder) arr[1];
                
                if (count > 0) {
                    sb.append(", ");
                }
                sb.append(element);
                arr[0] = count + 1;
            },
            
            // Combiner - merge two result containers
            (result1, result2) -> {
                Object[] arr1 = (Object[]) result1;
                Object[] arr2 = (Object[]) result2;
                int count1 = (int) arr1[0];
                int count2 = (int) arr2[0];
                StringBuilder sb1 = (StringBuilder) arr1[1];
                StringBuilder sb2 = (StringBuilder) arr2[1];
                
                if (count2 > 0 && count1 > 0) {
                    sb1.append(", ");
                }
                sb1.append(sb2);
                arr1[0] = count1 + count2;
                return result1;
            },
            
            // Finisher - create the final string
            result -> {
                Object[] arr = (Object[]) result;
                int count = (int) arr[0];
                StringBuilder sb = (StringBuilder) arr[1];
                return String.format("Total %d items: [%s]", count, sb.toString());
            }
        );
    }
}

// Usage
String result = people.stream()
    .map(Person::getName)
    .collect(CustomCollectors.toCountedString());
// Output: "Total 3 items: [Alice, Bob, Charlie]"
```

### Collector Characteristics

You can also specify characteristics for optimization:

```java
Collector<String, StringBuilder, String> customJoiner = Collector.of(
    StringBuilder::new,
    (builder, str) -> { /* ... */ },
    (b1, b2) -> { /* ... */ },
    builder -> builder.toString().toUpperCase(),
    Collector.Characteristics.CONCURRENT,
    Collector.Characteristics.UNORDERED
);
```

Main characteristics:
- `CONCURRENT`: Safe for parallel reduction
- `UNORDERED`: Results not affected by encounter order
- `IDENTITY_FINISH`: Finisher is identity function

📌 **Interview Insight**: Custom collectors are needed when you want to combine multiple aggregation operations in a single pass or when you need to perform complex transformations.

❌ **Common Mistake**: Not implementing the combiner function correctly for parallel streams, leading to incorrect results.

---------

## 8. 🔄 Combining Collectors

You can compose collectors to create sophisticated data transformations:

```java
// Group people by department, then calculate total salary by department
Map<String, Double> totalSalaryByDept = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.summingDouble(Person::getSalary)
    ));

// Group by department, then find average age and format as string
Map<String, String> avgAgeByDept = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.collectingAndThen(
            Collectors.averagingInt(Person::getAge),
            avg -> String.format("%.1f years", avg)
        )
    ));

// Group by department, then collect names as comma-separated string
Map<String, String> nameListByDept = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.mapping(
            Person::getName,
            Collectors.joining(", ")
        )
    ));
```

📌 **Interview Insight**: Composing collectors is powerful but can become hard to read. Break complex operations into smaller steps and use meaningful variable names when needed.

✅ **Best Practice**: When combining multiple collectors, add comments explaining the transformation or use descriptive variable names to make the code more readable.

---------

## 9. ❌ Common Mistakes and Traps

### 1. Reusing Mutable Collectors

```java
// WRONG: The collector is stateful
Collector<String, List<String>, List<String>> badCollector = 
    Collector.of(
        ArrayList::new,  // Always creates a new list
        List::add,
        (list1, list2) -> {
            list1.addAll(list2);
            return list1;
        }
    );

// This works for a single collect operation, but the collector isn't reusable
```

### 2. Not Handling Duplicates in toMap()

```java
// Will throw IllegalStateException if there are duplicate names
try {
    Map<String, Person> byName = people.stream()
        .collect(Collectors.toMap(
            Person::getName,
            p -> p
        ));
} catch (IllegalStateException e) {
    System.out.println("Duplicate keys found!");
}

// Better: provide a merge function
Map<String, Person> byName = people.stream()
    .collect(Collectors.toMap(
        Person::getName,
        p -> p,
        (existing, replacement) -> existing  // Keep first occurrence
    ));
```

### 3. Misunderstanding Collector Composition

```java
// WRONG: This doesn't count people by department
Map<String, Long> wrongCount = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.counting()  // This counts people in each dept
    ));
    
// WRONG: This tries to count departments, not people in departments
Map<String, Integer> alsoWrong = people.stream()
    .map(Person::getDepartment)
    .collect(Collectors.toMap(
        dept -> dept,
        dept -> 1,
        Integer::sum
    ));
    
// CORRECT: Count people by department
Map<String, Long> correctCount = people.stream()
    .collect(Collectors.groupingBy(
        Person::getDepartment,
        Collectors.counting()
    ));
```

### 4. Misusing Collectors in Parallel Streams

```java
// BAD: Not thread-safe for parallel streams
List<String> names = Collections.synchronizedList(new ArrayList<>());
people.parallelStream().forEach(p -> names.add(p.getName()));  // Not using collectors

// GOOD: Using collectors is thread-safe
List<String> names = people.parallelStream()
    .map(Person::getName)
    .collect(Collectors.toList());  // Thread-safe
```

📌 **Interview Insight**: Using collectors properly avoids thread-safety issues in parallel streams that would occur with manual accumulation.

---------

## 10. ✅ Best Practices

1. **Use built-in collectors** whenever possible before creating custom ones
   ```java
   // Instead of manual reduction
   String names = people.stream()
       .map(Person::getName)
       .collect(Collectors.joining(", "));
   ```

2. **Prefer specialized collectors** for better performance
   ```java
   // Use summingInt instead of reducing manually
   int totalAge = people.stream()
       .collect(Collectors.summingInt(Person::getAge));
   ```

3. **Consider collector composition** for complex transformations
   ```java
   // Compose collectors for complex operations
   Map<String, IntSummaryStatistics> statsByDept = people.stream()
       .collect(Collectors.groupingBy(
           Person::getDepartment,
           Collectors.summarizingInt(Person::getAge)
       ));
   ```

4. **Handle duplicate keys** in toMap() collectors
   ```java
   Map<String, Person> peopleByEmail = people.stream()
       .collect(Collectors.toMap(
           Person::getEmail,
           Function.identity(),
           (p1, p2) -> p1  // Keep the first occurrence on duplicate keys
       ));
   ```

5. **Use descriptive variables** for complex collector chains
   ```java
   // Break down complex collectors
   Collector<Person, ?, Double> averageAgeCollector = 
       Collectors.averagingInt(Person::getAge);
       
   Collector<Person, ?, Map<String, Double>> groupedByDeptCollector =
       Collectors.groupingBy(Person::getDepartment, averageAgeCollector);
       
   Map<String, Double> avgAgeByDept = people.stream()
       .collect(groupedByDeptCollector);
   ```

6. **Document custom collectors** thoroughly
   ```java
   /**
    * Creates a collector that builds a comma-separated string of elements
    * with a count prefix.
    * @param <T> The type of input elements
    * @return A collector that produces a formatted string
    */
   public static <T> Collector<T, ?, String> toCountedString() {
       // Implementation
   }
   ```

7. **Use collectingAndThen()** for post-processing
   ```java
   // Collect to list and then convert to unmodifiable list
   List<String> names = people.stream()
       .map(Person::getName)
       .collect(Collectors.collectingAndThen(
           Collectors.toList(),
           Collections::unmodifiableList
       ));
   ```

8. **Consider performance implications** of your collector choice
   ```java
   // In many cases, toList() is faster than toSet() if you know elements are unique
   // Only use toSet() when you need to eliminate duplicates
   ```

---------

## 11. 📊 Summary (Super Quick Revision)

Java Collectors provide a powerful way to gather and transform stream elements into collections or other values. Basic collectors like `toList()`, `toSet()`, and `toMap()` convert streams to standard collections. String-oriented collectors like `joining()` concatenate elements. Aggregation collectors such as `counting()`, `summingInt()`, and `averagingDouble()` perform statistical operations. `groupingBy()` and `partitioningBy()` categorize elements into groups based on classification functions. Custom collectors can be created using `Collector.of()` when built-in collectors aren't sufficient. Collectors can be combined for complex data transformations. Understanding when and how to use each collector is essential for writing efficient and readable Java code.

---------

## 12. 📑 Summary Table

| Category | Collector | Description | Example |
|----------|-----------|-------------|---------|
| **Basic** | toList() | Collects elements into ArrayList | `collect(Collectors.toList())` |
|  | toSet() | Collects elements into HashSet | `collect(Collectors.toSet())` |
|  | toMap() | Collects elements into HashMap | `collect(Collectors.toMap(Key::new, Value::new))` |
|  | toCollection() | Collects to specific collection | `collect(Collectors.toCollection(LinkedList::new))` |
| **String** | joining() | Concatenates elements | `collect(Collectors.joining(", "))` |
| **Aggregation** | counting() | Counts elements | `collect(Collectors.counting())` |
|  | summingInt() | Sums ints | `collect(Collectors.summingInt(Person::getAge))` |
|  | averagingDouble() | Averages doubles | `collect(Collectors.averagingDouble(Person::getSalary))` |
|  | summarizingInt() | Multiple int statistics | `collect(Collectors.summarizingInt(Person::getAge))` |
|  | maxBy()/minBy() | Finds max/min elements | `collect(Collectors.maxBy(comparator))` |
|  | reducing() | Custom reduction | `collect(Collectors.reducing(0, Person::getAge, Integer::sum))` |
| **Grouping** | groupingBy() | Groups by classifier | `collect(Collectors.groupingBy(Person::getDept))` |
|  | partitioningBy() | Splits by predicate | `collect(Collectors.partitioningBy(p -> p.getAge() > 30))` |
| **Transformation** | mapping() | Transforms before collection | `groupingBy(getDept(), mapping(getName(), toList()))` |
|  | collectingAndThen() | Post-processes result | `collectingAndThen(toList(), Collections::unmodifiableList)` |
| **Custom** | Collector.of() | Creates custom collector | `Collector.of(supplier, accumulator, combiner, finisher)` |

### Cheat Sheet for Common Tasks

| Task | Collector Code |
|------|--------------|
| List of names | `people.stream().map(Person::getName).collect(toList())` |
| Set of departments | `people.stream().map(Person::getDept).collect(toSet())` |
| Map of ID to Person | `people.stream().collect(toMap(Person::getId, p -> p))` |
| Comma-joined names | `people.stream().map(Person::getName).collect(joining(", "))` |
| Total age | `people.stream().collect(summingInt(Person::getAge))` |
| Average salary | `people.stream().collect(averagingDouble(Person::getSalary))` |
| All age statistics | `people.stream().collect(summarizingInt(Person::getAge))` |
| Oldest person | `people.stream().collect(maxBy(comparing(Person::getAge)))` |
| People by dept | `people.stream().collect(groupingBy(Person::getDept))` |
| Count by dept | `people.stream().collect(groupingBy(Person::getDept, counting()))` |
| Adults vs minors | `people.stream().collect(partitioningBy(p -> p.getAge() >= 18))` |
| Names by dept | `people.stream().collect(groupingBy(Person::getDept, mapping(Person::getName, toList())))` |
| Immutable result | `stream.collect(collectingAndThen(toList(), Collections::unmodifiableList))` |

I hope this guide helps you prepare effectively for your Java interviews! Good luck! 🍀