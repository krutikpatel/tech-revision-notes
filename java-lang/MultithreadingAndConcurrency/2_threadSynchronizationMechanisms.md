# Java Multithreading Synchronization Mechanisms 🔒

I'll guide you through the essential synchronization mechanisms in Java with a focus on interview preparation.

## 1. 🔐 Synchronized Keyword

The synchronized keyword provides intrinsic locking to prevent multiple threads from executing critical sections simultaneously.

### Synchronized Methods

```java
public class Counter {
    private int count = 0;
    
    // Method-level synchronization
    public synchronized void increment() {
        count++;
    }
    
    public synchronized int getCount() {
        return count;
    }
}
```

✅ **Pros**: Simple syntax, automatically acquires/releases lock on the object
❌ **Cons**: Lock granularity is coarse (entire method), can't interrupt lock acquisition

### Synchronized Blocks

```java
public class BetterCounter {
    private int count = 0;
    private final Object lock = new Object(); // Dedicated lock object
    
    public void increment() {
        // Block-level synchronization - more fine-grained
        synchronized(lock) {
            count++;
        }
    }
    
    public int getCount() {
        synchronized(lock) {
            return count;
        }
    }
}
```

✅ **Pros**: Fine-grained control, can use different locks for different parts
❌ **Cons**: Still can't interrupt lock acquisition, no timeout capability

### Class-Level Synchronization

```java
public class StaticCounter {
    private static int count = 0;
    
    // Locks on StaticCounter.class
    public static synchronized void increment() {
        count++;
    }
    
    // Equivalent to:
    public static void incrementAlt() {
        synchronized(StaticCounter.class) {
            count++;
        }
    }
}
```

📌 **Interview Insight**: Know the difference between object lock (`synchronized(this)`) and class lock (`synchronized(ClassName.class)`). They protect different resources and operate independently.

### Common Mistakes with Synchronized

❌ **Using different lock objects for related operations**
```java
// WRONG - using different locks for related operations
public void addItem(Item item) {
    synchronized(lockA) { items.add(item); }
}

public Item removeItem() {
    synchronized(lockB) { return items.remove(0); } // Different lock!
}
```

❌ **Forgetting that local variables don't need synchronization**
```java
public void process() {
    // Unnecessary synchronization - localVar is thread-local
    int localVar = 0;
    synchronized(this) {
        localVar++; // No synchronization needed for local variables
    }
}
```

-----------

## 2. 🔒 Lock Interface and Implementations

The `java.util.concurrent.locks` package provides more flexible locking mechanisms than synchronized.

### Basic Lock Usage

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LockCounter {
    private int count = 0;
    private final Lock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock(); // Explicitly acquire lock
        try {
            count++;
        } finally {
            lock.unlock(); // Always release in finally block
        }
    }
}
```

✅ **Pros**: More features than synchronized (tryLock, interruptible, timed waits)
❌ **Cons**: More verbose, must remember to unlock in finally block

### tryLock() - Non-blocking Attempt

```java
public boolean incrementIfAvailable() {
    if (lock.tryLock()) { // Non-blocking attempt to acquire lock
        try {
            count++;
            return true;
        } finally {
            lock.unlock();
        }
    }
    return false; // Lock wasn't available
}

// With timeout
public boolean incrementWithTimeout() throws InterruptedException {
    if (lock.tryLock(1, TimeUnit.SECONDS)) { // Wait up to 1 second
        try {
            count++;
            return true;
        } finally {
            lock.unlock();
        }
    }
    return false; // Couldn't get lock within timeout
}
```

### Interruptible Lock Acquisition

```java
public void incrementInterruptibly() throws InterruptedException {
    lock.lockInterruptibly(); // Can be interrupted while waiting
    try {
        count++;
    } finally {
        lock.unlock();
    }
}
```

📌 **Interview Insight**: Unlike synchronized, Lock interfaces allow you to:
- Attempt lock acquisition without blocking
- Set a timeout for lock acquisition
- Respond to thread interruption while waiting
- Query lock state or ownership

-----------

## 3. 🔄 ReentrantLock and ReadWriteLock

### ReentrantLock

A reentrant lock allows a thread to acquire the same lock multiple times without blocking itself.

```java
ReentrantLock lock = new ReentrantLock();

public void outerMethod() {
    lock.lock();
    try {
        // Do something
        innerMethod(); // Can acquire same lock again
    } finally {
        lock.unlock();
    }
}

private void innerMethod() {
    lock.lock();
    try {
        // Do something else
    } finally {
        lock.unlock();
    }
}
```

#### Fair vs. Unfair Locking

```java
// Default is unfair (higher throughput)
ReentrantLock unfairLock = new ReentrantLock();

// Fair lock (threads get access in order of arrival)
ReentrantLock fairLock = new ReentrantLock(true);
```

✅ **Pros of Fair Locks**: Prevents thread starvation
❌ **Cons of Fair Locks**: Lower throughput, higher overhead

### ReadWriteLock

Allows multiple concurrent readers but exclusive writers.

```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class CacheData {
    private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Map<String, String> cache = new HashMap<>();
    
    public String read(String key) {
        rwLock.readLock().lock(); // Multiple threads can read simultaneously
        try {
            return cache.get(key);
        } finally {
            rwLock.readLock().unlock();
        }
    }
    
    public void write(String key, String value) {
        rwLock.writeLock().lock(); // Exclusive lock - no readers allowed
        try {
            cache.put(key, value);
        } finally {
            rwLock.writeLock().unlock();
        }
    }
}
```

✅ **Pros**: Increased concurrency for read-heavy workloads
❌ **Cons**: More overhead than simple lock, possible writer starvation

📌 **Interview Insight**: For read-heavy scenarios with occasional updates, ReadWriteLock can significantly improve throughput over standard locks.

### Common Mistakes with Locks

❌ **Forgetting to release locks**
```java
// WRONG - no finally block
public void riskyMethod() {
    lock.lock();
    doSomething(); // If this throws an exception, lock is never released
    lock.unlock();
}
```

❌ **Nested lock acquisition in wrong order (deadlock risk)**
```java
// Thread 1: 
lock1.lock(); lock2.lock(); // Order: 1, 2

// Thread 2: 
lock2.lock(); lock1.lock(); // Order: 2, 1 - DEADLOCK RISK!
```

-----------

## 4. 📢 Conditions

Conditions provide a way for threads to suspend execution (wait) until notified by another thread that some state condition may now be true.

### Basic Condition Usage

```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class BlockingQueue<E> {
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notEmpty = lock.newCondition();
    private final Condition notFull = lock.newCondition();
    private final Queue<E> queue = new LinkedList<>();
    private final int capacity;
    
    public BlockingQueue(int capacity) {
        this.capacity = capacity;
    }
    
    public void put(E item) throws InterruptedException {
        lock.lock();
        try {
            while (queue.size() == capacity) {
                notFull.await(); // Wait until queue is not full
            }
            queue.add(item);
            notEmpty.signal(); // Signal that queue is not empty
        } finally {
            lock.unlock();
        }
    }
    
    public E take() throws InterruptedException {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                notEmpty.await(); // Wait until queue is not empty
            }
            E item = queue.remove();
            notFull.signal(); // Signal that queue is not full
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

### Condition Methods

```java
condition.await(); // Wait indefinitely
condition.await(1, TimeUnit.SECONDS); // Wait with timeout
condition.awaitUninterruptibly(); // Wait without interruption
condition.signal(); // Wake up one waiting thread
condition.signalAll(); // Wake up all waiting threads
```

✅ **Pros**: More explicit control than Object's wait/notify, multiple wait sets per lock
❌ **Cons**: More complex to use correctly, must be used with corresponding lock

📌 **Interview Insight**: Think of Condition objects as specialized "wait queues." Each Condition represents a different reason to wait on the same lock, improving clarity and reducing spurious wakeups.

### Common Mistakes with Conditions

❌ **Using await() without a loop check**
```java
// WRONG - should be in a loop
if (queue.isEmpty()) {
    notEmpty.await(); // Might wake up spuriously or when condition still false
}
```

❌ **Mixing locks and conditions from different objects**
```java
// WRONG - condition must be used with its creating lock
lock1.lock();
try {
    condition2.await(); // Error! condition2 belongs to lock2
} finally {
    lock1.unlock();
}
```

-----------

## 5. ⚛️ Atomic Variables

Atomic variables provide lock-free thread-safe operations on single values using hardware-level atomic instructions.

### Basic Atomic Types

```java
import java.util.concurrent.atomic.*;

// Atomic primitives
AtomicInteger counter = new AtomicInteger(0);
AtomicLong longCounter = new AtomicLong(0);
AtomicBoolean flag = new AtomicBoolean(false);
AtomicReference<User> userRef = new AtomicReference<>(user);

// Common operations
int newValue = counter.incrementAndGet(); // ++counter
int oldValue = counter.getAndIncrement(); // counter++
counter.addAndGet(5); // counter += 5
counter.compareAndSet(10, 20); // if (counter == 10) counter = 20;
```

### Advanced Operations

```java
// Atomic array
AtomicIntegerArray array = new AtomicIntegerArray(10);
array.getAndSet(5, 100); // Index 5 set to 100, returns old value

// Atomic field updater (no need to change class fields)
class User {
    volatile int age;
}

AtomicIntegerFieldUpdater<User> ageUpdater = 
    AtomicIntegerFieldUpdater.newUpdater(User.class, "age");
ageUpdater.incrementAndGet(userObj);

// Atomic operations with functions (Java 8+)
counter.updateAndGet(x -> x * 2); // Double the value atomically
counter.accumulateAndGet(5, (x, y) -> x * y); // Multiply by 5 atomically
```

### Example: Thread-safe Lazy Initialization

```java
public class SafeCache {
    private AtomicReference<ExpensiveObject> ref = new AtomicReference<>();
    
    public ExpensiveObject getInstance() {
        ExpensiveObject current = ref.get();
        if (current == null) {
            ExpensiveObject newObj = new ExpensiveObject();
            // Only one thread will succeed in setting the reference
            if (ref.compareAndSet(null, newObj)) {
                return newObj;
            }
            // Another thread won the race, use their object
            return ref.get();
        }
        return current;
    }
}
```

✅ **Pros**: Better performance than locks for simple operations, no deadlock risk
❌ **Cons**: Limited to single variable operations, complex operations require careful design

📌 **Interview Insight**: Atomic variables are ideal for counters, flags, and references that need thread safety without the overhead of locks.

### Common Mistakes with Atomic Variables

❌ **Assuming compound operations are atomic**
```java
// WRONG - not atomic as a whole operation
if (atomicCounter.get() < MAX_VALUE) {
    atomicCounter.incrementAndGet(); // Race condition between check and increment
}
```

❌ **Using atomic variables when synchronization is needed for multiple variables**
```java
// WRONG - individual operations are atomic but not coordinated
AtomicInteger x = new AtomicInteger(0);
AtomicInteger y = new AtomicInteger(0);

// Thread 1
x.set(1);
y.set(1);

// Thread 2 might see y=1, x=0 - inconsistent state!
```

-----------

## 6. 🛠️ Best Practices for Synchronization

### Choose the Right Tool

✅ **Use synchronized** for simple cases and when you don't need advanced features
```java
// Good for simple protection of internal state
private synchronized void updateState() { /* ... */ }
```

✅ **Use Lock** when you need timeouts, interruptibility, or try-lock behavior
```java
// Good when you need timeout capability
if (lock.tryLock(1, TimeUnit.SECONDS)) { /* ... */ }
```

✅ **Use ReadWriteLock** for read-heavy workloads
```java
// Good for frequently read, occasionally written data
rwLock.readLock().lock();
try { /* read data */ } finally { rwLock.readLock().unlock(); }
```

✅ **Use Atomic variables** for simple independent counters and flags
```java
// Good for standalone counters with no related state
AtomicInteger counter = new AtomicInteger(0);
```

### Avoid Overusing Synchronization

✅ **Use thread-local variables** when possible
```java
private static final ThreadLocal<SimpleDateFormat> dateFormat = 
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));
```

✅ **Use immutable objects** to avoid synchronization entirely
```java
// No synchronization needed - thread safe by design
public final class ImmutablePoint {
    private final int x, y;
    
    public ImmutablePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    public int getX() { return x; }
    public int getY() { return y; }
}
```

### Prevent Deadlocks

✅ **Always acquire locks in a fixed, consistent order**
```java
// Good - consistent ordering
void transferMoney(Account from, Account to, int amount) {
    // Sort by account number to ensure consistent lock order
    Account first = from.getId() < to.getId() ? from : to;
    Account second = from.getId() < to.getId() ? to : from;
    
    synchronized(first) {
        synchronized(second) {
            // Transfer logic
        }
    }
}
```

✅ **Use tryLock with timeout to detect and recover from deadlocks**
```java
boolean tryTransfer(Account from, Account to, int amount) throws InterruptedException {
    if (from.getLock().tryLock(1, TimeUnit.SECONDS)) {
        try {
            if (to.getLock().tryLock(1, TimeUnit.SECONDS)) {
                try {
                    // Transfer logic
                    return true;
                } finally {
                    to.getLock().unlock();
                }
            }
        } finally {
            from.getLock().unlock();
        }
    }
    return false; // Couldn't acquire both locks - potential deadlock avoided
}
```

📌 **Interview Insight**: Always have a strategy for handling deadlocks in your synchronization design. Either prevent them through lock ordering or detect and recover through timeouts.

-----------

## 7. 📋 Quick Summary

1. **Synchronized Keyword**:
   - Method-level: `synchronized void method()`
   - Block-level: `synchronized(object) { }`
   - Simple to use but limited in features

2. **Lock Interface**:
   - Explicit lock/unlock with try-finally pattern
   - Advanced features: tryLock, timed waits, interruptibility
   - More verbose but more powerful than synchronized

3. **ReentrantLock**:
   - Allows re-acquisition by same thread
   - Fair vs. unfair options for lock acquisition order
   - More features than intrinsic locks

4. **ReadWriteLock**:
   - Multiple readers, exclusive writers
   - Optimized for read-heavy workloads
   - Higher throughput in specific scenarios

5. **Conditions**:
   - Alternative to wait/notify with multiple wait sets
   - Must be used with associated lock
   - Always check conditions in loops with await()

6. **Atomic Variables**:
   - Lock-free thread-safe operations
   - Best for simple independent counters/flags
   - Higher performance than locks for basic operations

-----------

## 8. 📊 Quick Reference Table

| Mechanism | Use Cases | Key Methods | Common Pitfalls | Best Practices |
|-----------|-----------|-------------|----------------|----------------|
| **synchronized** | Simple thread safety | `synchronized method()`<br>`synchronized(obj) { }` | • Coarse-grained locking<br>• Can't interrupt/timeout | • Use smallest possible critical sections<br>• Use dedicated lock objects |
| **Lock Interface** | Advanced locking needs | `lock()`<br>`unlock()`<br>`tryLock()`<br>`lockInterruptibly()` | • Forgetting unlock in finally<br>• Deadlocks | • Always use try-finally pattern<br>• Consider tryLock with timeout |
| **ReentrantLock** | Complex locking patterns | Same as Lock +<br>`isHeldByCurrentThread()`<br>`getHoldCount()` | • Lock fairness overhead<br>• Over-nested locks | • Use unfair locks by default<br>• Consider fair for thread starvation |
| **ReadWriteLock** | Read-heavy data access | `readLock().lock()`<br>`writeLock().lock()` | • Writer starvation<br>• Lock downgrading | • Use for read-heavy workloads<br>• Cache the lock objects |
| **Conditions** | Thread signaling | `await()`<br>`signal()`<br>`signalAll()` | • Not using in a loop<br>• Missed signals | • Always check in while loop<br>• Prefer signalAll() when in doubt |
| **Atomic Variables** | Simple independent values | `get()`<br>`set()`<br>`compareAndSet()`<br>`getAndUpdate()` | • Complex compound operations<br>• Related variable updates | • Use for independent counters<br>• Consider AtomicReference for objects |

Remember that the choice of synchronization mechanism should depend on the specific requirements of your application. In interviews, be prepared to discuss the trade-offs between different approaches and justify your choices based on aspects like simplicity, performance, and functionality.