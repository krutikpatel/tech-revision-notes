# 🚀 Java Spring Framework: Data Access & Persistence Advanced Topics

I'll guide you through Pagination & Sorting, Transactions, Auditing, and Optimistic Locking with interview-ready insights.

## 1. 📚 Pagination & Sorting
---------

Pagination and sorting are essential for efficient data retrieval, especially when dealing with large datasets.

### 🧩 Key Components

✅ **Spring Data JPA Pagination**
- `Pageable` interface - core pagination component 
- `PageRequest` - concrete implementation of `Pageable`
- `Page<T>` - contains paginated result with metadata
- `Slice<T>` - lightweight alternative without count query

📌 **Basic Implementation**
```java
// Repository interface
public interface ProductRepository extends JpaRepository<Product, Long> {
    // Method that accepts Pageable
    Page<Product> findByCategory(String category, Pageable pageable);
    
    // Method with custom query and pagination
    @Query("SELECT p FROM Product p WHERE p.price > :minPrice")
    Page<Product> findExpensiveProducts(@Param("minPrice") BigDecimal minPrice, Pageable pageable);
}

// Service layer
@Service
public class ProductService {
    private final ProductRepository productRepository;
    
    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }
    
    // Method using pagination
    public Page<Product> getProductsByCategory(String category, int page, int size) {
        return productRepository.findByCategory(category, PageRequest.of(page, size));
    }
    
    // Method using pagination with sorting
    public Page<Product> getProductsByCategorySorted(String category, int page, int size, 
                                                   String sortField, String sortDirection) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDirection), sortField);
        return productRepository.findByCategory(category, PageRequest.of(page, size, sort));
    }
    
    // Method with multiple sort criteria
    public Page<Product> getProductsWithComplexSorting(int page, int size) {
        Sort sort = Sort.by(
            Sort.Order.desc("priority"),
            Sort.Order.asc("name")
        );
        return productRepository.findAll(PageRequest.of(page, size, sort));
    }
}
```

### 🧩 Controller Integration

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductService productService;
    
    // Constructor injection
    public ProductController(ProductService productService) {
        this.productService = productService;
    }
    
    @GetMapping
    public ResponseEntity<Map<String, Object>> getProducts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "name") String sortBy,
            @RequestParam(defaultValue = "asc") String direction) {
        
        Page<Product> productPage = productService.getProductsByCategorySorted(
            "electronics", page, size, sortBy, direction);
        
        // Create response with pagination metadata
        Map<String, Object> response = new HashMap<>();
        response.put("products", productPage.getContent());
        response.put("currentPage", productPage.getNumber());
        response.put("totalItems", productPage.getTotalElements());
        response.put("totalPages", productPage.getTotalPages());
        
        return ResponseEntity.ok(response);
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of pagination concepts (zero-based indexing)
- Knowledge of performance implications
- Proper handling of pagination metadata
- Implementation in REST APIs

❌ **Common Mistakes:**
- Not handling invalid page/size parameters
- Ignoring performance implications for large datasets
- Returning entire Page object to clients (exposing internal details)
- Using `findAll()` without pagination for large datasets

📌 **Best Practices:**
- Always paginate large datasets
- Use appropriate page sizes (10-50 items typically)
- Consider using `Slice<T>` instead of `Page<T>` when count query is expensive
- Return a custom response object with pagination metadata (not the raw Page)
- Use sort specifications to prevent SQL injection

## 2. 🔄 Transactions (@Transactional)
---------

Transactions ensure data integrity and consistency by grouping operations that should succeed or fail as a unit.

### 🧩 Basic Usage

✅ **Core Concepts**
- `@Transactional` annotation - marks methods that should execute in a transaction
- ACID properties (Atomicity, Consistency, Isolation, Durability)
- Propagation - how transactions interact with existing transactions
- Isolation - how transactions see other transactions' changes

📌 **Simple Transaction Example**
```java
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final InventoryRepository inventoryRepository;
    
    public OrderService(OrderRepository orderRepository, InventoryRepository inventoryRepository) {
        this.orderRepository = orderRepository;
        this.inventoryRepository = inventoryRepository;
    }
    
    @Transactional
    public Order createOrder(OrderRequest request) {
        // Create new order
        Order order = new Order();
        order.setCustomerId(request.getCustomerId());
        order.setStatus("PENDING");
        
        // Save order to get ID
        orderRepository.save(order);
        
        // Add order items and update inventory
        for (OrderItemRequest itemRequest : request.getItems()) {
            // Check inventory
            Inventory inventory = inventoryRepository.findById(itemRequest.getProductId())
                .orElseThrow(() -> new EntityNotFoundException("Product not found"));
                
            if (inventory.getQuantity() < itemRequest.getQuantity()) {
                throw new InsufficientInventoryException("Not enough stock available");
            }
            
            // Update inventory
            inventory.setQuantity(inventory.getQuantity() - itemRequest.getQuantity());
            inventoryRepository.save(inventory);
            
            // Create order item
            OrderItem item = new OrderItem();
            item.setOrder(order);
            item.setProductId(itemRequest.getProductId());
            item.setQuantity(itemRequest.getQuantity());
            item.setPrice(inventory.getPrice());
            
            order.getItems().add(item);
        }
        
        // Update order status
        order.setStatus("CREATED");
        return orderRepository.save(order);
    }
}
```

### 🧩 Advanced Transaction Features

```java
@Service
public class PaymentService {
    private final PaymentRepository paymentRepository;
    private final OrderRepository orderRepository;
    private final NotificationService notificationService;
    
    // Constructor injection
    
    // Custom transaction attributes
    @Transactional(
        propagation = Propagation.REQUIRED,
        isolation = Isolation.READ_COMMITTED,
        timeout = 30,
        rollbackFor = {PaymentFailedException.class},
        noRollbackFor = {RecordNotFoundException.class},
        readOnly = false
    )
    public Payment processPayment(Long orderId, PaymentRequest request) {
        // Implementation
    }
    
    // Read-only transaction
    @Transactional(readOnly = true)
    public List<Payment> getPaymentHistory(Long customerId) {
        return paymentRepository.findByCustomerId(customerId);
    }
    
    // Transaction with specific propagation
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logPaymentAttempt(PaymentAttempt attempt) {
        // Always creates a new transaction
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of transaction boundaries
- Knowledge of propagation modes and isolation levels
- Awareness of transaction pitfalls (self-invocation)
- Error handling within transactions

❌ **Common Mistakes:**
- Self-invocation problem (calling @Transactional method from within same class)
- Using @Transactional on private methods (won't work)
- Catching and handling exceptions without proper rollback
- Using unnecessarily high isolation levels
- Not considering transaction timeouts

📌 **Best Practices:**
- Use @Transactional at service layer (not repository or controller)
- Keep transactions as short as possible
- Use appropriate propagation and isolation levels
- Consider read-only for queries (optimization)
- Understand the persistence context lifecycle

## 3. 📝 Auditing (CreatedBy, LastModifiedBy)
---------

Auditing automatically tracks entity creation and modification metadata.

### 🧩 Basic Setup

✅ **Key Components**
- Spring Data JPA auditing annotations
- `@EnableJpaAuditing` - Enables auditing functionality
- `@EntityListeners` - Hooks into entity lifecycle
- `AuditorAware` - Provides the current user

📌 **Configuration**
```java
// Enable JPA Auditing
@Configuration
@EnableJpaAuditing
public class AuditingConfig {
    @Bean
    public AuditorAware<String> auditorProvider() {
        return new AuditorAwareImpl();
    }
}

// Custom AuditorAware implementation
public class AuditorAwareImpl implements AuditorAware<String> {
    @Override
    public Optional<String> getCurrentAuditor() {
        // Get username from Spring Security context
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        
        if (authentication == null || !authentication.isAuthenticated() ||
                authentication instanceof AnonymousAuthenticationToken) {
            return Optional.of("system");
        }
        
        return Optional.of(authentication.getName());
    }
}
```

### 🧩 Auditable Entities

```java
// Base entity with auditing fields
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {
    @CreatedBy
    @Column(name = "created_by", nullable = false, updatable = false)
    private String createdBy;
    
    @CreatedDate
    @Column(name = "created_date", nullable = false, updatable = false)
    private Instant createdDate;
    
    @LastModifiedBy
    @Column(name = "last_modified_by", nullable = false)
    private String lastModifiedBy;
    
    @LastModifiedDate
    @Column(name = "last_modified_date", nullable = false)
    private Instant lastModifiedDate;
    
    // Getters (no setters for auditing fields)
}

// Using the auditable base class
@Entity
@Table(name = "customers")
public class Customer extends Auditable {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    
    // Business fields, getters, setters
}
```

### 🧩 Custom Auditing Implementation

For cases where you need more control or additional fields:

```java
@Entity
@Table(name = "orders")
public class Order {
    @Id @GeneratedValue
    private Long id;
    
    private String status;
    private BigDecimal totalAmount;
    
    @Column(name = "created_by", updatable = false)
    private String createdBy;
    
    @Column(name = "created_date", updatable = false)
    private Instant createdDate;
    
    @Column(name = "modified_by")
    private String modifiedBy;
    
    @Column(name = "modified_date")
    private Instant modifiedDate;
    
    // Additional custom audit fields
    @Column(name = "status_changed_by")
    private String statusChangedBy;
    
    @Column(name = "status_changed_date")
    private Instant statusChangedDate;
    
    // Business methods, getters, setters
    
    // Custom status change tracking
    public void updateStatus(String newStatus, String username) {
        this.status = newStatus;
        this.statusChangedBy = username;
        this.statusChangedDate = Instant.now();
    }
    
    // Pre-persist lifecycle hook
    @PrePersist
    public void prePersist() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = auth != null ? auth.getName() : "system";
        
        this.createdBy = username;
        this.createdDate = Instant.now();
        this.modifiedBy = username;
        this.modifiedDate = Instant.now();
    }
    
    // Pre-update lifecycle hook
    @PreUpdate
    public void preUpdate() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = auth != null ? auth.getName() : "system";
        
        this.modifiedBy = username;
        this.modifiedDate = Instant.now();
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Knowledge of JPA lifecycle events
- Integration with security context
- Understanding of audit trail requirements
- Implementation of custom auditing logic

❌ **Common Mistakes:**
- Forgetting @EnableJpaAuditing configuration
- Not implementing AuditorAware correctly
- Making auditing fields updatable
- Relying on auditing without proper security context setup

📌 **Best Practices:**
- Create a base auditable class for consistency
- Separate technical auditing from business-specific tracking
- Consider storing user IDs instead of usernames
- Add indexes on frequently queried audit fields
- Consider using Envers for historical auditing

## 4. 🔒 Optimistic Locking
---------

Optimistic locking prevents conflicts when multiple users attempt to update the same entity concurrently.

### 🧩 Implementation

✅ **Core Concept**
- Uses a version field to detect concurrent modifications
- No database locks are acquired, hence "optimistic"
- Throws OptimisticLockingFailureException when conflict is detected

📌 **Basic Implementation**
```java
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue
    private Long id;
    
    private String name;
    private String description;
    private BigDecimal price;
    private Integer stockQuantity;
    
    @Version
    private Long version; // Optimistic locking version field
    
    // Getters and setters
}
```

### 🧩 Handling Optimistic Locking Exceptions

```java
@Service
public class InventoryService {
    private final ProductRepository productRepository;
    
    public InventoryService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }
    
    @Transactional
    public Product updateStock(Long productId, int quantity) {
        try {
            Product product = productRepository.findById(productId)
                .orElseThrow(() -> new EntityNotFoundException("Product not found"));
                
            product.setStockQuantity(quantity);
            return productRepository.save(product);
        } catch (OptimisticLockingFailureException e) {
            // Handle concurrency conflict
            throw new ConcurrentModificationException("Product was updated by another user. Please try again.");
        }
    }
    
    // Advanced retry mechanism
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public Product updateStockWithRetry(Long productId, int quantity, int maxRetries) {
        int attempts = 0;
        while (attempts < maxRetries) {
            try {
                Product product = productRepository.findById(productId)
                    .orElseThrow(() -> new EntityNotFoundException("Product not found"));
                    
                product.setStockQuantity(quantity);
                return productRepository.save(product);
            } catch (OptimisticLockingFailureException e) {
                attempts++;
                if (attempts >= maxRetries) {
                    throw new ConcurrentModificationException(
                        "Failed to update product after " + maxRetries + " attempts");
                }
                
                // Wait before retrying (with exponential backoff)
                try {
                    Thread.sleep((long) Math.pow(2, attempts) * 100);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Interrupted while waiting to retry", ie);
                }
            }
        }
        throw new RuntimeException("Unexpected error in retry logic");
    }
}
```

### 🧩 Controller Integration

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final InventoryService inventoryService;
    
    // Constructor injection
    
    @PutMapping("/{id}/stock")
    public ResponseEntity<?> updateStock(@PathVariable Long id, 
                                      @RequestBody StockUpdateRequest request) {
        try {
            Product product = inventoryService.updateStockWithRetry(id, request.getQuantity(), 3);
            return ResponseEntity.ok(product);
        } catch (ConcurrentModificationException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(new ErrorResponse("CONFLICT", e.getMessage()));
        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(new ErrorResponse("NOT_FOUND", e.getMessage()));
        }
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of concurrency control mechanisms
- Knowledge of optimistic vs. pessimistic locking
- Implementation of retry mechanisms
- Handling of conflict resolution

❌ **Common Mistakes:**
- Not considering optimistic locking for concurrent updates
- Ignoring OptimisticLockingFailureException
- Using pessimistic locking when optimistic would suffice
- Not implementing proper retry mechanisms
- Having too many retries or infinite retry loops

📌 **Best Practices:**
- Use optimistic locking for high-concurrency, low-conflict scenarios
- Implement exponential backoff in retry mechanisms
- Consider using @Version with both timestamp and numeric types
- Add appropriate exception handling at service and controller levels
- Communicate conflicts clearly to end users

## 5. 💻 Complete Example: Customer Order System
---------

This example integrates all four concepts in a real-world scenario:

```java
// Base auditable entity
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Version
    private Long version;
    
    @CreatedBy
    @Column(name = "created_by", nullable = false, updatable = false)
    private String createdBy;
    
    @CreatedDate
    @Column(name = "created_date", nullable = false, updatable = false)
    private Instant createdDate;
    
    @LastModifiedBy
    @Column(name = "last_modified_by", nullable = false)
    private String lastModifiedBy;
    
    @LastModifiedDate
    @Column(name = "last_modified_date", nullable = false)
    private Instant lastModifiedDate;
    
    // Getters (no setters for audit fields)
    // Getter and setter for id
    
    public Long getVersion() {
        return version;
    }
}

// Order entity
@Entity
@Table(name = "orders")
public class Order extends BaseEntity {
    @Column(nullable = false)
    private String status;
    
    @Column(name = "total_amount", nullable = false)
    private BigDecimal totalAmount;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;
    
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<OrderItem> items = new HashSet<>();
    
    // Getters and setters
    // Helper methods
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }
    
    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}

// Order Item entity
@Entity
@Table(name = "order_items")
public class OrderItem extends BaseEntity {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;
    
    @Column(nullable = false)
    private Integer quantity;
    
    @Column(nullable = false)
    private BigDecimal price;
    
    // Getters and setters
}

// Repository with pagination
public interface OrderRepository extends JpaRepository<Order, Long> {
    // Find orders by customer with pagination
    Page<Order> findByCustomerId(Long customerId, Pageable pageable);
    
    // Find orders by status with pagination
    Page<Order> findByStatus(String status, Pageable pageable);
    
    // Find orders by date range
    @Query("SELECT o FROM Order o WHERE o.createdDate BETWEEN :startDate AND :endDate")
    Page<Order> findByDateRange(
        @Param("startDate") Instant startDate,
        @Param("endDate") Instant endDate,
        Pageable pageable
    );
}

// Service with transactions and optimistic locking handling
@Service
public class OrderService {
    private static final int MAX_RETRIES = 3;
    
    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;
    private final ProductRepository productRepository;
    private final InventoryRepository inventoryRepository;
    
    // Constructor injection
    
    // Create a new order
    @Transactional
    public Order createOrder(Long customerId, List<OrderItemRequest> itemRequests) {
        Customer customer = customerRepository.findById(customerId)
            .orElseThrow(() -> new EntityNotFoundException("Customer not found"));
        
        Order order = new Order();
        order.setCustomer(customer);
        order.setStatus("PENDING");
        order.setTotalAmount(BigDecimal.ZERO);
        
        // Calculate total and add items
        BigDecimal total = BigDecimal.ZERO;
        for (OrderItemRequest itemRequest : itemRequests) {
            Product product = productRepository.findById(itemRequest.getProductId())
                .orElseThrow(() -> new EntityNotFoundException("Product not found"));
                
            // Update inventory with retry for concurrent modifications
            updateInventory(product.getId(), itemRequest.getQuantity());
            
            OrderItem item = new OrderItem();
            item.setProduct(product);
            item.setQuantity(itemRequest.getQuantity());
            item.setPrice(product.getPrice());
            order.addItem(item);
            
            // Calculate item total
            BigDecimal itemTotal = product.getPrice()
                .multiply(BigDecimal.valueOf(itemRequest.getQuantity()));
            total = total.add(itemTotal);
        }
        
        order.setTotalAmount(total);
        order.setStatus("CREATED");
        
        return orderRepository.save(order);
    }
    
    // Update inventory with retry logic for optimistic locking
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void updateInventory(Long productId, int quantityToSubtract) {
        int retries = 0;
        while (retries < MAX_RETRIES) {
            try {
                // Get inventory with pessimistic lock for this critical operation
                Inventory inventory = inventoryRepository.findByProductId(productId)
                    .orElseThrow(() -> new EntityNotFoundException("Inventory not found"));
                
                if (inventory.getQuantity() < quantityToSubtract) {
                    throw new InsufficientInventoryException(
                        "Not enough stock for product ID: " + productId);
                }
                
                inventory.setQuantity(inventory.getQuantity() - quantityToSubtract);
                inventoryRepository.save(inventory);
                return;
            } catch (OptimisticLockingFailureException e) {
                retries++;
                if (retries >= MAX_RETRIES) {
                    throw new ConcurrentModificationException(
                        "Failed to update inventory after " + MAX_RETRIES + " attempts");
                }
                
                // Exponential backoff
                try {
                    Thread.sleep((long) Math.pow(2, retries) * 100);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Retry interrupted", ie);
                }
            }
        }
    }
    
    // Get order history with pagination
    @Transactional(readOnly = true)
    public Page<Order> getCustomerOrders(Long customerId, int page, int size, String sortBy) {
        Sort sort = Sort.by(Sort.Direction.DESC, sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);
        return orderRepository.findByCustomerId(customerId, pageable);
    }
    
    // Update order status with optimistic locking
    @Transactional
    public Order updateOrderStatus(Long orderId, String newStatus) {
        try {
            Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new EntityNotFoundException("Order not found"));
                
            order.setStatus(newStatus);
            return orderRepository.save(order);
        } catch (OptimisticLockingFailureException e) {
            throw new ConcurrentModificationException(
                "Order was updated by another process. Please try again.");
        }
    }
}

// Controller with pagination support
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orderService;
    
    // Constructor injection
    
    @PostMapping
    public ResponseEntity<Order> createOrder(
            @RequestBody OrderRequest request) {
        Order order = orderService.createOrder(request.getCustomerId(), request.getItems());
        return ResponseEntity.status(HttpStatus.CREATED).body(order);
    }
    
    @GetMapping("/customer/{customerId}")
    public ResponseEntity<Map<String, Object>> getCustomerOrders(
            @PathVariable Long customerId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "createdDate") String sortBy) {
        
        Page<Order> orderPage = orderService.getCustomerOrders(customerId, page, size, sortBy);
        
        Map<String, Object> response = new HashMap<>();
        response.put("orders", orderPage.getContent());
        response.put("currentPage", orderPage.getNumber());
        response.put("totalItems", orderPage.getTotalElements());
        response.put("totalPages", orderPage.getTotalPages());
        
        return ResponseEntity.ok(response);
    }
    
    @PatchMapping("/{orderId}/status")
    public ResponseEntity<?> updateOrderStatus(
            @PathVariable Long orderId,
            @RequestBody StatusUpdateRequest request) {
        try {
            Order order = orderService.updateOrderStatus(orderId, request.getStatus());
            return ResponseEntity.ok(order);
        } catch (ConcurrentModificationException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(new ErrorResponse("CONFLICT", e.getMessage()));
        }
    }
}
```

## 6. 🎯 Summary
---------

### Key Takeaways

✅ **Pagination & Sorting**
- Essential for performance with large datasets
- Uses Pageable, PageRequest, and Page interfaces
- Supports dynamic sorting with Sort class
- Requires careful API design to include metadata

✅ **Transactions (@Transactional)**
- Ensures ACID properties for data operations
- Supports various propagation and isolation levels
- Works with Spring's declarative transaction management
- Must account for proxy-based limitations (self-invocation)

✅ **Auditing**
- Automatically tracks creation and modification metadata
- Requires @EnableJpaAuditing and AuditorAware implementation
- Uses EntityListeners to hook into JPA lifecycle events
- Can be extended for custom audit requirements

✅ **Optimistic Locking**
- Prevents concurrent update conflicts
- Uses @Version field to track entity state
- Throws OptimisticLockingFailureException on conflict
- Requires retry mechanisms for critical operations

### 📊 Quick Reference Table

| Topic | Key Components | Common Mistakes | Best Practices |
|-------|--------------|----------------|----------------|
| **Pagination & Sorting** | - Pageable interface<br>- PageRequest class<br>- Page/Slice return types | - Not handling large datasets<br>- Zero vs one-based indexing confusion | - Use appropriate page sizes<br>- Include pagination metadata<br>- Consider performance for count queries |
| **Transactions** | - @Transactional annotation<br>- Propagation modes<br>- Isolation levels | - Self-invocation problem<br>- Using on private methods<br>- Ignoring runtime exceptions | - Apply at service layer<br>- Keep transactions short<br>- Use readOnly for queries<br>- Understand propagation |
| **Auditing** | - @EnableJpaAuditing<br>- AuditorAware<br>- @CreatedBy, @LastModifiedBy | - Missing configuration<br>- No security context<br>- Making audit fields updatable | - Create base entity class<br>- Store user IDs, not names<br>- Consider performance impact |
| **Optimistic Locking** | - @Version annotation<br>- OptimisticLockingFailureException<br>- Retry mechanisms | - No conflict handling<br>- Infinite retry loops<br>- Poor user experience | - Use for low-conflict scenarios<br>- Implement exponential backoff<br>- Communicate conflicts clearly |

### 🔄 Integration Diagram

```
┌─────────────────┐          ┌────────────────┐          ┌───────────────┐
│                 │          │                │          │               │
│    Controller   │◄─────────┤    Service     │◄─────────┤  Repository   │
│    (API Layer)  │          │ (Transaction   │          │  (Data Access │
│                 │          │  Boundary)     │          │   Layer)      │
└─────────┬───────┘          └─────────┬──────┘          └───────┬───────┘
          │                            │                         │
          ▼                            ▼                         ▼
┌─────────────────┐          ┌────────────────┐          ┌───────────────┐
│  Pagination     │          │  Transaction   │          │  Entities     │
│  Parameters     │          │  Management    │          │  (Auditing &  │
│  & Response     │          │  & Retries     │          │   Versioning) │
└─────────────────┘          └────────────────┘          └───────────────┘
```

### 📝 Interview Preparation Tips

1. **Understand the Spring Data infrastructure** and how these features work together
2. **Be prepared to explain transaction isolation levels** and their trade-offs
3. **Know how to handle optimistic locking exceptions** with proper retry mechanisms
4. **Explain pagination best practices** for API design and frontend integration
5. **Discuss auditing implementation options** for different security requirements

Remember to focus on real-world application scenarios during interviews. Being able to explain not just how these features work but when and why to use them will demonstrate your practical experience with Spring Data JPA.