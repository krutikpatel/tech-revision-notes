# Java Thread Coordination for Interviews 🧵

I'll guide you through the essential concepts of thread coordination in Java with clear examples and interview-focused insights.

## 1. 🔄 wait(), notify(), notifyAll() (Object Methods)

These methods, defined in the `Object` class, provide the fundamental mechanism for thread communication and coordination in Java.

### wait()

Makes the current thread wait until another thread calls `notify()` or `notifyAll()` on the same object.

```java
synchronized (sharedObject) {
    while (!condition) {
        try {
            sharedObject.wait(); // Releases the lock and waits
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    // Process when condition is true
}
```

### notify()

Wakes up a single thread waiting on the object.

```java
synchronized (sharedObject) {
    // Change the condition
    condition = true;
    sharedObject.notify(); // Wake up ONE waiting thread
}
```

### notifyAll()

Wakes up ALL threads waiting on the object.

```java
synchronized (sharedObject) {
    // Change the condition
    condition = true;
    sharedObject.notifyAll(); // Wake up ALL waiting threads
}
```

✅ **Key Points**:
- These methods **must** be called from within a synchronized block/method on the object
- `wait()` releases the lock while waiting
- Always use `wait()` in a loop that checks the condition

❌ **Common Mistakes**:
- Calling without synchronization (throws `IllegalMonitorStateException`)
```java
// WRONG
sharedObject.wait(); // Not in synchronized block!

// CORRECT
synchronized (sharedObject) {
    sharedObject.wait();
}
```
- Using `if` instead of `while` for condition check
```java
// WRONG - doesn't recheck condition
synchronized (sharedObject) {
    if (!condition) {
        sharedObject.wait(); // Spurious wakeup risk!
    }
}

// CORRECT - recheck condition after waking
synchronized (sharedObject) {
    while (!condition) {
        sharedObject.wait();
    }
}
```

📌 **Interview Insight**: The use of a while loop protects against **spurious wakeups** - when a thread wakes up without being notified, interrupted, or timing out.

-----------

## 2. ⏱️ join(), yield(), sleep() (Thread Methods)

These methods provide additional control over thread execution.

### join()

Waits for a thread to die. Useful when you need one thread to complete before continuing.

```java
Thread worker = new Thread(() -> {
    // Perform task
});
worker.start();

try {
    worker.join(); // Current thread waits for worker to finish
    // Or with timeout
    worker.join(1000); // Wait up to 1 second
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### yield()

Hints to the scheduler that the current thread is willing to yield its current use of CPU.

```java
// Suggest to scheduler that other threads can run
Thread.yield();
```

### sleep()

Makes the current thread pause execution for a specified time.

```java
try {
    // Pause for 2 seconds
    Thread.sleep(2000);
    
    // More precise: sleep for 2 seconds and 500 milliseconds
    Thread.sleep(2000, 500000); // milliseconds, nanoseconds
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

✅ **Key Differences**:
- `join()`: Waits for another thread to complete
- `yield()`: Just a hint to the scheduler, no guarantees
- `sleep()`: Pauses the current thread for a specified time

❌ **Common Mistakes**:
- Ignoring or swallowing `InterruptedException`
```java
// WRONG
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    // Empty catch - lost interruption status!
}

// CORRECT
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt(); // Preserve interrupt status
}
```
- Thinking `yield()` guarantees thread switching
```java
// WRONG - yield() is just a hint
doPartialWork();
Thread.yield(); // No guarantee other threads will execute
doMoreWork();
```

📌 **Interview Insight**: Both `sleep()` and `wait()` pause a thread, but `sleep()` doesn't release locks while `wait()` does. This is a common interview question!

-----------

## 3. 🔄 Producer-Consumer Problem Implementation

The producer-consumer pattern is a classic multithreading scenario where one thread produces data that another thread consumes.

### Using wait() and notifyAll()

```java
public class SharedBuffer {
    private final Queue<Integer> queue = new LinkedList<>();
    private final int capacity;
    
    public SharedBuffer(int capacity) {
        this.capacity = capacity;
    }
    
    public synchronized void produce(int item) throws InterruptedException {
        while (queue.size() == capacity) {
            // Queue full, wait for consumer to take items
            wait();
        }
        queue.add(item);
        System.out.println("Produced: " + item);
        // Notify consumers that data is available
        notifyAll();
    }
    
    public synchronized Integer consume() throws InterruptedException {
        while (queue.isEmpty()) {
            // Queue empty, wait for producer to add items
            wait();
        }
        Integer item = queue.poll();
        System.out.println("Consumed: " + item);
        // Notify producers that space is available
        notifyAll();
        return item;
    }
}

// Usage
public class ProducerConsumerExample {
    public static void main(String[] args) {
        SharedBuffer buffer = new SharedBuffer(5);
        
        // Producer thread
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    buffer.produce(i);
                    Thread.sleep(100); // Simulate work
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    buffer.consume();
                    Thread.sleep(200); // Simulate work
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
    }
}
```

### Using BlockingQueue (Modern Approach)

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ModernProducerConsumer {
    public static void main(String[] args) {
        // Thread-safe queue with built-in blocking operations
        BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(5);
        
        // Producer thread
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    queue.put(i); // Blocks if queue is full
                    System.out.println("Produced: " + i);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    Integer item = queue.take(); // Blocks if queue is empty
                    System.out.println("Consumed: " + item);
                    Thread.sleep(200);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
    }
}
```

✅ **Key Points**:
- Producer waits when the buffer is full
- Consumer waits when the buffer is empty
- Notification happens after state changes

❌ **Common Mistakes**:
- Using `notify()` instead of `notifyAll()`
```java
// WRONG - might miss waking up threads that need to run
queue.add(item);
notify(); // Only wakes one random thread

// CORRECT - wakes all waiting threads
queue.add(item);
notifyAll(); // Ensures both consumers and producers can check conditions
```
- Not using a bounded buffer (capacity limit)
```java
// WRONG - unbounded queue can cause OutOfMemoryError
private final Queue<Integer> queue = new LinkedList<>();

// CORRECT - bounded queue prevents memory issues
private final Queue<Integer> queue = new LinkedList<>();
private final int capacity = 10;
```

📌 **Interview Insight**: In modern Java applications, prefer higher-level concurrent collections like `BlockingQueue` over low-level `wait()/notify()` for producer-consumer patterns. They handle all synchronization complexities internally.

-----------

## 4. 🧵 ThreadLocal Usage

`ThreadLocal` provides thread-confinement - each thread has its own private copy of a variable, preventing shared state issues.

### Basic Usage

```java
// Declaration and initialization
private static ThreadLocal<SimpleDateFormat> dateFormatter = 
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

// Using the thread-local variable
public String formatDate(Date date) {
    return dateFormatter.get().format(date); // Each thread gets its own formatter
}
```

### ThreadLocal with initialValue() (Legacy approach)

```java
private static ThreadLocal<User> currentUser = new ThreadLocal<User>() {
    @Override
    protected User initialValue() {
        return new User("Guest"); // Default value
    }
};

// Get current thread's value
User user = currentUser.get();

// Set value for current thread
currentUser.set(new User("John"));

// Remove value when done
currentUser.remove();
```

### InheritableThreadLocal

Special variant that passes values from parent to child threads:

```java
private static InheritableThreadLocal<User> userContext = 
    new InheritableThreadLocal<User>() {
        @Override
        protected User initialValue() {
            return new User("Guest");
        }
        
        @Override
        protected User childValue(User parentValue) {
            // Can customize what child threads inherit
            return new User(parentValue.getName() + "-child");
        }
    };

// Child threads will inherit the value from parent thread
userContext.set(new User("Parent"));
Thread childThread = new Thread(() -> {
    // Will have User("Parent-child")
    System.out.println(userContext.get().getName());
});
childThread.start();
```

✅ **Common Use Cases**:
- Thread-safe date formatters
- Per-thread database connections
- Request context in web applications
- User session information

❌ **Common Mistakes**:
- Not cleaning up with `remove()`
```java
// WRONG - potential memory leak in thread pools
threadLocal.set(expensiveObject);
// ... use the value ...
// Missing remove() at the end!

// CORRECT - clean up to avoid memory leaks
threadLocal.set(expensiveObject);
try {
    // ... use the value ...
} finally {
    threadLocal.remove(); // Always clean up in thread pools
}
```
- Using for performance when not needed
```java
// WRONG - unnecessarily complicated for local method use
private static ThreadLocal<StringBuilder> buffer = 
    ThreadLocal.withInitial(StringBuilder::new);

public String buildMessage() {
    StringBuilder sb = buffer.get();
    sb.setLength(0); // Clear for reuse
    sb.append("Hello").append(" World");
    return sb.toString();
}

// CORRECT - just use a local variable
public String buildMessage() {
    StringBuilder sb = new StringBuilder();
    sb.append("Hello").append(" World");
    return sb.toString();
}
```

📌 **Interview Insight**: `ThreadLocal` is excellent for maintaining thread confinement, but be cautious with thread pools where threads are reused. Always call `remove()` when finished to prevent memory leaks.

-----------

## 5. 🚫 Common Thread Coordination Mistakes

### Deadlocks

When two or more threads each wait forever for a resource held by another thread.

```java
// DEADLOCK RISK
synchronized(lockA) {
    // Do something
    synchronized(lockB) {
        // Do something else
    }
}

// In another thread:
synchronized(lockB) {
    // Do something
    synchronized(lockA) {
        // Now we have a deadlock!
    }
}
```

✅ **Prevention**: Always acquire locks in a consistent, fixed order.

### Livelock

Threads keep changing their state in response to another thread's action, preventing progress.

```java
// Example of potential livelock
while (!canProceed()) {
    // Yield to other thread
    Thread.yield();
    // But if other thread also yields, both keep spinning
}
```

✅ **Prevention**: Add randomized backoff times or priorities.

### Lost Wake-Up

A notification is sent before the receiving thread starts waiting.

```java
// WRONG - potential lost wake-up
public void produce(T item) {
    synchronized (this) {
        if (queue.size() == capacity) {
            // Check if queue is full
        } else {
            queue.add(item);
            notify(); // Wake up a consumer
        }
    }
}

public T consume() {
    synchronized (this) {
        if (queue.isEmpty()) {
            try {
                wait(); // Wait for item
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        return queue.poll();
    }
}
```

✅ **Prevention**: Always use wait() in a while loop, not an if statement.

-----------

## 6. 🛠️ Best Practices for Thread Coordination

### Use High-Level Concurrency Utilities

```java
// Instead of low-level wait/notify:
ExecutorService executor = Executors.newFixedThreadPool(10);
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);
CountDownLatch startSignal = new CountDownLatch(1);
CyclicBarrier barrier = new CyclicBarrier(5);
```

### Structured Resource Management

```java
// Using try-finally for locks
Lock lock = new ReentrantLock();
lock.lock();
try {
    // Critical section
} finally {
    lock.unlock(); // Always released
}

// Using try-with-resources for executors (Java 7+)
try (ExecutorService executor = Executors.newFixedThreadPool(10)) {
    // Submit tasks
    executor.submit(task);
    // No need to call shutdown()
}
```

### Timeout Everything

```java
// Always use timeouts for blocking operations
boolean acquired = lock.tryLock(1, TimeUnit.SECONDS);
if (acquired) {
    try {
        // Critical section with guaranteed timeout
    } finally {
        lock.unlock();
    }
} else {
    // Handle timeout case
}
```

### Prefer Interruption for Cancellation

```java
Thread worker = new Thread(() -> {
    while (!Thread.currentThread().isInterrupted()) {
        try {
            // Do work
            Thread.sleep(100); // Responsive to interruption
        } catch (InterruptedException e) {
            // Clean up resources
            Thread.currentThread().interrupt(); // Propagate interrupt
            return; // Exit the thread
        }
    }
});

// Later, to cancel:
worker.interrupt();
```

📌 **Interview Insight**: The ability to discuss these best practices shows a deeper understanding of Java concurrency. Be prepared to explain why these approaches are better than naive implementations.

-----------

## 7. 📝 Quick Summary

1. **Object Methods for Thread Coordination**:
   - `wait()`: Releases lock and waits for notification
   - `notify()`: Wakes up one waiting thread
   - `notifyAll()`: Wakes up all waiting threads
   - Must be called from synchronized context

2. **Thread Methods**:
   - `join()`: Waits for another thread to complete
   - `yield()`: Suggests that other threads can run (just a hint)
   - `sleep()`: Pauses the current thread without releasing locks

3. **Producer-Consumer Pattern**:
   - Classic thread coordination problem
   - Traditional implementation uses wait/notify
   - Modern approach uses BlockingQueue

4. **ThreadLocal**:
   - Provides thread-confined variables
   - Each thread has its own independent copy
   - Must be cleaned up with remove() in thread pools
   - InheritableThreadLocal passes values to child threads

5. **Common Coordination Issues**:
   - Deadlocks: Circular waiting for locks
   - Livelocks: Threads keep responding to each other without progress
   - Lost wake-ups: Notification before waiting
   - Always use wait() in a while loop, not if statement

-----------

## 8. 📊 Quick Reference Table

| Mechanism | Primary Use | Key Methods | Common Pitfalls | Best Practices |
|-----------|-------------|-------------|----------------|----------------|
| **wait/notify** | Thread coordination | `object.wait()`<br>`object.notify()`<br>`object.notifyAll()` | • Not using in synchronized block<br>• Using if instead of while loop<br>• Lost notifications | • Always use within synchronized block<br>• Always use while loop for condition<br>• Prefer notifyAll() over notify() |
| **Thread Methods** | Thread control | `thread.join()`<br>`Thread.yield()`<br>`Thread.sleep()` | • Ignoring InterruptedException<br>• Relying on yield() behavior<br>• sleep() doesn't release locks | • Restore interrupt status<br>• Use sleep() with reasonable timeouts<br>• Use join() when dependent on completion |
| **Producer-Consumer** | Work distribution | `queue.put()`<br>`queue.take()`<br>`queue.offer()`<br>`queue.poll()` | • Unbounded queues<br>• Deadlocks<br>• Inefficient notification | • Use BlockingQueue implementations<br>• Set reasonable capacity<br>• Consider timeout variants of operations |
| **ThreadLocal** | Thread confinement | `threadLocal.get()`<br>`threadLocal.set()`<br>`threadLocal.remove()` | • Memory leaks in thread pools<br>• Overuse for simple variables<br>• Thread escape | • Always call remove() when done<br>• Use withInitial() for initialization<br>• Consider thread pools implications |

For interviews, focus on understanding the mechanisms rather than memorizing API details. Be prepared to identify common concurrency bugs and explain how to solve them using these coordination techniques.