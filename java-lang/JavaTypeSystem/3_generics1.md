# 🧩 Java Generics

As a senior Java engineer and interview coach, I'll help you master Java Generics with interview-focused explanations and practical examples.

---------

## 1. 📦 Generic Classes and Interfaces

### What Are Generics?
- ✅ Introduced in Java 5 to provide compile-time type safety
- ✅ Allow you to create classes, interfaces, and methods that operate on different data types while maintaining type safety
- ✅ Eliminate need for casting and prevent runtime ClassCastExceptions
- ✅ Enable creation of reusable, type-safe collections and algorithms

### Generic Classes
- ✅ Classes that can operate on parameterized types
- ✅ Syntax: `class ClassName<T> { ... }`
- ✅ Type parameter `T` works as a placeholder for actual type

```java
// Generic class example
public class Box<T> {
    private T value;
    
    public Box(T value) {
        this.value = value;
    }
    
    public T getValue() {
        return value;
    }
    
    public void setValue(T value) {
        this.value = value;
    }
}

// Usage
Box<Integer> intBox = new Box<>(42);
Box<String> stringBox = new Box<>("Hello");

Integer i = intBox.getValue(); // No casting needed
String s = stringBox.getValue();
```

### Multiple Type Parameters
- ✅ Classes can have multiple type parameters
- ✅ Useful for container classes like maps, pairs, etc.

```java
// Multiple type parameters
public class Pair<K, V> {
    private K key;
    private V value;
    
    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }
    
    // Getters and setters
    public K getKey() { return key; }
    public V getValue() { return value; }
}

// Usage
Pair<String, Integer> pair = new Pair<>("Age", 30);
```

### Generic Interfaces
- ✅ Interfaces can also be parameterized with type variables
- ✅ Implementation classes must specify type parameters

```java
// Generic interface
public interface Repository<T, ID> {
    T findById(ID id);
    void save(T entity);
    void delete(T entity);
    List<T> findAll();
}

// Implementation for a specific type
public class UserRepository implements Repository<User, Long> {
    @Override
    public User findById(Long id) {
        // Implementation
        return null;
    }
    
    @Override
    public void save(User entity) {
        // Implementation
    }
    
    // Other implementations...
}
```

### Type Erasure
- 📌 Java's generics implementation uses type erasure
- 📌 Generic type information is removed at runtime
- 📌 At runtime, `Box<Integer>` and `Box<String>` are both just `Box`
- 📌 Compiler inserts necessary casts to maintain type safety

### Common Mistakes
- ❌ Using raw types (without type parameters) - never do this in new code
- ❌ Assuming generic type information is available at runtime
- ❌ Trying to create arrays of generic types
- ❌ Ignoring compiler warnings about unchecked casts

```java
// DON'T DO THIS - Using raw types
Box box = new Box("hello");  // Raw type
String s = (String) box.getValue();  // Requires explicit cast

// Cannot create arrays of generic types
// This doesn't compile:
// T[] array = new T[10];  // Error!

// Correct approach for creating "arrays" of generic types
List<T> list = new ArrayList<>();
```

---------

## 2. 🧪 Generic Methods

### Creating Generic Methods
- ✅ Methods that introduce their own type parameters
- ✅ Can appear in generic or non-generic classes
- ✅ Type parameters are declared before the return type
- ✅ Type inference often works, so explicit type arguments are usually optional when calling

```java
// Generic method in a non-generic class
public class Utilities {
    // Generic method
    public static <T> T find(List<T> list, Predicate<T> condition) {
        for (T item : list) {
            if (condition.test(item)) {
                return item;
            }
        }
        return null;
    }
    
    // Multiple type parameters
    public static <T, U> Map<U, T> invert(Map<T, U> map) {
        Map<U, T> result = new HashMap<>();
        for (Map.Entry<T, U> entry : map.entrySet()) {
            result.put(entry.getValue(), entry.getKey());
        }
        return result;
    }
}

// Usage
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
String name = Utilities.find(names, s -> s.startsWith("B"));  // Returns "Bob"
```

### Type Inference
- ✅ Compiler can often infer type parameters from context
- ✅ Makes code cleaner and less verbose
- ✅ Can be explicitly specified if needed: `ClassName.<String>methodName(...)`

```java
// Type inference examples
List<String> names = new ArrayList<>();  // Diamond operator
names.add("Alice");

// These are equivalent:
Utilities.<String>find(names, s -> s.length() > 4);
Utilities.find(names, s -> s.length() > 4);  // Type inferred
```

### Bounded Type Parameters
- ✅ Can restrict type parameters to be certain types or subclasses
- ✅ Upper bounds: `<T extends SomeClass>`
- ✅ Multiple bounds: `<T extends ClassA & InterfaceB & InterfaceC>`

```java
// Upper bound - T must extend Comparable<T>
public static <T extends Comparable<T>> T max(List<T> list) {
    if (list.isEmpty()) {
        throw new IllegalArgumentException("List cannot be empty");
    }
    
    T max = list.get(0);
    for (T item : list.subList(1, list.size())) {
        if (item.compareTo(max) > 0) {
            max = item;
        }
    }
    return max;
}

// Multiple bounds
public static <T extends Number & Comparable<T>> T sum(List<T> list) {
    // Implementation
    return null;
}
```

### Wildcards
- ✅ `?` represents an unknown type
- ✅ Upper bounded wildcard: `? extends Type`
- ✅ Lower bounded wildcard: `? super Type`
- ✅ Unbounded wildcard: just `?`

```java
// Example of wildcards
public static void printList(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}

// Upper bounded wildcard
// Can read from list but not add to it (except null)
public static double sum(List<? extends Number> numbers) {
    double sum = 0.0;
    for (Number num : numbers) {
        sum += num.doubleValue();
    }
    return sum;
}

// Lower bounded wildcard
// Can add elements but reading requires casting
public static void addNumbers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
    // Object obj = list.get(0);  // Returns Object, not Integer
}
```

### PECS Principle (Producer Extends, Consumer Super)
- 📌 "Producer Extends" - use `? extends T` when you only read from structure
- 📌 "Consumer Super" - use `? super T` when you only write to structure
- 📌 Critical for understanding Java collections framework

```java
// PECS examples
// Producer (extends) - only read from source
public static <T> void copy(List<? extends T> source, List<T> dest) {
    for (T item : source) {
        dest.add(item);
    }
}

// Consumer (super) - only write to dest
public static <T> void addAll(List<T> source, List<? super T> dest) {
    for (T item : source) {
        dest.add(item);
    }
}
```

### Common Mistakes with Generic Methods
- ❌ Confusing when to use bounded type parameters vs. wildcards
- ❌ Overusing wildcards when explicit type parameters would work better
- ❌ Using `List<Object>` when `List<?>` is needed
- ❌ Not following PECS principle

---------

## 3. 🔤 Type Parameters (T, E, K, V)

### Naming Conventions
- ✅ Common type parameter names have conventional meanings:
  - `T` - Type (general purpose)
  - `E` - Element (collections)
  - `K` - Key (maps)
  - `V` - Value (maps)
  - `N` - Number
  - `R` - Return type (functions)
  - `S`, `U`, `V` etc. - Additional types

```java
// Convention examples
public class Box<T> { /* ... */ }
public interface List<E> { /* ... */ }
public interface Map<K, V> { /* ... */ }
public <R> R transform(Function<T, R> function) { /* ... */ }
```

### Type Parameter Scope
- ✅ Type parameters are scoped to the class, interface, or method they're declared in
- ✅ Can be used almost anywhere a normal type can be used within their scope

```java
// Type parameter scoping
public class Container<T> {
    private T contents;
    
    // T is in scope here
    public T getContents() {
        return contents;
    }
    
    // Method with its own type parameter
    public <U> void process(U input, Function<U, T> processor) {
        T result = processor.apply(input);
        this.contents = result;
    }
}
```

### Type Parameter Bounds
- ✅ Upper bounds constrain type parameter to be a subtype
- ✅ No direct support for lower bounds on type parameters (use wildcards instead)
- ✅ Recursive bounds: `<T extends Comparable<T>>`

```java
// Various bounds examples
// Simple bound
public class NumericBox<T extends Number> {
    private T value;
    // ...
}

// Interface bound
public class Sorter<T extends Comparable<T>> {
    public void sort(List<T> list) {
        Collections.sort(list);
    }
}

// Multiple bounds
public class Calculator<T extends Number & Serializable> {
    // T is both a Number and Serializable
}

// Recursive bound
public class SelfComparable<T extends Comparable<T>> {
    // T can be compared to itself
}
```

### Type Parameter vs. Wildcards
- ✅ Type parameters: Used when you need to refer to the specific type later
- ✅ Wildcards: Used when you only care about a range of types, not the specific type

```java
// Type parameter - we need to refer to T
public <T> T getFirst(List<T> list) {
    return list.isEmpty() ? null : list.get(0);
}

// Wildcard - we don't need to refer to the specific type
public void printAll(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}
```

### Common Mistakes with Type Parameters
- ❌ Using overly complex bounds
- ❌ Not understanding the difference between `<T>` and `<?>`
- ❌ Forgetting that type parameters are not available at runtime
- ❌ Using meaningless type parameter names

---------

## 4. 🚀 Advanced Generics Concepts

### Invariance, Covariance, and Contravariance
- ✅ Java generics are invariant by default: `List<Integer>` is not a `List<Number>`
- ✅ Use extends wildcard for covariance: `List<? extends Number>` (read-only)
- ✅ Use super wildcard for contravariance: `List<? super Integer>` (write-only)

```java
// Variance examples
List<Integer> integers = new ArrayList<>();
// List<Number> numbers = integers; // ERROR - generics are invariant

// Covariance - can read Number from list of any Number subtype
List<? extends Number> covariantList = integers;
Number n = covariantList.get(0);  // OK
// covariantList.add(1);  // ERROR - can't add to a covariant list

// Contravariance - can add Integer to list of any Integer supertype
List<Number> numbers = new ArrayList<>();
List<? super Integer> contravariantList = numbers;
contravariantList.add(1);  // OK
// Integer i = contravariantList.get(0);  // ERROR - returns Object
```

### Type Erasure Implications
- 📌 Cannot overload methods that would have the same erasure
- 📌 Cannot directly create arrays of generic types
- 📌 Cannot use primitive types as type arguments
- 📌 Cannot use instanceof with generic types

```java
// Type erasure limitations

// ERROR: Overloaded methods with same erasure
// public void process(List<String> strings) { /* ... */ }
// public void process(List<Integer> integers) { /* ... */ }

// ERROR: Cannot create arrays of generic types directly
// T[] array = new T[10];

// Workaround for creating generic arrays
T[] createArray(Class<T> clazz, int size) {
    @SuppressWarnings("unchecked")
    T[] array = (T[]) Array.newInstance(clazz, size);
    return array;
}

// ERROR: Cannot use instanceof with parameterized types
Object obj = new ArrayList<String>();
// if (obj instanceof List<String>) // ERROR
// Correct: use unbounded wildcard
if (obj instanceof List<?>) {
    // OK
}
```

### Reifiable Types
- ✅ Reifiable types: information available at runtime
- ✅ Non-reifiable types: information lost due to type erasure
- ✅ Arrays are reifiable, generic types are not (except unbounded wildcards)

---------

## 5. 📋 Summary

✅ **Generics Basics**: Java Generics provide compile-time type safety, eliminating the need for explicit casting and preventing runtime ClassCastExceptions

✅ **Generic Classes**: Can work with any type specified at instantiation, with type parameters serving as placeholders

✅ **Generic Methods**: Introduce their own type parameters, allowing for type-safe operations regardless of the containing class

✅ **Type Parameters**: Follow naming conventions (T, E, K, V), can have bounds, and are scoped to their declaration

✅ **Wildcards**: Allow for more flexible APIs using `?`, `? extends Type`, and `? super Type`

✅ **PECS Principle**: "Producer Extends, Consumer Super" guides when to use which wildcard

✅ **Type Erasure**: Generics information is removed at runtime, creating limitations but maintaining backward compatibility

---------

## 6. 📊 Quick Reference Table

| Concept | Purpose | Syntax | When to Use | Common Mistakes |
|---------|---------|--------|-------------|----------------|
| **Generic Class** | Type-safe container/utility | `class Name<T> {}` | Collection-like classes, containers | Using raw types, unchecked warnings |
| **Generic Interface** | Type-safe contract | `interface Name<T> {}` | APIs, service contracts | Forgetting to specify type in implementation |
| **Generic Method** | Type-safe operations | `<T> returnType method()` | Utility methods, algorithms | Confusing with wildcard methods |
| **Type Parameter** | Placeholder for actual type | `<T>`, `<E>`, `<K, V>` | When you need to refer to the type | Forgetting naming conventions |
| **Upper Bound** | Restrict type parameter | `<T extends Class>` | When operations require specific capabilities | Too restrictive bounds |
| **Wildcard** | Unknown type | `<?>` | When specific type doesn't matter | Using when type parameter needed |
| **Upper Bounded Wildcard** | Read from structure | `<? extends Type>` | Read-only access (Producers) | Trying to add elements |
| **Lower Bounded Wildcard** | Write to structure | `<? super Type>` | Write-only access (Consumers) | Trying to read specific types |
| **Type Erasure** | Runtime implementation | N/A | Understanding limitations | Creating arrays of type T, instanceof checks |

---------

## 7. 🎯 Interview Tips

✅ **Type Erasure**: Be prepared to explain how generics are implemented in Java and the implications of type erasure

✅ **PECS**: Know the "Producer Extends, Consumer Super" principle inside out - it's frequently asked

✅ **Variance**: Understand the difference between invariance, covariance, and contravariance in Java generics

✅ **Common Patterns**: Recognize common uses like `Class<T>`, `Comparable<T>`, and collection interfaces

✅ **Limitations**: Be able to explain what you cannot do with generics (create arrays, use with primitives, etc.)

✅ **Wildcards vs. Type Parameters**: Know when to use each and why

✅ **Practical Example**: Be ready to write a generic class or method to solve a practical problem

✅ **Performance**: Understand that generics have no runtime overhead due to type erasure