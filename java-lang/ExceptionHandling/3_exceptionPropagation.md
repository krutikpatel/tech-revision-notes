# Java Exception Propagation For Interviews 🧠

## 1. 📤 Understanding Exception Propagation
---------

Exception propagation is the process of passing exceptions up the call stack. When an exception occurs in a method, if not caught, it "bubbles up" to the calling method.

### 1.1 Basic Propagation Flow

```
    main() method
        ↑
    processData() method
        ↑
    readFile() method
        ↑
    Exception occurs here
```

✅ **How Propagation Works**:

```java
public static void main(String[] args) {
    try {
        processData();
    } catch (IOException e) {
        System.err.println("Error in main: " + e.getMessage());
    }
}

public static void processData() throws IOException {
    readFile("data.txt");
}

public static void readFile(String filename) throws IOException {
    // Exception occurs here
    FileReader reader = new FileReader(filename); // FileNotFoundException (subclass of IOException)
    // code to read the file
}
```

📌 **Key Insight**: When an exception occurs in `readFile()`, it "bubbles up" to `processData()` and then to `main()` where it's finally caught.

❌ **Common Misconception**: Java doesn't just terminate the program when an exception occurs - it follows a structured propagation path.


## 2. 🏷️ Throws Clause
---------

The `throws` clause declares which checked exceptions a method might throw, forcing the caller to handle them.

### 2.1 Basic Syntax

```java
public void methodName() throws ExceptionType1, ExceptionType2 {
    // Method body
}
```

### 2.2 When to Use Throws

✅ **Use throws when**:
- You want the calling code to handle the exception
- The method cannot appropriately handle the exception itself
- You're working with checked exceptions

```java
// Method declares it throws a checked exception
public void readConfig() throws IOException {
    Properties props = new Properties();
    props.load(new FileInputStream("config.properties"));
}

// Caller must handle it
public void startApp() {
    try {
        readConfig();
    } catch (IOException e) {
        System.err.println("Could not load configuration: " + e.getMessage());
        // Use default configuration
    }
}
```

### 2.3 Throws Inheritance Rules

📌 **Important Rules**:
- Overriding methods can declare fewer exceptions than the superclass method
- Overriding methods cannot declare broader checked exceptions
- Overriding methods can declare any unchecked exceptions

```java
class Parent {
    public void process() throws IOException, SQLException {
        // Implementation
    }
}

class Child extends Parent {
    // VALID: Declares fewer exceptions
    @Override
    public void process() throws IOException {
        // Implementation
    }
}

class AnotherChild extends Parent {
    // INVALID: Exception not in parent's throws clause
    @Override
    public void process() throws ClassNotFoundException { // Compiler error
        // Implementation
    }
}
```

❌ **Interview Trap**: Assuming you can add new checked exceptions to an overriding method's throws clause.


## 3. 🔄 Rethrowing Exceptions
---------

Rethrowing allows you to catch an exception, perform some action, and then rethrow it to be handled further up the call stack.

### 3.1 Basic Rethrowing

```java
public void processFile(String filename) throws IOException {
    try {
        // Code that might throw IOException
        FileReader reader = new FileReader(filename);
        // Process file...
    } catch (IOException e) {
        // Log the exception
        logger.error("Error processing file: " + filename, e);
        
        // Rethrow the same exception
        throw e;
    }
}
```

### 3.2 Improved Rethrowing (Java 7+)

Before Java 7, rethrowing required you to declare all possible exception types in the catch block in your method's throws clause.

```java
// Pre-Java 7
public void processData() throws IOException, SQLException {
    try {
        // Code that might throw various exceptions
    } catch (Exception e) {
        // Log the error
        logger.error("Error processing data", e);
        
        // Must declare all potential types from the try block
        throw e;  // Compiler requires throws IOException, SQLException
    }
}
```

Java 7 improved this with "precise rethrow":

```java
// Java 7+
public void processData() throws IOException, SQLException {
    try {
        // Code that might throw various exceptions
    } catch (Exception e) {  // More general type in catch
        // Log the error
        logger.error("Error processing data", e);
        
        // Java 7+ can determine the actual exception types
        throw e;  // Only IOException and SQLException need to be declared
    }
}
```

📌 **Interview Insight**: Java 7+ will analyze which checked exceptions can actually reach the throw statement and only require those in the method's throws clause.


## 4. ⛓️ Exception Chaining (Exception Cause)
---------

Exception chaining preserves the original exception as the "cause" when throwing a new exception.

### 4.1 Basic Exception Chaining

```java
try {
    // Lower-level operation
    dbConnection.executeQuery("SELECT * FROM users");
} catch (SQLException e) {
    // Create a higher-level exception with the original as the cause
    throw new ServiceException("User data unavailable", e);
}
```

### 4.2 Accessing the Cause

```java
try {
    userService.getUsers();
} catch (ServiceException e) {
    System.err.println("Service error: " + e.getMessage());
    
    // Access the original cause
    Throwable cause = e.getCause();
    if (cause instanceof SQLException) {
        SQLException sqlEx = (SQLException) cause;
        System.err.println("SQL Error code: " + sqlEx.getErrorCode());
    }
}
```

### 4.3 Chaining Multiple Levels

```java
try {
    // Database operation
} catch (SQLException e) {
    try {
        // Try to recover
    } catch (RecoveryException re) {
        // Chain both exceptions
        ServiceException serviceEx = new ServiceException("Service failed", re);
        serviceEx.addSuppressed(e);  // Add the original as suppressed
        throw serviceEx;
    }
}
```

✅ **Best Practice**: Always pass the original exception as the cause when wrapping exceptions to preserve the full context.


## 5. 🔇 Exception Suppression
---------

Java 7+ introduced suppressed exceptions, primarily for handling multiple exceptions in try-with-resources.

### 5.1 Understanding Suppressed Exceptions

When a primary exception and additional exceptions occur, the additional ones get "suppressed" but are still accessible.

```java
class Resource implements AutoCloseable {
    @Override
    public void close() throws Exception {
        throw new IllegalStateException("Error during close");
    }
}

public void processResource() {
    try (Resource resource = new Resource()) {
        // This exception becomes the primary exception
        throw new RuntimeException("Error during processing");
        
        // The close() exception will be suppressed
    } catch (Exception e) {
        System.err.println("Primary: " + e.getMessage());
        
        // Access suppressed exceptions
        Throwable[] suppressed = e.getSuppressed();
        for (Throwable t : suppressed) {
            System.err.println("Suppressed: " + t.getMessage());
        }
    }
}
```

### 5.2 Manually Adding Suppressed Exceptions

```java
public void complexOperation() {
    Exception primaryException = null;
    
    try {
        // Main operation
    } catch (Exception e) {
        primaryException = e;
    }
    
    try {
        // Cleanup operation
    } catch (Exception e) {
        if (primaryException != null) {
            // Add as suppressed to the main exception
            primaryException.addSuppressed(e);
        } else {
            // No primary exception, so this becomes primary
            primaryException = e;
        }
    }
    
    // If any exception occurred, throw it
    if (primaryException != null) {
        throw primaryException;
    }
}
```

📌 **Interview Insight**: Suppressed exceptions are often overlooked but are crucial for preserving all error information, especially in resource cleanup scenarios.


## 6. 🛠️ Exception Propagation Patterns
---------

### 6.1 Layer-Specific Exception Translation

```java
// Data Access Layer
public User findUser(int id) throws DAOException {
    try {
        // Database operations
        return jdbcTemplate.queryForObject("SELECT * FROM users WHERE id = ?", User.class, id);
    } catch (DataAccessException e) {
        throw new DAOException("Failed to find user with ID: " + id, e);
    }
}

// Service Layer
public UserDTO getUserDetails(int id) throws ServiceException {
    try {
        User user = userDAO.findUser(id);
        return convertToDTO(user);
    } catch (DAOException e) {
        throw new ServiceException("User details unavailable", e);
    } catch (MappingException e) {
        throw new ServiceException("Invalid user data format", e);
    }
}

// API Layer
@GetMapping("/users/{id}")
public ResponseEntity<UserDTO> getUser(@PathVariable int id) {
    try {
        UserDTO user = userService.getUserDetails(id);
        return ResponseEntity.ok(user);
    } catch (ServiceException e) {
        logger.error("Error retrieving user", e);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body(null);
    }
}
```

✅ **Benefits**:
- Each layer handles exceptions at appropriate abstraction level
- Original cause is preserved through chaining
- API clients receive meaningful error responses without internal details

### 6.2 Partial Handling and Rethrowing

```java
public void processDocument(Document doc) throws DocumentProcessingException {
    try {
        // Process document
        validateDocument(doc);
        transformDocument(doc);
        saveDocument(doc);
    } catch (ValidationException e) {
        // Handle validation specifically
        notifyUser("Document validation failed: " + e.getMessage());
        
        // But still rethrow as processing failure
        throw new DocumentProcessingException("Invalid document", e);
    } catch (IOException e) {
        // Log storage issues
        logger.error("Storage error for document: " + doc.getId(), e);
        throw new DocumentProcessingException("Document storage failed", e);
    }
}
```


## 7. ⚠️ Common Mistakes and Best Practices
---------

### 7.1 Common Mistakes

❌ **Losing the Original Exception**

```java
// WRONG: Original exception lost
try {
    // Operation
} catch (SQLException e) {
    // Original exception lost!
    throw new ServiceException("Database error");
}

// RIGHT: Chain the exception
try {
    // Operation
} catch (SQLException e) {
    // Original cause preserved
    throw new ServiceException("Database error", e);
}
```

❌ **Catching Exception Too Generally**

```java
// WRONG: Too broad
try {
    // Operations that may throw different exceptions
} catch (Exception e) {
    // Generic handling for all exceptions
}

// RIGHT: Specific handling
try {
    // Operations
} catch (IOException e) {
    // Handle IO problems
} catch (SQLException e) {
    // Handle database problems
} catch (Exception e) {
    // Handle other unexpected exceptions
}
```

❌ **Neglecting Exception Hierarchy in throws Clause**

```java
// WRONG: Redundant
public void method() throws IOException, FileNotFoundException {
    // Method implementation
}

// RIGHT: FileNotFoundException is a subclass of IOException
public void method() throws IOException {
    // Method implementation
}
```

### 7.2 Best Practices

✅ **Document Exception Behavior**

```java
/**
 * Processes the user record.
 * 
 * @param userId The user ID to process
 * @throws DataNotFoundException If the user cannot be found
 * @throws SecurityException If the current user lacks permission
 * @throws ServiceException If a system error occurs
 */
public void processUser(int userId) throws DataNotFoundException, 
                                         SecurityException, 
                                         ServiceException {
    // Implementation
}
```

✅ **Create Custom Exception Hierarchies**

```java
// Base application exception
public class AppException extends Exception {
    public AppException(String message) { super(message); }
    public AppException(String message, Throwable cause) { super(message, cause); }
}

// Specific exception types
public class DataException extends AppException {
    public DataException(String message) { super(message); }
    public DataException(String message, Throwable cause) { super(message, cause); }
}

public class SecurityException extends AppException {
    public SecurityException(String message) { super(message); }
    public SecurityException(String message, Throwable cause) { super(message, cause); }
}
```

✅ **Balance Checked vs. Unchecked Exceptions**

```java
// Checked - for recoverable conditions
public void saveData(Data data) throws PersistenceException {
    // Implementation
}

// Unchecked - for programming errors
public void processValue(int value) {
    if (value < 0) {
        throw new IllegalArgumentException("Value cannot be negative");
    }
    // Implementation
}
```

✅ **Only Throw Exceptions That Make Sense**

```java
// WRONG: Throws unrelated exception
public User findById(int id) throws SQLException, NullPointerException {
    // Implementation
}

// RIGHT: Only throw exceptions that could actually occur
public User findById(int id) throws SQLException {
    // Implementation
}
```


## 8. 🎯 Interview Questions and Answers
---------

### 8.1 Common Interview Questions

📌 **Q: What's the difference between `throw` and `throws`?**
- A: `throw` is used to explicitly throw an exception within a method, while `throws` is used in the method signature to declare exceptions that the method might throw.

📌 **Q: Can a method declare that it throws RuntimeException?**
- A: Yes, though it's not required. Runtime exceptions don't need to be declared in the throws clause, but you can include them for documentation purposes.

📌 **Q: What happens if a finally block throws an exception while there's an active exception from the try block?**
- A: The exception from the finally block replaces the original exception, which gets lost unless it was explicitly saved.

📌 **Q: How can you preserve multiple exceptions in Java?**
- A: Use exception chaining for the primary cause and addSuppressed() for additional exceptions.

### 8.2 Scenario Questions

📌 **Scenario: How would you design exception handling for a layered application?**
- A: Each layer should have its own exception types. Lower-level exceptions should be caught and wrapped in layer-appropriate exceptions while preserving the original cause. This creates a clean separation of concerns while maintaining detailed error information.

📌 **Scenario: How would you handle connection exceptions in a database operation that needs transaction rollback?**
- A: 
```java
Connection conn = null;
try {
    conn = dataSource.getConnection();
    conn.setAutoCommit(false);
    
    // Perform multiple operations
    
    conn.commit();
} catch (SQLException e) {
    if (conn != null) {
        try {
            conn.rollback();
        } catch (SQLException rollbackEx) {
            e.addSuppressed(rollbackEx);
        }
    }
    throw new DataAccessException("Transaction failed", e);
} finally {
    if (conn != null) {
        try {
            conn.close();
        } catch (SQLException closeEx) {
            // Log but don't throw to avoid masking original exception
            logger.error("Error closing connection", closeEx);
        }
    }
}
```


## 9. 📝 Summary
---------

✅ **Key Points**:

- **Exception Propagation** is how exceptions travel up the call stack if not caught
- **Throws Clause** declares checked exceptions a method may throw, forcing callers to handle them
- **Rethrowing Exceptions** allows logging or partial handling before passing exceptions up
- **Exception Chaining** preserves the original exception as the cause of a higher-level exception
- **Exception Suppression** stores additional exceptions that occur during exception handling
- **Best Practices** include preserving original exceptions, creating meaningful hierarchies, and providing clear documentation


## 10. 📊 Quick Reference Table
---------

| Concept | Purpose | Syntax | Key Points |
|---------|---------|--------|------------|
| **Throws Clause** | Declare checked exceptions | `void method() throws ExType1, ExType2` | - Required for checked exceptions<br>- Overriding methods can declare fewer exceptions<br>- Cannot add new checked exceptions in subclasses |
| **Rethrowing** | Pass exception up after partial handling | `catch (Ex e) { log(e); throw e; }` | - Java 7+ has "precise rethrow"<br>- Useful for logging before propagation<br>- Preserves original stack trace |
| **Exception Chaining** | Link cause to new exception | `throw new HigherEx("msg", originalEx)` | - Preserves original cause<br>- Access with getCause()<br>- Essential for proper error context |
| **Exception Suppression** | Store multiple exceptions | `primaryEx.addSuppressed(secondaryEx)` | - Used with try-with-resources<br>- Access with getSuppressed()<br>- Prevents information loss |
| **Layer-Specific Exceptions** | Map exceptions to abstraction level | `catch(LowEx e) { throw new HighEx(e) }` | - Each layer has own exception types<br>- Hides implementation details<br>- Maintains cause chain |

Remember that well-designed exception handling should provide clear error information, preserve the error context through proper chaining, and maintain appropriate abstraction levels through exception translation.