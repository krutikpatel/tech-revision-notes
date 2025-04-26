# 🛡️ Spring Framework Exception Handling with @ExceptionHandler

## 1. 🔍 Introduction to @ExceptionHandler
---------

Exception handling is a critical aspect of building robust Spring applications. The `@ExceptionHandler` annotation is a powerful tool that allows you to handle exceptions in a clean, centralized way.

### 📌 What is @ExceptionHandler?

`@ExceptionHandler` is a Spring annotation that lets you define methods specifically dedicated to handling exceptions. When an exception occurs in your application, Spring will route it to the appropriate exception handler method based on the exception type.

```
┌───────────────┐    throws    ┌───────────────┐    routes to    ┌───────────────────┐
│   Controller  │─────────────▶│   Exception   │───────────────▶│  @ExceptionHandler │
│     Method    │              │               │                │      Method        │
└───────────────┘              └───────────────┘                └───────────────────┘
```

### 📌 Basic Implementation

At its simplest, you can add an `@ExceptionHandler` method directly in your controller:

```java
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        // Method that might throw UserNotFoundException
        return userService.findById(id);
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("USER_NOT_FOUND", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

## 2. 🧩 Advanced Usage
---------

### 📌 Handling Multiple Exception Types

You can handle multiple exception types with a single handler method by specifying them in the annotation:

```java
@ExceptionHandler({ResourceNotFoundException.class, AccessDeniedException.class})
public ResponseEntity<ErrorResponse> handleSecurityExceptions(Exception ex) {
    ErrorResponse error = new ErrorResponse("SECURITY_ERROR", ex.getMessage());
    HttpStatus status = (ex instanceof ResourceNotFoundException) ? 
                          HttpStatus.NOT_FOUND : HttpStatus.FORBIDDEN;
    return new ResponseEntity<>(error, status);
}
```

### 📌 Customizing Response Format

You can provide detailed error responses:

```java
@ExceptionHandler(ValidationException.class)
public ResponseEntity<ValidationErrorResponse> handleValidationErrors(ValidationException ex) {
    ValidationErrorResponse error = new ValidationErrorResponse();
    error.setTimestamp(LocalDateTime.now());
    error.setStatus(HttpStatus.BAD_REQUEST.value());
    error.setMessage("Validation Error");
    error.setErrors(ex.getViolations().stream()
            .map(v -> v.getField() + ": " + v.getMessage())
            .collect(Collectors.toList()));
    
    return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
}
```

### 📌 Accessing Request Information

You can access the request that caused the exception:

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handleAllExceptions(Exception ex, WebRequest request) {
    ErrorResponse error = new ErrorResponse("SERVER_ERROR", ex.getMessage());
    error.setPath(((ServletWebRequest)request).getRequest().getRequestURL().toString());
    error.setTimestamp(LocalDateTime.now());
    
    return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
}
```

## 3. 🌐 Global Exception Handling with @ControllerAdvice
---------

While controller-level `@ExceptionHandler` methods work, they only handle exceptions from that specific controller. For application-wide exception handling, use `@ControllerAdvice`.

### 📌 Creating a Global Exception Handler

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse("RESOURCE_NOT_FOUND", ex.getMessage());
        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(ValidationException ex) {
        // Validation error handling
        return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAllOtherExceptions(Exception ex) {
        // Generic error handling
        return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

### 📌 Targeting Specific Packages or Controllers

You can limit the scope of a `@ControllerAdvice`:

```java
// Only applies to controllers in this package and subpackages
@ControllerAdvice(basePackages = "com.example.api")
public class ApiExceptionHandler {
    // Exception handlers
}

// Only applies to specific controller classes
@ControllerAdvice(assignableTypes = {UserController.class, OrderController.class})
public class UserOrderExceptionHandler {
    // Exception handlers
}
```

## 4. ⚠️ Common Mistakes & Best Practices
---------

### ❌ Common Mistakes

1. **Handler Method Ordering**
   - Spring checks exception handlers in order. More specific exceptions should be handled before more general ones.

   ```java
   // BAD: This handler will never be called
   @ExceptionHandler(Exception.class)
   public ResponseEntity<Object> handleAllExceptions(Exception ex) { ... }
   
   @ExceptionHandler(ResourceNotFoundException.class)
   public ResponseEntity<Object> handleResourceNotFound(ResourceNotFoundException ex) { ... }
   ```

2. **Missing Exception Types**
   - Not handling custom exceptions explicitly, causing them to fall into the generic handler.

3. **Duplicated Exception Handlers**
   - Defining the same exception handler in multiple places.

4. **Exposing Sensitive Information**
   - Including stack traces or internal details in error responses.

5. **Not Using ResponseEntity**
   - Returning direct objects instead of properly wrapping them with status codes.

### ✅ Best Practices

1. **Create Custom Exceptions**
   - Define domain-specific exceptions for better error handling.

   ```java
   public class ResourceNotFoundException extends RuntimeException {
       private String resourceType;
       private String resourceId;
       
       public ResourceNotFoundException(String resourceType, String resourceId) {
           super(String.format("%s with id %s not found", resourceType, resourceId));
           this.resourceType = resourceType;
           this.resourceId = resourceId;
       }
       
       // Getters
   }
   ```

2. **Use @ResponseStatus When Appropriate**
   - For simpler cases, you can use @ResponseStatus on exceptions.

   ```java
   @ResponseStatus(HttpStatus.NOT_FOUND)
   public class ResourceNotFoundException extends RuntimeException {
       // Implementation
   }
   ```

3. **Create a Consistent Error Response Structure**
   - Use a standard format for all error responses.

   ```java
   public class ErrorResponse {
       private LocalDateTime timestamp;
       private int status;
       private String error;
       private String message;
       private String path;
       private List<String> details;
       
       // Constructors, getters, setters
   }
   ```

4. **Log Exceptions Appropriately**
   - Log exceptions with proper context for troubleshooting.

   ```java
   @ExceptionHandler(Exception.class)
   public ResponseEntity<ErrorResponse> handleAllExceptions(Exception ex) {
       log.error("Unexpected error occurred", ex);
       // Create and return error response
   }
   ```

5. **Organize Exception Handlers by Domain**
   - Have separate `@ControllerAdvice` classes for different application modules.

## 5. 📊 Summary Tables
---------

### 📌 Exception Handler Annotations

| Annotation | Scope | Use Case |
|------------|-------|----------|
| `@ExceptionHandler` | Controller-specific | Local exception handling for specific controller |
| `@ControllerAdvice` + `@ExceptionHandler` | Global | Application-wide exception handling |
| `@ResponseStatus` | Exception-specific | Simple HTTP status code mapping without response body customization |

### 📌 Common ResponseEntity Status Codes

| Exception Type | HTTP Status | Status Code |
|----------------|-------------|-------------|
| `ResourceNotFoundException` | NOT_FOUND | 404 |
| `ValidationException` | BAD_REQUEST | 400 |
| `AccessDeniedException` | FORBIDDEN | 403 |
| `AuthenticationException` | UNAUTHORIZED | 401 |
| Generic exceptions | INTERNAL_SERVER_ERROR | 500 |

### 📌 Exception Handler Method Parameters

| Parameter Type | Usage |
|----------------|-------|
| `Exception` (or subclass) | The caught exception |
| `WebRequest` | Access to the request that caused the exception |
| `HttpServletRequest` | Access to the HTTP request details |
| `HttpServletResponse` | Direct access to modify the response |
| `HttpHeaders` | Access or modification of response headers |
| `Model` | For view-based exception handling |

## 6. 🚀 Interview Q&A
---------

### 📌 Common Interview Questions

1. **Q: What is the difference between @ExceptionHandler and @ControllerAdvice?**

   A: `@ExceptionHandler` defines methods that handle exceptions at the controller level, affecting only the controller where it's defined. `@ControllerAdvice` creates global exception handlers that work across multiple controllers. Use `@ControllerAdvice` with `@ExceptionHandler` methods inside it for centralized exception handling.

2. **Q: How would you prioritize exception handlers when multiple could match?**

   A: Spring prioritizes more specific exception types over general ones. If you have handlers for both `ResourceNotFoundException` and `Exception`, the `ResourceNotFoundException` handler will be used for that specific exception. Within a `@ControllerAdvice`, you can control the order using `@Order` annotation.

3. **Q: How can you access the request path in an exception handler?**

   A: Include `WebRequest` or `HttpServletRequest` as a parameter in your exception handler method:
   ```java
   @ExceptionHandler(Exception.class)
   public ResponseEntity<ErrorResponse> handle(Exception ex, HttpServletRequest request) {
       ErrorResponse error = new ErrorResponse();
       error.setPath(request.getRequestURI());
       // Set other fields
       return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
   }
   ```

4. **Q: How would you handle exceptions from REST endpoints differently from MVC controllers?**

   A: For REST endpoints, return `ResponseEntity<>` with JSON error details. For MVC controllers, return a view name with a model:
   ```java
   @ExceptionHandler(Exception.class)
   public String handleExceptionMvc(Exception ex, Model model) {
       model.addAttribute("errorMessage", ex.getMessage());
       return "error-page";
   }
   ```

5. **Q: How can you customize the default Spring Boot error response?**

   A: Create a `@ControllerAdvice` class with exception handlers, implement `ErrorController` to handle errors at the dispatcher level, or configure `server.error.*` properties in `application.properties`.

## 7. 📝 Quick Revision Summary
---------

### 📌 Key Concepts

- **@ExceptionHandler**: Annotation to create methods that handle specific exceptions
- **@ControllerAdvice**: Creates global exception handlers that work across controllers
- **ResponseEntity**: Wrapper class for HTTP responses, allowing status code and body customization
- **Custom Exceptions**: Domain-specific exceptions improve clarity and handling options
- **Consistent Error Responses**: Standardized error format improves API usability

### 📌 Implementation Steps

1. Create custom exception classes for domain-specific errors
2. Define a standard error response structure
3. Create a global exception handler with `@ControllerAdvice`
4. Implement `@ExceptionHandler` methods for different exception types
5. Return appropriate HTTP status codes with meaningful error messages
6. Add proper logging for troubleshooting
7. Test your exception handlers thoroughly

---

Remember, effective exception handling doesn't just make your code more robust—it provides better user experience and simplifies debugging. Good luck with your interview! 🍀