# Java Garbage Collection Algorithms: G1, Serial, Parallel, CMS, ZGC 🗑️

As a senior Java engineer, I'll walk you through the key garbage collection algorithms in Java, focusing on what you need to know for interviews and practical application.

----------

## 1. 🔍 Garbage Collection Fundamentals

Before diving into specific algorithms, let's understand the core concepts:

### What is Garbage Collection?
Garbage Collection (GC) is Java's automatic memory management system that identifies and reclaims memory occupied by unreachable objects.

### The Generations Model:
Most Java GCs use a generational approach based on the weak generational hypothesis:

```
   [Young Generation]     [Old Generation]
   +-----------------+    +---------------+
   | Eden | S0 | S1  | -> |  Tenured      |
   +-----------------+    +---------------+
      ↑      ↑   ↑
    Allocation ↑   ↑
             Survivor Spaces
```

✅ **Key Concepts**:
- **Young Generation**: New objects start here (Eden space)
- **Survivor Spaces (S0, S1)**: Objects that survive Young GC are moved here
- **Old Generation**: Long-lived objects are eventually promoted here
- **Minor GC**: Collects young generation only
- **Major/Full GC**: Collects entire heap (potentially with stop-the-world pauses)

📌 **Interview Insight**: Different GC algorithms optimize different aspects of this process - throughput, latency, or footprint.

----------

## 2. 🧮 Serial Collector (The Original)

The simplest GC algorithm that uses a single thread for collection.

### How It Works:
```
  [Before Collection]       [During Collection - Stop the World]
   +----------------+        +----------------+
   |  Used Memory   |   →    |     Single     |
   |                |        |  GC Thread     |
   +----------------+        +----------------+
```

### Key Characteristics:
- 🔹 Single-threaded collector
- 🔹 Stop-the-world pauses (all application threads halt)
- 🔹 Simple and efficient for small heaps
- 🔹 Low memory footprint

### When to Use:
- 👍 Single-processor systems
- 👍 Small applications with small heaps (< 100MB)
- 👍 Batch processing jobs

### Configuration:
```java
// JVM flags
-XX:+UseSerialGC
```

❌ **Common Mistake**: Using Serial GC for large server applications, causing long pauses.

----------

## 3. 🚀 Parallel Collector (Throughput Collector)

Parallel version of the Serial collector that utilizes multiple threads for collection.

### How It Works:
```
  [Before Collection]       [During Collection - Stop the World]
   +----------------+        +----+----+----+----+
   |  Used Memory   |   →    | GC | GC | GC | GC |
   |                |        | T1 | T2 | T3 | T4 |
   +----------------+        +----+----+----+----+
```

### Key Characteristics:
- 🔹 Multi-threaded young generation collector
- 🔹 Multi-threaded old generation collector (Parallel Old)
- 🔹 Stop-the-world pauses, but shorter than Serial due to parallelism
- 🔹 Optimized for throughput (application performance)

### When to Use:
- 👍 Multi-processor or multi-core systems
- 👍 Applications that can tolerate pauses but need high throughput
- 👍 Batch processing jobs

### Configuration:
```java
// JVM flags
-XX:+UseParallelGC              // Parallel for young gen
-XX:+UseParallelOldGC           // Parallel for old gen (default with -XX:+UseParallelGC)
-XX:ParallelGCThreads=N         // Number of GC threads
-XX:MaxGCPauseMillis=N          // Target for max pause time
-XX:GCTimeRatio=N               // Ratio of GC time to application time (default 99)
```

✅ **Best Practice**: Set `-XX:ParallelGCThreads` to match the number of CPU cores.

----------

## 4. ♻️ Concurrent Mark Sweep (CMS) Collector

A low-latency collector that minimizes pause times by doing most of its work concurrently with application threads.

### How It Works:
```
  [Application Running]      [Concurrent Marking]          [Short Pause for Final Mark+Sweep]
   +------------------+      +------------------+         +------------------+
   | App | App | App  |  →   | App | CMS | App  |    →    |  CMS  |  CMS     |   →   [Resume]
   | T1  | T2  | T3   |      | T1  | T2  | T3   |         |  T1   |  T2      |
   +------------------+      +------------------+         +------------------+
```

### Key Phases:
1. **Initial Mark** (STW): Mark GC roots (short pause)
2. **Concurrent Mark**: Trace references from roots (concurrent)
3. **Concurrent Preclean**: Process changes during marking (concurrent)
4. **Remark** (STW): Final marking accounting for changes (short pause)
5. **Concurrent Sweep**: Reclaim garbage (concurrent)
6. **Concurrent Reset**: Prepare for next cycle (concurrent)

### Key Characteristics:
- 🔹 Low-pause collector
- 🔹 Most work done concurrently with application threads
- 🔹 Uses more CPU and memory than Parallel GC
- 🔹 Can suffer from fragmentation
- 🔹 **Deprecated** in JDK 9 and removed in JDK 14

### When to Use:
- 👍 Applications requiring low latency (< 1 second pauses)
- 👍 Web servers, trading applications, UI applications
- 👍 Available RAM > 4GB and multiple cores

### Configuration:
```java
// JVM flags
-XX:+UseConcMarkSweepGC        // Use CMS collector
-XX:CMSInitiatingOccupancyFraction=N  // When to start CMS (% of old gen)
-XX:+UseCMSInitiatingOccupancyOnly    // Use fixed threshold for initiating CMS
-XX:+CMSParallelRemarkEnabled  // Parallel remark phase
```

⚠️ **Warning**: CMS doesn't compact the heap, leading to fragmentation.

❌ **Common Mistake**: Setting CMSInitiatingOccupancyFraction too high, risking "concurrent mode failures."

----------

## 5. 🌐 Garbage First (G1) Collector

The G1 collector divides the heap into equal-sized regions and prioritizes collection in regions with the most garbage.

### How It Works:
```
   Heap divided into equal-sized regions
   
   +----+----+----+----+
   | E  | E  | O  | O  |
   +----+----+----+----+
   | O  | H  | O  | E  |
   +----+----+----+----+
   | S  | O  | E  | H  |
   +----+----+----+----+
   | O  | S  | O  | O  |
   +----+----+----+----+
   
   E = Eden, S = Survivor, O = Old, H = Humongous
```

### Key Characteristics:
- 🔹 Designed for large heaps (>4GB)
- 🔹 Regions-based collector
- 🔹 Predictable pause times through incremental collection
- 🔹 Concurrent global marking
- 🔹 Incremental compaction
- 🔹 Default collector since Java 9

### Key Phases:
1. **Young Collection**: Collect Eden and Survivor regions
2. **Concurrent Marking**: Mark live objects in old regions
3. **Mixed Collection**: Collect Eden, Survivor, and some Old regions
4. **Clean-up**: Reclaim completely empty regions, etc.

### When to Use:
- 👍 Applications with large heaps (>4GB)
- 👍 Balance between throughput and latency
- 👍 Predictable pause time requirements
- 👍 General-purpose server applications

### Configuration:
```java
// JVM flags
-XX:+UseG1GC                   // Use G1 collector
-XX:MaxGCPauseMillis=N         // Target pause time
-XX:G1NewSizePercent=N         // Min young gen size (default 5%)
-XX:G1MaxNewSizePercent=N      // Max young gen size (default 60%)
-XX:InitiatingHeapOccupancyPercent=N  // Start marking (default 45%)
```

✅ **Best Practice**: Focus on setting your target pause time with `-XX:MaxGCPauseMillis`.

----------

## 6. ⚡ ZGC (Z Garbage Collector)

A scalable, low-latency collector introduced in Java 11, designed for very large heaps.

### How It Works:
ZGC uses colored pointers and load barriers to track references, enabling concurrent compaction.

```
   Colored Pointer on 64-bit systems
   
   +----------------+-------+----------------+
   |   Object Addr  | Color |    Unused     |
   |    (42 bits)   |  (4)  |    (18 bits)  |
   +----------------+-------+----------------+
```

### Key Characteristics:
- 🔹 Designed for very large heaps (terabytes)
- 🔹 Extremely low pause times (<10ms) regardless of heap size
- 🔹 Concurrent compaction
- 🔹 NUMA-aware
- 🔹 Production-ready since JDK 15

### When to Use:
- 👍 Applications requiring consistent low latency (<10ms pauses)
- 👍 Very large heaps (>100GB)
- 👍 Real-time trading systems, gaming servers, UI applications
- 👍 Many CPU cores available

### Configuration:
```java
// JVM flags
-XX:+UseZGC                    // Use ZGC
-XX:ZCollectionInterval=N      // Time between GC cycles in seconds
-XX:+UnlockExperimentalVMOptions  // Required before JDK 15
```

📌 **Interview Insight**: ZGC is a generational collector starting in JDK 21, which improves its efficiency with short-lived objects.

----------

## 7. 🛠️ Determining Which Collector Is Used

You can see which collector your application is using with these options:

```java
// JVM flags to print GC details
-XX:+PrintCommandLineFlags  // Shows which GC is selected
-Xlog:gc                    // Basic GC logging (JDK 9+)
-Xlog:gc*                   // Detailed GC logging (JDK 9+)
-verbose:gc                 // Basic GC details (JDK 8)
-XX:+PrintGCDetails         // Detailed GC info (JDK 8)
```

### Code to detect GC at runtime:
```java
import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.util.List;

public class GCDetector {
    public static void main(String[] args) {
        List<GarbageCollectorMXBean> gcMxBeans = ManagementFactory.getGarbageCollectorMXBeans();
        
        System.out.println("Garbage Collectors:");
        for (GarbageCollectorMXBean gcMxBean : gcMxBeans) {
            System.out.println(gcMxBean.getName());
        }
    }
}
```

📌 **Interview Tip**: Be ready to interpret basic GC logs in interviews, as it demonstrates practical experience.

----------

## 8. 📊 Selecting the Right Collector

### Collector Selection Decision Tree:

```
                         ┌─── Latency Critical? ───┐
                         │                         │
                         ▼                         ▼
                        Yes                        No
                         │                         │
                         ▼                         ▼
              ┌─── Heap >100GB? ───┐       ┌─── Heap >4GB? ───┐
              │                    │       │                  │
              ▼                    ▼       ▼                  ▼
             Yes                  No      Yes                 No
              │                    │       │                  │
              ▼                    ▼       ▼                  ▼
            ZGC                   G1    Parallel GC       Serial GC
```

### Quick Selection Guide:

| Goal | Recommended Collector |
|------|----------------------|
| Maximum throughput | Parallel GC |
| Low latency (<1s pauses) | G1 GC |
| Ultra-low latency (<10ms) | ZGC |
| Small applications | Serial GC |
| General purpose/balanced | G1 GC |

✅ **Best Practice**: Test your application with different collectors before making a decision.

----------

## 9. 💻 Interview-Ready Code Examples

### Example 1: Force garbage collection and measure collection time

```java
public class GCTimeTest {
    private static final int MB = 1024 * 1024;
    
    public static void main(String[] args) {
        // Record start time
        long startTime = System.nanoTime();
        
        // Allocate memory to force GC
        for (int i = 0; i < 100; i++) {
            byte[] allocation = new byte[MB];
        }
        
        // Force garbage collection
        System.gc();
        
        // Calculate elapsed time
        long elapsedTime = System.nanoTime() - startTime;
        System.out.println("Garbage collection took: " + 
                          (elapsedTime / 1_000_000) + " ms");
    }
}
```

### Example 2: Monitor allocation rate and GC overhead

```java
import java.lang.management.*;

public class GCMonitor {
    public static void main(String[] args) throws InterruptedException {
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        
        // Initial measurements
        long initialUsed = memoryBean.getHeapMemoryUsage().getUsed();
        long[] initialGcCounts = new long[gcBeans.size()];
        long[] initialGcTimes = new long[gcBeans.size()];
        
        for (int i = 0; i < gcBeans.size(); i++) {
            GarbageCollectorMXBean gcBean = gcBeans.get(i);
            initialGcCounts[i] = gcBean.getCollectionCount();
            initialGcTimes[i] = gcBean.getCollectionTime();
        }
        
        // Run some allocation work
        allocateMemory();
        
        // Final measurements
        long finalUsed = memoryBean.getHeapMemoryUsage().getUsed();
        
        System.out.println("Memory allocation: " + 
                          (finalUsed - initialUsed) / (1024 * 1024) + " MB");
        
        // Calculate GC overhead
        for (int i = 0; i < gcBeans.size(); i++) {
            GarbageCollectorMXBean gcBean = gcBeans.get(i);
            long gcCount = gcBean.getCollectionCount() - initialGcCounts[i];
            long gcTime = gcBean.getCollectionTime() - initialGcTimes[i];
            
            System.out.println(gcBean.getName() + " collections: " + gcCount);
            System.out.println(gcBean.getName() + " collection time: " + gcTime + " ms");
        }
    }
    
    private static void allocateMemory() {
        // Allocate and release memory
        List<byte[]> allocations = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            allocations.add(new byte[1024 * 1024]); // 1MB each
            if (i % 100 == 0) {
                allocations.clear();
            }
        }
    }
}
```

❌ **Common Mistake**: Manually calling `System.gc()` in production code.

✅ **Best Practice**: Use `-XX:+DisableExplicitGC` to prevent explicit GC calls from affecting production systems.

----------

## 10. ⚠️ Common Traps and Mistakes

1. **Undersizing Young Generation**
   - Symptom: Frequent minor GCs
   - Fix: Increase young generation size (`-XX:NewRatio` or `-Xmn`)

2. **Ignoring GC Logs**
   - Symptom: Performance issues discovered too late
   - Fix: Enable GC logging and monitor regularly

3. **Wrong Collector for the Job**
   - Symptom: Excessive pauses or poor throughput
   - Fix: Select collector based on application needs

4. **Premature Optimization**
   - Symptom: Complex GC configuration without measuring
   - Fix: Establish baselines before tuning; use metrics

5. **Tuning for Peak Load Only**
   - Symptom: Poor performance during normal operation
   - Fix: Balance configuration for both peak and steady-state

✅ **Best Practice**: Measure performance with realistic workloads before and after any GC tuning.

----------

## 11. 🏆 Best Practices

1. **Select the Right Collector**:
   - Choose based on your application needs (latency vs. throughput)
   - Default to G1 for most modern applications

2. **Heap Sizing**:
   - Set initial heap size equal to maximum (`-Xms` = `-Xmx`) to avoid resizing
   - Aim for heap usage around 70% after a full GC

3. **Monitoring**:
   - Enable GC logging in production
   - Track metrics like collection frequency, pause times, and overhead
   - Set up alerts for excessive GC activity

4. **Performance Testing**:
   - Test with realistic data volumes and access patterns
   - Include GC metrics in performance criteria

5. **Application Design**:
   - Design with GC in mind (object pooling for large objects)
   - Avoid creating many short-lived objects in critical paths
   - Consider soft/weak references for caches

----------

## 12. 🚥 Collector-Specific Tips

### G1 GC (Most Common)
- Start with default settings
- Adjust `-XX:MaxGCPauseMillis` based on latency requirements
- Monitor and adjust `-XX:InitiatingHeapOccupancyPercent` as needed

### ZGC
- Enable NUMA awareness with `-XX:+UseNUMA` for multi-socket systems
- Monitor CPU usage as ZGC trades CPU for lower latency

### Parallel GC
- Set `-XX:ParallelGCThreads` appropriately for your system
- Balance `-XX:GCTimeRatio` to control throughput/pause time trade-off

### Serial GC
- Consider for applications in containers with limited CPU resources
- Good for small heaps with infrequent GC

----------

## 13. 🔑 Summary

Java offers multiple garbage collection algorithms, each with different strengths:

- **Serial GC**: Simple, single-threaded, good for small applications
- **Parallel GC**: High throughput, multiple threads, accepts longer pauses
- **CMS**: Low latency, concurrent collection, complex tuning (deprecated)
- **G1 GC**: Balanced latency/throughput, predictable pauses, default since Java 9
- **ZGC**: Ultra-low latency, scalable to terabytes, newer algorithm

The choice depends on your application's requirements, with G1 being the best default choice for most modern applications.

### Quick Revision Table

| Collector | When to Use | Key Advantages | Key Disadvantages | Default In | Flag |
|-----------|-------------|----------------|-------------------|------------|------|
| **Serial** | Small apps, limited resources | Low overhead, small footprint | Long pauses | Client JVM (32-bit) | `-XX:+UseSerialGC` |
| **Parallel** | Batch processing, maximum throughput | High throughput | Longer pauses | Server JVM (pre-Java 9) | `-XX:+UseParallelGC` |
| **CMS** | Low-latency apps (pre-Java 9) | Low pause times | Memory fragmentation, CPU overhead | Never | `-XX:+UseConcMarkSweepGC` |
| **G1** | General-purpose, large heaps | Predictable pauses, balanced | More complex, overhead | Java 9+ | `-XX:+UseG1GC` |
| **ZGC** | Ultra-low latency, huge heaps | Consistent <10ms pauses | Higher CPU usage | Never | `-XX:+UseZGC` |

📌 **Interview Bottom Line**: Understand the trade-offs between collectors, know how to select the right one for different applications, and be able to explain basic tuning parameters.