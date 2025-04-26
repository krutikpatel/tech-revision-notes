Here's a comprehensive request processing time metrics collection filter for a WebFlux-based project:

```java
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

@Component
public class MetricsCollectionFilter implements WebFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(MetricsCollectionFilter.class);
    private final MeterRegistry meterRegistry;
    
    public MetricsCollectionFilter(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        long startTime = System.nanoTime();
        
        // Extract path for metric tagging
        String path = exchange.getRequest().getPath().value();
        String method = exchange.getRequest().getMethod().name();
        
        // Add request start time as an attribute
        exchange.getAttributes().put("requestStartTime", startTime);
        
        return chain.filter(exchange)
            // This doFinally block ensures metrics are recorded even if errors occur
            .doFinally(signalType -> {
                long endTime = System.nanoTime();
                long durationNanos = endTime - startTime;
                
                // Record the request duration
                Timer timer = meterRegistry.timer(
                    "http.server.requests", 
                    "uri", getSimplifiedUri(path),
                    "method", method,
                    "status", String.valueOf(exchange.getResponse().getStatusCode().value()),
                    "outcome", getOutcome(exchange)
                );
                timer.record(durationNanos, TimeUnit.NANOSECONDS);
                
                // Record specific endpoint metrics for fine-grained monitoring
                meterRegistry.timer(
                    "http.server.endpoint." + sanitizeUriForMetricName(path),
                    "method", method
                ).record(durationNanos, TimeUnit.NANOSECONDS);
                
                // Additional metrics - you can add more based on your needs
                meterRegistry.counter(
                    "http.server.requests.count", 
                    "uri", getSimplifiedUri(path),
                    "method", method
                ).increment();
                
                // Log slow requests (thresholds could be configuration properties)
                Duration threshold = Duration.ofMillis(500);
                if (Duration.ofNanos(durationNanos).compareTo(threshold) > 0) {
                    logger.warn("Slow request detected: {} {} took {}ms", 
                        method, path, TimeUnit.NANOSECONDS.toMillis(durationNanos));
                    
                    // Record slow request metric
                    meterRegistry.counter("http.server.requests.slow").increment();
                }
                
                // Log at debug level for all requests
                logger.debug("Request processed: {} {} - Status: {} - Duration: {}ms", 
                    method, path, 
                    exchange.getResponse().getStatusCode(),
                    TimeUnit.NANOSECONDS.toMillis(durationNanos));
            });
    }
    
    /**
     * Simplifies URIs to avoid high cardinality metrics
     * Transforms paths like /users/123/profile to /users/{id}/profile
     */
    private String getSimplifiedUri(String uri) {
        // This is a simple implementation - you might want to use a more sophisticated
        // approach based on your API design
        return uri.replaceAll("/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", "/{uuid}")
                 .replaceAll("/[0-9]+", "/{id}");
    }
    
    /**
     * Maps HTTP status codes to logical outcomes for better metric grouping
     */
    private String getOutcome(ServerWebExchange exchange) {
        int statusCode = exchange.getResponse().getStatusCode().value();
        if (statusCode < 200) return "INFORMATIONAL";
        if (statusCode < 300) return "SUCCESS";
        if (statusCode < 400) return "REDIRECTION";
        if (statusCode < 500) return "CLIENT_ERROR";
        return "SERVER_ERROR";
    }
    
    /**
     * Creates a metric-friendly name from a URI path
     */
    private String sanitizeUriForMetricName(String uri) {
        // Replace all non-alphanumeric characters with underscores
        // and simplify dynamic parts of the URI
        return getSimplifiedUri(uri)
                .replaceAll("[^a-zA-Z0-9]", "_")
                .replaceAll("_+", "_")
                .toLowerCase();
    }
}
```

This filter provides comprehensive metrics collection for a WebFlux application:

1. **Request Duration Tracking**: Measures how long each request takes in nanoseconds for high precision
2. **Multiple Metric Types**: Records both timers and counters
3. **Dimensional Metrics**: Tags metrics with important dimensions like path, method, status code
4. **Path Normalization**: Converts dynamic paths (like IDs) to templates to avoid metric explosion
5. **Slow Request Identification**: Flags requests that exceed configurable thresholds
6. **Outcome Classification**: Groups status codes into logical categories
7. **Endpoint-Specific Metrics**: Creates specific metrics for individual endpoints
8. **Proper Logging**: Logs at appropriate levels based on request characteristics

To configure this filter in your application, you'll need:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import io.micrometer.core.instrument.MeterRegistry;

@Configuration
public class WebFluxConfig {
    
    @Bean
    @Order(1) // High priority to ensure accurate timing
    public MetricsCollectionFilter metricsCollectionFilter(MeterRegistry meterRegistry) {
        return new MetricsCollectionFilter(meterRegistry);
    }
}
```

This implementation works with Micrometer, which is Spring Boot's recommended metrics collection system. Micrometer can export metrics to various monitoring systems like Prometheus, Datadog, New Relic, and others.

You can visualize these metrics using dashboards in Grafana or your preferred monitoring tool to track:
- Request rates
- Error rates
- Request latencies (min, max, average, percentiles)
- Endpoint performance comparisons
- SLA compliance