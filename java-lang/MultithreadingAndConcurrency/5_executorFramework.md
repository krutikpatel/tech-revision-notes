# Java Executor Framework for Interviews 🚀

## 1. 🧵 Thread Pools

Thread pools manage a pool of worker threads, reducing the overhead of thread creation and providing more control over the system's resource usage.

### Core Concepts

Thread pools solve several problems with creating threads directly:

✅ **Resource Management**: Limits the number of threads that can exist simultaneously  
✅ **Performance**: Reuses existing threads rather than creating new ones  
✅ **Predictability**: Provides better control over system resources  

### Creating Thread Pools with Executors

Java provides factory methods in the `Executors` class to create different types of thread pools:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// Fixed thread pool with 5 threads
ExecutorService fixedPool = Executors.newFixedThreadPool(5);

// Single-threaded executor
ExecutorService singleThreadExecutor = Executors.newSingleThreadExecutor();

// Cached thread pool that creates threads as needed and reuses idle threads
ExecutorService cachedPool = Executors.newCachedThreadPool();

// Work-stealing pool (Java 8+) - parallelism level equals available processors
ExecutorService workStealingPool = Executors.newWorkStealingPool();
```

### Thread Pool Types and Use Cases

1. **Fixed Thread Pool**
   - Fixed number of threads
   - Requests queue up if all threads are busy
   - Good for: Limiting resource usage, CPU-bound tasks

   ```java
   ExecutorService executor = Executors.newFixedThreadPool(10);
   ```

2. **Cached Thread Pool**
   - Creates new threads as needed
   - Reuses idle threads when available
   - Terminates unused threads after 60 seconds
   - Good for: Many short-lived tasks, I/O-bound work with varying load

   ```java
   ExecutorService executor = Executors.newCachedThreadPool();
   ```

3. **Single Thread Executor**
   - Only one thread executing tasks sequentially
   - Good for: Tasks that must execute in order, single-threaded subsystems

   ```java
   ExecutorService executor = Executors.newSingleThreadExecutor();
   ```

4. **Work Stealing Pool** (Java 8+)
   - Uses Fork/Join framework underneath
   - Each thread has its own queue, can "steal" work from other threads
   - Good for: Tasks that spawn subtasks, recursive algorithms

   ```java
   ExecutorService executor = Executors.newWorkStealingPool();
   ```

### Custom Thread Pool Configuration

For more control, you can use `ThreadPoolExecutor` directly:

```java
import java.util.concurrent.*;

ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5,                          // Core pool size
    10,                         // Maximum pool size
    60L, TimeUnit.SECONDS,      // Keep-alive time for excess idle threads
    new ArrayBlockingQueue<>(100), // Work queue
    new ThreadFactory() {       // Thread factory
        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r);
            t.setDaemon(true);
            t.setName("Worker-" + t.getId());
            return t;
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy() // Rejection policy
);
```

### Thread Pool Lifecycle

```java
// Submit tasks
executor.execute(() -> System.out.println("Task running"));

// Initiate shutdown - stops accepting new tasks
executor.shutdown();

// Wait for tasks to complete (with timeout)
boolean completed = executor.awaitTermination(30, TimeUnit.SECONDS);

// Force shutdown - attempts to stop all executing tasks
executor.shutdownNow();
```

### Common Mistakes with Thread Pools

❌ **Not shutting down the executor**
```java
// WRONG - Executor keeps running, prevents JVM shutdown
ExecutorService executor = Executors.newFixedThreadPool(5);
executor.execute(task);
// Program ends without executor.shutdown()
```

❌ **Using unbounded queues with fixed thread pools**
```java
// WRONG - Can lead to OutOfMemoryError with many tasks
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5, 5, 0L, TimeUnit.MILLISECONDS,
    new LinkedBlockingQueue<>() // Unbounded queue!
);
```

❌ **Using thread pools for blocking tasks without proper sizing**
```java
// WRONG - All threads could block, causing deadlock
// For a database with 10 connections:
ExecutorService executor = Executors.newFixedThreadPool(20);
// If all 20 tasks try to get a connection, 10 will block indefinitely
```

📌 **Interview Insight**: Be prepared to explain how you would size a thread pool. A common formula for CPU-bound tasks is N+1 threads where N is the number of CPU cores. For I/O-bound tasks, you typically want more threads than cores.

-----------

## 2. 🧰 ExecutorService & ScheduledExecutorService

### ExecutorService Basics

`ExecutorService` extends the `Executor` interface, providing methods for managing tasks and executor lifecycle.

```java
ExecutorService executor = Executors.newFixedThreadPool(5);

// Different ways to submit tasks
executor.execute(() -> System.out.println("Simple task")); // No return value

Future<String> future = executor.submit(() -> {
    // Do some work
    return "Result";
}); // Returns a Future

List<Callable<String>> tasks = Arrays.asList(
    () -> "Task 1 result",
    () -> "Task 2 result",
    () -> "Task 3 result"
);

// Execute multiple tasks
List<Future<String>> futures = executor.invokeAll(tasks); // Wait for all
String firstResult = executor.invokeAny(tasks); // Wait for any one
```

### ScheduledExecutorService - Delayed and Periodic Tasks

`ScheduledExecutorService` extends `ExecutorService` to support scheduled and periodic task execution.

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

// Schedule a task to run after a delay
ScheduledFuture<?> future1 = scheduler.schedule(
    () -> System.out.println("Delayed task"),
    10, TimeUnit.SECONDS
);

// Schedule a task to run periodically
ScheduledFuture<?> future2 = scheduler.scheduleAtFixedRate(
    () -> System.out.println("Periodic task"),
    5,   // Initial delay
    20,  // Period between starts
    TimeUnit.SECONDS
);

// Schedule with fixed delay between task completions
ScheduledFuture<?> future3 = scheduler.scheduleWithFixedDelay(
    () -> System.out.println("Fixed delay task"),
    0,   // Initial delay
    10,  // Delay between task completion and next start
    TimeUnit.SECONDS
);

// Cancel a scheduled task
future2.cancel(false);
```

### Fixed Rate vs. Fixed Delay

```
scheduleAtFixedRate:
[Task1]-----[Task2]-----[Task3]-----
|     |     |     |     |     |
0s    5s    10s   15s   20s   25s
(Tasks start at fixed intervals)

scheduleWithFixedDelay (assuming each task takes 2s):
[Task1]--[10s]--[Task2]--[10s]--[Task3]--
|    |           |    |           |    |
0s   2s          12s  14s         24s  26s
(Delay starts after task completion)
```

### ExecutorService Exception Handling

```java
ExecutorService executor = Executors.newFixedThreadPool(1);

// Exceptions in execute() are sent to the thread's UncaughtExceptionHandler
Thread.setDefaultUncaughtExceptionHandler((t, e) -> {
    System.err.println("Thread " + t.getName() + " threw exception: " + e);
});

// Exceptions in submit() are captured in the Future
Future<String> future = executor.submit(() -> {
    if (true) throw new RuntimeException("Task failed");
    return "Success";
});

try {
    String result = future.get(); // Exception will be thrown here
} catch (ExecutionException e) {
    Throwable actualException = e.getCause();
    System.err.println("Task failed: " + actualException);
}
```

### Common Mistakes with ExecutorService

❌ **Not handling task exceptions properly**
```java
// WRONG - Exception is swallowed and not reported anywhere
executor.submit(() -> {
    throw new RuntimeException("This exception is lost"); 
});
```

❌ **Not checking cancellation status in long-running tasks**
```java
// WRONG - Task does not respect cancellation
Future<?> future = executor.submit(() -> {
    while (true) { // Never checks for interruption
        doWork();
    }
});
future.cancel(true); // Interrupts but task keeps running
```

❌ **Blocking in scheduleAtFixedRate tasks**
```java
// WRONG - Can cause starvation or OOM if tasks take longer than period
scheduler.scheduleAtFixedRate(() -> {
    try {
        Thread.sleep(2000); // Task takes 2 seconds
    } catch (InterruptedException e) {}
}, 0, 1, TimeUnit.SECONDS); // But scheduled every 1 second
```

✅ **Best Practices**:
- Use `scheduleWithFixedDelay` for tasks that might take longer than their period
- Always handle exceptions in scheduled tasks
- Implement proper cancellation checks in long-running tasks

📌 **Interview Insight**: A good understanding of the difference between `scheduleAtFixedRate` and `scheduleWithFixedDelay` demonstrates attention to detail that interviewers value.

-----------

## 3. 🔄 Future and FutureTask

### Future Interface

The `Future` interface represents the result of an asynchronous computation.

```java
ExecutorService executor = Executors.newSingleThreadExecutor();

// Submit a task that returns a result
Future<Integer> future = executor.submit(() -> {
    Thread.sleep(1000);
    return 42;
});

try {
    // Check if completed without blocking
    boolean isDone = future.isDone();
    
    // Wait for the result with a timeout
    Integer result = future.get(2, TimeUnit.SECONDS);
    System.out.println("Result: " + result);
    
    // Cancel the task if not started
    boolean canceled = future.cancel(true);
    
    // Check if task was canceled
    boolean isCanceled = future.isCancelled();
} catch (InterruptedException e) {
    // Current thread was interrupted
} catch (ExecutionException e) {
    // Task threw an exception
    Throwable cause = e.getCause();
} catch (TimeoutException e) {
    // Timeout occurred before completion
    future.cancel(true); // Try to cancel the task
}
```

### FutureTask Class

`FutureTask` is a concrete implementation of `Future` that also implements `Runnable`, so it can be executed by a thread or submitted to an executor.

```java
// Create a FutureTask with a Callable
FutureTask<String> futureTask = new FutureTask<>(() -> {
    Thread.sleep(1000);
    return "Result from FutureTask";
});

// Execute directly with a thread
new Thread(futureTask).start();

// Or submit to an executor
executor.execute(futureTask);

// Get the result (blocks until available)
String result = futureTask.get();
```

### Implementing Custom Futures with FutureTask

```java
public class CallbackFutureTask<V> extends FutureTask<V> {
    private final Runnable callback;
    
    public CallbackFutureTask(Callable<V> callable, Runnable callback) {
        super(callable);
        this.callback = callback;
    }
    
    @Override
    protected void done() {
        callback.run();
    }
}

// Usage
CallbackFutureTask<Integer> task = new CallbackFutureTask<>(
    () -> performComputation(),
    () -> System.out.println("Task completed")
);
executor.execute(task);
```

### Limitations of Futures

❌ **Manual composition**
```java
// PROBLEM: Chaining futures is cumbersome
Future<Integer> future1 = executor.submit(() -> 10);
Future<Integer> future2 = executor.submit(() -> {
    int value1 = future1.get(); // Blocks
    return value1 * 2;
});
```

❌ **Awkward exception handling**
```java
// PROBLEM: Must explicitly call get() to see exceptions
Future<String> future = executor.submit(() -> { 
    throw new RuntimeException("Error");
});
// Exception is not thrown until:
try {
    future.get();
} catch (ExecutionException e) {
    // Finally see the exception here
}
```

❌ **No support for completion callbacks**
```java
// PROBLEM: No way to attach a callback to a Future
Future<String> future = executor.submit(task);
// No direct way to run code when future completes
```

### Common Mistakes with Futures

❌ **Forgetting to check for cancellation/interruption**
```java
Future<Result> future = executor.submit(() -> {
    // Long-running task without checking Thread.interrupted()
    while (!done) {
        doWork(); // Won't respond to cancellation
    }
    return result;
});
```

❌ **Blocking on get() without timeout**
```java
// WRONG - May block forever
Future<String> future = executor.submit(task);
String result = future.get(); // No timeout specified
```

✅ **Best Practices**:
- Always use timeouts with `get()`
- Check for interruption in long-running tasks
- Consider `CompletableFuture` for complex operations

📌 **Interview Insight**: Understanding Future's limitations provides good context for why CompletableFuture was introduced in Java 8. Being able to articulate these limitations shows depth of knowledge.

-----------

## 4. 🌟 CompletableFuture (Java 8+)

`CompletableFuture` significantly improves on `Future` by providing a rich set of methods for composition, error handling, and callback registration.

### Creating CompletableFutures

```java
// Create with a value already available
CompletableFuture<String> future1 = CompletableFuture.completedFuture("Result");

// Create an empty future to complete later
CompletableFuture<String> future2 = new CompletableFuture<>();
// Complete it
future2.complete("Result");
// Or complete it exceptionally
future2.completeExceptionally(new RuntimeException("Failed"));

// Run asynchronously with no result
CompletableFuture<Void> future3 = CompletableFuture.runAsync(() -> {
    System.out.println("Running asynchronously");
});

// Supply a value asynchronously
CompletableFuture<String> future4 = CompletableFuture.supplyAsync(() -> {
    return "Result from async computation";
});

// Using a specific executor
ExecutorService executor = Executors.newFixedThreadPool(10);
CompletableFuture<String> future5 = CompletableFuture.supplyAsync(() -> {
    return "Result using custom executor";
}, executor);
```

### Transforming Results (Composition)

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 10);

// Transform the result
CompletableFuture<Integer> doubled = future.thenApply(x -> x * 2);

// Transform with another async operation
CompletableFuture<Integer> asyncDoubled = future.thenApplyAsync(x -> x * 2);

// Transform and flatten (for methods that return CompletableFuture)
CompletableFuture<Integer> composedFuture = future.thenCompose(x -> 
    CompletableFuture.supplyAsync(() -> x * 2)
);
```

### Combining Multiple Futures

```java
CompletableFuture<Integer> future1 = CompletableFuture.supplyAsync(() -> 10);
CompletableFuture<Integer> future2 = CompletableFuture.supplyAsync(() -> 20);

// Combine results when both complete
CompletableFuture<Integer> combined = future1.thenCombine(future2, (x, y) -> x + y);

// Execute after both complete (but don't combine results)
CompletableFuture<Void> allDone = CompletableFuture.allOf(future1, future2);

// Execute after any completes
CompletableFuture<Object> anyDone = CompletableFuture.anyOf(future1, future2);
```

### Error Handling

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    if (Math.random() > 0.5) {
        throw new RuntimeException("Failed");
    }
    return "Success";
});

// Handle exceptions
CompletableFuture<String> handled = future.exceptionally(ex -> {
    System.err.println("Error: " + ex.getMessage());
    return "Default value after error";
});

// Handle both success and failure cases
CompletableFuture<String> result = future.handle((value, ex) -> {
    if (ex != null) {
        return "Error occurred: " + ex.getMessage();
    }
    return "Got value: " + value;
});
```

### Timeout Handling

```java
// Java 9+ has built-in timeout
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(this::longRunningTask)
    .orTimeout(1, TimeUnit.SECONDS); // Completes exceptionally after timeout

// For earlier Java versions:
CompletableFuture<String> futureWithTimeout = new CompletableFuture<>();
CompletableFuture<String> original = CompletableFuture.supplyAsync(this::longRunningTask);

// Set up a scheduled timeout
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
scheduler.schedule(() -> {
    futureWithTimeout.completeExceptionally(new TimeoutException());
}, 1, TimeUnit.SECONDS);

// Complete our future when the original completes
original.thenAccept(futureWithTimeout::complete);
```

### Callbacks and Continuation

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 42);

// Run code when the future completes (with result)
future.thenAccept(result -> System.out.println("Got: " + result));

// Run code when the future completes (ignore result)
future.thenRun(() -> System.out.println("Future completed"));

// Chain multiple operations
future.thenApply(x -> x * 2)
      .thenApply(x -> x + 10)
      .thenAccept(System.out::println);
```

### Real-World Example: Parallel API Calls

```java
public class ApiClient {
    public CompletableFuture<UserData> getUserData(long userId) {
        return CompletableFuture.supplyAsync(() -> {
            // Simulate API call
            return new UserData(userId, "User " + userId);
        });
    }
    
    public CompletableFuture<List<Order>> getUserOrders(long userId) {
        return CompletableFuture.supplyAsync(() -> {
            // Simulate API call
            return Arrays.asList(new Order(1L), new Order(2L));
        });
    }
    
    public CompletableFuture<List<Product>> getRecommendations(UserData user, List<Order> orders) {
        return CompletableFuture.supplyAsync(() -> {
            // Generate recommendations based on user and orders
            return Arrays.asList(new Product(100L), new Product(200L));
        });
    }
}

// Usage: parallelize independent calls
public CompletableFuture<UserProfile> getUserProfile(long userId) {
    ApiClient client = new ApiClient();
    
    CompletableFuture<UserData> userDataFuture = client.getUserData(userId);
    CompletableFuture<List<Order>> ordersFuture = client.getUserOrders(userId);
    
    // Combine independent futures
    return userDataFuture.thenCombine(ordersFuture, (userData, orders) -> {
        // Then process dependent operation
        return client.getRecommendations(userData, orders)
            .thenApply(recommendations -> {
                return new UserProfile(userData, orders, recommendations);
            });
    }).thenCompose(Function.identity()); // Flatten the nested CompletableFuture
}
```

### Common Mistakes with CompletableFuture

❌ **Not specifying executor for async methods**
```java
// WRONG - Uses ForkJoinPool.commonPool() which might not be ideal
CompletableFuture.supplyAsync(() -> heavyTask());

// BETTER - Use a specific executor
ExecutorService executor = Executors.newFixedThreadPool(20);
CompletableFuture.supplyAsync(() -> heavyTask(), executor);
```

❌ **Confusion between thenApply vs thenCompose**
```java
// WRONG - Creates a CompletableFuture<CompletableFuture<String>>
CompletableFuture<CompletableFuture<String>> wrongNested = 
    CompletableFuture.supplyAsync(() -> "first")
                     .thenApply(result -> CompletableFuture.supplyAsync(
                         () -> result + " second"));

// CORRECT - Creates a flattened CompletableFuture<String>
CompletableFuture<String> correctFlattened = 
    CompletableFuture.supplyAsync(() -> "first")
                     .thenCompose(result -> CompletableFuture.supplyAsync(
                         () -> result + " second"));
```

❌ **Ignoring exceptions**
```java
// WRONG - Exception handling is omitted
CompletableFuture.supplyAsync(() -> riskyOperation())
                 .thenApply(this::moreProcessing);

// CORRECT - Handle exceptions
CompletableFuture.supplyAsync(() -> riskyOperation())
                 .exceptionally(ex -> fallbackValue())
                 .thenApply(this::moreProcessing);
```

✅ **Best Practices**:
- Use a dedicated executor rather than relying on the common pool
- Understand the difference between `thenApply` (map) and `thenCompose` (flatMap)
- Always handle exceptions with `exceptionally` or `handle`
- Remember that async operations complete in different threads

📌 **Interview Insight**: CompletableFuture proficiency is highly valued in interviews. Understanding the difference between synchronous methods (thenApply, thenAccept) and their async variants (thenApplyAsync, thenAcceptAsync) shows deep understanding.

-----------

## 5. 🎯 Best Practices for the Executor Framework

### Thread Pool Sizing

```java
// CPU-bound tasks: N+1 threads (where N is the number of CPU cores)
int cpuCores = Runtime.getRuntime().availableProcessors();
ExecutorService cpuBoundPool = Executors.newFixedThreadPool(cpuCores + 1);

// I/O-bound tasks: More threads than cores
int threads = (int) (cpuCores * (1 + 0.5 * expectedBlockingCoefficient));
ExecutorService ioBoundPool = Executors.newFixedThreadPool(threads);
```

### Graceful Shutdown Pattern

```java
public void shutdown(ExecutorService executor) {
    try {
        // Disable new tasks from being submitted
        executor.shutdown();
        
        // Wait for existing tasks to terminate
        if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
            // Cancel currently executing tasks
            executor.shutdownNow();
            
            // Wait for tasks to respond to cancellation
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                System.err.println("Executor did not terminate");
            }
        }
    } catch (InterruptedException e) {
        // (Re-)Cancel if current thread also interrupted
        executor.shutdownNow();
        // Preserve interrupt status
        Thread.currentThread().interrupt();
    }
}
```

### Thread Naming Factory

```java
// Makes debugging much easier
ThreadFactory threadFactory = new ThreadFactory() {
    private final AtomicInteger threadNumber = new AtomicInteger(1);
    
    @Override
    public Thread newThread(Runnable r) {
        Thread thread = new Thread(r);
        thread.setName("MyApp-Worker-" + threadNumber.getAndIncrement());
        return thread;
    }
};

ExecutorService executor = Executors.newFixedThreadPool(10, threadFactory);
```

### Monitor ExecutorService Performance

```java
ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor) executor;

// Scheduled task to log thread pool metrics
ScheduledExecutorService monitor = Executors.newSingleThreadScheduledExecutor();
monitor.scheduleAtFixedRate(() -> {
    System.out.println(String.format("Thread Pool Stats: " +
        "Active: %d, Completed: %d, Task: %d, Queue Size: %d",
        threadPoolExecutor.getActiveCount(),
        threadPoolExecutor.getCompletedTaskCount(),
        threadPoolExecutor.getTaskCount(),
        threadPoolExecutor.getQueue().size()));
}, 0, 10, TimeUnit.SECONDS);
```

### Rejection Policy Selection

```java
// Options for handling rejected tasks when the queue is full:

// 1. Caller runs policy (runs task in the caller's thread)
new ThreadPoolExecutor.CallerRunsPolicy();

// 2. Abort policy (throws RejectedExecutionException)
new ThreadPoolExecutor.AbortPolicy();

// 3. Discard policy (silently discards the task)
new ThreadPoolExecutor.DiscardPolicy();

// 4. Discard oldest policy (discards the oldest task in the queue)
new ThreadPoolExecutor.DiscardOldestPolicy();

// 5. Custom policy
new RejectedExecutionHandler() {
    @Override
    public void rejectedExecution(Runnable r, ThreadPoolExecutor executor) {
        // Log rejection
        logger.warn("Task rejected: " + r);
        // Retry with exponential backoff
        retryWithBackoff(r);
    }
}
```

### Prefer CompletableFuture for Complex Flows

```java
// Instead of nested callbacks or multiple futures:
CompletableFuture.supplyAsync(this::fetchUserData)
    .thenApply(this::processData)
    .thenCompose(this::saveToDatabase)
    .thenAccept(this::notifyUser)
    .exceptionally(ex -> {
        handleError(ex);
        return null;
    });
```

📌 **Interview Insight**: Knowing these best practices demonstrates that you've used the Executor Framework in real applications and understand its complexities beyond simple examples.

-----------

## 6. 📝 Quick Summary

1. **Thread Pools**:
   - Manage pools of worker threads for better resource utilization
   - Types: Fixed, Cached, Single Thread, Work Stealing
   - Created using `Executors` factory methods or directly with `ThreadPoolExecutor`

2. **ExecutorService**:
   - Interface for managing threads and tasks
   - Methods: `execute()`, `submit()`, `invokeAll()`, `invokeAny()`
   - Lifecycle: `shutdown()`, `shutdownNow()`, `awaitTermination()`

3. **ScheduledExecutorService**:
   - For delayed and periodic task execution
   - Methods: `schedule()`, `scheduleAtFixedRate()`, `scheduleWithFixedDelay()`
   - Fixed Rate vs. Fixed Delay timing models

4. **Future and FutureTask**:
   - Represents result of asynchronous computation
   - Methods: `get()`, `isDone()`, `cancel()`, `isCancelled()`
   - Limitations: manual composition, awkward exception handling

5. **CompletableFuture** (Java 8+):
   - Advanced Future with composition and callback support
   - Creation: `completedFuture()`, `supplyAsync()`, `runAsync()`
   - Composition: `thenApply()`, `thenCompose()`, `thenCombine()`
   - Error handling: `exceptionally()`, `handle()`

-----------

## 7. 📊 Quick Reference Table

| Feature | Key Methods | Common Uses | Pitfalls | Best Practices |
|---------|-------------|------------|----------|----------------|
| **Thread Pools** | `newFixedThreadPool()`<br>`newCachedThreadPool()`<br>`newSingleThreadExecutor()`<br>`newWorkStealingPool()` | • Limiting resource usage<br>• Reusing threads<br>• Controlled task execution | • Not shutting down<br>• Unbounded queues<br>• Improper sizing | • Size based on task type<br>• Use custom ThreadFactory<br>• Always shutdown properly |
| **ExecutorService** | `execute()`<br>`submit()`<br>`invokeAll()`<br>`invokeAny()`<br>`shutdown()`<br>`shutdownNow()` | • Executing tasks<br>• Managing thread lifecycle<br>• Collecting task results | • Swallowed exceptions<br>• Not handling rejections<br>• Missing shutdown | • Check futures for exceptions<br>• Use appropriate queue size<br>• Implement graceful shutdown |
| **ScheduledExecutorService** | `schedule()`<br>`scheduleAtFixedRate()`<br>`scheduleWithFixedDelay()` | • Delayed execution<br>• Periodic tasks<br>• Timeouts | • Task overruns<br>• Blocked scheduler threads<br>• Uncaught exceptions | • Use fixed delay for varying tasks<br>• Keep tasks short<br>• Handle all exceptions |
| **Future/FutureTask** | `get()`<br>`isDone()`<br>`cancel()`<br>`isCancelled()` | • Get async results<br>• Check task status<br>• Cancel tasks | • Blocking without timeout<br>• Lost exceptions<br>• Unchecked cancellations | • Always use timeouts<br>• Check for exceptions<br>• Respect interruption |
| **CompletableFuture** | `thenApply()`<br>`thenCompose()`<br>`thenCombine()`<br>`exceptionally()`<br>`allOf()`<br>`anyOf()` | • Complex async flows<br>• Dependent tasks<br>• Non-blocking composition | • Wrong executor<br>• thenApply vs thenCompose<br>• Missed exceptions | • Specify custom executor<br>• Handle exceptions explicitly<br>• Understand sync vs async methods |

Remember, interviewers often look for your understanding of not just how to use these features, but when to use them, their limitations, and how to avoid common pitfalls.