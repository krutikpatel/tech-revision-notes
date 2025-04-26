# 🚀 Java Spring Framework: Advanced Data Access & Persistence

I'll guide you through JPQL & Native Queries, Query Methods, and Criteria API for Spring Data JPA with interview-ready examples.

## 1. 🔍 JPQL & Native Queries
---------

JPQL (Java Persistence Query Language) is a platform-independent object-oriented query language defined as part of the JPA specification, while Native Queries are database-specific SQL queries.

### 🧩 JPQL Queries

✅ **Basic Concepts**
- JPQL syntax is similar to SQL but operates on entity objects, not database tables
- Entity and property names in JPQL are case-sensitive
- JPQL uses the entity name (not table name) and field names (not column names)

📌 **JPQL in Repositories**
```java
public interface EmployeeRepository extends JpaRepository<Employee, Long> {
    // Using @Query with JPQL
    @Query("SELECT e FROM Employee e WHERE e.department.name = :deptName")
    List<Employee> findByDepartmentName(@Param("deptName") String deptName);
    
    // JPQL with ordering
    @Query("SELECT e FROM Employee e WHERE e.salary > :minSalary ORDER BY e.salary DESC")
    List<Employee> findHighPaidEmployees(@Param("minSalary") BigDecimal minSalary);
    
    // JPQL with JOIN
    @Query("SELECT e FROM Employee e JOIN e.projects p WHERE p.name = :projectName")
    List<Employee> findByProjectName(@Param("projectName") String projectName);
}
```

### 🧩 Native SQL Queries

Native queries allow you to use database-specific SQL when JPQL isn't sufficient.

```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    // Native SQL query (note the nativeQuery = true)
    @Query(value = "SELECT * FROM products WHERE YEAR(created_date) = :year", 
           nativeQuery = true)
    List<Product> findProductsCreatedInYear(@Param("year") int year);
    
    // Native query with complex database functions
    @Query(value = "SELECT * FROM products WHERE MATCH(description) AGAINST(:terms IN BOOLEAN MODE)",
           nativeQuery = true)
    List<Product> fullTextSearch(@Param("terms") String searchTerms);
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of when to use JPQL vs Native queries
- Ability to write complex joins and subqueries
- Knowledge of performance implications
- Parameter binding security awareness

❌ **Common Mistakes:**
- Using native queries when JPQL would suffice
- String concatenation instead of parameter binding (SQL injection risk)
- Not considering database portability with native queries
- Ignoring query optimization

📌 **Best Practices:**
- Use JPQL for most queries (database portability)
- Use native queries only when necessary (database-specific features)
- Always use parameter binding with @Param to prevent SQL injection
- Consider using projections for better performance

## 2. 📚 Query Methods
---------

Query methods allow you to define repository methods using method naming conventions that Spring Data JPA automatically translates into queries.

### 🧩 Method Name Structure

Query methods follow a defined pattern: `findBy`, `countBy`, `deleteBy`, etc., followed by property expressions.

```java
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    // Simple property expression
    List<Customer> findByLastName(String lastName);
    
    // AND condition
    List<Customer> findByFirstNameAndLastName(String firstName, String lastName);
    
    // OR condition
    List<Customer> findByFirstNameOrLastName(String firstName, String lastName);
    
    // Comparison operators
    List<Customer> findByAgeLessThan(int age);
    List<Customer> findByAgeGreaterThanEqual(int age);
    List<Customer> findByAgeBetween(int startAge, int endAge);
    
    // LIKE operations
    List<Customer> findByEmailContaining(String emailPart);
    List<Customer> findByLastNameStartingWith(String prefix);
    List<Customer> findByFirstNameEndingWith(String suffix);
    
    // NULL checks
    List<Customer> findByPhoneNumberIsNull();
    List<Customer> findByPhoneNumberIsNotNull();
    
    // IN clause
    List<Customer> findByStatusIn(List<String> statuses);
    
    // Nested properties
    List<Customer> findByAddressCity(String city);
    List<Customer> findByOrdersItemName(String itemName);
    
    // Sorting
    List<Customer> findByLastNameOrderByFirstNameAsc(String lastName);
    
    // First/Top/Distinct
    Customer findFirstByOrderByCreatedAtDesc();
    List<Customer> findTop3ByOrderByPointsDesc();
    List<Customer> findDistinctByAddressZipCode(String zipCode);
}
```

### 🧩 Advanced Query Methods

✅ **Pagination and Sorting**
```java
// Using Pageable for dynamic pagination and sorting
Page<Customer> findByStatus(String status, Pageable pageable);

// Usage in service layer
public Page<Customer> getActiveCustomers(int page, int size, String sortBy) {
    return customerRepository.findByStatus(
        "ACTIVE", 
        PageRequest.of(page, size, Sort.by(sortBy))
    );
}
```

✅ **Streaming Results**
```java
// For processing large result sets
@Query("SELECT c FROM Customer c")
Stream<Customer> streamAllCustomers();

// Usage with try-with-resources
public void processAllCustomers() {
    try (Stream<Customer> customerStream = customerRepository.streamAllCustomers()) {
        customerStream.forEach(this::processCustomer);
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Knowledge of supported keywords and operators
- Understanding of how method names translate to queries
- Awareness of performance implications for complex names
- Knowledge of when to use method names vs. @Query

❌ **Common Mistakes:**
- Overly complex method names that are hard to read
- Not understanding generated SQL complexity
- Using query methods for complex queries better suited for @Query
- Ignoring the N+1 query problem with nested properties

📌 **Best Practices:**
- Keep method names concise and readable
- Use @Query for complex queries instead of long method names
- Leverage Pageable for large result sets
- Use projections to fetch only needed data
- Check generated SQL for method names in development

## 3. 🔧 Criteria API
---------

The Criteria API provides a programmatic, type-safe way to construct queries that can be built dynamically at runtime.

### 🧩 Basic Criteria Queries

```java
@Repository
public class CustomerCriteriaRepository {
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<Customer> findCustomersByMultipleCriteria(String firstName, 
                                                       String lastName,
                                                       Integer minAge,
                                                       String city) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Customer> query = cb.createQuery(Customer.class);
        Root<Customer> customer = query.from(Customer.class);
        
        // Start with an always-true predicate
        Predicate predicate = cb.conjunction();
        
        // Add conditions only if parameters are provided
        if (firstName != null) {
            predicate = cb.and(predicate, cb.equal(customer.get("firstName"), firstName));
        }
        
        if (lastName != null) {
            predicate = cb.and(predicate, cb.equal(customer.get("lastName"), lastName));
        }
        
        if (minAge != null) {
            predicate = cb.and(predicate, cb.greaterThanOrEqualTo(customer.get("age"), minAge));
        }
        
        if (city != null) {
            // Join to address entity
            Join<Customer, Address> address = customer.join("address");
            predicate = cb.and(predicate, cb.equal(address.get("city"), city));
        }
        
        query.where(predicate);
        
        return entityManager.createQuery(query).getResultList();
    }
}
```

### 🧩 Integrating Criteria API With Spring Data JPA

Using JPA's Specification interface with Spring Data JPA:

```java
// Define the repository interface
public interface CustomerRepository extends JpaRepository<Customer, Long>, 
                                           JpaSpecificationExecutor<Customer> {
}

// Create specifications
public class CustomerSpecifications {
    public static Specification<Customer> hasFirstName(String firstName) {
        return (root, query, criteriaBuilder) -> 
            firstName == null ? null : criteriaBuilder.equal(root.get("firstName"), firstName);
    }
    
    public static Specification<Customer> hasLastName(String lastName) {
        return (root, query, criteriaBuilder) -> 
            lastName == null ? null : criteriaBuilder.equal(root.get("lastName"), lastName);
    }
    
    public static Specification<Customer> hasMinAge(Integer minAge) {
        return (root, query, criteriaBuilder) -> 
            minAge == null ? null : criteriaBuilder.greaterThanOrEqualTo(root.get("age"), minAge);
    }
    
    public static Specification<Customer> livesIn(String city) {
        return (root, query, criteriaBuilder) -> {
            if (city == null) return null;
            Join<Customer, Address> address = root.join("address");
            return criteriaBuilder.equal(address.get("city"), city);
        };
    }
}

// Usage in service
@Service
public class CustomerService {
    private final CustomerRepository customerRepository;
    
    public CustomerService(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }
    
    public Page<Customer> searchCustomers(String firstName, String lastName, 
                                        Integer minAge, String city,
                                        int page, int size) {
        Specification<Customer> spec = Specification
            .where(CustomerSpecifications.hasFirstName(firstName))
            .and(CustomerSpecifications.hasLastName(lastName))
            .and(CustomerSpecifications.hasMinAge(minAge))
            .and(CustomerSpecifications.livesIn(city));
            
        return customerRepository.findAll(spec, PageRequest.of(page, size));
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of when to use Criteria API over JPQL or Query Methods
- Knowledge of dynamic query construction
- Type-safety awareness
- Integration with Spring Data JPA

❌ **Common Mistakes:**
- Using Criteria API for simple queries (over-engineering)
- Not handling null parameters properly
- Creating complex joins without proper planning
- Missing proper error handling or validation

📌 **Best Practices:**
- Use Criteria API for complex dynamic queries
- Combine with Specification pattern for clean, reusable code
- Consider creating a query builder abstraction for complex cases
- Test generated SQL with different parameter combinations
- Use metamodel classes for type-safe property references

## 4. 💻 Complete Example: Product Catalog System
---------

This example shows all three approaches working together in a product catalog system:

```java
// Entity classes
@Entity
@Table(name = "categories")
public class Category {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String name;
    
    @OneToMany(mappedBy = "category", cascade = CascadeType.ALL)
    private Set<Product> products = new HashSet<>();
    
    // Getters and setters
}

@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    private String description;
    
    @Column(nullable = false)
    private BigDecimal price;
    
    @Column(name = "stock_quantity")
    private Integer stockQuantity;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;
    
    @ManyToMany
    @JoinTable(
        name = "product_tags",
        joinColumns = @JoinColumn(name = "product_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();
    
    // Getters and setters
}

@Entity
@Table(name = "tags")
public class Tag {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String name;
    
    @ManyToMany(mappedBy = "tags")
    private Set<Product> products = new HashSet<>();
    
    // Getters and setters
}

// DTO for query results
public class ProductSummary {
    private Long id;
    private String name;
    private BigDecimal price;
    private String categoryName;
    
    // Constructor, getters, setters
    public ProductSummary(Long id, String name, BigDecimal price, String categoryName) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.categoryName = categoryName;
    }
}

// Repository with mixed query approaches
public interface ProductRepository extends JpaRepository<Product, Long>, 
                                          JpaSpecificationExecutor<Product> {
    // 1. Query methods
    List<Product> findByCategoryName(String categoryName);
    List<Product> findByPriceBetweenOrderByPriceAsc(BigDecimal min, BigDecimal max);
    
    // 2. JPQL queries
    @Query("SELECT p FROM Product p WHERE p.price < :price AND p.stockQuantity > 0")
    List<Product> findInStockProductsCheaperThan(@Param("price") BigDecimal price);
    
    @Query("SELECT p FROM Product p JOIN p.tags t WHERE t.name IN :tagNames GROUP BY p HAVING COUNT(t) = :tagCount")
    List<Product> findByAllTagNames(@Param("tagNames") List<String> tagNames, @Param("tagCount") Long tagCount);
    
    // 3. Native query example
    @Query(value = "SELECT * FROM products p WHERE MATCH(p.description) AGAINST(:keywords IN BOOLEAN MODE) LIMIT 20", 
           nativeQuery = true)
    List<Product> findByFullTextSearch(@Param("keywords") String keywords);
    
    // 4. Projection example
    @Query("SELECT new com.example.shop.dto.ProductSummary(p.id, p.name, p.price, p.category.name) " +
           "FROM Product p WHERE p.category.name = :categoryName")
    List<ProductSummary> findProductSummariesByCategory(@Param("categoryName") String categoryName);
}

// Specifications for Criteria API
public class ProductSpecifications {
    public static Specification<Product> hasCategory(String categoryName) {
        return (root, query, cb) -> {
            if (categoryName == null) return null;
            Join<Product, Category> category = root.join("category");
            return cb.equal(category.get("name"), categoryName);
        };
    }
    
    public static Specification<Product> hasPriceRange(BigDecimal min, BigDecimal max) {
        return (root, query, cb) -> {
            if (min == null && max == null) return null;
            if (min == null) return cb.lessThanOrEqualTo(root.get("price"), max);
            if (max == null) return cb.greaterThanOrEqualTo(root.get("price"), min);
            return cb.between(root.get("price"), min, max);
        };
    }
    
    public static Specification<Product> hasKeywordInName(String keyword) {
        return (root, query, cb) -> {
            if (keyword == null) return null;
            return cb.like(cb.lower(root.get("name")), "%" + keyword.toLowerCase() + "%");
        };
    }
    
    public static Specification<Product> isInStock() {
        return (root, query, cb) -> cb.greaterThan(root.get("stockQuantity"), 0);
    }
    
    public static Specification<Product> hasTag(String tagName) {
        return (root, query, cb) -> {
            if (tagName == null) return null;
            Join<Product, Tag> tag = root.join("tags");
            return cb.equal(tag.get("name"), tagName);
        };
    }
}

// Service using all approaches
@Service
public class ProductService {
    private final ProductRepository productRepository;
    private final EntityManager entityManager;
    
    public ProductService(ProductRepository productRepository, EntityManager entityManager) {
        this.productRepository = productRepository;
        this.entityManager = entityManager;
    }
    
    // Using query methods
    public List<Product> getProductsByCategory(String categoryName) {
        return productRepository.findByCategoryName(categoryName);
    }
    
    // Using JPQL
    public List<Product> getAffordableInStockProducts(BigDecimal maxPrice) {
        return productRepository.findInStockProductsCheaperThan(maxPrice);
    }
    
    // Using native query
    public List<Product> searchProductsByKeywords(String keywords) {
        return productRepository.findByFullTextSearch(keywords);
    }
    
    // Using criteria API with specifications  
    public Page<Product> searchProducts(String keyword, String categoryName, 
                                     BigDecimal minPrice, BigDecimal maxPrice,
                                     Boolean inStockOnly, String tagName,
                                     int page, int size) {
        Specification<Product> spec = Specification
            .where(ProductSpecifications.hasKeywordInName(keyword))
            .and(ProductSpecifications.hasCategory(categoryName))
            .and(ProductSpecifications.hasPriceRange(minPrice, maxPrice))
            .and(inStockOnly ? ProductSpecifications.isInStock() : null)
            .and(ProductSpecifications.hasTag(tagName));
            
        return productRepository.findAll(spec, PageRequest.of(page, size));
    }
    
    // Using pure criteria API for complex dynamic query
    public List<Product> findSimilarProducts(Long productId, boolean includeSameCategory, 
                                          boolean includeOverlappingTags, 
                                          boolean includeSimilarPrice,
                                          int maxResults) {
        // Get reference product
        Product reference = productRepository.findById(productId)
            .orElseThrow(() -> new EntityNotFoundException("Product not found"));
            
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Product> query = cb.createQuery(Product.class);
        Root<Product> product = query.from(Product.class);
        
        // Exclude the reference product itself
        Predicate predicate = cb.notEqual(product.get("id"), productId);
        
        if (includeSameCategory && reference.getCategory() != null) {
            predicate = cb.and(predicate, 
                cb.equal(product.get("category"), reference.getCategory()));
        }
        
        if (includeSimilarPrice && reference.getPrice() != null) {
            BigDecimal minPrice = reference.getPrice().multiply(new BigDecimal("0.8"));
            BigDecimal maxPrice = reference.getPrice().multiply(new BigDecimal("1.2"));
            predicate = cb.and(predicate, 
                cb.between(product.get("price"), minPrice, maxPrice));
        }
        
        if (includeOverlappingTags && !reference.getTags().isEmpty()) {
            // This requires a subquery to find products with matching tags
            Subquery<Long> tagSubquery = query.subquery(Long.class);
            Root<Product> subProduct = tagSubquery.from(Product.class);
            Join<Product, Tag> tag = subProduct.join("tags");
            
            tagSubquery.select(cb.count(tag))
                .where(cb.and(
                    cb.equal(subProduct.get("id"), product.get("id")),
                    tag.in(reference.getTags())
                ));
                
            predicate = cb.and(predicate, cb.greaterThan(tagSubquery, 0L));
        }
        
        query.where(predicate);
        
        // Order by relevance (count of matching criteria)
        return entityManager.createQuery(query)
            .setMaxResults(maxResults)
            .getResultList();
    }
}
```

## 5. 🎯 Summary
---------

### Key Takeaways

✅ **JPQL & Native Queries**
- JPQL works with entities, not tables
- Native queries provide direct SQL access for database-specific features
- Both support named parameters with @Param annotation
- Use @Query annotation in repository interfaces

✅ **Query Methods**
- Method names automatically translated to queries
- Support for conditions, sorting, limiting, and pagination
- Great for simple to moderately complex queries
- Type-safe but can get unwieldy for complex conditions

✅ **Criteria API**
- Programmatic, type-safe query construction
- Perfect for dynamic queries with conditional clauses
- Integrates with Spring Data via Specifications
- More verbose but offers maximum flexibility

### 📊 Quick Reference Table

| Topic | Key Features | When to Use | Common Pitfalls | Best Practices |
|-------|-------------|------------|----------------|----------------|
| **JPQL Queries** | - Entity-based<br>- Database agnostic<br>- Support for joins, aggregates | - Complex queries<br>- When query logic is static | - N+1 problem<br>- String-based (not type-safe) | - Use named parameters<br>- Consider projections<br>- Test with explain plan |
| **Native Queries** | - Raw SQL<br>- Database specific<br>- Full SQL feature access | - DB-specific features needed<br>- Complex reporting | - DB portability issues<br>- SQL injection risk | - Only when necessary<br>- Always use parameters<br>- Document DB dependencies |
| **Query Methods** | - Method name parsing<br>- Automatic implementation<br>- Type-safe | - Simple conditions<br>- Standard operations | - Long method names<br>- Limited expressiveness | - Keep names short<br>- Use for simple queries<br>- Check generated SQL |
| **Criteria API** | - Type-safe<br>- Dynamic query building<br>- Programmatic control | - Complex conditions<br>- Runtime query building | - Verbose code<br>- Learning curve | - Use specifications<br>- Create reusable components<br>- Unit test thoroughly |

### 🔄 Selection Flow Chart

```
┌─────────────────────┐     Simple query?     ┌─────────────────────┐
│                     │        Yes            │                     │
│  Need to query      ├────────────────────────►  Query Methods     │
│  data in Spring     │                       │                     │
│  Data JPA?          │                       └─────────────────────┘
│                     │
└──────────┬──────────┘
           │
           │ No
           ▼
┌─────────────────────┐     Static query?     ┌─────────────────────┐
│  Complex query      │        Yes            │                     │
│  conditions?        ├────────────────────────►  JPQL with @Query  │
│                     │                       │                     │
└──────────┬──────────┘                       └─────────────────────┘
           │
           │ No
           ▼
┌─────────────────────┐    DB specific        ┌─────────────────────┐
│  Dynamic query      │    features?          │                     │
│  built at runtime?  │        Yes            │  Native SQL Query   │
│                     ├────────────────────────►                     │
└──────────┬──────────┘                       └─────────────────────┘
           │
           │ No
           ▼
┌─────────────────────┐
│                     │
│  Criteria API with  │
│  Specifications     │
│                     │
└─────────────────────┘
```

### 📝 Interview Preparation Tips

1. **Understand the strengths and weaknesses** of each query approach
2. **Be ready to explain** when you would choose one approach over another
3. **Practice writing complex queries** using all three approaches
4. **Know how to optimize** performance for each approach
5. **Understand transaction management** context for queries

Remember to focus on practical use cases rather than just syntax. Interviewers want to see that you can apply these different querying techniques to solve real-world problems effectively and know which technique is most appropriate for different scenarios.