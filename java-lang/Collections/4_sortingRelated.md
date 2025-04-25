# Java Collections Comparators and Sorting: Interview Preparation Guide 🧠

## 1. 📊 Comparable vs Comparator
---------

### What Are They? 📌
Both `Comparable` and `Comparator` are interfaces used for sorting objects in Java, but they serve different purposes and are implemented differently.

#### Comparable Interface ✅
- **Purpose**: Provides a natural ordering for a class
- **Package**: `java.lang`
- **Method**: `int compareTo(T o)`
- **Implementation**: The class itself implements this interface

```java
public class Employee implements Comparable<Employee> {
    private String name;
    private int id;
    
    // Constructor, getters, setters...
    
    @Override
    public int compareTo(Employee other) {
        // Natural ordering by employee ID
        return Integer.compare(this.id, other.id);
    }
}

// Usage:
List<Employee> employees = getEmployees();
Collections.sort(employees);  // Uses natural ordering (by ID)
```

#### Comparator Interface ✅
- **Purpose**: Provides custom ordering for any class (even those you don't own)
- **Package**: `java.util`
- **Method**: `int compare(T o1, T o2)`
- **Implementation**: External class or lambda implements this interface

```java
// External Comparator class
public class EmployeeNameComparator implements Comparator<Employee> {
    @Override
    public int compare(Employee e1, Employee e2) {
        return e1.getName().compareTo(e2.getName());
    }
}

// Usage:
List<Employee> employees = getEmployees();
Collections.sort(employees, new EmployeeNameComparator());  // Custom ordering
```

### Key Differences 🔍

```
               Comparable                 Comparator
               ----------                 ----------
Package        java.lang                  java.util
Method         compareTo(T o)             compare(T o1, T o2)
Implemented by Class itself               External class/lambda
Purpose        Natural ordering           Custom ordering
Usage          Collections.sort(list)     Collections.sort(list, comparator)
Can sort       One way only               Multiple ways
```

### Common Interview Traps ❌
- Forgetting return values: negative (<), zero (=), positive (>)
- Inconsistent comparison (violating transitivity)
- Modifying objects during comparison
- Not handling null values properly

### Best Practices ✨
- Make `compareTo` consistent with `equals` when implementing `Comparable`
- Use `Comparator` for multiple sorting options
- Use `Comparator` when you can't modify the class's source code
- For numeric comparisons, use `Integer.compare()`, `Double.compare()`, etc.
- For string comparisons, consider case-sensitivity with `String.CASE_INSENSITIVE_ORDER`


## 2. 🌿 Natural Ordering vs Custom Ordering
---------

### Natural Ordering 📌
Natural ordering is the default way objects of a class are sorted when the class implements `Comparable`.

#### Common Natural Orderings in Java ✅
- **String**: Lexicographical (dictionary) order
- **Numeric types**: Ascending numeric order
- **Date/Time**: Chronological order
- **Boolean**: false before true
- **Character**: Unicode value

```java
// Examples of natural ordering
List<String> names = Arrays.asList("Charlie", "Alice", "Bob");
Collections.sort(names);  // Results in [Alice, Bob, Charlie]

List<Integer> numbers = Arrays.asList(5, 2, 8, 1);
Collections.sort(numbers);  // Results in [1, 2, 5, 8]
```

### Custom Ordering 📌
Custom ordering allows sorting objects in ways different from their natural order, using `Comparator`.

#### Common Custom Ordering Patterns ✅
- Reverse order
- Multiple fields (primary/secondary sorting)
- Case-insensitive string comparison
- Nulls handling (first or last)

```java
// Reverse order
List<Integer> numbers = Arrays.asList(5, 2, 8, 1);
Collections.sort(numbers, Collections.reverseOrder());  // [8, 5, 2, 1]

// Custom multi-field ordering
Comparator<Employee> byDeptThenName = Comparator
    .comparing(Employee::getDepartment)
    .thenComparing(Employee::getName);
Collections.sort(employees, byDeptThenName);

// Case-insensitive sorting
Collections.sort(names, String.CASE_INSENSITIVE_ORDER);

// Null handling
Comparator<String> nullsLast = Comparator.nullsLast(String::compareTo);
Collections.sort(stringList, nullsLast);
```

### Common Interview Traps ❌
- Assuming all Java classes have natural ordering (many do not)
- Not handling null values in custom comparators
- Creating inconsistent ordering that violates transitivity
- Not understanding performance implications

### Best Practices ✨
- Make custom comparators stateless and serializable
- Use `Comparator.nullsFirst()` or `nullsLast()` for null handling
- For complex objects, create separate comparators for different use cases
- Chain comparators for multi-field sorting using `thenComparing()`


## 3. λ Lambda-Based Sorting (Java 8+)
---------

### Modern Sorting Approaches 📌
Java 8 revolutionized sorting with lambda expressions and method references, making code more concise and readable.

#### Key Comparator Factory Methods ✅
- `Comparator.comparing()`: Create comparator using key extractor
- `Comparator.thenComparing()`: Add secondary sort keys
- `Comparator.reversed()`: Reverse ordering
- `Comparator.nullsFirst()/nullsLast()`: Handle null values

### Code Examples 💻

```java
List<Employee> employees = getEmployees();

// Basic lambda sorting
employees.sort((e1, e2) -> e1.getName().compareTo(e2.getName()));

// Method reference (equivalent to above)
employees.sort(Comparator.comparing(Employee::getName));

// Reversed order
employees.sort(Comparator.comparing(Employee::getSalary).reversed());

// Multiple fields with method references
employees.sort(
    Comparator.comparing(Employee::getDepartment)
              .thenComparing(Employee::getName)
              .thenComparing(Employee::getSalary, Comparator.reverseOrder())
);

// Handling nulls
employees.sort(Comparator.comparing(
    Employee::getManager,  // Manager might be null
    Comparator.nullsLast(Comparator.comparing(Manager::getName))
));

// Custom comparison logic (e.g., case-insensitive)
employees.sort(Comparator.comparing(
    Employee::getName, 
    String.CASE_INSENSITIVE_ORDER
));
```

### Stream API Integration ✅

```java
// Sorting within streams
List<Employee> sortedEmployees = employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary).reversed())
    .collect(Collectors.toList());

// Getting top 5 highest paid employees
List<Employee> topPaid = employees.stream()
    .sorted(Comparator.comparing(Employee::getSalary).reversed())
    .limit(5)
    .collect(Collectors.toList());
```

### Common Interview Traps ❌
- Not handling potential NullPointerException in key extractors
- Overcomplicating simple comparisons
- Performance overhead of lambda capture
- Creating intermediate collections unnecessarily

### Best Practices ✨
- Use method references (`Employee::getName`) instead of lambdas when possible
- Chain comparators for multi-field sorting instead of complex custom logic
- Reuse comparator instances if they're used multiple times
- Consider creating static utility comparators for common sorting needs


## 4. 💡 Interview-Ready Insights
---------

### Performance Considerations ⚡
- Sorting is O(n log n) for most Java collections
- `Collections.sort()` uses a modified mergesort (stable)
- `Arrays.sort()` uses quicksort for primitives (unstable) and mergesort for objects (stable)
- Method reference comparators generally perform better than lambda expressions
- `Comparable` can be slightly faster than `Comparator` (no indirection)

### Common Interview Questions 🎯
1. "What's the difference between Comparable and Comparator?"
2. "How do you sort a list of custom objects in reverse order?"
3. "How would you sort a list by multiple fields?"
4. "How do you handle null values in comparators?"
5. "Why should compareTo be consistent with equals?"

### Java Evolution Context 🌱
- Java 8 dramatically simplified comparators with lambdas and method references
- Java 8 added `Comparator.comparing()`, `thenComparing()`, etc.
- Java 8 Stream API integrated sorting capabilities
- Modern approach is more declarative and functional

### Real-World Application 🌐
- Database-like ordering in UI tables
- Custom sorting in search results
- Priority queues in scheduling systems
- Natural key ordering in TreeSet/TreeMap


## 5. 📝 Summary
---------

### Comparable vs Comparator
- **Comparable**: Single natural ordering; implemented by the class itself
- **Comparator**: Multiple custom orderings; implemented externally
- **Choice**: Use Comparable for fundamental ordering, Comparator for alternative orderings

### Natural vs Custom Ordering
- **Natural**: Default order defined by class's `compareTo` method
- **Custom**: Alternative ordering defined by external comparators
- **Application**: Use natural for standard cases, custom for specific needs

### Lambda-Based Sorting
- **Traditional**: Anonymous Comparator classes
- **Modern**: Lambda expressions and method references
- **Utility Methods**: `comparing()`, `thenComparing()`, `reversed()`, `nullsFirst()`
- **Integration**: Works well with Stream API for functional-style operations


## 6. 📊 Quick Reference Table
---------

| Feature | Comparable | Comparator |
|---------|------------|------------|
| **Interface** | `java.lang.Comparable` | `java.util.Comparator` |
| **Method** | `int compareTo(T o)` | `int compare(T o1, T o2)` |
| **Implementation** | By class itself | External class/lambda |
| **Usage** | `Collections.sort(list)` | `Collections.sort(list, comparator)` |
| **Java 8+** | No changes | Factory methods & lambda support |
| **Number of ways** | One (natural) | Multiple (custom) |
| **Null support** | Typically no | Yes with `nullsFirst()/nullsLast()` |

### Sorting Evolution in Java

```
Java Version     Typical Syntax
-----------      -------------
Java 5           Collections.sort(list, new NameComparator())
Java 7           Collections.sort(list, new Comparator<Employee>() {
                     public int compare(Employee e1, Employee e2) {
                         return e1.getName().compareTo(e2.getName());
                     }
                 })
Java 8           list.sort((e1, e2) -> e1.getName().compareTo(e2.getName()))
Java 8 (modern)  list.sort(Comparator.comparing(Employee::getName))
```

### Common Sorting Patterns Quick Reference

```java
// Basic natural ordering (Comparable)
Collections.sort(list);

// Basic custom ordering (Comparator)
list.sort(comparator);  // Java 8+
Collections.sort(list, comparator);  // Pre-Java 8

// Reverse natural ordering
list.sort(Comparator.reverseOrder());

// Sorting by specific property
list.sort(Comparator.comparing(Person::getAge));

// Multiple field sorting
list.sort(Comparator.comparing(Person::getLastName)
                   .thenComparing(Person::getFirstName));

// Null handling
list.sort(Comparator.nullsLast(Comparator.naturalOrder()));

// Complex example
list.sort(Comparator.comparing(Person::getDepartment)
                   .thenComparing(Person::getSalary, Comparator.reverseOrder())
                   .thenComparing(Person::getName));
```

Remember these patterns for your Java interviews, as sorting is a fundamental operation that comes up frequently in both theoretical and practical questions!
