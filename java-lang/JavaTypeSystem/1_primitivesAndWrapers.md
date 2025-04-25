# 🔍 Java Type System: Primitives and Wrappers

As a senior Java engineer and interview coach, I'll help you understand Java's type system with a focus on primitives and wrappers. Let's make this interview-ready in a compact, efficient format.

---------

## 1. 🧱 Primitives vs Wrapper Classes

### Primitives
- ✅ Basic data types built into Java
- ✅ Stored directly in stack memory (faster access)
- ✅ 8 primitive types: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`
- ✅ Lowercase naming convention
- ✅ Cannot be null
- ✅ No methods or behaviors

### Wrapper Classes
- ✅ Object representations of primitives in `java.lang` package
- ✅ Stored in heap memory with reference in stack
- ✅ Corresponding classes: `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean`
- ✅ UpperCamelCase naming convention
- ✅ Can be null
- ✅ Provide utility methods and behaviors

```java
// Primitives
int a = 5;
boolean isValid = true;

// Wrappers
Integer boxedA = Integer.valueOf(5);
Boolean boxedValid = Boolean.valueOf(true);
```

---------

## 2. 🔄 Autoboxing and Unboxing

### Autoboxing
- ✅ Automatic conversion from primitive to wrapper object
- ✅ Handled by Java compiler since Java 5
- 📌 Occurs when assigning primitive to wrapper reference
- 📌 Happens when passing primitive to method expecting wrapper

### Unboxing
- ✅ Automatic conversion from wrapper object to primitive
- ✅ Handled by Java compiler since Java 5
- 📌 Occurs when assigning wrapper to primitive reference
- 📌 Happens when passing wrapper to method expecting primitive

```java
// Autoboxing
Integer boxed = 42;  // Compiler converts to: Integer boxed = Integer.valueOf(42);

// Unboxing
int unboxed = boxed;  // Compiler converts to: int unboxed = boxed.intValue();

// Autoboxing in collections
List<Integer> numbers = new ArrayList<>();
numbers.add(10);  // Autoboxing: 10 -> Integer(10)

// Unboxing in operations
Integer a = 10;
Integer b = 20;
int sum = a + b;  // Both wrappers are unboxed before addition
```

### Common Mistakes
- ❌ Forgetting that autoboxing/unboxing has performance overhead
- ❌ Using wrapper when primitive would suffice
- ❌ Not handling potential `NullPointerException` when unboxing
- ❌ Excessive boxing/unboxing in loops

```java
// AVOID: NullPointerException risk
Integer nullValue = null;
int primitive = nullValue;  // Runtime NullPointerException!

// BETTER: Null check before unboxing
Integer nullableValue = null;
int safeValue = (nullableValue != null) ? nullableValue : 0;
```

---------

## 3. 🔍 `==` vs `.equals()` in Wrappers

### `==` Operator
- ✅ For primitives: compares values
- ✅ For wrappers: compares object references (memory addresses)
- ❌ Often causes subtle bugs with wrappers
- 📌 Integer cache: special case for values between -128 and 127 (configurable)

### `.equals()` Method
- ✅ Compares values for wrapper objects
- ✅ Should always be used for wrapper value comparison
- ✅ Each wrapper class overrides `equals()` to compare actual values

```java
// == vs equals() with wrappers
Integer a = 100;
Integer b = 100;
Integer c = 200;
Integer d = 200;

// Integer cache in action (-128 to 127)
System.out.println(a == b);         // true! Both references point to same cached object
System.out.println(c == d);         // false! Different objects outside cache range
System.out.println(a.equals(b));    // true (comparing values)
System.out.println(c.equals(d));    // true (comparing values)

// Autoboxing and == can be tricky
Integer x = 1000;
int y = 1000;
System.out.println(x == y);         // true! y is unboxed before comparison
```

### Interview Traps
- ❌ Assuming `==` works the same for primitives and wrappers
- ❌ Not understanding the Integer cache
- ❌ Using `==` for wrapper value comparison

```java
// TRICKY: Creating wrappers with new operator bypasses cache
Integer a = 100;             // Uses Integer cache
Integer b = Integer.valueOf(100);  // Uses Integer cache
Integer c = new Integer(100);      // Creates new object (deprecated in Java 9+)

System.out.println(a == b);        // true (both from cache)
System.out.println(a == c);        // false (different objects)
System.out.println(a.equals(c));   // true (same value)
```

---------

## 4. ⚡ Performance Implications

### Memory Usage
- ✅ Primitives: Fixed small size (e.g., int = 4 bytes)
- ✅ Wrappers: Larger memory footprint (object header + value + potential padding)
- 📌 Wrapper typically uses 16+ bytes vs 4 bytes for an int

### Processing Speed
- ✅ Primitives: Fast direct access
- ✅ Wrappers: Slower due to:
  - Heap allocation
  - Object dereferencing
  - Autoboxing/unboxing overhead
  - Garbage collection pressure

### When to Use Each
- ✅ Use primitives for:
  - Performance-critical code
  - Large arrays
  - Arithmetic operations
  - Known non-null values
  
- ✅ Use wrappers for:
  - Collections (they require objects)
  - When nullability is needed
  - When methods on the value are needed
  - APIs that require objects

```java
// Performance comparison
long start = System.nanoTime();

// Primitive sum
int sum1 = 0;
for (int i = 0; i < 10000000; i++) {
    sum1 += i;
}

long primitiveDuration = System.nanoTime() - start;
start = System.nanoTime();

// Wrapper sum with autoboxing/unboxing
Integer sum2 = 0;
for (Integer i = 0; i < 10000000; i++) {
    sum2 += i;  // Unbox, add, autobox
}

long wrapperDuration = System.nanoTime() - start;
System.out.println("Primitive is about " + (wrapperDuration / primitiveDuration) + "x faster");
// Output: Primitive is about 5-10x faster (varies by JVM)
```

### Best Practices
- ✅ Prefer primitives unless you need wrapper features
- ✅ Be careful with null when using wrappers
- ✅ Use the right tool for collections: primitive collections libraries like Trove, Eclipse Collections for high-performance needs
- ✅ Be aware of excessive boxing/unboxing in loops
- ✅ Always use `.equals()` for wrapper value comparison

---------

## 5. 📋 Summary

✅ **Primitives** are simple, fast, stack-based data types (`int`, `boolean`, etc.)

✅ **Wrappers** are object versions of primitives (`Integer`, `Boolean`, etc.) with added functionality

✅ **Autoboxing** automatically converts primitives to wrappers; **unboxing** does the reverse

✅ Use `==` for primitives but `.equals()` for wrappers to compare values

✅ Wrapper objects have a significant performance overhead compared to primitives

✅ Integer caching happens for common values between -128 and 127

✅ Primitives are more efficient, but wrappers provide nullability and are required for generics/collections

---------

## 6. 📊 Quick Reference Table

| Aspect | Primitives | Wrappers |
|--------|------------|----------|
| **Types** | `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean` | `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double`, `Character`, `Boolean` |
| **Memory** | Stack (4-8 bytes) | Heap (16+ bytes) |
| **Nullability** | Cannot be null | Can be null |
| **Methods** | None | Many utility methods |
| **Performance** | Faster | Slower (5-10x) |
| **Collections** | Not directly usable | Required for generics |
| **Comparison** | `==` for value | `.equals()` for value, `==` for reference |
| **Value Caching** | N/A | Integer cache (-128 to 127) |
| **When to Use** | Performance-critical code, arithmetic | Collections, APIs requiring objects, when null is needed |

---------

## 7. 🎯 Interview Tips

✅ **Know the Integer cache range** (-128 to 127 by default) and explain why `Integer a = 100; Integer b = 100; a == b` returns `true`

✅ **Recognize potential `NullPointerException` cases** when using wrappers in arithmetic operations

✅ **Be prepared to discuss performance implications** of auto-boxing in loops or high-throughput scenarios

✅ **Understand generics limitations** with primitives and why Java collections need wrapper types

✅ **Remember common gotchas** with `==` vs `.equals()` for wrappers

✅ **Consider immutability** - all wrapper classes are immutable (cannot be changed after creation)