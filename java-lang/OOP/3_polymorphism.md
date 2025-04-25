# Object-Oriented Programming in Java: Polymorphism 🔄

I'll help you master Java polymorphism with interview-ready explanations that are clear and concise. Let's dive in!

---------

## 1. 🧩 Compile-time Polymorphism (Method Overloading)

Method overloading allows multiple methods with the same name but different parameter lists in the same class.

### Mini Code Example:
```java
public class Calculator {
    // Overloaded methods
    public int add(int a, int b) {
        return a + b;
    }
    
    public double add(double a, double b) {
        return a + b;
    }
    
    public int add(int a, int b, int c) {
        return a + b + c;
    }
    
    public String add(String a, String b) {
        return a + b;  // String concatenation
    }
}
```

### 📌 Interview Insights:
- Resolved at compile time (static binding)
- Method selection based on:
  1. Exact match
  2. Widening primitive conversion
  3. Autoboxing/unboxing
  4. Varargs
- Return type alone is not enough to overload methods

### ❌ Common Mistakes:
- Trying to overload methods that differ only by return type
- Confusion with type promotion rules (int → long → float → double)
- Overloading with both primitive and wrapper types can be ambiguous
- Relying on overloading for drastically different behaviors

```java
// This won't compile - methods differ only by return type
public int getValue() { return 1; }
public double getValue() { return 1.0; }  // ERROR!

// Ambiguous when autoboxing is involved
public void process(int a) { /*...*/ }
public void process(Integer a) { /*...*/ }
// Which one gets called with process(5)? It's confusing!
```

### ✅ Best Practices:
- Keep overloaded method behavior consistent and predictable
- Avoid excessive overloading - use meaningful method names instead
- Be careful with autoboxing/unboxing in overloaded methods
- Document differences between overloaded methods clearly

---------

## 2. 🚀 Runtime Polymorphism (Method Overriding)

Method overriding occurs when a subclass provides a specific implementation of a method already defined in its parent class.

### Mini Code Example:
```java
// Parent class
public class Shape {
    protected String color;
    
    public Shape(String color) {
        this.color = color;
    }
    
    public double calculateArea() {
        return 0.0;  // Default implementation
    }
    
    public String getInfo() {
        return "Shape with color: " + color;
    }
    
    // Final method - cannot be overridden
    public final String getColor() {
        return color;
    }
}

// Child class
public class Circle extends Shape {
    private double radius;
    
    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public String getInfo() {
        return "Circle with radius: " + radius + ", " + super.getInfo();
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        Shape shape = new Circle("red", 5.0);
        System.out.println(shape.calculateArea());  // Calls Circle's implementation
        System.out.println(shape.getInfo());        // Calls Circle's implementation
    }
}
```

### 📌 Interview Insights:
- Resolved at runtime (dynamic binding)
- Method must have:
  - Same name
  - Same parameters (signature)
  - Same or covariant return type
  - Same or less restrictive access modifier
- `@Override` annotation is not required but strongly recommended

### ❌ Common Mistakes:
- Forgetting `@Override` annotation, leading to accidental overloading
- Trying to override private or final methods
- Making access modifiers more restrictive in overridden methods
- Ignoring the parent implementation when it should be called

```java
// Common mistake: missing @Override annotation
class Animal {
    public void makeSound() { /* ... */ }
}

class Dog extends Animal {
    // Method signature is slightly different (typo) - not overriding!
    public void makesound() { /* ... */ }  // Notice lowercase 'sound'
}
```

### ✅ Best Practices:
- Always use `@Override` annotation
- Consider calling the parent implementation with `super.method()`
- Document when and why you're completely replacing parent behavior
- Make methods `final` if they shouldn't be overridden

---------

## 3. 🔄 Type Casting with Inheritance Hierarchies

Type casting allows conversion between related types in the inheritance hierarchy.

### Mini Code Example:
```java
// Inheritance hierarchy
class Animal { 
    public void eat() { 
        System.out.println("Animal eating"); 
    }
}

class Dog extends Animal {
    public void eat() { 
        System.out.println("Dog eating"); 
    }
    
    public void bark() { 
        System.out.println("Woof!"); 
    }
}

class Cat extends Animal {
    public void eat() { 
        System.out.println("Cat eating"); 
    }
    
    public void meow() { 
        System.out.println("Meow!"); 
    }
}

// Usage with type casting
public class Main {
    public static void main(String[] args) {
        // Upcasting (implicit)
        Animal animal1 = new Dog();  // Dog -> Animal
        Animal animal2 = new Cat();  // Cat -> Animal
        
        animal1.eat();  // "Dog eating" (polymorphism)
        animal2.eat();  // "Cat eating" (polymorphism)
        
        // Won't compile - bark() not in Animal
        // animal1.bark();  
        
        // Downcasting (explicit) - with check
        if (animal1 instanceof Dog) {
            Dog dog = (Dog) animal1;  // Animal -> Dog
            dog.bark();  // Now works: "Woof!"
        }
        
        // ClassCastException at runtime if not checked
        try {
            Dog wrongDog = (Dog) animal2;  // animal2 is a Cat, not a Dog!
            wrongDog.bark();  // This line will never execute
        } catch (ClassCastException e) {
            System.out.println("Cannot cast Cat to Dog");
        }
    }
}
```

### 📌 Interview Insights:
- Upcasting (child to parent) is always safe and implicit
- Downcasting (parent to child) requires explicit cast and runtime checking
- ClassCastException occurs if downcasting to incompatible type
- Type casting doesn't change the actual object, just how it's accessed

### ❌ Common Mistakes:
- Downcasting without checking with `instanceof` first
- Not handling potential ClassCastException
- Unnecessary casting when using polymorphism
- Type checking based solely on class names (brittle design)

### ✅ Best Practices:
- Always check with `instanceof` before downcasting
- Try to minimize explicit downcasting in code
- Use polymorphism instead of type checking when possible
- Design class hierarchies to minimize need for downcasting

---------

## 4. 🔍 instanceof Operator and Pattern Matching (Java 16+)

The `instanceof` operator checks if an object is an instance of a specific type, while pattern matching (Java 16+) combines this check with variable assignment.

### Mini Code Example:
```java
// Traditional approach (pre-Java 16)
public void processShape(Object shape) {
    if (shape instanceof Rectangle) {
        Rectangle rectangle = (Rectangle) shape;
        System.out.println("Rectangle with width: " + rectangle.getWidth() 
                         + " and height: " + rectangle.getHeight());
    } else if (shape instanceof Circle) {
        Circle circle = (Circle) shape;
        System.out.println("Circle with radius: " + circle.getRadius());
    } else if (shape instanceof Triangle) {
        Triangle triangle = (Triangle) shape;
        System.out.println("Triangle with base: " + triangle.getBase() 
                         + " and height: " + triangle.getHeight());
    }
}

// Pattern matching approach (Java 16+)
public void processShapeModern(Object shape) {
    if (shape instanceof Rectangle rectangle) {
        System.out.println("Rectangle with width: " + rectangle.getWidth() 
                         + " and height: " + rectangle.getHeight());
    } else if (shape instanceof Circle circle) {
        System.out.println("Circle with radius: " + circle.getRadius());
    } else if (shape instanceof Triangle triangle) {
        System.out.println("Triangle with base: " + triangle.getBase() 
                         + " and height: " + triangle.getHeight());
    }
}

// Switch pattern matching (Java 17+)
public void processShapeSwitch(Object shape) {
    switch (shape) {
        case Rectangle rectangle -> 
            System.out.println("Rectangle with width: " + rectangle.getWidth() 
                             + " and height: " + rectangle.getHeight());
        case Circle circle -> 
            System.out.println("Circle with radius: " + circle.getRadius());
        case Triangle triangle -> 
            System.out.println("Triangle with base: " + triangle.getBase() 
                             + " and height: " + triangle.getHeight());
        default -> 
            System.out.println("Unknown shape");
    }
}
```

### 📌 Interview Insights:
- Pattern matching reduces boilerplate and improves code readability
- Pattern variable is in scope only in the conditional branch where it's defined
- Enhances type safety by combining check and cast in one operation
- Java 17+ extends pattern matching to switch statements

### ❌ Common Mistakes:
- Using pattern matching without being aware of target Java version
- Trying to use pattern variables outside their scope
- Not handling all possible types in switch expressions
- Nesting pattern matching too deeply, making code hard to read

### ✅ Best Practices:
- Use pattern matching to simplify type checking and casting
- Combine with sealed classes (Java 17+) for exhaustiveness checking
- Keep type checking code simple and maintainable
- Consider switch expressions for multiple type patterns

---------

## 5. 📊 Summary of Key Points

- **Compile-time Polymorphism**: Method overloading with different parameters, resolved at compile time
- **Runtime Polymorphism**: Method overriding in subclasses, resolved at runtime based on object type
- **Type Casting**: Conversion between related types in inheritance hierarchy
  - Upcasting: implicit, always safe
  - Downcasting: explicit, requires type checking
- **Pattern Matching**: Modern approach that combines `instanceof` with variable assignment

### 💡 Key Tips for Interviews:
- Be ready to explain the difference between overloading and overriding clearly
- Know when polymorphism is resolved (compile-time vs runtime)
- Understand inheritance hierarchies and the role of polymorphism
- Be familiar with pattern matching as a modern Java feature
- Be prepared to discuss the safety concerns with downcasting

---------

## 6. 🔍 Quick Reference Table

| Concept | Key Points | Interview Focus |
|---------|------------|----------------|
| **Method Overloading** | - Same name, different parameters<br>- Compile-time binding<br>- Return type doesn't distinguish<br>- Type promotion rules apply | Parameter type resolution, method selection |
| **Method Overriding** | - Same signature in subclass<br>- Runtime binding<br>- `@Override` annotation<br>- Covariant return types allowed | Polymorphic behavior, virtual method invocation |
| **Type Casting** | - Upcasting: implicit, child to parent<br>- Downcasting: explicit, parent to child<br>- `instanceof` checks required<br>- ClassCastException risk | Type safety, avoiding runtime exceptions |
| **Pattern Matching** | - Combines `instanceof` and variable assignment<br>- Introduced in Java 16<br>- Extended to switch in Java 17<br>- Enhances readability | Modern Java features, code simplification |

Remember to focus on practical examples during interviews that demonstrate your understanding of polymorphism. Good luck with your interview preparation! 🚀