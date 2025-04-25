# Java Functional Interfaces: Interview-Ready Guide 🚀

I'll help you master Java Functional Interfaces with a comprehensive yet concise guide perfect for interview preparation. Let's dive in!

---------

## 1. 📋 Functional Interfaces Basics

A functional interface is an interface with exactly one abstract method. They are the foundation of Java's functional programming capabilities.

```java
@FunctionalInterface  // Optional but recommended annotation
interface SimpleFunction {
    void execute();   // Single abstract method
}
```

The `@FunctionalInterface` annotation is optional but recommended. It helps the compiler validate that the interface has exactly one abstract method and provides better documentation.

✅ **Key Point**: A functional interface can have any number of default or static methods, but exactly one abstract method.

📌 **Interview Insight**: The compiler treats any interface with a single abstract method as a functional interface, even without the annotation.

---------

## 2. 🧩 Built-in Functional Interfaces

Java provides several built-in functional interfaces in the `java.util.function` package. Let's explore the most important ones:

### Function<T, R>

Represents a function that accepts one argument of type T and produces a result of type R.

```java
Function<String, Integer> stringLength = s -> s.length();
Integer length = stringLength.apply("Hello"); // Returns 5
```

### Consumer<T>

Represents an operation that accepts a single input argument of type T and returns no result.

```java
Consumer<String> printer = s -> System.out.println("Consuming: " + s);
printer.accept("Hello"); // Prints "Consuming: Hello"
```

### Supplier<T>

Represents a supplier of results of type T, with no input arguments.

```java
Supplier<LocalDate> today = () -> LocalDate.now();
LocalDate date = today.get(); // Returns current date
```

### Predicate<T>

Represents a predicate (boolean-valued function) of one argument of type T.

```java
Predicate<String> isEmpty = s -> s.isEmpty();
boolean result = isEmpty.test(""); // Returns true
```

### BiFunction<T, U, R>

Represents a function that accepts two arguments and produces a result.

```java
BiFunction<String, String, Integer> totalLength = 
    (s1, s2) -> s1.length() + s2.length();
Integer length = totalLength.apply("Hello", "World"); // Returns 10
```

Other useful interfaces include:
- `BiConsumer<T, U>`: Takes two inputs, returns nothing
- `BiPredicate<T, U>`: Takes two inputs, returns boolean
- `UnaryOperator<T>`: Special case of Function where input and output types are the same
- `BinaryOperator<T>`: Special case of BiFunction where all types are the same

📌 **Interview Insight**: Know which interface to use for a given scenario based on input and output requirements.

❌ **Common Mistake**: Creating custom functional interfaces when standard ones would suffice.

---------

## 3. 🔧 Primitive Specializations

To avoid boxing/unboxing overhead with primitives, Java provides specialized versions of functional interfaces for primitive types:

### Function Specializations

```java
// Instead of Function<Integer, Double>
IntToDoubleFunction converter = i -> i * 1.5;
double result = converter.applyAsDouble(5); // Returns 7.5

// Other examples
IntFunction<String> intToString = i -> String.valueOf(i);
ToIntFunction<String> stringToInt = s -> Integer.parseInt(s);
```

### Consumer Specializations

```java
IntConsumer intPrinter = i -> System.out.println(i);
intPrinter.accept(42); // No boxing happens

LongConsumer longPrinter = l -> System.out.println(l);
DoubleConsumer doublePrinter = d -> System.out.println(d);
```

### Supplier Specializations

```java
IntSupplier randomInt = () -> new Random().nextInt(100);
int value = randomInt.getAsInt(); // Returns random int 0-99

LongSupplier timestamp = System::currentTimeMillis;
BooleanSupplier isWeekend = () -> {
    int day = Calendar.getInstance().get(Calendar.DAY_OF_WEEK);
    return day == Calendar.SATURDAY || day == Calendar.SUNDAY;
};
```

### Predicate Specializations

```java
IntPredicate isEven = i -> i % 2 == 0;
boolean result = isEven.test(4); // Returns true

LongPredicate isPositive = l -> l > 0;
DoublePredicate isInRange = d -> d >= 0 && d <= 1.0;
```

### Bi-Type Specializations

```java
// Instead of BiFunction<Integer, Integer, Integer>
IntBinaryOperator sum = (a, b) -> a + b;
int result = sum.applyAsInt(5, 3); // Returns 8

// Others
LongBinaryOperator longMultiplier = (a, b) -> a * b;
ObjIntConsumer<String> repeat = (str, count) -> {
    for (int i = 0; i < count; i++) {
        System.out.println(str);
    }
};
```

✅ **Best Practice**: Use primitive specializations when working with primitive values to avoid boxing/unboxing overhead.

📌 **Interview Insight**: Be ready to explain performance benefits of primitive specializations (avoiding autoboxing).

---------

## 4. ⛓️ Function Chaining

Many functional interfaces provide default methods for combining operations:

### Function Chaining with andThen() and compose()

```java
Function<String, String> toUpperCase = String::toUpperCase;
Function<String, String> trim = String::trim;

// andThen: First apply "this" function, then the "after" function
Function<String, String> trimThenUpperCase = trim.andThen(toUpperCase);
String result1 = trimThenUpperCase.apply("  hello  "); // "HELLO"

// compose: First apply the "before" function, then "this" function
Function<String, String> upperCaseThenTrim = toUpperCase.compose(trim);
String result2 = upperCaseThenTrim.apply("  hello  "); // "HELLO"
```

The difference between `andThen()` and `compose()` is the order of operations:
```
For andThen: result = g(f(x))
For compose: result = f(g(x))
```

### Predicate Chaining with and(), or(), negate()

```java
Predicate<String> isNotEmpty = s -> !s.isEmpty();
Predicate<String> isLengthGreaterThan5 = s -> s.length() > 5;

// Combine with logical AND
Predicate<String> isValidString = isNotEmpty.and(isLengthGreaterThan5);
boolean valid = isValidString.test("Hello World"); // true

// Combine with logical OR
Predicate<String> isAcceptable = isNotEmpty.or(isLengthGreaterThan5);
boolean acceptable = isAcceptable.test("Hi"); // true (not empty)

// Negate a predicate
Predicate<String> isEmpty = isNotEmpty.negate();
boolean empty = isEmpty.test(""); // true
```

### Consumer Chaining with andThen()

```java
Consumer<String> logger = s -> System.out.println("Logging: " + s);
Consumer<String> emailSender = s -> System.out.println("Sending email about: " + s);

// Chain consumers
Consumer<String> logAndEmail = logger.andThen(emailSender);
logAndEmail.accept("New user registered"); 
// Prints:
// Logging: New user registered
// Sending email about: New user registered
```

❌ **Common Mistake**: Confusing the execution order of `andThen()` vs `compose()`.

📌 **Interview Insight**: Chaining operations with functional interfaces is similar to the decorator pattern.

```
// ASCII Diagram: andThen vs compose
andThen:  [Input] --> [First Function] --> [Second Function] --> [Output]
compose:  [Input] --> [Second Function] --> [First Function] --> [Output]
```

---------

## 5. 🛠️ Custom Functional Interfaces

When built-in interfaces don't fit your needs, you can create custom ones:

```java
@FunctionalInterface
interface TriFunction<T, U, V, R> {
    R apply(T t, U u, V v);
    
    // You can add default methods
    default <S> TriFunction<T, U, V, S> andThen(Function<? super R, ? extends S> after) {
        Objects.requireNonNull(after);
        return (T t, U u, V v) -> after.apply(apply(t, u, v));
    }
}

// Usage
TriFunction<Integer, Integer, Integer, Integer> sum3 = (a, b, c) -> a + b + c;
int result = sum3.apply(1, 2, 3); // Returns 6

// Using the andThen method
TriFunction<Integer, Integer, Integer, String> sumAsString = 
    sum3.andThen(String::valueOf);
String strResult = sumAsString.apply(1, 2, 3); // Returns "6"
```

### When to Create Custom Functional Interfaces

1. When you need a specific number of parameters not covered by built-in interfaces
2. When you need a specific combination of primitive and object parameters
3. When the semantic meaning is important for code clarity

✅ **Best Practice**: Add clear Javadoc to custom functional interfaces explaining their purpose.

```java
/**
 * Represents a function that accepts three arguments and produces a result.
 * This is the three-arity specialization of {@link Function}.
 *
 * @param <T> the type of the first argument
 * @param <U> the type of the second argument
 * @param <V> the type of the third argument
 * @param <R> the type of the result
 */
@FunctionalInterface
interface TriFunction<T, U, V, R> {
    // ...
}
```

📌 **Interview Insight**: Be prepared to explain when to use custom functional interfaces vs. built-in ones.

---------

## 6. 🎯 Practical Examples

Let's see some practical examples that combine different aspects:

### Data Processing Pipeline

```java
public class DataProcessor {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("John", "Alice", "", "Bob", "Charlie", "");
        
        // Define operations
        Predicate<String> isNotEmpty = s -> !s.isEmpty();
        Function<String, String> toUpperCase = String::toUpperCase;
        Consumer<String> printer = System.out::println;
        
        // Process data
        names.stream()
            .filter(isNotEmpty)
            .map(toUpperCase)
            .forEach(printer);
    }
}
```

### Complex Function Composition

```java
public class FunctionComposition {
    public static void main(String[] args) {
        // Parse string to int, double it, convert back to string
        Function<String, Integer> parser = Integer::parseInt;
        Function<Integer, Integer> doubler = x -> x * 2;
        Function<Integer, String> formatter = String::valueOf;
        
        // Compose these functions
        Function<String, String> stringProcessor = parser
            .andThen(doubler)
            .andThen(formatter);
            
        String result = stringProcessor.apply("5"); // "10"
        
        // Alternatively with compose (reverse order)
        Function<String, String> composedProcessor = formatter
            .compose(doubler)
            .compose(parser);
            
        String result2 = composedProcessor.apply("5"); // "10"
    }
}
```

### Custom Validation Logic

```java
public class Validator {
    public static void main(String[] args) {
        // Email validation
        Predicate<String> hasAtSign = s -> s.contains("@");
        Predicate<String> hasDomain = s -> s.matches(".*\\.\\w+$");
        Predicate<String> isNotEmpty = s -> !s.isEmpty();
        
        // Combine validation rules
        Predicate<String> isValidEmail = isNotEmpty
            .and(hasAtSign)
            .and(hasDomain);
            
        // Test emails
        System.out.println(isValidEmail.test("user@domain.com")); // true
        System.out.println(isValidEmail.test("invalid-email")); // false
    }
}
```

---------

## 7. ❌ Common Mistakes & Traps

### 1. Overusing Custom Functional Interfaces

```java
// Unnecessary custom interface
@FunctionalInterface
interface StringTransformer {
    String transform(String input);
}

// Better to use the standard Function
Function<String, String> transformer = s -> s.toUpperCase();
```

### 2. Not Using Primitive Specializations

```java
// Unnecessary boxing/unboxing
Function<Integer, Integer> square = x -> x * x;
int result = square.apply(5); // Boxing/unboxing happens

// Better approach
IntUnaryOperator efficientSquare = x -> x * x;
int efficientResult = efficientSquare.applyAsInt(5); // No boxing
```

### 3. Confusion with Function Composition

```java
Function<String, Integer> strToInt = Integer::parseInt;
Function<Integer, Double> intToDouble = i -> i * 1.5;

// Wrong expectation
Function<String, Double> composed = strToInt.compose(intToDouble); // Wrong order!
// This won't work because intToDouble expects Integer but gets String

// Correct approach
Function<String, Double> correct = strToInt.andThen(intToDouble);
// or
Function<String, Double> alsoCorrect = intToDouble.compose(strToInt);
```

### 4. Exception Handling in Lambdas

```java
// This might throw exceptions
Function<String, Integer> unsafeParser = Integer::parseInt;

// Better to handle exceptions
Function<String, Integer> safeParser = s -> {
    try {
        return Integer.parseInt(s);
    } catch (NumberFormatException e) {
        return 0; // Default value
    }
};
```

📌 **Interview Insight**: Unlike checked exceptions, runtime exceptions don't need to be declared in the functional interface method.

---------

## 8. ✅ Best Practices

1. **Use Standard Interfaces When Possible**
   - Prefer built-in interfaces over custom ones for better interoperability

2. **Use Primitive Specializations for Performance**
   - When working with primitives, use specialized interfaces to avoid boxing/unboxing

3. **Keep Lambda Expressions Simple**
   - For complex operations, use method references or extract to named methods

4. **Make Methods that Return Functional Interfaces**
   - Create factory methods that return preconfigured functional interfaces

   ```java
   public static Predicate<String> lengthGreaterThan(int minLength) {
       return s -> s.length() > minLength;
   }
   ```

5. **Annotate Custom Functional Interfaces**
   - Always use `@FunctionalInterface` for better documentation and compile-time checking

6. **Use Default Methods for Utility Operations**
   - Provide useful default methods in custom functional interfaces similar to the standard ones

7. **Handle Exceptions Properly**
   - Wrap lambdas that might throw exceptions in try-catch blocks

8. **Consider Composition over Raw Implementation**
   - Build complex operations by combining simpler ones with andThen(), compose(), etc.

---------

## 9. 📊 Summary (Super Quick Revision)

Java Functional Interfaces form the foundation of functional programming in Java. They are interfaces with exactly one abstract method, allowing them to be implemented using lambda expressions. Java provides many built-in interfaces like Function, Consumer, Supplier, and Predicate in the java.util.function package. For performance, primitive specializations like IntFunction, LongConsumer are available. Functions can be chained using methods like andThen(), compose(), and(), or(), and negate(). When necessary, custom functional interfaces can be created with the @FunctionalInterface annotation.

---------

## 10. 📑 Summary Table

| Interface Category | Main Types | Method Name | Primitive Versions | Chaining Methods |
|-------------------|------------|------------|-------------------|-----------------|
| **Function** | Function<T,R> | apply() | IntFunction, LongFunction, etc. | andThen(), compose() |
| **Consumer** | Consumer<T> | accept() | IntConsumer, LongConsumer, etc. | andThen() |
| **Supplier** | Supplier<T> | get() | IntSupplier, BooleanSupplier, etc. | None |
| **Predicate** | Predicate<T> | test() | IntPredicate, DoublePredicate, etc. | and(), or(), negate() |
| **BiFunction** | BiFunction<T,U,R> | apply() | ToIntBiFunction, etc. | andThen() |
| **Operators** | UnaryOperator<T>, BinaryOperator<T> | apply() | IntUnaryOperator, etc. | Same as Function |

### Common Interface Methods:

| Interface | Method | Return Type | Example |
|-----------|--------|------------|---------|
| Function<T,R> | apply(T t) | R | `Function<String, Integer> f = s -> s.length();` |
| Consumer<T> | accept(T t) | void | `Consumer<String> c = s -> System.out.println(s);` |
| Supplier<T> | get() | T | `Supplier<String> s = () -> "Hello";` |
| Predicate<T> | test(T t) | boolean | `Predicate<String> p = s -> s.isEmpty();` |
| BiFunction<T,U,R> | apply(T t, U u) | R | `BiFunction<String, String, String> bf = (s1, s2) -> s1 + s2;` |

### Chaining Methods:

| Method | Interface | Purpose | Example |
|--------|-----------|---------|---------|
| andThen() | Function, Consumer | Execute operations sequentially | `function1.andThen(function2)` |
| compose() | Function | Execute operations in reverse order | `function1.compose(function2)` |
| and() | Predicate | Logical AND | `predicate1.and(predicate2)` |
| or() | Predicate | Logical OR | `predicate1.or(predicate2)` |
| negate() | Predicate | Logical NOT | `predicate.negate()` |

I hope this guide helps you prepare effectively for your Java interviews! Good luck! 🍀