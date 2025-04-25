# Object-Oriented Programming in Java: Inheritance 🧩

I'll help you master Java inheritance concepts with focused, interview-ready explanations. Let's dive in!

---------

## 1. 🔄 `extends` Keyword and Inheritance Hierarchies

Inheritance allows a class to inherit fields and methods from another class, creating an "is-a" relationship.

### Mini Code Example:
```java
// Base class (parent/superclass)
public class Vehicle {
    protected String make;
    protected String model;
    protected int year;
    
    public Vehicle(String make, String model, int year) {
        this.make = make;
        this.model = model;
        this.year = year;
    }
    
    public void startEngine() {
        System.out.println("Vehicle engine started");
    }
    
    public String getDetails() {
        return year + " " + make + " " + model;
    }
}

// Derived class (child/subclass)
public class Car extends Vehicle {
    private int numDoors;
    
    public Car(String make, String model, int year, int numDoors) {
        super(make, model, year); // Call parent constructor
        this.numDoors = numDoors;
    }
    
    @Override
    public void startEngine() {
        System.out.println("Car engine started with key");
    }
    
    public void honk() {
        System.out.println("Beep beep!");
    }
}
```

### 📌 Interview Insights:
- Java supports single inheritance only (extends one class)
- `super()` must be the first statement in constructor
- Child class can access parent's protected members
- `final` classes cannot be extended

### ❌ Common Mistakes:
- Forgetting to call `super()` constructor
- Overriding final methods
- Creating too deep inheritance hierarchies
- Using inheritance for code reuse rather than modeling "is-a" relationships

### ✅ Best Practices:
- Keep inheritance hierarchies shallow (typically < 3 levels)
- Use `@Override` annotation for all overridden methods
- Design parent classes for extension (or make them final)
- Document inheritance design decisions

---------

## 2. 🎯 Method Resolution and Dynamic Method Dispatch

Method resolution determines which method implementation is executed at runtime.

### Mini Code Example:
```java
public class Animal {
    public void makeSound() {
        System.out.println("Animal makes a sound");
    }
    
    public void eat() {
        System.out.println("Animal eats");
    }
}

public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Dog barks");
    }
    
    public void fetch() {
        System.out.println("Dog fetches");
    }
}

public class Main {
    public static void main(String[] args) {
        // Dynamic method dispatch
        Animal animal = new Dog();
        animal.makeSound();  // Outputs: "Dog barks" (runtime type)
        animal.eat();        // Outputs: "Animal eats" (from parent)
        
        // Won't compile - fetch() not in Animal
        // animal.fetch();
        
        // Type casting
        if (animal instanceof Dog) {
            Dog dog = (Dog) animal;
            dog.fetch();     // Now works
        }
    }
}
```

### 📌 Interview Insights:
- Method resolution is determined by the actual object type at runtime
- Variable type (compile-time type) determines which methods can be called
- `instanceof` and casting allow access to subclass-specific methods
- Static methods are not dynamically dispatched (bound at compile time)

### ❌ Common Mistakes:
- Confusion between compile-time type checking and runtime method binding
- Incorrect downcasting without `instanceof` check
- Hiding methods (same signature but static) vs overriding
- Expecting parent private methods to be overridable

### ✅ Best Practices:
- Design for polymorphism when using inheritance
- Use `@Override` to ensure method signature matches
- Be cautious with downcasting and always verify with `instanceof`
- Prefer interface types for variables when possible

---------

## 3. 🧱 Composition vs Inheritance

Composition creates "has-a" relationships by including object references as fields.

### Mini Code Example:
```java
// Inheritance approach
public class ElectricCar extends Car {
    private int batteryCapacity;
    
    public void chargeBattery() {
        System.out.println("Charging battery");
    }
}

// Composition approach
public class ElectricCar2 {
    private Car car; // Composition
    private Battery battery; // Composition
    
    public ElectricCar2(Car car, Battery battery) {
        this.car = car;
        this.battery = battery;
    }
    
    public void startEngine() {
        car.startEngine();
    }
    
    public void chargeBattery() {
        battery.charge();
    }
    
    // Delegate to car object
    public String getDetails() {
        return car.getDetails() + ", Battery: " + battery.getCapacity() + "kWh";
    }
}

class Battery {
    private int capacity;
    
    public Battery(int capacity) {
        this.capacity = capacity;
    }
    
    public void charge() {
        System.out.println("Charging battery");
    }
    
    public int getCapacity() {
        return capacity;
    }
}
```

### 📌 Interview Insights:
- "Favor composition over inheritance" is a key design principle
- Composition offers more flexibility and looser coupling
- Inheritance creates tighter coupling between classes
- Composition enables changing behavior at runtime

### ❌ Common Mistakes:
- Using inheritance for code reuse when there's no true "is-a" relationship
- Creating fragile class hierarchies that are difficult to modify
- Not considering the impact of changes in parent classes on child classes
- "Inheritance hell" with multiple levels making code hard to understand

### ✅ Best Practices:
- Use composition for "has-a" relationships
- Use inheritance only for genuine "is-a" relationships
- Prefer interfaces + composition over abstract classes
- Consider the Decorator or Strategy patterns as alternatives to inheritance

---------

## 4. 📜 Design by Contract

Design by Contract (DbC) specifies preconditions, postconditions, and invariants for methods and classes.

### Mini Code Example:
```java
/**
 * A simple bank account class implementing Design by Contract principles.
 */
public class BankAccount {
    private double balance;
    
    /**
     * Withdraws money from the account.
     * 
     * @param amount the amount to withdraw
     * @throws IllegalArgumentException if amount <= 0 (precondition)
     * @throws InsufficientFundsException if amount > balance (precondition)
     * @ensures getBalance() == old getBalance() - amount (postcondition)
     */
    public void withdraw(double amount) {
        // Precondition
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        
        // Precondition
        if (amount > balance) {
            throw new InsufficientFundsException("Insufficient funds");
        }
        
        // Operation
        balance -= amount;
        
        // Postcondition check (in real code might use assertions)
        assert balance >= 0 : "Balance cannot be negative";
    }
    
    /**
     * Deposits money into the account.
     * 
     * @param amount the amount to deposit
     * @throws IllegalArgumentException if amount <= 0 (precondition)
     * @ensures getBalance() == old getBalance() + amount (postcondition)
     */
    public void deposit(double amount) {
        // Precondition
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        
        // Operation
        balance += amount;
    }
    
    /**
     * @return the current balance
     * @ensures result >= 0 (class invariant)
     */
    public double getBalance() {
        return balance;
    }
}

class InsufficientFundsException extends RuntimeException {
    public InsufficientFundsException(String message) {
        super(message);
    }
}
```

### 📌 Interview Insights:
- Liskov Substitution Principle (LSP) is closely related to DbC
- Subclasses must maintain or strengthen preconditions
- Subclasses must maintain or weaken postconditions
- Class invariants must be preserved in all subclasses

### ❌ Common Mistakes:
- Weakening preconditions in subclasses
- Strengthening postconditions in subclasses
- Not documenting contracts clearly
- Violating parent class invariants in subclasses

### ✅ Best Practices:
- Document contracts in Javadoc
- Use assertions to verify postconditions and invariants
- Throw exceptions for precondition violations
- Design parent classes with contracts in mind to enable safe inheritance

---------

## 5. 📊 Summary of Key Points

- **Extends Keyword**: Java supports single inheritance with `extends`. Use `super()` to call parent constructors.
- **Method Resolution**: Runtime type determines which method implementation runs (polymorphism).
- **Composition vs Inheritance**: Prefer composition ("has-a") over inheritance ("is-a") for flexibility.
- **Design by Contract**: Define preconditions, postconditions, and invariants for robust inheritance.

### 💡 Key Tips for Interviews:
- Explain inheritance in terms of "is-a" relationships and polymorphism
- Know the difference between overriding and overloading
- Be ready to discuss tradeoffs between composition and inheritance
- Understand Liskov Substitution Principle for proper inheritance design

---------

## 6. 🔍 Quick Reference Table

| Concept | Key Points | Interview Focus |
|---------|------------|----------------|
| **extends Keyword** | - Single inheritance only<br>- `super()` must be first in constructor<br>- `final` classes can't be extended | Class hierarchy design, constructor chaining |
| **Method Resolution** | - Runtime type determines method<br>- Static binding for static methods<br>- Variable type determines available methods | Polymorphism, downcasting safety |
| **Composition vs Inheritance** | - Inheritance: "is-a"<br>- Composition: "has-a"<br>- Composition offers more flexibility | Design principles, coupling reduction |
| **Design by Contract** | - Preconditions<br>- Postconditions<br>- Invariants<br>- Liskov Substitution Principle | Contract enforcement, inheritance safety |

Remember to focus on the "why" behind these concepts during interviews, not just the technical implementation. Good luck with your interview preparation! 🚀