# 🛡️ @ControllerAdvice & @RestControllerAdvice in Spring Framework

## 1. 🔍 Introduction to Global Exception Handling
---------

Exception handling is a critical aspect of building robust Spring applications. The `@ControllerAdvice` and `@RestControllerAdvice` annotations provide a powerful mechanism for centralizing exception handling across your entire application.

### 📌 What are @ControllerAdvice & @RestControllerAdvice?

`@ControllerAdvice` is a specialized annotation that allows you to handle exceptions globally across all controllers in your Spring application. It's essentially a component that can contain `@ExceptionHandler`, `@InitBinder`, and `@ModelAttribute` methods that apply to all `@Controller` classes.

`@RestControllerAdvice` is a convenience annotation that combines `@ControllerAdvice` and `@ResponseBody`, making it suitable for REST API exception handling where responses are automatically converted to JSON/XML.

```
┌─────────────────┐     throws     ┌────────────────┐     routed to     ┌─────────────────────┐
│   Any           │────────────────│   Exception    │───────────────────│  @ControllerAdvice  │
│   Controller    │                │                │                   │  Exception Handler  │
└─────────────────┘                └────────────────┘                   └─────────────────────┘
```

## 2. 🛠️ Basic Implementation
---------

### 📌 Creating a Simple @ControllerAdvice Class

Here's a basic implementation of a global exception handler using `@ControllerAdvice`:

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    // Handle specific exceptions
    @ExceptionHandler(ResourceNotFoundException.class)
    public ModelAndView handleResourceNotFoundException(ResourceNotFoundException ex) {
        ModelAndView modelAndView = new ModelAndView("error");
        modelAndView.addObject("errorMessage", ex.getMessage());
        return modelAndView;
    }
    
    // Generic exception handler
    @ExceptionHandler(Exception.class)
    public ModelAndView handleGenericException(Exception ex) {
        ModelAndView modelAndView = new ModelAndView("error");
        modelAndView.addObject("errorMessage", "An unexpected error occurred");
        return modelAndView;
    }
}
```

### 📌 Creating a @RestControllerAdvice for REST APIs

For REST APIs, use `@RestControllerAdvice` to create JSON/XML responses:

```java
@RestControllerAdvice
public class GlobalRestExceptionHandler {

    // Handle resource not found exception
    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleResourceNotFoundException(ResourceNotFoundException ex) {
        return new ErrorResponse("RESOURCE_NOT_FOUND", ex.getMessage());
    }
    
    // Handle validation exceptions
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ValidationErrorResponse handleValidationExceptions(MethodArgumentNotValidException ex) {
        ValidationErrorResponse errorResponse = new ValidationErrorResponse();
        errorResponse.setErrorCode("VALIDATION_FAILED");
        errorResponse.setMessage("Validation failed");
        
        ex.getBindingResult().getFieldErrors().forEach(error -> {
            errorResponse.addValidationError(error.getField(), error.getDefaultMessage());
        });
        
        return errorResponse;
    }
    
    // Handle all other exceptions
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleAllExceptions(Exception ex) {
        return new ErrorResponse("SERVER_ERROR", "An unexpected error occurred");
    }
}
```

### 📌 Custom Error Response Classes

Create structured error response classes for better API responses:

```java
// Base error response
public class ErrorResponse {
    private String errorCode;
    private String message;
    private LocalDateTime timestamp = LocalDateTime.now();
    
    // Constructors, getters, setters
}

// Extended for validation errors
public class ValidationErrorResponse extends ErrorResponse {
    private List<ValidationError> errors = new ArrayList<>();
    
    public void addValidationError(String field, String message) {
        errors.add(new ValidationError(field, message));
    }
    
    // Inner class for field-specific errors
    @Data
    public static class ValidationError {
        private String field;
        private String message;
        
        // Constructor, getters, setters
    }
}
```

## 3. 🔧 Advanced Features
---------

### 📌 Targeting Specific Controllers or Packages

You can limit the scope of your `@ControllerAdvice` to specific controllers, packages, or annotations:

```java
// Target by package
@ControllerAdvice(basePackages = {"com.example.controllers.user", "com.example.controllers.product"})
public class ApiExceptionHandler {
    // Exception handlers
}

// Target by controller type
@ControllerAdvice(assignableTypes = {UserController.class, ProductController.class})
public class UserProductExceptionHandler {
    // Exception handlers
}

// Target by annotation
@ControllerAdvice(annotations = RestController.class)
public class RestApiExceptionHandler {
    // Exception handlers for all @RestController classes
}
```

### 📌 Ordering Multiple ControllerAdvice Classes

When you have multiple `@ControllerAdvice` classes, you can control their execution order:

```java
@ControllerAdvice
@Order(Ordered.HIGHEST_PRECEDENCE)
public class PrimaryExceptionHandler {
    // This will be checked first
}

@ControllerAdvice
@Order(Ordered.LOWEST_PRECEDENCE)
public class FallbackExceptionHandler {
    // This will be checked last
}
```

### 📌 Accessing Request Details

You can access the original request information in your handlers:

```java
@RestControllerAdvice
public class DetailedExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex, WebRequest request) {
        ErrorResponse errorResponse = new ErrorResponse("SERVER_ERROR", ex.getMessage());
        
        // Access request details
        if (request instanceof ServletWebRequest) {
            HttpServletRequest servletRequest = ((ServletWebRequest) request).getRequest();
            errorResponse.setPath(servletRequest.getRequestURI());
            errorResponse.setMethod(servletRequest.getMethod());
        }
        
        return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

## 4. 🔄 ModelAttribute and InitBinder in ControllerAdvice
---------

### 📌 Global @ModelAttribute Methods

Beyond exception handling, `@ControllerAdvice` can also contain `@ModelAttribute` methods that add attributes to all models across the application:

```java
@ControllerAdvice
public class GlobalModelAttributes {

    @ModelAttribute
    public void addAttributes(Model model) {
        model.addAttribute("globalAttribute", "Value available in all views");
    }
    
    @ModelAttribute("currentYear")
    public int getCurrentYear() {
        return LocalDate.now().getYear();
    }
}
```

### 📌 Global @InitBinder Methods

You can also define global `@InitBinder` methods to configure WebDataBinder for all controllers:

```java
@ControllerAdvice
public class GlobalBindingInitializer {

    @InitBinder
    public void initBinder(WebDataBinder binder) {
        // Prevent direct binding of specified fields for security
        binder.setDisallowedFields("admin", "role");
        
        // Register custom editors
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, true));
        
        // Trim string values
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
    }
}
```

## 5. ⚠️ Common Mistakes & Traps
---------

### ❌ Common Mistakes

1. **Misplaced exception handler order:**
   ```java
   // BAD: More specific exception won't be caught because general Exception catches it first
   @ExceptionHandler(Exception.class)
   public ResponseEntity<ErrorResponse> handleAllExceptions(Exception ex) {
       // This catches everything, including ResourceNotFoundException
   }
   
   @ExceptionHandler(ResourceNotFoundException.class)
   public ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException ex) {
       // This will never be called!
   }
   ```

2. **Inconsistent response formats:**
   Having different error response structures from different handlers confuses API clients.

3. **Missing HTTP status codes:**
   ```java
   // BAD: No HTTP status specified, defaults to 200 OK for errors!
   @ExceptionHandler(ResourceNotFoundException.class)
   public ErrorResponse handleResourceNotFoundException(ResourceNotFoundException ex) {
       return new ErrorResponse("NOT_FOUND", ex.getMessage());
   }
   ```

4. **Exposing sensitive exception details:**
   ```java
   // BAD: Exposing internal error details and stack traces
   @ExceptionHandler(Exception.class)
   public ResponseEntity<String> handleException(Exception ex) {
       StringWriter sw = new StringWriter();
       ex.printStackTrace(new PrintWriter(sw));
       return new ResponseEntity<>(sw.toString(), HttpStatus.INTERNAL_SERVER_ERROR);
   }
   ```

5. **Forgetting to log exceptions:**
   Not logging exceptions makes troubleshooting difficult.

6. **Conflicting ControllerAdvice:**
   Having multiple `@ControllerAdvice` classes handling the same exceptions without proper ordering.

## 6. ✅ Best Practices
---------

### 📌 Structure & Organization

1. **Group related exception handlers:**
   Organize handlers logically, such as validation errors, security errors, and resource access errors.

2. **Create a consistent error response structure:**
   ```java
   public class ApiError {
       private HttpStatus status;
       private String message;
       private String errorCode;
       private LocalDateTime timestamp;
       private List<String> errors;
       
       // Constructors, getters, setters
   }
   ```

3. **Use HTTP status appropriately:**
   ```java
   @ExceptionHandler(ResourceNotFoundException.class)
   public ResponseEntity<ApiError> handleResourceNotFoundException(ResourceNotFoundException ex) {
       ApiError error = new ApiError(
           HttpStatus.NOT_FOUND,
           ex.getMessage(),
           "RESOURCE_NOT_FOUND"
       );
       return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
   }
   ```

### 📌 Logging & Security

4. **Log exceptions properly:**
   ```java
   @ExceptionHandler(Exception.class)
   public ResponseEntity<ApiError> handleAllExceptions(Exception ex) {
       log.error("Unhandled exception occurred", ex);
       
       ApiError error = new ApiError(
           HttpStatus.INTERNAL_SERVER_ERROR,
           "An unexpected error occurred",
           "INTERNAL_ERROR"
       );
       return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
   }
   ```

5. **Hide sensitive information:**
   Don't include database details, stack traces, or server paths in responses.

### 📌 Advanced Techniques

6. **Create custom exception hierarchies:**
   ```java
   // Base exception
   public class BaseApiException extends RuntimeException {
       private String errorCode;
       
       // Constructors, getters
   }
   
   // More specific exceptions
   public class ResourceNotFoundException extends BaseApiException {
       public ResourceNotFoundException(String resource, String id) {
           super(String.format("%s with id %s not found", resource, id));
           setErrorCode("RESOURCE_NOT_FOUND");
       }
   }
   ```

7. **Use @ResponseStatus on custom exceptions:**
   ```java
   @ResponseStatus(HttpStatus.NOT_FOUND)
   public class ResourceNotFoundException extends RuntimeException {
       // Implementation
   }
   ```

8. **Define different ControllerAdvice for APIs vs. Web:**
   ```java
   @ControllerAdvice(annotations = Controller.class)
   public class WebExceptionHandler {
       // Return ModelAndView for web pages
   }
   
   @RestControllerAdvice(annotations = RestController.class)
   public class ApiExceptionHandler {
       // Return JSON/XML for APIs
   }
   ```

## 7. 📊 Summary Tables
---------

### 📌 @ControllerAdvice vs. @RestControllerAdvice

| Aspect | @ControllerAdvice | @RestControllerAdvice |
|--------|------------------|------------------------|
| Purpose | Global exception handling, model attributes, and data binding | Same, but specifically for REST APIs |
| Response | Views (ModelAndView) by default | JSON/XML responses (has implicit @ResponseBody) |
| Combines | @Component + @ControllerAdvice | @ControllerAdvice + @ResponseBody |
| Best for | Traditional web applications | RESTful web services |

### 📌 Common Exception Types & Status Codes

| Exception Type | HTTP Status | Use Case |
|----------------|-------------|----------|
| ResourceNotFoundException | 404 NOT_FOUND | Resource lookup failures |
| MethodArgumentNotValidException | 400 BAD_REQUEST | Bean validation failures |
| AccessDeniedException | 403 FORBIDDEN | Security/authorization issues |
| HttpMessageNotReadableException | 400 BAD_REQUEST | Invalid request body |
| MissingServletRequestParameterException | 400 BAD_REQUEST | Missing required parameters |
| HttpRequestMethodNotSupportedException | 405 METHOD_NOT_ALLOWED | Unsupported HTTP method |
| Generic Exception | 500 INTERNAL_SERVER_ERROR | Unexpected errors |

### 📌 ControllerAdvice Filtering Options

| Filter Type | Example | Use Case |
|-------------|---------|----------|
| basePackages | @ControllerAdvice(basePackages = "com.example.api") | Target specific packages |
| assignableTypes | @ControllerAdvice(assignableTypes = {UserController.class}) | Target specific controller classes |
| annotations | @ControllerAdvice(annotations = RestController.class) | Target controllers with specific annotations |

## 8. 🚀 Quick Revision Summary
---------

### 📌 Key Concepts

- **@ControllerAdvice**: Global exception handling for all controllers
- **@RestControllerAdvice**: Global exception handling specifically for REST APIs
- Both annotations allow **@ExceptionHandler**, **@InitBinder**, and **@ModelAttribute** methods
- Can be **scoped** to specific packages, classes, or annotations
- Multiple advice classes can be **ordered** using @Order annotation
- Should provide **consistent error responses** with appropriate HTTP status codes

### 📌 Implementation Steps

1. Create custom exception classes for different error scenarios
2. Define a standard error response structure
3. Create @ControllerAdvice/@RestControllerAdvice classes
4. Implement exception handlers for specific exceptions
5. Add a fallback handler for unexpected exceptions
6. Ensure proper logging for all exceptions
7. Add appropriate security measures to prevent information leakage

## 9. 🎯 Interview Q&A
---------

### 📌 Common Interview Questions

1. **Q: What is the difference between @ControllerAdvice and @RestControllerAdvice?**

   A: `@RestControllerAdvice` is a specialized version of `@ControllerAdvice` that includes the `@ResponseBody` annotation. This means methods in a `@RestControllerAdvice` class automatically return data directly in the response body (typically as JSON/XML) rather than as a view name. It's a convenience annotation for REST API exception handling.

2. **Q: How can you make a @ControllerAdvice apply only to certain controllers?**

   A: You can limit the scope of a `@ControllerAdvice` using:
   - `basePackages` attribute to target specific packages
   - `assignableTypes` to target specific controller classes
   - `annotations` to target controllers with specific annotations
   
   ```java
   @ControllerAdvice(assignableTypes = {UserController.class, OrderController.class})
   public class UserOrderExceptionHandler {
       // Exception handlers
   }
   ```

3. **Q: How would you handle validation errors from @Valid annotations?**

   A: Implement an exception handler for `MethodArgumentNotValidException`:
   
   ```java
   @RestControllerAdvice
   public class ValidationExceptionHandler {
   
       @ExceptionHandler(MethodArgumentNotValidException.class)
       @ResponseStatus(HttpStatus.BAD_REQUEST)
       public ValidationErrorResponse handleValidationExceptions(MethodArgumentNotValidException ex) {
           ValidationErrorResponse response = new ValidationErrorResponse();
           response.setMessage("Validation failed");
           
           ex.getBindingResult().getFieldErrors().forEach(error -> {
               response.addValidationError(error.getField(), error.getDefaultMessage());
           });
           
           return response;
       }
   }
   ```

4. **Q: How can you handle multiple types of exceptions with a single handler method?**

   A: Specify multiple exception types in the `@ExceptionHandler` annotation:
   
   ```java
   @ExceptionHandler({ResourceNotFoundException.class, EntityNotFoundException.class})
   @ResponseStatus(HttpStatus.NOT_FOUND)
   public ErrorResponse handleNotFoundExceptions(Exception ex) {
       return new ErrorResponse("NOT_FOUND", ex.getMessage());
   }
   ```

5. **Q: How do you prioritize multiple @ControllerAdvice classes?**

   A: Use the `@Order` annotation to control the execution order:
   
   ```java
   @ControllerAdvice
   @Order(Ordered.HIGHEST_PRECEDENCE)
   public class PrimaryExceptionHandler {
       // This will be checked first
   }
   
   @ControllerAdvice
   @Order(Ordered.LOWEST_PRECEDENCE)
   public class FallbackExceptionHandler {
       // This will be checked last
   }
   ```
   
   Lower values indicate higher priority.

6. **Q: Beyond exception handling, what else can you do with @ControllerAdvice?**

   A: `@ControllerAdvice` can also contain:
   - `@ModelAttribute` methods to add attributes to all models
   - `@InitBinder` methods to configure data binding and validation for all controllers

7. **Q: How would you build a consistent error response structure for your API?**

   A: Create a standard error response class with fields like:
   - HTTP status code
   - Error code (application-specific)
   - Human-readable message
   - Timestamp
   - Path/endpoint where the error occurred
   - Detailed validation errors (when applicable)
   
   And ensure all exception handlers use this structure.

---

Use these concepts to build robust exception handling in your Spring applications. Good luck with your interview! 🍀