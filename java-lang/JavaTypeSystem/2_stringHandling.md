# 🧵 Java String Handling

As a senior Java engineer and interview coach, I'll help you master Java String handling concepts with interview-focused explanations and examples.

---------

## 1. 🔒 String Immutability and String Pool

### String Immutability
- ✅ In Java, String objects are **immutable** – once created, they cannot be changed
- ✅ Any operation that appears to modify a String actually creates a new String object
- ✅ Immutability provides thread safety and security benefits
- ✅ Allows String to be used safely as keys in HashMaps and similar data structures

```java
String name = "Alice";
name.concat(" Smith");    // Creates new String, but doesn't change original
System.out.println(name); // Still prints "Alice"

// Correct approach
name = name.concat(" Smith"); // Reassigns reference to new String
System.out.println(name);     // Now prints "Alice Smith"
```

### String Pool
- ✅ Special memory area in Java Heap for storing unique String literals
- ✅ Helps conserve memory by reusing String objects
- ✅ String literals are automatically interned (added to String Pool)
- ✅ String objects created with `new` are not automatically pooled

```java
// Both references point to same object in String Pool
String s1 = "hello";
String s2 = "hello";
System.out.println(s1 == s2); // true

// Creates new object outside String Pool
String s3 = new String("hello");
System.out.println(s1 == s3); // false

// Explicitly adds String to pool
String s4 = s3.intern();
System.out.println(s1 == s4); // true
```

### String Creation ASCII Diagram
```
String s1 = "hello";    |    String s2 = new String("hello");
                        |
         Heap           |           Heap
     +-----------+      |      +-----------+
     |           |      |      |           |
     |  String   |      |      |  String   |<---- s2 reference
     |   Pool    |      |      |  Object   |
     |           |      |      |  "hello"  |
     |  "hello"  |<---- s1     |           |
     |           |      |      +-----------+
     +-----------+      |
```

### Common Mistakes and Interview Traps
- ❌ Using `==` instead of `.equals()` to compare String values
- ❌ Not understanding memory implications of String concatenation in loops
- ❌ Forgetting that String literals are pooled but `new String()` objects are not
- ❌ Failing to recognize when a new String object is created vs. reused

---------

## 2. 🏗️ StringBuilder vs StringBuffer

### StringBuilder
- ✅ Mutable sequence of characters introduced in Java 5
- ✅ **Not thread-safe** – faster but unsafe for multi-threaded use
- ✅ Use for single-threaded string manipulations
- ✅ Primary methods: `append()`, `insert()`, `delete()`, `replace()`

### StringBuffer
- ✅ Original mutable string class (Java 1.0)
- ✅ **Thread-safe** – all methods are synchronized
- ✅ Slower than StringBuilder due to synchronization overhead
- ✅ Same methods as StringBuilder (they share a common abstract parent)

### Performance Comparison
- 📌 String: Very slow for multiple concatenations (creates many objects)
- 📌 StringBuilder: ~5x faster than StringBuffer for single-threaded apps
- 📌 StringBuffer: Only use when thread safety is required

```java
// BAD: Creates many temporary String objects
String result = "";
for (int i = 0; i < 10000; i++) {
    result += "item " + i;
}

// GOOD: Uses single buffer, much more efficient
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 10000; i++) {
    sb.append("item ").append(i);
}
String result = sb.toString();

// Only use when thread safety is required
StringBuffer sbuf = new StringBuffer();
```

### Best Practices
- ✅ Use StringBuilder by default for concatenation operations
- ✅ Pre-size your StringBuilder when you know approximate size: `new StringBuilder(1000)`
- ✅ Method chaining with StringBuilder makes code cleaner: `sb.append("x").append("y")`
- ✅ Convert to String only when necessary with `toString()`
- ✅ StringBuffer only needed in multi-threaded contexts

---------

## 3. 📝 String Methods and Operations

### Core String Methods
- ✅ **Comparison**: `equals()`, `equalsIgnoreCase()`, `compareTo()`, `startsWith()`, `endsWith()`
- ✅ **Search**: `indexOf()`, `lastIndexOf()`, `contains()`
- ✅ **Extraction**: `substring()`, `split()`, `charAt()`, `toCharArray()`
- ✅ **Modification**: `trim()`, `strip()` (Java 11+), `replace()`, `toLowerCase()`, `toUpperCase()`
- ✅ **Utility**: `length()`, `isEmpty()`, `isBlank()` (Java 11+)

```java
String text = " Hello, World! ";

// Comparison
boolean isEqual = text.equals("Hello");               // false
boolean matches = text.trim().startsWith("Hello");    // true

// Search
int commaPos = text.indexOf(',');                     // 6
boolean hasExclamation = text.contains("!");         // true

// Extraction
String greeting = text.substring(1, 6);               // "Hello"
String[] parts = text.trim().split(", ");            // ["Hello", "World!"]
char firstChar = text.trim().charAt(0);               // 'H'

// Modification
String cleaned = text.trim();                         // "Hello, World!"
String noCommas = text.replace(",", "");             // " Hello World! "
String lower = text.toLowerCase();                    // " hello, world! "

// Utility
int len = text.length();                              // 15
boolean empty = text.isEmpty();                       // false
boolean blank = "   ".isBlank();                      // true (Java 11+)
```

### Modern String Methods (Java 11+)
- ✅ `strip()`, `stripLeading()`, `stripTrailing()` - Unicode-aware trim
- ✅ `isBlank()` - Checks if string is empty or only whitespace
- ✅ `lines()` - Stream of lines from a string
- ✅ `repeat(int)` - Repeats a string n times

```java
// Java 11+ methods
String msg = "  Message with spaces  ";
String stripped = msg.strip();           // "Message with spaces"
String[] lines = "Line1\nLine2".lines().toArray(String[]::new);
String repeated = "abc".repeat(3);       // "abcabcabc"
```

### Common Traps
- ❌ `String.replace()` replaces ALL occurrences (unlike JavaScript)
- ❌ `substring()` used to share character arrays with original (memory leak potential in older Java)
- ❌ Forgetting that `trim()` only removes ASCII whitespace while `strip()` handles all Unicode whitespace
- ❌ Not checking for empty strings before operations

---------

## 4. 🔍 Regular Expressions with String

### String Regex Methods
- ✅ `matches(regex)`: Tests if entire string matches pattern
- ✅ `split(regex)`: Splits string by regex pattern
- ✅ `replaceAll(regex, replacement)`: Replaces all matches
- ✅ `replaceFirst(regex, replacement)`: Replaces first match only

```java
String text = "John Doe: 555-123-4567, jane_smith@example.com";

// Validate phone number format
boolean isPhone = "555-123-4567".matches("\\d{3}-\\d{3}-\\d{4}");  // true

// Split by multiple delimiters
String[] parts = text.split("[,:]");  // Split by comma or colon

// Replace all digits with 'X'
String anonymized = text.replaceAll("\\d", "X");
// Result: "John Doe: XXX-XXX-XXXX, jane_smith@example.com"

// Extract email using replacement
String email = text.replaceAll(".*?([\\w.-]+@[\\w.-]+).*", "$1");
// Result: "jane_smith@example.com"
```

### Pattern and Matcher Classes
- ✅ For complex regex operations, use the `java.util.regex` package
- ✅ More efficient for repeated use of the same pattern
- ✅ Provides access to match indices and groups

```java
import java.util.regex.*;

String text = "Contact us: support@company.com or sales@company.com";

// Create pattern for email (more efficient for reuse)
Pattern emailPattern = Pattern.compile("[\\w.-]+@[\\w.-]+");
Matcher matcher = emailPattern.matcher(text);

// Find all matches
while (matcher.find()) {
    System.out.println("Found email: " + matcher.group());
    System.out.println("Position: " + matcher.start() + "-" + matcher.end());
}
```

### Regex Best Practices
- ✅ Compile patterns once and reuse them for better performance
- ✅ Use capturing groups `()` to extract specific parts of matches
- ✅ Test regex expressions thoroughly with various inputs
- ✅ For complex patterns, build them incrementally
- ✅ Consider using comments mode `(?x)` for complex patterns

### Common Regex Traps
- ❌ Forgetting to escape backslashes in Java strings (`\\` not `\`)
- ❌ Using `matches()` when you meant `find()` (matches requires the ENTIRE string to match)
- ❌ Overly greedy patterns without proper boundaries
- ❌ Excessive backtracking causing performance issues

---------

## 5. 📑 Text Blocks (Java 15+)

### Text Block Features
- ✅ Multi-line string literals with preserved formatting
- ✅ Triple quotes (`"""`) to denote start and end
- ✅ No need for escape sequences for most quotes and newlines
- ✅ Automatic removal of incidental indentation
- ✅ Explicit newline control with `\` at line end

```java
// Traditional multi-line string (before Java 15)
String html = "<html>\n" +
              "    <body>\n" +
              "        <p>Hello, World!</p>\n" +
              "    </body>\n" +
              "</html>";

// Same string as a text block (Java 15+)
String html = """
              <html>
                  <body>
                      <p>Hello, World!</p>
                  </body>
              </html>
              """;

// Control trailing spaces with \ (no newline where \ appears)
String query = """
               SELECT id, name \
               FROM customers \
               WHERE city = 'New York' \
               ORDER BY name
               """;
```

### Text Block Benefits
- ✅ Improved readability for multi-line content (HTML, SQL, JSON)
- ✅ No string concatenation and escape sequences for quotes
- ✅ Preserved indentation relative to closing delimiter
- ✅ Better representation of intended formatting

### Common Misconceptions
- ❌ Text blocks are not raw strings – escape sequences still work inside them
- ❌ Indentation handling can be confusing for beginners
- ❌ The closing `"""` position determines the base indentation
- ❌ Line breaks in the source directly affect the string content

---------

## 6. 📋 Summary

✅ **String Immutability**: Strings in Java are immutable; operations create new String objects; enables efficient reuse via the String Pool

✅ **String Pool**: Special memory area that stores unique String literals to optimize memory usage

✅ **StringBuilder vs StringBuffer**: Use StringBuilder for efficient string manipulation (not thread-safe); StringBuffer when thread safety is required

✅ **String Methods**: Rich set of built-in methods for common operations (comparison, search, extraction, modification)

✅ **Regular Expressions**: String provides regex methods; use Pattern and Matcher classes for complex or repeated operations

✅ **Text Blocks**: Java 15+ feature for clean multi-line strings with preserved formatting

✅ **Best Practices**: Use String.equals() for comparison, StringBuilder for concatenation, and compile regex patterns for reuse

---------

## 7. 📊 Quick Reference Table

| Topic | Key Points | Best Practices | Common Mistakes |
|-------|------------|---------------|----------------|
| **String Immutability** | • Cannot change after creation<br>• Operations create new objects<br>• Thread-safe | • Use StringBuilder for mutations<br>• Reuse String constants | • Excessive concatenation<br>• Modifying in loops |
| **String Pool** | • Memory area for String literals<br>• Automatic for string literals<br>• Manual with .intern() | • Use literals for constants<br>• Consider interning repetitive strings | • Using == for comparison<br>• Creating too many unique strings |
| **StringBuilder** | • Mutable, not thread-safe<br>• ~5x faster than StringBuffer | • Default choice for concatenation<br>• Pre-size when possible | • Not converting to String<br>• Using in multi-threaded code |
| **StringBuffer** | • Mutable, thread-safe<br>• Synchronized methods | • Only use when thread safety needed | • Using when StringBuilder suffices<br>• Thread safety overhead |
| **String Methods** | • Rich built-in functionality<br>• Comparison, search, extraction | • Chaining methods<br>• Check empty/null before operations | • Mixing up methods<br>• Not handling null strings |
| **Regex** | • Built into String class<br>• Pattern/Matcher for complex cases | • Compile patterns once<br>• Test with varied inputs | • Forgetting double backslashes<br>• Using matches() vs find() |
| **Text Blocks** | • Multi-line literals (Java 15+)<br>• Triple quotes \"""...""" | • Use for HTML, SQL, JSON<br>• Control format with \ | • Misunderstanding indentation<br>• Expecting raw strings |

---------

## 8. 🎯 Interview Tips

✅ **For string comparison**: Always explain why `equals()` should be used instead of `==`

✅ **For performance questions**: Be ready to discuss why StringBuilder is better than String concatenation in loops

✅ **For memory management**: Understand how String Pool works and when strings are interned

✅ **For thread safety**: Know when StringBuffer is necessary vs. StringBuilder

✅ **For regex**: Be able to write basic patterns and explain Pattern/Matcher advantages

✅ **For modern Java**: Highlight Text Blocks and modern String methods as improvements

✅ **For coding exercises**: Many interview questions involve string manipulation - practice common operations!