# Java Garbage Collection: Reachability and Object Lifecycle 🗑️

As a senior Java engineer, I'll guide you through the essential concepts of Java's garbage collection system with a focus on object reachability and lifecycle. This knowledge is crucial for Java interviews and daily engineering work.

----------

## 1. 🔄 Object Lifecycle Overview

In Java, objects follow a predictable lifecycle from creation to destruction:

```
[Creation] → [In Use] → [Unreachable] → [Finalized] → [Reclaimed] → [Reused]
```

✅ **Key Stages**:
- **Creation**: Object is instantiated with `new` keyword
- **In Use**: Object is reachable from application roots
- **Unreachable**: No live references to the object exist
- **Finalized**: `finalize()` method has been called (if present)
- **Reclaimed**: Memory has been freed by garbage collector
- **Reused**: Memory space is available for new objects

📌 **Interview Insight**: Understanding this lifecycle is fundamental for debugging memory issues and optimizing application performance.

----------

## 2. 🎯 Reachability States

Java's garbage collector determines object eligibility for collection based on reachability:

```
Strongly Reachable → Softly Reachable → Weakly Reachable → Phantom Reachable → Unreachable
```

### Visual Representation:
```
Root References
     ↓
  [Object A] → [Object B] → [Object C]      [Object D]
     ↑                                          ↑
Direct Reference                         No Path from Roots
(Strongly Reachable)                      (Unreachable)
```

📊 **Reachability Levels**:

| Reachability Level | Description | Reference Type | GC Behavior |
|-------------------|-------------|----------------|------------|
| Strongly Reachable | Direct path from root | Normal references | Never collected while reachable |
| Softly Reachable | Only via SoftReference | java.lang.ref.SoftReference | Collected before OOM error |
| Weakly Reachable | Only via WeakReference | java.lang.ref.WeakReference | Collected on next GC cycle |
| Phantom Reachable | Finalized, only via PhantomReference | java.lang.ref.PhantomReference | Ready for resource cleanup |
| Unreachable | No references | None | Will be collected |

----------

## 3. 💻 Code Examples: Reference Types

Understanding reference types is crucial for controlling object lifecycles:

```java
// Strong reference - standard object reference
Object strongRef = new Object();

// Soft reference - memory-sensitive caching
SoftReference<Object> softRef = new SoftReference<>(new Object());
Object obj = softRef.get(); // May return null if collected

// Weak reference - non-essential references
WeakReference<Object> weakRef = new WeakReference<>(new Object());
Object weakObj = weakRef.get(); // Often null after GC

// Phantom reference - post-finalization cleanup
ReferenceQueue<Object> refQueue = new ReferenceQueue<>();
PhantomReference<Object> phantomRef = 
    new PhantomReference<>(new Object(), refQueue);
// Note: phantomRef.get() always returns null
```

❌ **Common Mistake**: Creating SoftReferences for many large objects, causing delayed OOM errors.

✅ **Best Practice**: Use WeakHashMap for caches where entries should be removed when keys are no longer referenced elsewhere.

----------

## 4. 🧪 Reachability Determination

The JVM uses an algorithm called "Mark and Sweep" to determine object reachability:

```
1. Start from GC roots
2. Follow all references recursively 
3. Mark all visited objects
4. Any unmarked objects are unreachable
```

### Key GC Roots Include:

- Local variables in currently executing methods
- Active Java threads
- Static variables
- JNI references
- Classes loaded by the system classloader

```java
public void demonstrateGCRoots() {
    // Local variable - GC root while method is on stack
    Object localRoot = new Object();
    
    // Static field - GC root until class is unloaded
    MyClass.staticObject = new Object();
    
    // Objects reachable from either root won't be collected
    localRoot.referencedObject = new Object();
}
```

📌 **Interview Tip**: Always be able to identify what constitutes a GC root in Java.

----------

## 5. 📉 Object Finalization

The finalization process occurs before an object is garbage collected:

```java
public class ResourceHolder {
    private Resource resource;
    
    public ResourceHolder() {
        resource = Resource.acquire();
    }
    
    @Override
    protected void finalize() throws Throwable {
        try {
            // Release resources before object is collected
            if (resource != null) {
                resource.release();
            }
        } finally {
            super.finalize();
        }
    }
}
```

❌ **IMPORTANT**: `finalize()` is deprecated since Java 9!

✅ **Better Alternative**: Use try-with-resources or explicit close methods:

```java
// Modern approach with try-with-resources
public void modernResourceManagement() {
    try (Resource resource = Resource.acquire()) {
        // Use resource
    } // Automatically closed when block exits
}
```

⚠️ **Warning**: Relying on finalization can cause:
- Unpredictable garbage collection timing
- Performance issues
- Resource leaks
- Objects resurrecting themselves

----------

## 6. 🔍 Memory Leaks and Reachability

Memory leaks in Java occur when objects remain reachable but are no longer needed:

```java
public class LeakExample {
    // Static collection - objects added here remain reachable forever
    private static final List<Object> leakyStorage = new ArrayList<>();
    
    public void potentialLeak() {
        // This object will never be garbage collected
        LargeObject obj = new LargeObject();
        leakyStorage.add(obj);
    }
}
```

### Common Memory Leak Scenarios:

1. **Static Collections**: Objects in static collections remain reachable
2. **Unclosed Resources**: Streams, connections not properly closed
3. **Inner Classes**: Implicit reference to outer class
4. **ThreadLocal Variables**: Not properly removed
5. **Cached Objects**: Forgotten or unbounded caches

✅ **Best Practice**: Use memory profilers like VisualVM, JProfiler, or YourKit to identify memory leaks.

----------

## 7. 🚀 Practical Interview-Ready Code

### Example 1: Custom Cache with WeakReferences

```java
public class WeakCache<K, V> {
    private final Map<K, WeakReference<V>> cache = 
        new ConcurrentHashMap<>();
        
    public V get(K key) {
        WeakReference<V> ref = cache.get(key);
        return (ref != null) ? ref.get() : null;
    }
    
    public void put(K key, V value) {
        cache.put(key, new WeakReference<>(value));
    }
    
    // Clear null references periodically
    public void cleanupNullReferences() {
        cache.entrySet().removeIf(entry -> entry.getValue().get() == null);
    }
}
```

### Example 2: Detecting Objects Pending Garbage Collection

```java
public class GCNotificationExample {
    public static void main(String[] args) {
        // Create a reference queue
        ReferenceQueue<Object> queue = new ReferenceQueue<>();
        
        // Create a phantom reference to track object
        Object obj = new Object();
        PhantomReference<Object> phantomRef = 
            new PhantomReference<>(obj, queue);
            
        // Make object eligible for GC
        obj = null;
        System.gc(); // Request GC
        
        // Check if object was reclaimed
        Reference<?> polledRef = queue.poll();
        System.out.println("Object collected: " + (polledRef != null));
    }
}
```

----------

## 8. ⚠️ Common Traps and Mistakes

1. **Resurrection**: Objects "coming back to life" in finalize()

```java
public class ResurrectionExample {
    private static ResurrectionExample instance;
    
    @Override
    protected void finalize() {
        // DANGEROUS: resurrects this object
        instance = this;
    }
}
```

2. **Memory Leaks in Listeners/Observers**:

```java
public class LeakyListener {
    public void start() {
        EventSource source = EventSource.getInstance();
        // Registers this instance but never unregisters
        source.addListener(new EventListener() {
            public void onEvent(Event e) {
                // Handle event
            }
        });
    }
}
```

3. **ClassLoader Leaks**: Preventing classes from being unloaded

✅ **Fix**: Always unregister listeners, use WeakReferences for callbacks

----------

## 9. 🏆 Best Practices

1. **Minimize Strong References**:
   - Use local variables when possible
   - Clean up after operations complete
   - Use appropriate reference types for caches and lookup tables

2. **Explicitly Null References**:
   - Only when objects are large and won't be used for a while
   - Particularly important in long-running methods

3. **Avoid Finalizers**:
   - Use try-with-resources instead
   - Implement AutoCloseable for resource management

4. **Use Weak Collections**:
   - WeakHashMap
   - Collections wrapped with WeakReferences

5. **Memory Usage Monitoring**:
   - Regular profiling
   - JVM metrics monitoring

----------

## 10. 🔑 Summary

Java's garbage collection system relies on object reachability to determine what memory can be reclaimed. Understanding the object lifecycle and different reference types enables you to write memory-efficient applications and diagnose issues effectively.

### Quick Revision Table

| Concept | Key Points |
|---------|------------|
| **Object Lifecycle** | Creation → In Use → Unreachable → Finalized → Reclaimed |
| **Reachability Levels** | Strong → Soft → Weak → Phantom → Unreachable |
| **GC Roots** | Local vars, static fields, active threads, JNI refs |
| **Reference Types** | Strong, SoftReference, WeakReference, PhantomReference |
| **Memory Leaks** | Static collections, unclosed resources, inner classes |
| **Best Practices** | Minimize strong refs, avoid finalizers, use WeakHashMap |
| **Common Errors** | Object resurrection, listener leaks, unbounded caches |

📌 **Interview Bottom Line**: Understanding object reachability is fundamental to Java memory management and performance optimization. Be prepared to discuss the trade-offs between reference types and demonstrate knowledge of common memory leak patterns.