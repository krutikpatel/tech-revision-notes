# Java Custom Exceptions for Interviews 🧠

## 1. 🧩 Creating Custom Exception Classes
---------

Custom exceptions allow you to create application-specific exception types that clearly communicate what went wrong in your code.

### 1.1 Basic Custom Exception

The simplest way to create a custom exception is to extend either `Exception` (for checked exceptions) or `RuntimeException` (for unchecked exceptions).

```java
// Basic checked exception
public class ResourceNotFoundException extends Exception {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

// Basic unchecked exception
public class InvalidOperationException extends RuntimeException {
    public InvalidOperationException(String message) {
        super(message);
    }
}
```

✅ **When to create custom exceptions**:
- When standard Java exceptions don't adequately describe your error condition
- To provide domain-specific error types that align with your business logic
- To make error handling and debugging more intuitive

### 1.2 Adding Constructors

A well-designed custom exception should provide multiple constructors for flexibility:

```java
public class OrderProcessingException extends Exception {
    private String orderId;

    // Basic constructor
    public OrderProcessingException(String message) {
        super(message);
    }

    // Constructor with cause
    public OrderProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
    
    // Constructor with additional context
    public OrderProcessingException(String message, String orderId) {
        super(message);
        this.orderId = orderId;
    }
    
    // Constructor with cause and context
    public OrderProcessingException(String message, Throwable cause, String orderId) {
        super(message, cause);
        this.orderId = orderId;
    }
    
    // Getter for additional context
    public String getOrderId() {
        return orderId;
    }
}
```

📌 **Interview Insight**: Including constructors that take a cause parameter allows for proper exception chaining, which is crucial for debugging.

### 1.3 Adding Custom Data and Methods

Custom exceptions can include additional data and methods to provide context about the error:

```java
public class ValidationException extends Exception {
    private Map<String, String> validationErrors;
    
    public ValidationException(String message) {
        super(message);
        this.validationErrors = new HashMap<>();
    }
    
    public ValidationException(String message, Map<String, String> validationErrors) {
        super(message);
        this.validationErrors = validationErrors;
    }
    
    public void addValidationError(String field, String errorMessage) {
        validationErrors.put(field, errorMessage);
    }
    
    public Map<String, String> getValidationErrors() {
        return Collections.unmodifiableMap(validationErrors);
    }
    
    public boolean hasErrors() {
        return !validationErrors.isEmpty();
    }
}
```

✅ **Benefits of custom data**:
- Provides detailed context about the error
- Enables more specific error handling
- Allows for better error reporting to users

❌ **Common Mistake**: Not making the returned map unmodifiable, which could lead to unexpected modifications.


## 2. 🏗️ Best Practices for Exception Hierarchy
---------

A well-designed exception hierarchy improves code maintainability and makes error handling more intuitive.

### 2.1 Creating a Base Exception

Start with a base exception for your application or module:

```java
// Base application exception
public class ApplicationException extends Exception {
    public ApplicationException(String message) {
        super(message);
    }
    
    public ApplicationException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### 2.2 Building an Exception Hierarchy

Create specialized exceptions that extend your base exception:

```java
// Layer-specific exceptions
public class DataAccessException extends ApplicationException {
    public DataAccessException(String message) {
        super(message);
    }
    
    public DataAccessException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class ServiceException extends ApplicationException {
    public ServiceException(String message) {
        super(message);
    }
    
    public ServiceException(String message, Throwable cause) {
        super(message, cause);
    }
}

// More specific exceptions
public class EntityNotFoundException extends DataAccessException {
    private String entityType;
    private String entityId;
    
    public EntityNotFoundException(String entityType, String entityId) {
        super(entityType + " with ID " + entityId + " not found");
        this.entityType = entityType;
        this.entityId = entityId;
    }
    
    // Getters for entityType and entityId
}
```

Here's a visual representation of this hierarchy:

```
          ApplicationException
           /               \
DataAccessException    ServiceException
        |
EntityNotFoundException
```

### 2.3 Organizing by Domain or Layer

There are two main approaches to organizing exception hierarchies:

✅ **Layer-based approach**:
- Exceptions aligned with application layers (data, service, presentation)
- Example: `DataAccessException`, `ServiceException`, `ApiException`

```java
// Layer-based hierarchy
ApplicationException
  ├── DataAccessException
  │     ├── DatabaseConnectionException
  │     └── QueryExecutionException
  ├── ServiceException
  │     ├── ValidationException
  │     └── BusinessRuleException
  └── ApiException
        ├── InvalidRequestException
        └── ResourceNotFoundException
```

✅ **Domain-based approach**:
- Exceptions aligned with business domains
- Example: `OrderException`, `UserException`, `PaymentException`

```java
// Domain-based hierarchy
ApplicationException
  ├── OrderException
  │     ├── OrderNotFoundException
  │     └── OrderAlreadyProcessedException
  ├── UserException
  │     ├── UserNotFoundException
  │     └── AuthenticationException
  └── PaymentException
        ├── PaymentDeclinedException
        └── InsufficientFundsException
```

📌 **Interview Insight**: The choice between layer-based and domain-based hierarchies depends on your application's complexity and how you want to handle exceptions. Layer-based is common in larger applications, while domain-based may be more intuitive for domain-driven designs.

### 2.4 Exception Translation Pattern

Use exception translation to convert low-level exceptions to your custom hierarchy:

```java
public User findUserById(String userId) throws UserNotFoundException {
    try {
        return userRepository.findById(userId);
    } catch (SQLException e) {
        // Translate low-level exception to your custom hierarchy
        throw new UserNotFoundException("User with ID " + userId + " not found", e);
    }
}
```

✅ **Benefits of exception translation**:
- Hides implementation details from higher layers
- Provides more meaningful exceptions for your application domain
- Maintains the original cause for debugging


## 3. 🤔 When to Use Checked vs Unchecked Exceptions
---------

The decision to make your custom exception checked or unchecked is critical and impacts how clients interact with your code.

### 3.1 Checked Exceptions (Extend Exception)

Checked exceptions are verified at compile time and must be either caught or declared.

```java
// Checked exception
public class FileFormatException extends Exception {
    public FileFormatException(String message) {
        super(message);
    }
}

// Method using checked exception
public void processFile(String path) throws FileFormatException {
    if (!isValidFormat(path)) {
        throw new FileFormatException("Invalid file format: " + path);
    }
    // Process file...
}

// Caller must handle the exception
public void importData() {
    try {
        processFile("data.csv");
    } catch (FileFormatException e) {
        System.err.println("Import failed: " + e.getMessage());
    }
}
```

✅ **Use checked exceptions when**:
- The exception represents a condition that the caller might reasonably recover from
- You want to force the caller to acknowledge and handle the exception
- The condition is expected in normal operation (e.g., file not found)
- The exception represents a business rule violation that can be addressed

📌 **Examples**: `FileNotFoundException`, `SQLException`, `ParseException`

### 3.2 Unchecked Exceptions (Extend RuntimeException)

Unchecked exceptions don't require explicit handling and typically represent programming errors.

```java
// Unchecked exception
public class InvalidInputException extends RuntimeException {
    public InvalidInputException(String message) {
        super(message);
    }
}

// Method using unchecked exception
public void validateInput(String input) {
    if (input == null || input.isEmpty()) {
        throw new InvalidInputException("Input cannot be null or empty");
    }
    // Process input...
}

// Caller can handle it, but isn't required to
public void processUserInput(String input) {
    try {
        validateInput(input);
        // Process valid input...
    } catch (InvalidInputException e) {
        // Handle invalid input...
    }
}
```

✅ **Use unchecked exceptions when**:
- The exception represents a programming error that should be fixed, not handled
- Recovery is unlikely or impossible
- Forcing every caller to handle the exception would create unnecessary boilerplate
- The exception indicates a precondition violation (e.g., null parameter)

📌 **Examples**: `NullPointerException`, `IllegalArgumentException`, `UnsupportedOperationException`

### 3.3 Decision Guidelines

Ask these questions to decide whether to make your exception checked or unchecked:

1. **Can the caller reasonably recover from this exception?**
   - Yes → Checked
   - No → Unchecked

2. **Is this exception caused by a programming error?**
   - Yes → Unchecked
   - No → Checked

3. **Would requiring handling add value or just boilerplate?**
   - Value → Checked
   - Boilerplate → Unchecked

❌ **Common Mistake**: Making all custom exceptions checked because it seems "safer", leading to catch blocks that simply log and rethrow, or worse, empty catch blocks.

```java
// BAD: Overuse of checked exceptions
try {
    someOperation();
} catch (MyCheckedException e) {
    // Empty catch block or just logging
    logger.error("Error", e);
}
```


## 4. 🌟 Best Practices for Custom Exceptions
---------

### 4.1 Naming Conventions

✅ **Follow these naming conventions**:
- End class names with "Exception"
- Use descriptive names that indicate the error condition
- Use positive phrasing (e.g., `InvalidArgumentException` instead of `ArgumentNotValidException`)

```java
// GOOD: Clear, descriptive names
ConnectionPoolExhaustedException
UsernameAlreadyExistsException
PaymentDeclinedException

// BAD: Vague or poorly named
DataErrorException
ProcessingFailedException
BadArgumentException
```

### 4.2 Exception Message Best Practices

Create informative, actionable exception messages:

```java
// BAD: Vague message
throw new OrderException("Error processing order");

// GOOD: Detailed, actionable message
throw new OrderException("Order #12345 cannot be shipped: payment status is PENDING");
```

✅ **Exception message guidelines**:
- Include relevant IDs and values (but sanitize sensitive data)
- Explain what went wrong and possibly why
- Suggest a potential solution if applicable
- Be consistent in message formatting

### 4.3 Serialization Considerations

If your exceptions might cross JVM boundaries (e.g., in RMI or serialized applications), implement `Serializable` and provide a serialVersionUID:

```java
public class ConfigurationException extends Exception implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String configFile;
    
    public ConfigurationException(String message, String configFile) {
        super(message);
        this.configFile = configFile;
    }
    
    // Getters and other methods
}
```

### 4.4 Documentation for Custom Exceptions

Properly document your custom exceptions with Javadoc:

```java
/**
 * Thrown when a requested user cannot be found in the system.
 * 
 * @author YourName
 */
public class UserNotFoundException extends ServiceException {
    /**
     * Constructs a new UserNotFoundException with the specified user ID.
     *
     * @param userId the ID of the user that could not be found
     */
    public UserNotFoundException(String userId) {
        super("User not found with ID: " + userId);
    }
    
    /**
     * Constructs a new UserNotFoundException with the specified message and cause.
     *
     * @param message the detail message
     * @param cause the cause of this exception
     */
    public UserNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

✅ **Documentation guidelines**:
- Explain when and why the exception is thrown
- Document each constructor
- Describe any custom methods or properties
- Include `@throws` in methods that might throw your exception


## 5. 📋 Real-World Examples and Patterns
---------

### 5.1 Layered Exception Handling Pattern

This pattern translates exceptions between layers in your application:

```java
// Data layer
public class UserRepository {
    public User findById(String id) throws DatabaseException {
        try {
            // Database access code...
            return user;
        } catch (SQLException e) {
            throw new DatabaseException("Database error while finding user: " + id, e);
        }
    }
}

// Service layer
public class UserService {
    private UserRepository repository;
    
    public UserDTO getUser(String id) throws ServiceException {
        try {
            User user = repository.findById(id);
            if (user == null) {
                throw new UserNotFoundException(id);
            }
            return convertToDTO(user);
        } catch (DatabaseException e) {
            throw new ServiceException("Failed to retrieve user: " + id, e);
        }
    }
}

// API layer
@RestController
public class UserController {
    private UserService service;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable String id) {
        try {
            return ResponseEntity.ok(service.getUser(id));
        } catch (UserNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                               .body(null);
        } catch (ServiceException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                               .body(null);
        }
    }
}
```

### 5.2 Exception Factory Pattern

For applications with many similar exceptions, use a factory pattern:

```java
public class ExceptionFactory {
    public static ValidationException validationError(String field, String message) {
        ValidationException ex = new ValidationException("Validation failed for: " + field);
        ex.addValidationError(field, message);
        return ex;
    }
    
    public static ResourceNotFoundException userNotFound(String userId) {
        return new ResourceNotFoundException("User", userId);
    }
    
    public static ResourceNotFoundException orderNotFound(String orderId) {
        return new ResourceNotFoundException("Order", orderId);
    }
}

// Usage
if (user == null) {
    throw ExceptionFactory.userNotFound(userId);
}
```

### 5.3 Status Enum Pattern

Use enums to represent different error conditions:

```java
public class BusinessException extends Exception {
    private ErrorCode errorCode;
    
    public enum ErrorCode {
        INSUFFICIENT_FUNDS(1001, "Insufficient funds available"),
        ACCOUNT_LOCKED(1002, "Account is locked"),
        DAILY_LIMIT_EXCEEDED(1003, "Daily transfer limit exceeded");
        
        private final int code;
        private final String defaultMessage;
        
        ErrorCode(int code, String defaultMessage) {
            this.code = code;
            this.defaultMessage = defaultMessage;
        }
        
        public int getCode() {
            return code;
        }
        
        public String getDefaultMessage() {
            return defaultMessage;
        }
    }
    
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getDefaultMessage());
        this.errorCode = errorCode;
    }
    
    public BusinessException(ErrorCode errorCode, String customMessage) {
        super(customMessage);
        this.errorCode = errorCode;
    }
    
    public ErrorCode getErrorCode() {
        return errorCode;
    }
}

// Usage
throw new BusinessException(ErrorCode.INSUFFICIENT_FUNDS, 
    "Account #12345 has insufficient funds for withdrawal of $500");
```


## 6. 🚫 Common Mistakes and Anti-Patterns
---------

### 6.1 Swallowing Exceptions

❌ **Anti-pattern**:
```java
try {
    riskyOperation();
} catch (Exception e) {
    // Do nothing or just log
    logger.error("Error occurred", e);
}
```

✅ **Better approach**:
```java
try {
    riskyOperation();
} catch (Exception e) {
    logger.error("Error occurred", e);
    throw new ServiceException("Operation failed", e);
}
```

### 6.2 Overusing Checked Exceptions

❌ **Anti-pattern**:
```java
// Too many checked exceptions
public void doSomething() throws Exception1, Exception2, Exception3, Exception4 {
    // Implementation
}
```

✅ **Better approach**:
```java
// Use a common base exception
public void doSomething() throws ServiceException {
    try {
        // Implementation that might throw Exception1, Exception2, etc.
    } catch (Exception1 | Exception2 e) {
        throw new ServiceException("Service operation failed", e);
    }
}
```

### 6.3 Breaking Encapsulation with Exceptions

❌ **Anti-pattern**:
```java
// Exposing implementation details
public class UserService {
    public User getUser(String id) throws SQLException {
        // Database code
    }
}
```

✅ **Better approach**:
```java
// Using appropriate abstraction
public class UserService {
    public User getUser(String id) throws UserNotFoundException, ServiceException {
        try {
            // Database code
        } catch (SQLException e) {
            throw new ServiceException("Database error", e);
        }
    }
}
```

### 6.4 Overly Generic Exceptions

❌ **Anti-pattern**:
```java
// Too generic
throw new Exception("Something went wrong");
```

✅ **Better approach**:
```java
// Specific and descriptive
throw new PaymentDeclinedException("Payment declined: insufficient funds");
```


## 7. 📝 Summary
---------

✅ **Key Points**:

1. **Creating Custom Exceptions**:
   - Extend `Exception` for checked exceptions or `RuntimeException` for unchecked
   - Include constructors with cause parameter for proper exception chaining
   - Add custom data and methods to provide more context

2. **Exception Hierarchy**:
   - Create a base application exception
   - Build specialized exceptions in a logical hierarchy
   - Organize by layer or domain based on application needs
   - Use exception translation to hide implementation details

3. **Checked vs. Unchecked**:
   - Use checked exceptions for recoverable conditions
   - Use unchecked exceptions for programming errors
   - Consider the impact on callers when choosing

4. **Best Practices**:
   - Follow naming conventions (end with "Exception")
   - Create informative, actionable exception messages
   - Consider serialization if crossing JVM boundaries
   - Document exceptions thoroughly with Javadoc

5. **Common Patterns**:
   - Layered exception handling
   - Exception factory pattern
   - Status enum pattern

6. **Avoid Anti-Patterns**:
   - Don't swallow exceptions
   - Don't overuse checked exceptions
   - Don't break encapsulation
   - Avoid overly generic exceptions


## 8. 📊 Quick Reference Table
---------

| Aspect | Checked Exceptions | Unchecked Exceptions |
|--------|-------------------|---------------------|
| **Base Class** | `Exception` | `RuntimeException` |
| **Compile-time Checking** | Yes | No |
| **Declaration Required** | Yes (`throws` clause) | No |
| **When to Use** | Recoverable conditions | Programming errors |
| | Expected in normal operation | Precondition violations |
| | Business rule violations | Unrecoverable situations |
| **Examples** | `FileNotFoundException` | `IllegalArgumentException` |
| | `SQLException` | `NullPointerException` |
| | `ParseException` | `UnsupportedOperationException` |
| **Custom Examples** | `ResourceNotFoundException` | `InvalidInputException` |
| | `PaymentDeclinedException` | `ConfigurationException` |
| **Advantages** | Forces error handling | Less boilerplate code |
| | Documents potential failures | Cleaner method signatures |
| **Disadvantages** | More verbose code | May be missed by callers |
| | Can lead to catch/ignore pattern | Less compile-time safety |

Remember, the decision to use checked or unchecked exceptions should be based on whether the exception represents a condition that the caller can reasonably be expected to recover from.