I'll provide 5 self-contained examples of reactive pipelines in Project Reactor with explanations for each stage. Each example will demonstrate different aspects of reactive programming including creation, filtering, combining, and error handling.

## Example 1: User Service with Fallback and Caching

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class UserServiceExample {

    // Simulated cache
    private static final Map<Integer, User> userCache = new HashMap<>();
    
    public static void main(String[] args) throws InterruptedException {
        fetchUserWithResilience(1).subscribe(
            user -> System.out.println("Successfully retrieved user: " + user),
            error -> System.err.println("Error in main flow: " + error.getMessage()),
            () -> System.out.println("User retrieval completed")
        );
        
        // Wait for async operations
        Thread.sleep(3000);
    }
    
    public static Mono<User> fetchUserWithResilience(int userId) {
        return Mono.just(userId)
            // 1. First check the cache
            .flatMap(id -> getUserFromCache(id)
                // 2. If not in cache, try primary database
                .switchIfEmpty(getUserFromDatabase(id)
                    // 3. Store in cache when retrieved from DB
                    .doOnNext(user -> userCache.put(user.getId(), user))
                )
            )
            // 4. If primary DB fails, try backup service with retry
            .onErrorResume(e -> {
                System.out.println("Primary source failed: " + e.getMessage() + ". Trying backup...");
                return getUserFromBackupService(userId)
                    .doOnNext(user -> userCache.put(user.getId(), user))
                    .retryWhen(Retry.backoff(3, Duration.ofMillis(100))
                        .maxBackoff(Duration.ofSeconds(1))
                        .doBeforeRetry(rs -> System.out.println("Retry attempt: " + rs.totalRetries()))
                    );
            })
            // 5. Add additional user info from another service
            .flatMap(user -> enrichUserWithPreferences(user)
                // 6. If enrichment fails, just return the basic user
                .onErrorReturn(user)
            )
            // 7. Ensure database operations run on suitable scheduler
            .subscribeOn(Schedulers.boundedElastic());
    }
    
    // Simulated service methods
    private static Mono<User> getUserFromCache(int userId) {
        User cachedUser = userCache.get(userId);
        return cachedUser != null ? Mono.just(cachedUser) : Mono.empty();
    }
    
    private static Mono<User> getUserFromDatabase(int userId) {
        // Simulate DB errors for certain IDs
        if (userId % 2 == 0) {
            return Mono.error(new RuntimeException("Database connection failed"));
        }
        return Mono.just(new User(userId, "User" + userId));
    }
    
    private static Mono<User> getUserFromBackupService(int userId) {
        AtomicInteger attempts = new AtomicInteger(0);
        return Mono.defer(() -> {
            // Simulate first attempt failing, then succeeding
            if (attempts.getAndIncrement() == 0) {
                return Mono.error(new RuntimeException("Backup service temporarily unavailable"));
            }
            return Mono.just(new User(userId, "BackupUser" + userId));
        });
    }
    
    private static Mono<User> enrichUserWithPreferences(User user) {
        // Simulate enrichment
        if (user.getId() > 100) {
            return Mono.error(new RuntimeException("Preferences service unavailable"));
        }
        
        return Mono.just(user).map(u -> {
            u.setPreferences(Arrays.asList("pref1", "pref2"));
            return u;
        });
    }
    
    // User class
    static class User {
        private int id;
        private String name;
        private java.util.List<String> preferences;
        
        User(int id, String name) {
            this.id = id;
            this.name = name;
        }
        
        public int getId() { return id; }
        public String getName() { return name; }
        public java.util.List<String> getPreferences() { return preferences; }
        public void setPreferences(java.util.List<String> preferences) { this.preferences = preferences; }
        
        @Override
        public String toString() {
            return "User{id=" + id + ", name='" + name + "', preferences=" + preferences + "}";
        }
    }
}
```

**Pipeline Explanation:**

1. **Creation**: Starts with `Mono.just(userId)` to create the initial reactive stream.
2. **Cache Check**: Uses `flatMap` with `getUserFromCache`, which returns an existing user if found.
3. **Primary Source**: If cache is empty, `switchIfEmpty` redirects to the database call.
4. **Caching Logic**: `doOnNext` is used to store successfully retrieved users in the cache.
5. **Error Handling**: `onErrorResume` catches failures from the primary database and switches to a backup service.
6. **Retry Logic**: `retryWhen` with exponential backoff attempts to recover from temporary failures in the backup service.
7. **Enrichment**: `flatMap` combines the user data with additional information from another service.
8. **Fallback for Enrichment**: `onErrorReturn` ensures we still get the basic user even if enrichment fails.
9. **Scheduler Management**: `subscribeOn` ensures database operations run on an appropriate thread pool.

This example demonstrates a complete resilient data fetching flow with multiple fallback strategies and proper error handling.

## Example 2: Real-time Search with Debounce and Parallel Processing

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;

public class SearchServiceExample {

    public static void main(String[] args) throws InterruptedException {
        // Simulate user typing a search query character by character
        Flux<String> searchTerms = Flux.just("r", "re", "rea", "reac", "react", "reacti", "reactiv", "reactive")
            .delayElements(Duration.ofMillis(100));
            
        // Process the search terms
        processSearchTerms(searchTerms).subscribe(
            results -> System.out.println("Search results: " + results),
            error -> System.err.println("Search error: " + error.getMessage()),
            () -> System.out.println("Search completed")
        );
        
        // Wait for async operations
        Thread.sleep(5000);
    }
    
    public static Flux<List<String>> processSearchTerms(Flux<String> terms) {
        return terms
            // 1. Show what's being typed
            .doOnNext(term -> System.out.println("User typed: " + term))
            
            // 2. Ignore rapid typing with debounce
            .debounce(Duration.ofMillis(300))
            
            // 3. Filter out short search terms
            .filter(term -> term.length() >= 3)
            .doOnNext(term -> System.out.println("Processing search for: " + term))
            
            // 4. Combine results from multiple search sources
            .flatMap(term -> Flux.merge(
                searchDatabase(term).subscribeOn(Schedulers.parallel()),
                searchExternalApi(term).subscribeOn(Schedulers.parallel()),
                searchCache(term).subscribeOn(Schedulers.boundedElastic())
            )
            // 5. Group results by search term to handle out-of-order returns
            .collectList()
            
            // 6. Add error handling for each search term
            .onErrorResume(e -> {
                System.out.println("Error searching for '" + term + "': " + e.getMessage());
                return Mono.just(new ArrayList<>());
            }))
            
            // 7. Limit search rate for API protection
            .limitRate(2)
            
            // 8. Add timeout to prevent hanging
            .timeout(Duration.ofSeconds(3))
            
            // 9. Global error recovery
            .onErrorResume(e -> {
                System.out.println("Global search error: " + e.getMessage());
                return Flux.just(Arrays.asList("Error occurred, please try again"));
            });
    }
    
    // Simulated search services
    private static Flux<String> searchDatabase(String term) {
        // Simulate DB search with random results
        List<String> dbItems = Arrays.asList(
            "Reactive Programming", "Reactor Core", "Reactive Streams", 
            "Reactive Systems", "Reactive Manifesto"
        );
        
        return Flux.fromIterable(dbItems)
            .filter(item -> item.toLowerCase().contains(term.toLowerCase()))
            .delayElements(Duration.ofMillis(ThreadLocalRandom.current().nextInt(100, 500)));
    }
    
    private static Flux<String> searchExternalApi(String term) {
        // Simulate external API with occasional errors
        if (term.equals("reactive")) {
            return Flux.error(new RuntimeException("External API rate limit exceeded"));
        }
        
        List<String> apiItems = Arrays.asList(
            "ReactiveX", "Reactive Extensions", "React", "ReactiveCocoa"
        );
        
        return Flux.fromIterable(apiItems)
            .filter(item -> item.toLowerCase().contains(term.toLowerCase()))
            .delayElements(Duration.ofMillis(ThreadLocalRandom.current().nextInt(200, 800)));
    }
    
    private static Flux<String> searchCache(String term) {
        // Simulate cache with fast responses
        List<String> cacheItems = Arrays.asList("Reactive Java", "Spring Reactive");
        
        return Flux.fromIterable(cacheItems)
            .filter(item -> item.toLowerCase().contains(term.toLowerCase()))
            .delayElements(Duration.ofMillis(50));
    }
}
```

**Pipeline Explanation:**

1. **Creation**: Simulates user typing with `Flux.just()` and `delayElements` to create a time-based stream.
2. **Debouncing**: `debounce` waits for 300ms of inactivity before processing, preventing unnecessary searches during rapid typing.
3. **Filtering**: `filter` removes search terms that are too short (less than 3 characters).
4. **Parallel Processing**: `flatMap` with `Flux.merge` combines results from multiple search sources.
5. **Thread Management**: Each search source runs on its own scheduler with `subscribeOn` for true parallelism.
6. **Result Collection**: `collectList` gathers all results for each search term into a single list.
7. **Per-Search Error Handling**: Inner `onErrorResume` handles failures for individual search terms.
8. **Rate Limiting**: `limitRate` prevents overwhelming downstream consumers with too many results at once.
9. **Timeout**: `timeout` ensures searches don't hang indefinitely.
10. **Global Error Recovery**: Outer `onErrorResume` provides a fallback for any unhandled errors in the pipeline.

This example shows how to build a responsive search interface with debouncing, parallel data fetching, and robust error handling.

## Example 3: Stock Price Monitoring System with Alerts

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicReference;

public class StockMonitoringExample {

    public static void main(String[] args) throws InterruptedException {
        // List of stock symbols to monitor
        List<String> stockSymbols = List.of("AAPL", "GOOGL", "MSFT", "AMZN");
        
        // Create the monitoring system
        monitorStockPrices(stockSymbols, 10.0).subscribe(
            alert -> System.out.println("ALERT: " + alert),
            error -> System.err.println("System error: " + error.getMessage()),
            () -> System.out.println("Monitoring stopped")
        );
        
        // Run for a while
        Thread.sleep(10000);
    }
    
    public static Flux<String> monitorStockPrices(List<String> symbols, double alertThreshold) {
        // 1. Create a stream of stock price updates
        return Flux.interval(Duration.ofMillis(200))
            // 2. Generate a price update for a random stock
            .map(tick -> {
                String symbol = symbols.get(ThreadLocalRandom.current().nextInt(symbols.size()));
                double price = 100 + ThreadLocalRandom.current().nextDouble(-5, 5);
                return new StockPrice(symbol, price, LocalDateTime.now());
            })
            // 3. Share the stock price stream for multiple operations
            .publish().autoConnect(2)
            
            // 4. Create a branch for tracking price history
            .share().transform(sharedPrices -> {
                // Store recent prices for each symbol
                AtomicReference<List<StockPrice>> recentPrices = 
                    new AtomicReference<>(new ArrayList<>());
                
                // One branch updates the history
                sharedPrices
                    .doOnNext(price -> {
                        List<StockPrice> currentPrices = new ArrayList<>(recentPrices.get());
                        currentPrices.add(price);
                        // Keep only last 10 prices per symbol
                        if (currentPrices.size() > symbols.size() * 10) {
                            currentPrices.remove(0);
                        }
                        recentPrices.set(currentPrices);
                    })
                    .subscribe();
                
                // The other branch generates alerts based on price movements
                return sharedPrices
                    // 5. Calculate price changes compared to moving average
                    .flatMap(currentPrice -> {
                        List<StockPrice> history = recentPrices.get();
                        // Get recent prices for same symbol
                        List<StockPrice> symbolHistory = history.stream()
                            .filter(p -> p.getSymbol().equals(currentPrice.getSymbol()))
                            .toList();
                        
                        if (symbolHistory.size() < 3) {
                            return Mono.empty(); // Not enough history
                        }
                        
                        // Calculate average of recent prices
                        double avg = symbolHistory.stream()
                            .limit(symbolHistory.size() - 1) // Exclude current price
                            .mapToDouble(StockPrice::getPrice)
                            .average()
                            .orElse(currentPrice.getPrice());
                        
                        // Calculate percent change
                        double percentChange = (currentPrice.getPrice() - avg) / avg * 100;
                        
                        // 6. Filter for significant changes
                        if (Math.abs(percentChange) >= alertThreshold) {
                            String direction = percentChange > 0 ? "UP" : "DOWN";
                            return Mono.just(
                                String.format("%s moved %s by %.2f%% (from $%.2f to $%.2f)", 
                                currentPrice.getSymbol(), direction, Math.abs(percentChange), 
                                avg, currentPrice.getPrice())
                            );
                        }
                        
                        return Mono.empty();
                    })
                    // 7. Simulate occasional service errors
                    .map(alert -> {
                        if (ThreadLocalRandom.current().nextInt(20) == 0) {
                            throw new RuntimeException("Market data service temporarily unavailable");
                        }
                        return alert;
                    })
                    // 8. Handle errors to keep the stream alive
                    .onErrorContinue((error, item) -> 
                        System.out.println("Error processing alert: " + error.getMessage())
                    )
                    // 9. Rate limit alerts to prevent spam
                    .sample(Duration.ofMillis(1000))
                    // 10. Apply exponential backoff retry for data service
                    .retryWhen(reactor.util.retry.Retry.backoff(3, Duration.ofMillis(100))
                        .maxBackoff(Duration.ofSeconds(1))
                        .doBeforeRetry(rs -> System.out.println("Retrying after error, attempt: " + rs.totalRetries()))
                    );
            });
    }
    
    // Stock price data class
    static class StockPrice {
        private final String symbol;
        private final double price;
        private final LocalDateTime timestamp;
        
        StockPrice(String symbol, double price, LocalDateTime timestamp) {
            this.symbol = symbol;
            this.price = price;
            this.timestamp = timestamp;
        }
        
        public String getSymbol() { return symbol; }
        public double getPrice() { return price; }
        public LocalDateTime getTimestamp() { return timestamp; }
        
        @Override
        public String toString() {
            return symbol + " @ $" + price;
        }
    }
}
```

**Pipeline Explanation:**

1. **Stream Creation**: `Flux.interval` creates a regular tick of events, which are mapped to random stock prices.
2. **Stream Sharing**: `publish().autoConnect(2)` allows sharing the stock price stream for multiple consumers.
3. **State Management**: An `AtomicReference` stores recent price history, updated through a shared stream.
4. **Complex Transformation**: `flatMap` calculates price changes by comparing current prices with a moving average.
5. **Conditional Filtering**: Inside the `flatMap`, we filter for significant price movements that exceed the threshold.
6. **Error Simulation**: The `map` stage randomly introduces errors to simulate service failures.
7. **Error Continuity**: `onErrorContinue` ensures the stream doesn't terminate due to individual errors.
8. **Rate Limiting**: `sample` prevents alert flooding by emitting at most one alert per second.
9. **Retry Logic**: `retryWhen` with backoff handles transient failures in the data service.

This example demonstrates a real-time monitoring system with shared streams, stateful processing, and sophisticated error handling strategies.

## Example 4: File Processing Pipeline with Batching and Throttling

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.util.function.Tuple2;
import reactor.util.function.Tuples;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.BaseStream;

public class FileProcessingExample {

    // Track processing statistics
    private static final Map<String, Integer> processedFileStats = new ConcurrentHashMap<>();
    
    public static void main(String[] args) throws Exception {
        // Directory with files to process
        Path directory = Paths.get(System.getProperty("java.io.tmpdir"));
        
        // Process log files in the directory
        processLogFiles(directory, ".log")
            .doOnComplete(() -> {
                System.out.println("\nProcessing summary:");
                processedFileStats.forEach((file, count) -> 
                    System.out.println(file + ": " + count + " records processed")
                );
            })
            .subscribe(
                result -> System.out.println("Processed batch: " + result),
                error -> System.err.println("Processing failed: " + error.getMessage()),
                () -> System.out.println("All files processed successfully")
            );
        
        // Wait for async operations to complete
        Thread.sleep(10000);
    }
    
    public static Flux<BatchResult> processLogFiles(Path directory, String fileExtension) {
        // 1. List files in the directory with the specified extension
        return Mono.fromCallable(() -> Files.list(directory))
            .flatMapMany(stream -> Flux.fromStream(stream))
            .filter(path -> path.toString().endsWith(fileExtension))
            .doOnNext(path -> System.out.println("Found file: " + path.getFileName()))
            
            // 2. Read each file line by line
            .flatMap(path -> Flux.using(
                // Resource supplier
                () -> Files.lines(path),
                // Stream mapping function
                lines -> processFileLines(lines, path.getFileName().toString()),
                // Resource cleanup function
                BaseStream::close
            )
            // 3. Run file processing on IO thread pool
            .subscribeOn(Schedulers.boundedElastic()))
            
            // 4. Group lines into batches for efficient processing
            .buffer(100)
            .map(batch -> {
                // 5. Process each batch
                int validLines = (int) batch.stream()
                    .filter(line -> line.isValid())
                    .count();
                    
                int errorLines = batch.size() - validLines;
                
                return new BatchResult(batch.size(), validLines, errorLines);
            })
            
            // 6. Throttle processing to prevent overwhelming downstream systems
            .delayElements(Duration.ofMillis(500))
            
            // 7. Handle errors at different levels
            .onErrorResume(e -> {
                if (e instanceof java.io.IOException) {
                    System.err.println("IO error: " + e.getMessage() + ". Skipping file.");
                    return Mono.empty();
                }
                return Mono.error(new ProcessingException("Fatal error: " + e.getMessage(), e));
            })
            
            // 8. Add timeout for the entire operation
            .timeout(Duration.ofMinutes(5))
            
            // 9. Retry with exponential backoff for transient failures
            .retryWhen(reactor.util.retry.Retry.backoff(3, Duration.ofSeconds(1))
                .filter(e -> !(e instanceof ProcessingException)) // Don't retry fatal errors
                .doBeforeRetry(rs -> System.out.println("Retrying, attempt: " + rs.totalRetries()))
            );
    }
    
    private static Flux<ProcessedLine> processFileLines(java.util.stream.Stream<String> lines, String fileName) {
        AtomicInteger lineCounter = new AtomicInteger(0);
        
        return Flux.fromStream(lines)
            // Process each line
            .map(line -> {
                lineCounter.incrementAndGet();
                
                // Track statistics
                processedFileStats.compute(fileName, (k, v) -> (v == null) ? 1 : v + 1);
                
                // Simulate line validation and processing
                boolean isValid = !line.trim().isEmpty() && !line.contains("ERROR");
                
                // Simulate occasional processing failure
                if (line.contains("FATAL")) {
                    throw new RuntimeException("Fatal error processing line: " + line);
                }
                
                return new ProcessedLine(fileName, lineCounter.get(), line, isValid);
            })
            // Handle per-line errors without killing the stream
            .onErrorContinue((error, line) -> 
                System.err.println("Error processing line: " + error.getMessage())
            );
    }
    
    // Data classes
    static class ProcessedLine {
        private final String fileName;
        private final int lineNumber;
        private final String content;
        private final boolean valid;
        
        ProcessedLine(String fileName, int lineNumber, String content, boolean valid) {
            this.fileName = fileName;
            this.lineNumber = lineNumber;
            this.content = content;
            this.valid = valid;
        }
        
        public boolean isValid() { return valid; }
        
        @Override
        public String toString() {
            return fileName + ":" + lineNumber + " [" + (valid ? "VALID" : "INVALID") + "] " + content;
        }
    }
    
    static class BatchResult {
        private final int totalLines;
        private final int validLines;
        private final int errorLines;
        
        BatchResult(int totalLines, int validLines, int errorLines) {
            this.totalLines = totalLines;
            this.validLines = validLines;
            this.errorLines = errorLines;
        }
        
        @Override
        public String toString() {
            return totalLines + " lines (" + validLines + " valid, " + errorLines + " errors)";
        }
    }
    
    static class ProcessingException extends RuntimeException {
        ProcessingException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
```

**Pipeline Explanation:**

1. **Resource-Safe Creation**: `Mono.fromCallable` and `Flux.using` ensure clean resource handling when listing files and reading lines.
2. **Filtering**: Files are filtered by extension with the `filter` operator.
3. **Thread Management**: `subscribeOn(Schedulers.boundedElastic())` moves file I/O to a dedicated thread pool.
4. **Batching**: `buffer` groups lines into batches for more efficient processing.
5. **Transformation**: Each batch is processed with `map` to count valid and error lines.
6. **Rate Limiting**: `delayElements` throttles processing to prevent overwhelming downstream systems.
7. **Error Differentiation**: `onErrorResume` handles different error types differently, skipping files with IO errors.
8. **Timeout**: The entire operation has a global timeout with the `timeout` operator.
9. **Selective Retry**: `retryWhen` with a filter only retries non-fatal errors.
10. **Per-Item Error Handling**: `onErrorContinue` in the line processing ensures a single bad line doesn't stop file processing.

This example demonstrates a complete file processing pipeline with resource management, batching for efficiency, and multi-level error handling strategies.

I'll finish the last example for you.

## Example 5: Reactive Aggregation Service with Circuit Breaker (continued)

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;

public class ReactiveDashboardExample {

    // Circuit breaker state
    private static final Map<String, CircuitBreaker> circuitBreakers = new ConcurrentHashMap<>();
    
    public static void main(String[] args) throws InterruptedException {
        // Simulate dashboard data refresh
        getDashboardData()
            .repeat(3) // Refresh a few times
            .delayElements(Duration.ofSeconds(2))
            .subscribe(
                dashboard -> System.out.println("Dashboard updated: " + dashboard),
                error -> System.err.println("Dashboard update failed: " + error.getMessage()),
                () -> System.out.println("Dashboard updates completed")
            );
            
        // Wait for async operations
        Thread.sleep(15000);
    }
    
    public static Mono<Dashboard> getDashboardData() {
        // 1. Define the various data sources to aggregate
        Mono<UserStats> userStats = getUserStats();
        Mono<List<SalesRecord>> recentSales = getRecentSales();
        Mono<SystemHealth> systemHealth = getSystemHealth();
        Mono<List<AlertMessage>> activeAlerts = getActiveAlerts();
        
        // 2. Combine all data sources in parallel
        return Mono.zip(
            // 3. Apply circuit breaker pattern to each source
            applyCircuitBreaker(userStats, "user-service", UserStats.unknown()),
            applyCircuitBreaker(recentSales, "sales-service", List.of()),
            applyCircuitBreaker(systemHealth, "health-service", SystemHealth.unknown()),
            applyCircuitBreaker(activeAlerts, "alerts-service", List.of())
        )
        // 4. Map the combined results to a dashboard object
        .map(tuple -> new Dashboard(
            tuple.getT1(),
            tuple.getT2(),
            tuple.getT3(),
            tuple.getT4(),
            java.time.LocalDateTime.now()
        ))
        // 5. Add timeout for the entire operation
        .timeout(Duration.ofSeconds(3))
        // 6. Log the operation stages
        .doOnSubscribe(s -> System.out.println("Starting dashboard data fetch"))
        .doOnSuccess(d -> System.out.println("Successfully collected all dashboard data"))
        .doOnError(e -> System.err.println("Error fetching dashboard data: " + e.getMessage()))
        // 7. Global fallback if anything goes wrong
        .onErrorResume(e -> Mono.just(Dashboard.empty()))
        // 8. Ensure UI updates happen on the right scheduler
        .subscribeOn(Schedulers.parallel());
    }
    
    // Circuit breaker pattern implementation
    private static <T> Mono<T> applyCircuitBreaker(Mono<T> source, String serviceName, T fallback) {
        CircuitBreaker breaker = circuitBreakers.computeIfAbsent(
            serviceName, 
            name -> new CircuitBreaker(name, 3, Duration.ofSeconds(5))
        );
        
        return breaker.isOpen()
            ? Mono.just(fallback).doOnSubscribe(s -> 
                System.out.println("Circuit open for " + serviceName + ", using fallback"))
            : source
                .doOnError(e -> breaker.recordFailure())
                .doOnSuccess(v -> breaker.recordSuccess())
                .onErrorResume(e -> {
                    System.out.println("Error in " + serviceName + ": " + e.getMessage());
                    return Mono.just(fallback);
                });
    }
    
    // Simulated data source methods
    private static Mono<UserStats> getUserStats() {
        return simulateServiceCall(
            () -> new UserStats(
                ThreadLocalRandom.current().nextInt(1000, 5000),
                ThreadLocalRandom.current().nextInt(50, 300),
                ThreadLocalRandom.current().nextInt(10, 100)
            ),
            80
        );
    }
    
    private static Mono<List<SalesRecord>> getRecentSales() {
        return simulateServiceCall(
            () -> {
                int count = ThreadLocalRandom.current().nextInt(3, 8);
                return Flux.range(1, count)
                    .map(i -> new SalesRecord("PROD-" + i, ThreadLocalRandom.current().nextDouble(10, 500)))
                    .collectList()
                    .block();
            },
            70
        );
    }
    
    private static Mono<SystemHealth> getSystemHealth() {
        return simulateServiceCall(
            () -> {
                int serverCount = ThreadLocalRandom.current().nextInt(3, 6);
                int healthyCount = ThreadLocalRandom.current().nextInt(1, serverCount + 1);
                return new SystemHealth(serverCount, healthyCount, ThreadLocalRandom.current().nextDouble(0.1, 0.9));
            },
            90
        );
    }
    
    private static Mono<List<AlertMessage>> getActiveAlerts() {
        return simulateServiceCall(
            () -> {
                int count = ThreadLocalRandom.current().nextInt(0, 4);
                return Flux.range(1, count)
                    .map(i -> new AlertMessage("ALERT-" + i, "Alert message " + i, 
                        ThreadLocalRandom.current().nextInt(1, 4)))
                    .collectList()
                    .block();
            },
            60
        );
    }
    
    // Helper to simulate service calls with random failures
    private static <T> Mono<T> simulateServiceCall(java.util.function.Supplier<T> supplier, int reliability) {
        return Mono.defer(() -> {
            // Simulate random latency
            try {
                Thread.sleep(ThreadLocalRandom.current().nextInt(50, 500));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            // Simulate random failures based on reliability percentage
            if (ThreadLocalRandom.current().nextInt(100) >= reliability) {
                return Mono.error(new ServiceException("Service temporarily unavailable"));
            }
            
            return Mono.just(supplier.get());
        });
    }
    
    // Circuit breaker implementation
    static class CircuitBreaker {
        private final String name;
        private final int failureThreshold;
        private final Duration resetTimeout;
        private final AtomicInteger failureCount = new AtomicInteger(0);
        private volatile boolean open = false;
        private volatile long lastFailureTime = 0;
        
        CircuitBreaker(String name, int failureThreshold, Duration resetTimeout) {
            this.name = name;
            this.failureThreshold = failureThreshold;
            this.resetTimeout = resetTimeout;
        }
        
        public boolean isOpen() {
            // Check if it's time to try resetting the circuit
            if (open && System.currentTimeMillis() - lastFailureTime > resetTimeout.toMillis()) {
                System.out.println("Circuit for " + name + " half-open, attempting reset");
                open = false;
                failureCount.set(0);
            }
            return open;
        }
        
        public void recordSuccess() {
            failureCount.set(0);
        }
        
        public void recordFailure() {
            int failures = failureCount.incrementAndGet();
            if (failures >= failureThreshold) {
                open = true;
                lastFailureTime = System.currentTimeMillis();
                System.out.println("Circuit for " + name + " opened after " + failures + " failures");
            }
        }
    }
    
    // Data classes
    static class Dashboard {
        private final UserStats userStats;
        private final List<SalesRecord> recentSales;
        private final SystemHealth systemHealth;
        private final List<AlertMessage> activeAlerts;
        private final java.time.LocalDateTime timestamp;
        
        Dashboard(UserStats userStats, List<SalesRecord> recentSales, 
                 SystemHealth systemHealth, List<AlertMessage> activeAlerts, 
                 java.time.LocalDateTime timestamp) {
            this.userStats = userStats;
            this.recentSales = recentSales;
            this.systemHealth = systemHealth;
            this.activeAlerts = activeAlerts;
            this.timestamp = timestamp;
        }
        
        public static Dashboard empty() {
            return new Dashboard(
                UserStats.unknown(),
                List.of(),
                SystemHealth.unknown(),
                List.of(),
                java.time.LocalDateTime.now()
            );
        }
        
        @Override
        public String toString() {
            return "Dashboard [" + 
                "timestamp=" + timestamp + 
                ", users=" + userStats + 
                ", health=" + systemHealth + 
                ", alerts=" + activeAlerts.size() + 
                ", sales=" + recentSales.size() + 
                "]";
        }
    }
    
    static class UserStats {
        private final int totalUsers;
        private final int activeUsers;
        private final int newUsers;
        
        UserStats(int totalUsers, int activeUsers, int newUsers) {
            this.totalUsers = totalUsers;
            this.activeUsers = activeUsers;
            this.newUsers = newUsers;
        }
        
        public static UserStats unknown() {
            return new UserStats(-1, -1, -1);
        }
        
        @Override
        public String toString() {
            if (totalUsers < 0) return "UNKNOWN";
            return "Users[total=" + totalUsers + ", active=" + activeUsers + ", new=" + newUsers + "]";
        }
    }
    
    static class SalesRecord {
        private final String productId;
        private final double amount;
        
        SalesRecord(String productId, double amount) {
            this.productId = productId;
            this.amount = amount;
        }
        
        @Override
        public String toString() {
            return productId + ": $" + amount;
        }
    }
    
    static class SystemHealth {
        private final int totalServers;
        private final int healthyServers;
        private final double cpuLoad;
        
        SystemHealth(int totalServers, int healthyServers, double cpuLoad) {
            this.totalServers = totalServers;
            this.healthyServers = healthyServers;
            this.cpuLoad = cpuLoad;
        }
        
        public static SystemHealth unknown() {
            return new SystemHealth(-1, -1, -1);
        }
        
        @Override
        public String toString() {
            if (totalServers < 0) return "UNKNOWN";
            return "Health[servers=" + healthyServers + "/" + totalServers + 
                ", load=" + String.format("%.1f", cpuLoad * 100) + "%]";
        }
    }
    
    static class AlertMessage {
        private final String id;
        private final String message;
        private final int severity;
        
        AlertMessage(String id, String message, int severity) {
            this.id = id;
            this.message = message;
            this.severity = severity;
        }
        
        @Override
        public String toString() {
            return id + " (sev=" + severity + "): " + message;
        }
    }
    
    static class ServiceException extends RuntimeException {
        ServiceException(String message) {
            super(message);
        }
    }
}
```

**Pipeline Explanation:**

1. **Creation**: Multiple data sources are created as independent `Mono` publishers.
2. **Combining**: `Mono.zip` combines all data sources to run in parallel, waiting for all to complete.
3. **Circuit Breaker Pattern**: Custom circuit breaker implementation protects against cascading failures from unreliable services.
4. **Transformation**: The combined results are mapped into a unified `Dashboard` object.
5. **Error Handling**:
   - For individual services: Circuit breakers track failures and prevent overloading failing services
   - For each service: `onErrorResume` provides service-specific fallbacks
   - For the entire pipeline: Global `onErrorResume` ensures dashboard updates continue even with errors
6. **Timeouts**: A global timeout ensures dashboard updates don't hang indefinitely.
7. **Observability**: `doOnSubscribe`, `doOnSuccess`, and `doOnError` provide logging at key points.
8. **Scheduling**: `subscribeOn` ensures processing happens on appropriate thread pools.
9. **Periodic Execution**: The main method uses `repeat` and `delayElements` to create a periodic refresh.

This example demonstrates an advanced reactive pattern for aggregating data from multiple services with resilience features like circuit breakers, timeouts, and fallbacks at multiple levels. It shows how to build a robust system that can continue functioning even when some components fail.

These five examples cover a wide range of reactive patterns and techniques that would be valuable to discuss in interviews. They demonstrate how to create complex, resilient reactive pipelines that handle various real-world scenarios including:

1. User service with caching and fallbacks
2. Real-time search with debouncing and parallel processing
3. Stock price monitoring with alerts
4. File processing with batching and error handling
5. Data aggregation with circuit breakers

Each example shows how to properly combine creation, filtering, transformation, combining, and error handling operators to build robust reactive applications.