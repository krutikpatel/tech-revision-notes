# 🧩 Advanced Java Generics

As a senior Java engineer and interview coach, I'll help you master advanced Java Generics concepts with interview-ready explanations and examples.

---------

## 1. 🔍 Wildcards (?, ? extends, ? super)

### Unbounded Wildcards (?)
- ✅ Represents "any type" - most flexible but least specific
- ✅ Used when actual type parameter doesn't matter
- ✅ Common in utility methods that don't depend on specific type
- ✅ Can only read `Object` from such collections

```java
// Using unbounded wildcard
public static void printList(List<?> list) {
    for (Object elem : list) {
        System.out.println(elem);
    }
}

// Usage
List<String> strings = Arrays.asList("Hello", "World");
List<Integer> numbers = Arrays.asList(1, 2, 3);
printList(strings); // Works
printList(numbers); // Also works
```

### Upper Bounded Wildcards (? extends T)
- ✅ Represents "T or any subtype of T"
- ✅ Enables read-only access to collection elements as type T
- ✅ Cannot add elements (except null) to such collections
- ✅ Provides covariance: if A is a subtype of B, then List<? extends A> is a subtype of List<? extends B>

```java
// Upper bounded wildcard
public static double sumOfList(List<? extends Number> list) {
    double sum = 0.0;
    for (Number num : list) {
        sum += num.doubleValue();
    }
    return sum;
}

// Usage
List<Integer> integers = Arrays.asList(1, 2, 3);
List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3);
System.out.println(sumOfList(integers)); // Works
System.out.println(sumOfList(doubles));  // Also works

// Cannot add elements (read-only view)
List<? extends Number> numbers = integers;
// numbers.add(10); // Compile error!
// numbers.add(new Integer(10)); // Compile error!
numbers.add(null); // Only null is allowed
```

### Lower Bounded Wildcards (? super T)
- ✅ Represents "T or any supertype of T"
- ✅ Enables adding elements of type T (or its subtypes) to collection
- ✅ Can only read as Object from such collections
- ✅ Provides contravariance: if A is a supertype of B, then List<? super A> is a subtype of List<? super B>

```java
// Lower bounded wildcard
public static void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
    list.add(3);
}

// Usage
List<Number> numberList = new ArrayList<>();
List<Object> objectList = new ArrayList<>();
addIntegers(numberList); // Works
addIntegers(objectList); // Also works

// Can add elements but reading gives Object
List<? super Integer> consumers = numberList;
consumers.add(42);
// Integer x = consumers.get(0); // Compile error!
Object obj = consumers.get(0); // Only as Object
```

### PECS Principle (Producer Extends, Consumer Super)
- 📌 "Producer Extends, Consumer Super" - Josh Bloch's guideline
- 📌 Use `? extends T` when reading values out (producer)
- 📌 Use `? super T` when inserting values in (consumer)
- 📌 Critical for designing flexible, reusable generic APIs

```java
// PECS example: Copy method
public static <T> void copy(List<? extends T> source, List<? super T> dest) {
    for (T item : source) {
        dest.add(item);
    }
}

// Usage
List<Integer> ints = Arrays.asList(1, 2, 3);
List<Number> nums = new ArrayList<>();
copy(ints, nums); // Integers (extends Number) -> Numbers
```

### Wildcard Capture
- 📌 Java compiler sometimes needs to "capture" the unknown type
- 📌 Helpful for helper methods that need to work with specific but unknown type
- 📌 Used to overcome limitations of wildcards

```java
// Wildcard capture example
public static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j); // Helper method with captured type
}

// Helper method with captured type parameter
private static <T> void swapHelper(List<T> list, int i, int j) {
    T temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}
```

### Common Mistakes with Wildcards
- ❌ Using bounded wildcard when type parameter would work better
- ❌ Adding elements to a `List<? extends T>` (not allowed)
- ❌ Expecting to read specific types from a `List<? super T>` (only Object)
- ❌ Not following PECS principle
- ❌ Confusing unbounded wildcard (`List<?>`) with raw type (`List`)

---------

## 2. 🔒 Bounded Type Parameters

### Upper Bounds
- ✅ Restricts type parameter to be subtype of specified type
- ✅ Syntax: `<T extends UpperBound>`
- ✅ Allows access to methods/properties of the bound
- ✅ "extends" keyword used for both classes and interfaces

```java
// Upper bound to ensure T has Comparable methods
public static <T extends Comparable<T>> T findMax(List<T> list) {
    if (list.isEmpty()) {
        throw new IllegalArgumentException("Empty list");
    }
    
    T max = list.get(0);
    for (T item : list.subList(1, list.size())) {
        if (item.compareTo(max) > 0) {
            max = item;
        }
    }
    return max;
}

// Usage
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
String longest = findMax(names); // Returns "Charlie"
```

### Multiple Bounds
- ✅ Type parameter can have multiple bounds
- ✅ Syntax: `<T extends Class1 & Interface1 & Interface2>`
- ✅ At most one class can be specified (and must be first)
- ✅ Ensures type has all specified capabilities

```java
// Multiple bounds example
public static <T extends Number & Comparable<T>> T findMinimum(List<T> list) {
    if (list.isEmpty()) {
        return null;
    }
    
    T min = list.get(0);
    for (T item : list.subList(1, list.size())) {
        if (item.compareTo(min) < 0) {
            min = item;
        }
    }
    return min;
}

// Usage
List<Integer> numbers = Arrays.asList(3, 1, 4, 1, 5);
Integer min = findMinimum(numbers); // Returns 1
```

### Recursive Bounds
- ✅ Type parameter bound can reference itself
- ✅ Common pattern with Comparable interface
- ✅ Ensures "self-comparable" types

```java
// Recursive bound example
public class Box<T extends Comparable<T>> implements Comparable<Box<T>> {
    private T value;
    
    public Box(T value) {
        this.value = value;
    }
    
    public T getValue() {
        return value;
    }
    
    @Override
    public int compareTo(Box<T> other) {
        return this.value.compareTo(other.value);
    }
}
```

### More Complex Recursive Bounds
- ✅ Sometimes need to handle recursive relationships with inheritance
- ✅ Pattern: `<T extends Comparable<? super T>>`
- ✅ Allows for comparing to parent types

```java
// More complex recursive bound
public static <T extends Comparable<? super T>> T max(List<T> list) {
    // Implementation
    return null;
}

// This works for:
// class Person implements Comparable<Person> {}
// class Employee extends Person {}
// List<Employee> can be passed to max() even though Employee doesn't directly implement Comparable<Employee>
```

### Common Mistakes with Bounded Type Parameters
- ❌ Too restrictive bounds limiting reusability
- ❌ Confusing when to use bounded type parameters vs. bounded wildcards
- ❌ Forgetting that bounds are not enforced at runtime due to type erasure
- ❌ Not considering class hierarchies when designing bounds

---------

## 3. 🔄 Type Erasure and Its Implications

### What is Type Erasure?
- ✅ Java's implementation mechanism for generics
- ✅ Process where compiler removes generic type information after compilation
- ✅ Replaces type parameters with their bounds (or Object if unbounded)
- ✅ Inserts necessary casts to maintain type safety
- ✅ Added to Java for backward compatibility with pre-generics code

```java
// Before erasure
public class Box<T> {
    private T value;
    public T getValue() { return value; }
    public void setValue(T value) { this.value = value; }
}

// After erasure (conceptually)
public class Box {
    private Object value;
    public Object getValue() { return value; }
    public void setValue(Object value) { this.value = value; }
}
```

### Bridge Methods
- 📌 Compiler generates synthetic "bridge methods" to handle inheritance with generics
- 📌 Ensures type safety and preserves polymorphism
- 📌 Not typically visible to developers but important to understand

```java
// Before compilation
class NumberBox<T extends Number> {
    public void set(T value) { /* implementation */ }
}

class IntegerBox extends NumberBox<Integer> {
    @Override
    public void set(Integer value) { /* implementation */ }
}

// After compilation (conceptually)
class NumberBox {
    public void set(Number value) { /* implementation */ }
}

class IntegerBox extends NumberBox {
    // Original method
    public void set(Integer value) { /* implementation */ }
    
    // Bridge method (synthetic)
    public void set(Number value) {
        set((Integer) value); // Cast and delegate
    }
}
```

### Implications of Type Erasure

#### 1. Cannot Overload Methods That Erase to Same Signature
- ❌ Methods with different generic parameters but same erasure won't compile

```java
// ERROR: These have same erasure
public void process(List<String> strings) { /* ... */ }
public void process(List<Integer> integers) { /* ... */ }

// After erasure (both become):
public void process(List list) { /* ... */ }
```

#### 2. Cannot Create Instances of Type Parameters
- ❌ Cannot use `new T()` because T's constructor is unknown at runtime

```java
// ERROR: Cannot instantiate type parameter
public <T> T createInstance() {
    return new T(); // Compile error!
}

// Workaround using Class<T> parameter
public <T> T createInstance(Class<T> clazz) throws Exception {
    return clazz.getDeclaredConstructor().newInstance();
}
```

#### 3. Cannot Create Arrays of Parameterized Types
- ❌ Cannot create arrays of generic types directly

```java
// ERROR: Cannot create array of parameterized type
public <T> T[] createArray(int size) {
    return new T[size]; // Compile error!
}

// Workaround
@SuppressWarnings("unchecked")
public <T> T[] createArray(Class<T> clazz, int size) {
    return (T[]) Array.newInstance(clazz, size);
}
```

#### 4. Cannot Use instanceof with Parameterized Types
- ❌ Type parameters are not available at runtime for instanceof checks

```java
// ERROR: Cannot use instanceof with parameterized types
public boolean checkIfStringList(Object list) {
    // return list instanceof List<String>; // Compile error!
    
    // Workaround: use raw type and cast safely inside
    return list instanceof List; // Can only check raw type
}
```

#### 5. Static Fields Shared Among All Instantiations
- ❌ Static fields are shared across all instantiations regardless of type parameter

```java
// CAUTION: Static field shared across all instantiations
public class Container<T> {
    private static List<T> items; // T is erased, same list for all types
    
    public static void add(T item) {
        if (items == null) {
            items = new ArrayList<>();
        }
        items.add(item);
    }
}

// Both modify the same list!
Container<String>.add("hello");
Container<Integer>.add(42); // Runtime error: ClassCastException
```

### Performance Implications
- ✅ No runtime overhead for using generics (unlike C# generics)
- ✅ All generic instances share same code, reducing code size
- ✅ Some boxing/unboxing overhead when using generic collections with primitives

---------

## 4. 🧪 Reifiable vs Non-reifiable Types

### Reifiable Types
- ✅ Types whose information is fully available at runtime
- ✅ Can be used in instanceof checks and class literals
- ✅ Examples: primitives, non-generic classes, raw types, unbounded wildcards, arrays of reifiable types

```java
// Reifiable types examples
Class<String> stringClass = String.class; // Class literal for reifiable type
boolean isString = obj instanceof String; // instanceof with reifiable type
String[] strings = new String[10]; // Array of reifiable type
```

### Non-reifiable Types
- ✅ Types whose information is partially or completely unavailable at runtime due to type erasure
- ✅ Cannot use in certain contexts (instanceof, class literals, array creation)
- ✅ Examples: parameterized types, bounded wildcards, type parameters

```java
// Non-reifiable types examples (these don't work)
// Class<List<String>> listClass = List<String>.class; // ERROR
// boolean isStringList = obj instanceof List<String>; // ERROR
// List<String>[] stringLists = new List<String>[10]; // ERROR
```

### Heap Pollution
- 📌 When a variable of parameterized type references an object not of that type
- 📌 Can occur with unchecked warnings or varargs with generics
- 📌 Can lead to ClassCastExceptions

```java
// Example of potential heap pollution
@SuppressWarnings("unchecked")
List<String> stringList = (List<String>) unsafeMethod();

// Potential heap pollution with varargs
public static <T> void addAll(List<T> list, T... elements) {
    for (T element : elements) {
        list.add(element);
    }
}

// Usage that causes heap pollution
List<String> strings = new ArrayList<>();
Object[] objects = new Object[] {"Hello", 42}; // Mixed types
addAll(strings, objects); // Runtime ClassCastException when accessing the Integer
```

### Reifiable Types and Arrays
- 📌 Arrays in Java are reifiable and have runtime type information
- 📌 This creates issues with generic types due to array covariance
- 📌 Explains why generic array creation is prohibited

```java
// Arrays are covariant
Object[] objectArray = new String[10]; // Legal
objectArray[0] = "Hello"; // Fine
objectArray[1] = 42; // Runtime ArrayStoreException

// This is why generic arrays are not allowed
// List<String>[] stringLists = new List<String>[10]; // Not allowed

// If it were allowed:
// List<String>[] stringLists = new List<String>[10]; // Assume this works
// List<Integer>[] intLists = (List<Integer>[]) stringLists; // Would compile with unchecked warning
// intLists[0] = new ArrayList<Integer>();
// String s = stringLists[0].get(0); // ClassCastException at runtime
```

### @SafeVarargs Annotation
- ✅ Suppresses unchecked warnings related to varargs usage with generics
- ✅ Indicates that method does not perform unsafe operations on varargs parameter
- ✅ Can only be applied to final, static, or private methods (Java 9+: constructors too)

```java
// Safe varargs example
@SafeVarargs
public static <T> List<T> asList(T... elements) {
    List<T> list = new ArrayList<>();
    for (T element : elements) {
        list.add(element);
    }
    return list;
}
```

---------

## 5. 🕰️ Raw Types and Backward Compatibility

### What are Raw Types?
- ✅ Generic type used without any type parameters
- ✅ Example: `List` instead of `List<String>`
- ✅ Maintained for backward compatibility with pre-Java 5 code
- ✅ Bypasses generic type checks at compile time

```java
// Raw type examples
List rawList = new ArrayList(); // Raw type
rawList.add("string");
rawList.add(42); // No compile-time error!

// When using raw types, you lose type safety
String s = (String) rawList.get(0); // Explicit cast needed
Integer i = (Integer) rawList.get(1); // Explicit cast needed
```

### Backward Compatibility
- ✅ Java generics designed for migration compatibility
- ✅ Raw types allow interaction with legacy code
- ✅ Generic code can be used with non-generic code (with warnings)
- ✅ Ensures existing code continues to work after introducing generics

```java
// Legacy code (pre-Java 5)
void legacyMethod(List list) {
    list.add(new Object());
}

// Modern code with generics
List<String> strings = new ArrayList<>();
legacyMethod(strings); // Unchecked warning
// String s = strings.get(0); // Potential ClassCastException
```

### Unchecked Warnings
- 📌 Compiler issues "unchecked" warnings when mixing raw types with generics
- 📌 Indicates potential type safety problems
- 📌 Can be suppressed with `@SuppressWarnings("unchecked")` where appropriate

```java
// Unchecked warnings examples
List<String> strings = new ArrayList<>();
List rawList = strings; // Unchecked warning
rawList.add(42); // Corrupts the strings list!

// Sometimes suppression is necessary but use with caution
@SuppressWarnings("unchecked")
public <T> T[] toArray(T[] a) {
    // Implementation involving unchecked cast
    return a;
}
```

### Why Avoid Raw Types
- ❌ Lose type safety at compile time
- ❌ Lose expressiveness (cannot differentiate List<String> from List<Integer>)
- ❌ Only compatible with Object methods in IDE autocompletion
- ❌ Can lead to runtime ClassCastExceptions
- ❌ Only use when interacting with legacy code

```java
// DON'T DO THIS in new code
List dates = new ArrayList();
dates.add("2023-01-01"); // Should be a date
dates.add("not a date");

// Better approach
List<Date> dates = new ArrayList<>();
dates.add(new Date());
// dates.add("not a date"); // Compile error!
```

### Common Mistakes with Raw Types
- ❌ Using raw types in new code (should always use proper generics)
- ❌ Confusing raw types with unbounded wildcards
- ❌ Ignoring unchecked warnings without understanding them
- ❌ Assuming legacy code will work correctly with generic collections

### Raw Types vs. Unbounded Wildcards
- 📌 Raw type: `List` - bypasses generics entirely
- 📌 Unbounded wildcard: `List<?>` - uses generics with unknown type
- 📌 Always prefer `List<?>` over raw `List` in new code

```java
// Raw type vs. unbounded wildcard
// Raw type (unsafe)
void printRaw(List list) {
    list.add(new Object()); // Allowed but potentially unsafe
    for (Object obj : list) {
        System.out.println(obj);
    }
}

// Unbounded wildcard (safe)
void printSafe(List<?> list) {
    // list.add(new Object()); // Compile error! (except null)
    for (Object obj : list) {
        System.out.println(obj);
    }
}
```

---------

## 6. 📋 Summary

✅ **Wildcards**: Provide flexibility in API design with `?` (any type), `? extends T` (T or subtypes), and `? super T` (T or supertypes)

✅ **PECS Principle**: "Producer Extends, Consumer Super" - use `? extends` when reading, `? super` when writing

✅ **Bounded Type Parameters**: Restrict type parameters to certain types (`<T extends Number>`) or even multiple bounds (`<T extends Number & Comparable<T>>`)

✅ **Type Erasure**: Java removes generic type information at runtime, replacing type parameters with their bounds or Object

✅ **Reifiable Types**: Types with complete runtime information (primitives, non-generic classes, raw types) vs non-reifiable types (parameterized types, type parameters)

✅ **Raw Types**: Generic types used without type parameters, maintained for backward compatibility but should be avoided in new code

✅ **Best Practices**: Follow PECS, avoid raw types, understand erasure limitations, handle unchecked warnings properly

---------

## 7. 📊 Quick Reference Table

| Concept | Description | Syntax | Use When | Limitations |
|---------|-------------|--------|----------|-------------|
| **Unbounded Wildcard** | Any type | `List<?>` | Type doesn't matter, read-only | Can't add elements except null |
| **Upper Bounded Wildcard** | T or any subtype | `List<? extends T>` | Reading from collection (Producer) | Can't add elements except null |
| **Lower Bounded Wildcard** | T or any supertype | `List<? super T>` | Adding to collection (Consumer) | Can only read as Object |
| **PECS Principle** | Producer Extends, Consumer Super | N/A | Designing flexible APIs | Need to understand variance |
| **Bounded Type Parameter** | Restrict type parameter | `<T extends Bound>` | Need to use bound's methods | Not enforced at runtime |
| **Multiple Bounds** | Multiple constraints | `<T extends A & B & C>` | Type needs multiple capabilities | Max one class, must be first |
| **Type Erasure** | Runtime implementation | N/A | Understanding limitations | Information lost at runtime |
| **Reifiable Types** | Full runtime type info | N/A | Arrays, instanceof, reflection | Limited to non-generic types |
| **Non-reifiable Types** | Incomplete runtime info | N/A | Awareness of limitations | Can't create arrays, use instanceof |
| **Raw Types** | Pre-generics compatibility | `List` instead of `List<T>` | Legacy code integration only | Bypasses type safety |

---------

## 8. 👨‍💻 Interview-Ready Code Examples

### Complete PECS Example (Collection Copy)
```java
public class GenericUtil {
    // Demonstrates PECS principle
    public static <T> void copy(List<? extends T> source, List<? super T> destination) {
        for (T item : source) {
            destination.add(item);
        }
    }
    
    public static void main(String[] args) {
        // Copying from specific type to more general type
        List<Integer> integers = Arrays.asList(1, 2, 3);
        List<Number> numbers = new ArrayList<>();
        
        copy(integers, numbers); // Works - Integer extends Number
        System.out.println(numbers); // [1, 2, 3]
        
        // Won't compile - wrong direction:
        // copy(numbers, integers);
    }
}
```

### Type Erasure Example (Bridge Methods)
```java
class Node<T> {
    private T data;
    
    public T getData() {
        return data;
    }
    
    public void setData(T data) {
        this.data = data;
    }
}

class StringNode extends Node<String> {
    // Override with more specific type
    @Override
    public void setData(String data) {
        if (data != null && !data.isEmpty()) {
            super.setData(data);
        }
    }
    
    // After erasure and bridge method generation:
    // 1. Original method: public void setData(String data) {...}
    // 2. Bridge method (synthetic): public void setData(Object data) {
    //        setData((String) data);
    //    }
}
```

### Bounded Type Parameter Practical Example
```java
public class MathUtils {
    // Method to find sum of any numbers
    public static <T extends Number> double sum(List<T> numbers) {
        double sum = 0.0;
        for (T number : numbers) {
            sum += number.doubleValue();
        }
        return sum;
    }
    
    // Method to find max element with recursive bound
    public static <T extends Comparable<? super T>> T max(List<T> list) {
        if (list.isEmpty()) {
            throw new IllegalArgumentException("Empty list");
        }
        
        T result = list.get(0);
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i).compareTo(result) > 0) {
                result = list.get(i);
            }
        }
        return result;
    }
}
```

---------

## 9. 🔍 Common Interview Questions and Answers

### Q: Explain PECS principle and give an example
**A:** PECS stands for "Producer Extends, Consumer Super." It guides when to use upper vs. lower bounded wildcards:
- Use `? extends T` when you only read values from a structure (the structure produces values)
- Use `? super T` when you only write values to a structure (the structure consumes values)

Example: In `Collections.copy(List<? extends T> src, List<? super T> dest)`, the source list produces values (we read from it), so it uses `? extends T`. The destination list consumes values (we write to it), so it uses `? super T`.

### Q: Why can't you add elements to a List<? extends T>?
**A:** When you have a `List<? extends T>`, the actual list could be of any subtype of T. The compiler cannot guarantee type safety because:
- If you have `List<? extends Number> list`, it could be a `List<Integer>` or a `List<Double>`
- If it were a `List<Integer>` and you could add a `Double`, this would violate type safety
- Since the compiler can't determine the exact type, it conservatively prevents adding any elements (except null)

### Q: Why are generic arrays not allowed in Java?
**A:** Generic arrays are not allowed because arrays are reifiable (retain their component type at runtime) and covariant (if A is a subtype of B, then A[] is a subtype of B[]), while generics are non-reifiable (type information erased at runtime) and invariant.

This combination would break type safety. For example, if we could create `List<String>[]`, we could upcast it to `Object[]`, store a `List<Integer>` in it, and then try to get a String from an Integer list, causing a ClassCastException.

### Q: What's the difference between List<?> and List<Object>?
**A:** 
- `List<?>` is an unbounded wildcard representing "a list of some unknown type"
- `List<Object>` is a list that can contain objects of any type

The key difference: with `List<?>`, you can't add any elements except null because the actual type is unknown. With `List<Object>`, you can add any object. Also, `List<String>` is a subtype of `List<?>` but not of `List<Object>`.

### Q: When would you use a bounded type parameter vs. a bounded wildcard?
**A:** 
- Use bounded type parameter (`<T extends Bound>`) when you need to refer to that type multiple times in a method signature or need to enforce relationships between parameters
- Use bounded wildcard (`? extends Bound`) when you only need to refer to the type once, typically as a parameter type

Example:
```java
// Type parameter - need to refer to T multiple times
<T extends Comparable<T>> T max(List<T> list)

// Wildcard - only need to refer to the type once
void process(List<? extends Number> list)
```