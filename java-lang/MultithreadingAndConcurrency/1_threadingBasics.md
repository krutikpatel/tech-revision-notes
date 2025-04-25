# Java Multithreading and Concurrency for Interviews 🧵

I'll guide you through these essential multithreading concepts with a focus on interview preparation. Let's break it down into clear, bite-sized sections.

## 1. 🚀 Creating Threads: Thread vs Runnable vs Callable

### Thread Class

The most direct way to create a thread is by extending the `Thread` class:

```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
    
    public static void main(String[] args) {
        MyThread thread = new MyThread();
        thread.start(); // Starts the thread
    }
}
```

✅ **Pros**: Simple implementation
❌ **Cons**: Java doesn't support multiple inheritance, so extending Thread limits your class hierarchy

### Runnable Interface

Implementing the `Runnable` interface is generally preferred:

```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Thread running: " + Thread.currentThread().getName());
    }
    
    public static void main(String[] args) {
        Thread thread = new Thread(new MyRunnable());
        thread.start(); // Starts the thread
    }
}
```

✅ **Pros**: Allows your class to extend other classes, better for OOP design
✅ **Pros**: Can pass the same Runnable to multiple threads
❌ **Cons**: Cannot return results or throw checked exceptions

### Callable Interface

For tasks that need to return results or throw exceptions:

```java
import java.util.concurrent.*;

public class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "Thread result: " + Thread.currentThread().getName();
    }
    
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Future<String> future = executor.submit(new MyCallable());
        
        String result = future.get(); // Blocks until result is available
        System.out.println(result);
        
        executor.shutdown();
    }
}
```

✅ **Pros**: Can return results and throw checked exceptions
✅ **Pros**: Works with ExecutorService for advanced thread management
❌ **Cons**: More complex implementation than Runnable

📌 **Interview Insight**: Know when to use each approach:
- Use `Thread` for simple, standalone threads (rare in practice)
- Use `Runnable` for most general threading needs
- Use `Callable` when you need return values or exception handling

-----------

## 2. ⏱️ Thread Lifecycle and States

A Java thread goes through various states during its lifecycle:

```
NEW → RUNNABLE → [BLOCKED/WAITING/TIMED_WAITING] → TERMINATED
```

### Thread States Detailed

1. **NEW**: Thread created but not started yet
   ```java
   Thread t = new Thread(); // Thread is NEW
   ```

2. **RUNNABLE**: Thread is executing or ready to execute
   ```java
   t.start(); // Thread becomes RUNNABLE
   ```

3. **BLOCKED**: Thread waiting to acquire a monitor lock
   ```java
   synchronized(object) { /* Thread may be BLOCKED here */ }
   ```

4. **WAITING**: Thread waiting indefinitely for another thread
   ```java
   object.wait(); // Thread enters WAITING state
   ```

5. **TIMED_WAITING**: Thread waiting for a specified time
   ```java
   Thread.sleep(1000); // Thread in TIMED_WAITING for 1 second
   ```

6. **TERMINATED**: Thread completed execution
   ```java
   // After run() method completes
   ```

You can check a thread's state:
```java
Thread.State state = thread.getState();
System.out.println("Current state: " + state);
```

ASCII Diagram of Thread Lifecycle:
```
              start()               
  NEW ──────────────────→ RUNNABLE ─────────→ TERMINATED
                             ↑  ↓
                             │  │ block/wait
                             │  ↓
                     notify, │  BLOCKED/    
                     timeout │  WAITING/  
                             │  TIMED_WAITING
```

📌 **Interview Insight**: Understand that RUNNABLE doesn't guarantee execution - it means the thread is eligible for execution. The actual scheduling depends on the JVM/OS.

-----------

## 3. 🔄 start() vs run()

### start() Method

```java
Thread thread = new Thread(() -> System.out.println("Task executing"));
thread.start(); // Creates a new thread and executes run() in that thread
```

### run() Method

```java
Thread thread = new Thread(() -> System.out.println("Task executing"));
thread.run(); // Executes run() in the current thread - no new thread created!
```

✅ **Key Differences**:
- `start()`: Creates a new thread and calls `run()` in that new thread
- `run()`: Simply calls the method in the current thread (no multithreading)

❌ **Common Mistake**: Calling `run()` directly instead of `start()` when multithreading is intended

📌 **Interview Insight**: Calling `start()` twice on the same Thread object throws `IllegalThreadStateException`. You need to create a new Thread object if you want to start again.

-----------

## 4. 🔖 Thread Priorities and Daemon Threads

### Thread Priorities

Thread priorities range from 1 (MIN_PRIORITY) to 10 (MAX_PRIORITY), with 5 (NORM_PRIORITY) as default:

```java
Thread thread = new Thread(runnable);
thread.setPriority(Thread.MAX_PRIORITY); // Set to highest priority (10)

// Constants available:
// Thread.MIN_PRIORITY (1)
// Thread.NORM_PRIORITY (5)
// Thread.MAX_PRIORITY (10)
```

⚠️ **Important**: Thread priorities are just hints to the scheduler, not guarantees! Different platforms/JVMs handle priorities differently.

### Daemon Threads

Daemon threads are background threads that don't prevent the JVM from exiting:

```java
Thread thread = new Thread(runnable);
thread.setDaemon(true); // Must be called before start()
thread.start();
```

✅ **Characteristics**:
- JVM exits when only daemon threads remain
- Typical usage: garbage collection, housekeeping tasks
- Any thread created by a daemon thread is also a daemon thread

❌ **Common Mistake**: Setting daemon status after calling `start()` throws `IllegalThreadStateException`

📌 **Interview Insight**: If your application has only daemon threads running, the JVM will exit. This is important for service applications that might otherwise hang on exit.

-----------

## 5. 📋 Common Interview Pitfalls and Best Practices

### Common Mistakes

❌ **Extending Thread when implementing Runnable would be better**
```java
// Avoid this when you also need to extend another class
public class MyClass extends Thread { /*...*/ }

// Better approach
public class MyClass extends BaseClass implements Runnable { /*...*/ }
```

❌ **Race Conditions**: Multiple threads accessing/modifying shared data

```java
// Problematic code
public class Counter {
    private int count = 0;
    
    // Not thread-safe!
    public void increment() {
        count++;  // This is not an atomic operation!
    }
}
```

❌ **Deadlocks**: Two or more threads waiting for each other

```java
// Potential deadlock
synchronized(resourceA) {
    // Do something
    synchronized(resourceB) {
        // Do something else
    }
}

// Another thread might do:
synchronized(resourceB) {
    // Do something
    synchronized(resourceA) {
        // Both threads now waiting for each other's resource
    }
}
```

### Best Practices

✅ **Use higher-level concurrency utilities when possible**
```java
// Instead of managing threads directly:
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(task);
```

✅ **Prefer immutable objects for thread safety**
```java
// Thread-safe because it's immutable
public final class ImmutableValue {
    private final int value;
    
    public ImmutableValue(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    // No setters, only creates new objects
    public ImmutableValue add(int more) {
        return new ImmutableValue(value + more);
    }
}
```

✅ **Use proper synchronization mechanisms**
```java
// Using synchronized keyword
public synchronized void increment() {
    count++;
}

// Or lock objects
private final Object lock = new Object();
public void increment() {
    synchronized(lock) {
        count++;
    }
}

// Or concurrent collections
import java.util.concurrent.ConcurrentHashMap;
Map<String, String> threadSafeMap = new ConcurrentHashMap<>();
```

✅ **Use atomic classes for simple counters**
```java
import java.util.concurrent.atomic.AtomicInteger;

public class Counter {
    private AtomicInteger count = new AtomicInteger(0);
    
    public void increment() {
        count.incrementAndGet(); // Atomic operation
    }
}
```

📌 **Interview Insight**: Be prepared to discuss thread safety strategies and when to use each approach.

-----------

## 6. 🔍 Quick Summary

1. **Thread Creation Options**:
   - Extend `Thread`: Simple but limits inheritance
   - Implement `Runnable`: Flexible, preferred for most cases
   - Implement `Callable`: Use when needing return values or exceptions

2. **Thread Lifecycle**:
   - NEW → RUNNABLE → BLOCKED/WAITING/TIMED_WAITING → TERMINATED

3. **start() vs run()**:
   - `start()`: Creates new thread and calls run() in that thread
   - `run()`: Executes in current thread (no new thread created)

4. **Priorities and Daemon Threads**:
   - Priorities (1-10): Just hints, not guarantees
   - Daemon threads: Background threads that don't block JVM exit

5. **Best Practices**:
   - Use high-level concurrency utilities (ExecutorService)
   - Apply proper synchronization
   - Prefer immutable objects for thread sharing
   - Use atomic variables for counters
   - Avoid extending Thread when possible

-----------

## 7. 📊 Quick Reference Table

| Concept | Key Points | Common Pitfalls |
|---------|------------|----------------|
| **Thread Creation** | • Thread (extend)<br>• Runnable (implement)<br>• Callable (with return values) | • Overuse of Thread extension<br>• Not choosing Callable when returns needed |
| **Thread Lifecycle** | • NEW → RUNNABLE → BLOCKED/WAITING → TERMINATED | • Assuming RUNNABLE means thread is executing<br>• Not handling interrupted exceptions |
| **start() vs run()** | • start(): Creates new thread<br>• run(): Executes in current thread | • Calling run() instead of start()<br>• Calling start() twice on same thread |
| **Thread Priorities** | • Range 1-10 (default 5)<br>• Just hints to scheduler | • Assuming priorities guarantee execution order<br>• Platform-dependent behavior |
| **Daemon Threads** | • Don't prevent JVM exit<br>• Must set before start() | • Setting daemon status after start()<br>• Using for critical operations |
| **Thread Safety** | • Synchronization<br>• Atomic variables<br>• Concurrent collections<br>• Immutability | • Race conditions<br>• Deadlocks<br>• Over-synchronization causing contention |

Remember to focus on understanding the concepts rather than memorizing the code. Interviewers typically want to assess your understanding of when and why to use different threading approaches and how to avoid common pitfalls.