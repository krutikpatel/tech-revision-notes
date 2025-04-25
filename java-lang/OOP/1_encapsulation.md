# Object-Oriented Programming in Java: Encapsulation 🧠

I'll help you master Java encapsulation concepts with interview-ready explanations. Let's dive in!

---------

## 1. 🔐 Access Modifiers

Access modifiers control visibility of classes, methods, and fields:

| Modifier | Class | Package | Subclass | World |
|----------|-------|---------|----------|-------|
| public | ✅ | ✅ | ✅ | ✅ |
| protected | ✅ | ✅ | ✅ | ❌ |
| default (no modifier) | ✅ | ✅ | ❌ | ❌ |
| private | ✅ | ❌ | ❌ | ❌ |

### Mini Code Example:
```java
package com.example;

public class AccessModifierDemo {
    public String publicField = "Accessible everywhere";
    protected String protectedField = "Accessible in package and subclasses";
    String defaultField = "Accessible only in package";
    private String privateField = "Accessible only in this class";
    
    private void privateMethod() {
        // Can access all fields here
        System.out.println(privateField);
        System.out.println(defaultField);
        System.out.println(protectedField);
        System.out.println(publicField);
    }
}
```

### 📌 Interview Insights:
- Know exactly where each modifier is visible
- `protected` is often misunderstood - it's accessible in subclasses even in different packages
- `default` (package-private) provides visibility within the same package only

### ❌ Common Mistakes:
- Exposing implementation details with overly permissive modifiers
- Using `protected` when `private` with targeted getters would be better
- Forgetting that `protected` members are visible to all classes in the same package

### ✅ Best Practices:
- Use the most restrictive access level possible
- Make fields private and provide controlled access via methods
- Avoid `protected` unless you explicitly design for inheritance

---------

## 2. 📝 Getters and Setters

Getters and setters provide controlled access to private fields.

### Mini Code Example:
```java
public class Employee {
    private String name;
    private int age;
    private double salary;
    
    // Getter
    public String getName() {
        return name;
    }
    
    // Setter with validation
    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name;
        } else {
            throw new IllegalArgumentException("Name cannot be empty");
        }
    }
    
    // Getter
    public int getAge() {
        return age;
    }
    
    // Setter with validation
    public void setAge(int age) {
        if (age >= 18 && age <= 120) {
            this.age = age;
        } else {
            throw new IllegalArgumentException("Age must be between 18 and 120");
        }
    }
    
    // Getter
    public double getSalary() {
        return salary;
    }
    
    // Setter
    public void setSalary(double salary) {
        if (salary >= 0) {
            this.salary = salary;
        } else {
            throw new IllegalArgumentException("Salary cannot be negative");
        }
    }
}
```

### 📌 Interview Insights:
- Getters/setters provide a layer of abstraction for future changes
- Validate input in setters to maintain object integrity
- JavaBeans naming convention: `getX()`, `setX()`, `isX()` for booleans

### ❌ Common Mistakes:
- Creating "dumb" getters/setters that don't validate input
- Exposing internal representation (returning direct reference to mutable objects)
- Not using getters/setters consistently throughout the code

### ✅ Best Practices:
- Always validate input in setters
- Consider whether a setter is truly needed (immutability)
- Document the validation rules in method Javadoc

---------

## 3. 🛡️ Immutability Pattern and Defensive Copying

Immutable objects cannot be modified after creation, enhancing thread safety and reducing errors.

### Mini Code Example:
```java
public final class ImmutablePerson {
    private final String name;
    private final int age;
    private final Date birthDate;
    private final List<String> skills;
    
    public ImmutablePerson(String name, int age, Date birthDate, List<String> skills) {
        this.name = name;
        this.age = age;
        // Defensive copy for mutable objects
        this.birthDate = birthDate != null ? new Date(birthDate.getTime()) : null;
        // Defensive copy of collection
        this.skills = skills != null ? new ArrayList<>(skills) : new ArrayList<>();
    }
    
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public Date getBirthDate() {
        // Return defensive copy
        return birthDate != null ? new Date(birthDate.getTime()) : null;
    }
    
    public List<String> getSkills() {
        // Return defensive copy
        return new ArrayList<>(skills);
    }
}
```

### 📌 Interview Insights:
- Immutable classes are inherently thread-safe
- Five rules for immutability:
  1. Don't provide methods that modify state
  2. Make all fields final
  3. Make the class final (prevent subclassing)
  4. Defensive copy mutable parameters in constructor
  5. Defensive copy mutable objects in getters

### ❌ Common Mistakes:
- Forgetting defensive copies for mutable objects
- Exposing internal collections with direct references
- Using only some immutability techniques but not all

### ✅ Best Practices:
- Use immutable objects when possible
- Consider using existing immutable classes (String, Integer, etc.)
- For collections, consider unmodifiable wrappers: `Collections.unmodifiableList()`
- Use the Builder pattern for complex immutable objects with many fields

---------

## 4. 📦 Package Structure and Organization

Proper package organization enhances maintainability, encapsulation, and access control.

### Common Package Structure:
```
com.company.project/
├── api/        (public interfaces)
├── impl/       (implementation classes)
├── model/      (domain objects)
├── service/    (business logic)
├── util/       (utility classes)
└── exception/  (custom exceptions)
```

### Mini Code Example:
```java
// File: com/company/banking/api/AccountService.java
package com.company.banking.api;

public interface AccountService {
    void deposit(String accountId, double amount);
    boolean withdraw(String accountId, double amount);
    double getBalance(String accountId);
}

// File: com/company/banking/impl/AccountServiceImpl.java
package com.company.banking.impl;

import com.company.banking.api.AccountService;
import com.company.banking.model.Account;
import com.company.banking.exception.InsufficientFundsException;

class AccountServiceImpl implements AccountService {
    // Implementation details hidden from other packages
    private Map<String, Account> accounts = new HashMap<>();
    
    @Override
    public void deposit(String accountId, double amount) {
        // Implementation
    }
    
    @Override
    public boolean withdraw(String accountId, double amount) {
        // Implementation
    }
    
    @Override
    public double getBalance(String accountId) {
        // Implementation
        return 0.0;
    }
}
```

### 📌 Interview Insights:
- Package structure can enforce architectural boundaries
- Default access modifier helps hide implementation classes
- Packages represent a namespace and an encapsulation boundary

### ❌ Common Mistakes:
- Mixing concerns within packages
- Not distinguishing between API and implementation
- Creating too deep/complex package hierarchies
- Circular dependencies between packages

### ✅ Best Practices:
- Follow domain-driven design principles for package structure
- Keep implementation details in separate packages
- Use package-private (default) access for implementation classes
- Group related classes in the same package
- Avoid package cycles (A depends on B depends on A)

---------

## 5. 📊 Summary of Key Points

- **Access Modifiers**: Control visibility with public, protected, default, private
- **Getters/Setters**: Provide controlled access with validation
- **Immutability**: Create thread-safe objects that can't change after creation
- **Defensive Copying**: Protect internal state by copying mutable objects
- **Package Structure**: Organize code logically to enhance encapsulation

### 💡 Key Tips for Interviews:
- Focus on explaining not just how but why encapsulation is important
- Be ready to explain access control and its impact on API design
- Understand thread-safety implications of immutability
- Know defensive copying techniques for collections and mutable objects
- Discuss trade-offs between different encapsulation approaches

---------

## 6. 🔍 Quick Reference Table

| Concept | Key Points | Interview Focus |
|---------|------------|----------------|
| **Access Modifiers** | - public: visible everywhere<br>- protected: package + subclasses<br>- default: package only<br>- private: class only | Visibility boundaries, API design |
| **Getters/Setters** | - Control access to internal state<br>- Enable validation<br>- Support encapsulation | Input validation, API stability |
| **Immutability** | - Final class<br>- Final fields<br>- No state-changing methods<br>- Defensive copying | Thread safety, error reduction |
| **Defensive Copying** | - Copy in constructors<br>- Copy in getters<br>- Protect collections | Protecting internal representation |
| **Package Structure** | - Logical organization<br>- Implementation hiding<br>- API separation | Architecture, maintainability |

Remember to explain your reasoning during interviews, not just the technical details. Good luck with your interview preparation! 🚀