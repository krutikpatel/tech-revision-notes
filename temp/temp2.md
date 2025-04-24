# Method Resolution and Dynamic Method Dispatch in Java 📚

## 1. 📌 Understanding Method Resolution

Method resolution is how Java determines which method to call when you invoke a method on an object. This process differs depending on whether we're dealing with static or dynamic binding.

**Static Binding (Compile-time)** 🔍
- Occurs during compilation
- Used for private, static, and final methods
- Based on the reference type, not the actual object

**Dynamic Binding (Runtime)** ⚡
- Occurs during execution
- Used for virtual methods (non-static, non-final, non-private)
- Based on the actual object type, not the reference type

```java
class Parent {
    void display() {
        System.out.println("Parent's display method");
    }
    
    static void staticMethod() {
        System.out.println("Parent's static method");
    }
}

class Child extends Parent {
    @Override
    void display() {
        System.out.println("Child's display method");
    }
    
    static void staticMethod() {
        System.out.println("Child's static method");
    }
}

public class Test {
    public static void main(String[] args) {
        Parent p1 = new Parent();
        Parent p2 = new Child();
        
        p1.display();  // "Parent's display method"
        p2.display();  // "Child's display method" (Dynamic binding)
        
        p1.staticMethod();  // "Parent's static method"
        p2.staticMethod();  // "Parent's static method" (Static binding)
    }
}
```

✅ **Interview Insight**: Be able to explain why `p2.display()` calls the Child's method but `p2.staticMethod()` calls the Parent's method.

----------


## 2. 🔄 Dynamic Method Dispatch

Dynamic Method Dispatch is a mechanism where the JVM decides at runtime which version of an overridden method to execute based on the object's type, not the reference type.

```java
class Animal {
    void makeSound() {
        System.out.println("Animal makes a sound");
    }
}

class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println("Dog barks");
    }
}

class Cat extends Animal {
    @Override
    void makeSound() {
        System.out.println("Cat meows");
    }
}

public class Example {
    public static void main(String[] args) {
        Animal myPet;
        
        myPet = new Dog();
        myPet.makeSound();  // "Dog barks"
        
        myPet = new Cat();
        myPet.makeSound();  // "Cat meows"
    }
}
```

✅ **Key Point**: Dynamic dispatch is essential for polymorphism in Java, allowing you to write flexible, extensible code.

💡 **Remember**: The variable type determines which methods you can call, but the object type determines which implementation gets executed.

----------


## 3. 🔍 The Method Resolution Process

When a method is called, Java follows these steps to resolve which method to execute:

1. Check if the method exists in the reference type
2. If not found, check in each superclass going up the inheritance chain
3. If found in multiple places, determine if it's a static or instance method
4. For instance methods:
   - If the method is overridden, use the actual object's implementation (dynamic dispatch)
   - If not overridden, use the implementation from the reference type

```java
class Base {
    void method1() { System.out.println("Base method1"); }
    void method2() { System.out.println("Base method2"); }
}

class Middle extends Base {
    @Override
    void method1() { System.out.println("Middle method1"); }
    void method3() { System.out.println("Middle method3"); }
}

class Derived extends Middle {
    @Override
    void method1() { System.out.println("Derived method1"); }
    @Override
    void method3() { System.out.println("Derived method3"); }
}

public class ResolutionExample {
    public static void main(String[] args) {
        Base obj = new Derived();
        obj.method1();  // "Derived method1" - overridden twice
        obj.method2();  // "Base method2" - not overridden
        // obj.method3();  // Compile Error: method3 not in Base
    }
}
```

❌ **Common Mistake**: Assuming method calls are resolved based only on the reference type. Remember that overridden methods use the actual object's implementation!

⚠️ **Interview Trap**: Interviewers often test whether you understand that the reference type determines which methods are accessible, while the object type determines which implementation gets called.

----------


## 4. 🧩 Method Hiding vs. Method Overriding

Method hiding (static methods) and method overriding (instance methods) behave differently with respect to dynamic dispatch:

```java
class Parent {
    static void staticMethod() {
        System.out.println("Parent static method");
    }
    
    void instanceMethod() {
        System.out.println("Parent instance method");
    }
}

class Child extends Parent {
    // This HIDES the parent's static method
    static void staticMethod() {
        System.out.println("Child static method");
    }
    
    // This OVERRIDES the parent's instance method
    @Override
    void instanceMethod() {
        System.out.println("Child instance method");
    }
}

public class HidingVsOverriding {
    public static void main(String[] args) {
        Parent p = new Child();
        p.staticMethod();    // "Parent static method" (method hiding)
        p.instanceMethod();  // "Child instance method" (method overriding)
        
        Child c = new Child();
        c.staticMethod();    // "Child static method"
    }
}
```

📌 **Interview Insight**: Static methods can't be overridden because they belong to classes, not objects. They can only be hidden. This is a common interview question!

🚫 **Watch Out**: Static methods don't participate in polymorphism - they're bound at compile time based on the reference type.

----------


## 5. ⚠️ Common Pitfalls and Edge Cases

### Overloaded vs. Overridden Methods 🔄

```java
class Base {
    void print(String s) {
        System.out.println("Base: " + s);
    }
}

class Derived extends Base {
    // Overloaded method (different parameter)
    void print(int i) {
        System.out.println("Derived: " + i);
    }
    
    // Overridden method (same signature)
    @Override
    void print(String s) {
        System.out.println("Derived override: " + s);
    }
}

public class OverloadingExample {
    public static void main(String[] args) {
        Base b = new Derived();
        b.print("Hello");  // "Derived override: Hello" (overridden)
        // b.print(42);    // Compile Error: print(int) not in Base
        
        Derived d = new Derived();
        d.print("World");  // "Derived override: World"
        d.print(42);       // "Derived: 42" (overloaded)
    }
}
```

❌ **Common Mistake**: Confusing overloading (different method signatures) with overriding (same signature). Overloaded methods don't participate in dynamic dispatch!

### Private, Final, and Static Methods 🔒

```java
class SuperClass {
    private void privateMethod() {
        System.out.println("SuperClass private method");
    }
    
    final void finalMethod() {
        System.out.println("SuperClass final method");
    }
    
    static void staticMethod() {
        System.out.println("SuperClass static method");
    }
    
    void normalMethod() {
        System.out.println("SuperClass normal method");
        privateMethod();  // Calls SuperClass's privateMethod
    }
}

class SubClass extends SuperClass {
    // This is not overriding, just a new method
    private void privateMethod() {
        System.out.println("SubClass private method");
    }
    
    // Cannot override final methods
    // void finalMethod() { } // Compile error
    
    // This hides the parent's static method
    static void staticMethod() {
        System.out.println("SubClass static method");
    }
    
    @Override
    void normalMethod() {
        System.out.println("SubClass normal method");
        // privateMethod();  // Calls SubClass's privateMethod
    }
}
```

📌 **Interview Insight**: Private methods are not inherited, final methods cannot be overridden, and static methods are hidden, not overridden. These distinctions are crucial for interviews!

💡 **Memory Aid**: 
- Private → Not inherited at all
- Final → Inherited but can't be changed
- Static → Belongs to class, not object

----------


## 6. 🚀 Best Practices

1. ✅ **Use `@Override` annotation** when overriding methods to catch errors at compile time

2. ✅ **Be careful with method overloading** in inheritance hierarchies to avoid confusion

3. ✅ **Understand the difference** between overriding and hiding

4. ✅ **Make methods final** when they shouldn't be overridden to prevent unintended behavior

5. ✅ **Be aware of covariant return types** - an overriding method can return a subtype of the original return type

```java
class Animal { }
class Dog extends Animal { }

class AnimalShelter {
    Animal getAnimal() {
        return new Animal();
    }
}

class DogShelter extends AnimalShelter {
    @Override
    Dog getAnimal() {  // Covariant return type
        return new Dog();
    }
}
```

6. ✅ **Create clean hierarchies** where overridden methods have the same semantics to follow the Liskov Substitution Principle

🔍 **Pro Tip**: When designing inheritance hierarchies, make sure overridden methods maintain the contract specified by the parent class. This follows the "L" in SOLID principles.

----------


## 7. 📝 Summary

Dynamic Method Dispatch is a key feature of Java's OOP implementation that enables polymorphism. Here's what you need to remember:

- Method binding can be static (compile-time) or dynamic (runtime)
- Overridden methods use dynamic dispatch based on the actual object type
- Static, private, and final methods don't participate in dynamic dispatch
- Method overloading is resolved at compile time based on reference type
- The `@Override` annotation helps catch errors when overriding methods
- Private methods can't be overridden, only hidden
- Static methods can't be overridden, only hidden
- Final methods can't be overridden at all

This mechanism allows you to write code that works with objects of different types through a common interface, making your code more flexible and maintainable.

💡 **Real-world Example**: Dynamic method dispatch is what powers frameworks like Spring, Hibernate, and Java Collections, where code written against interfaces works with various implementations without knowing the concrete types.

----------


## 8. 📊 Quick Reference Table

| Feature | Method Overriding | Method Hiding | Method Overloading |
|---------|------------------|--------------|-------------------|
| **Applies to** | Instance methods | Static methods | Any methods |
| **Resolution time** | Runtime (dynamic) | Compile time | Compile time |
| **Based on** | Actual object type | Reference type | Reference type & parameters |
| **@Override annotation** | Required/Recommended | Not applicable | Not applicable |
| **Inheritance requirement** | Yes | Yes | No |
| **Same signature** | Yes | Yes | No (parameters differ) |
| **Can add for private methods** | No | Yes | Yes |
| **Can add for final methods** | No | N/A | Yes |

✅ **Quick Check**: For interviews, make sure you understand how the JVM resolves method calls for overridden methods vs. hidden static methods vs. overloaded methods!

🎯 **Interview Focus Areas**:
- Explain polymorphism using dynamic method dispatch
- Differentiate between overriding and overloading
- Explain why static methods can't be overridden
- Describe how final and private methods affect inheritance
