# 🚀 Java Spring Framework: Database Integration - Advanced Topics

I'll guide you through configuring multiple data sources and working with NoSQL databases in Spring to help you prepare for interviews.

## 1. 📊 Multiple Data Sources
---------

Working with multiple databases is common in enterprise applications, especially when dealing with legacy systems, microservices, or data segregation requirements.

### 🧩 Core Concepts

✅ **Why Multiple Data Sources?**
- Data segregation for security or compliance reasons
- Integration with legacy systems
- Microservice architecture with separate databases
- Read/write splitting for performance optimization
- Different database technologies for different use cases

📌 **Basic Implementation Steps**
1. Configure multiple DataSource beans
2. Create separate EntityManager instances
3. Configure transaction managers for each DataSource
4. Use appropriate annotations to direct repositories to correct data sources

### 🧩 Configuration Example

#### Maven Dependencies
```xml
<dependencies>
    <!-- Spring Data JPA -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- Multiple database drivers -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
    </dependency>
</dependencies>
```

#### Properties Configuration
```properties
# Primary Database (MySQL)
spring.datasource.primary.jdbc-url=jdbc:mysql://localhost:3306/primary_db
spring.datasource.primary.username=root
spring.datasource.primary.password=password
spring.datasource.primary.driver-class-name=com.mysql.cj.jdbc.Driver

# Secondary Database (H2)
spring.datasource.secondary.jdbc-url=jdbc:h2:mem:secondary_db
spring.datasource.secondary.username=sa
spring.datasource.secondary.password=
spring.datasource.secondary.driver-class-name=org.h2.Driver
```

#### Java Configuration
```java
@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
    basePackages = "com.example.primary.repository",
    entityManagerFactoryRef = "primaryEntityManagerFactory",
    transactionManagerRef = "primaryTransactionManager"
)
public class PrimaryDataSourceConfig {

    @Primary
    @Bean(name = "primaryDataSource")
    @ConfigurationProperties("spring.datasource.primary")
    public DataSource dataSource() {
        return DataSourceBuilder.create().build();
    }

    @Primary
    @Bean(name = "primaryEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("primaryDataSource") DataSource dataSource) {
        
        return builder
                .dataSource(dataSource)
                .packages("com.example.primary.model")
                .persistenceUnit("primary")
                .properties(getHibernateProperties())
                .build();
    }

    @Primary
    @Bean(name = "primaryTransactionManager")
    public PlatformTransactionManager transactionManager(
            @Qualifier("primaryEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        
        return new JpaTransactionManager(entityManagerFactory);
    }
    
    private Map<String, Object> getHibernateProperties() {
        Map<String, Object> properties = new HashMap<>();
        properties.put("hibernate.hbm2ddl.auto", "update");
        properties.put("hibernate.dialect", "org.hibernate.dialect.MySQL8Dialect");
        return properties;
    }
}
```

```java
@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
    basePackages = "com.example.secondary.repository",
    entityManagerFactoryRef = "secondaryEntityManagerFactory",
    transactionManagerRef = "secondaryTransactionManager"
)
public class SecondaryDataSourceConfig {

    @Bean(name = "secondaryDataSource")
    @ConfigurationProperties("spring.datasource.secondary")
    public DataSource dataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name = "secondaryEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("secondaryDataSource") DataSource dataSource) {
        
        return builder
                .dataSource(dataSource)
                .packages("com.example.secondary.model")
                .persistenceUnit("secondary")
                .properties(getHibernateProperties())
                .build();
    }

    @Bean(name = "secondaryTransactionManager")
    public PlatformTransactionManager transactionManager(
            @Qualifier("secondaryEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        
        return new JpaTransactionManager(entityManagerFactory);
    }
    
    private Map<String, Object> getHibernateProperties() {
        Map<String, Object> properties = new HashMap<>();
        properties.put("hibernate.hbm2ddl.auto", "create-drop");
        properties.put("hibernate.dialect", "org.hibernate.dialect.H2Dialect");
        return properties;
    }
}
```

### 🧩 Entity and Repository Classes

```java
// Primary database entity
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String email;
    
    // Getters and setters
}

// Secondary database entity
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private BigDecimal price;
    
    // Getters and setters
}
```

```java
// Primary database repository
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByEmail(String email);
}

// Secondary database repository
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByPriceGreaterThan(BigDecimal price);
}
```

### 🧩 Service Layer Example

```java
@Service
public class UserService {
    private final UserRepository userRepository;
    private final ProductRepository productRepository;
    
    @Autowired
    public UserService(UserRepository userRepository, 
                      ProductRepository productRepository) {
        this.userRepository = userRepository;
        this.productRepository = productRepository;
    }
    
    // Method using primary database
    @Transactional("primaryTransactionManager")
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    // Method using secondary database
    @Transactional("secondaryTransactionManager")
    public Product createProduct(Product product) {
        return productRepository.save(product);
    }
    
    // Method using both databases
    public UserProductSummary getUserProductSummary(Long userId) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
        
        List<Product> products = productRepository.findAll();
        
        return new UserProductSummary(user, products);
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of Spring's configuration for multiple data sources
- Knowledge of transaction management across multiple databases
- Awareness of the trade-offs and complexities involved
- Implementation strategies for cross-database operations

❌ **Common Mistakes:**
- Forgetting the @Primary annotation for default datasource
- Missing @Qualifier annotations when autowiring DataSource beans
- Incorrect package scanning configuration for repositories
- Transaction management issues with cross-database operations
- Not considering connection pool settings for each datasource

📌 **Best Practices:**
- Clearly separate entities and repositories by package structure
- Always specify the transaction manager for methods accessing specific databases
- Keep cross-database operations to a minimum
- Use DTO patterns for data that spans multiple databases
- Consider using AbstractRoutingDataSource for dynamic data source switching
- Monitor connection pools for each datasource independently

## 2. 🔄 Working with NoSQL Databases
---------

NoSQL databases provide flexible schema designs, horizontal scalability, and specialized data models for different use cases.

### 🧩 MongoDB Integration

MongoDB is a document-oriented NoSQL database that stores data in flexible, JSON-like documents.

#### Maven Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-mongodb</artifactId>
</dependency>
```

#### Basic Configuration
```properties
# MongoDB configuration
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.database=testdb
spring.data.mongodb.username=admin
spring.data.mongodb.password=password
```

#### Document Class
```java
@Document(collection = "customers")
public class Customer {
    @Id
    private String id;
    
    private String firstName;
    private String lastName;
    private String email;
    
    @Field("birth_date")
    private LocalDate birthDate;
    
    @DBRef
    private List<Address> addresses;
    
    // Embedded document
    private ContactInfo contactInfo;
    
    // Getters and setters
}

@Document(collection = "addresses")
public class Address {
    @Id
    private String id;
    
    private String street;
    private String city;
    private String state;
    private String zipCode;
    
    // Getters and setters
}

// Embedded document class (no @Document annotation)
public class ContactInfo {
    private String phoneNumber;
    private String alternateEmail;
    
    // Getters and setters
}
```

#### Repository Interface
```java
@Repository
public interface CustomerRepository extends MongoRepository<Customer, String> {
    
    List<Customer> findByLastName(String lastName);
    
    List<Customer> findByAddressesCity(String city);
    
    @Query("{ 'contactInfo.phoneNumber': ?0 }")
    Optional<Customer> findByPhoneNumber(String phoneNumber);
    
    @Query("{ 'birthDate': { $gte: ?0, $lte: ?1 } }")
    List<Customer> findByBirthDateBetween(LocalDate startDate, LocalDate endDate);
    
    @Aggregation(pipeline = {
        "{ $match: { 'addresses.city': ?0 } }",
        "{ $group: { _id: '$lastName', count: { $sum: 1 } } }",
        "{ $sort: { count: -1 } }"
    })
    List<Document> countCustomersByLastNameInCity(String city);
}
```

#### Service Layer
```java
@Service
public class CustomerService {
    private final CustomerRepository customerRepository;
    private final MongoTemplate mongoTemplate;
    
    @Autowired
    public CustomerService(CustomerRepository customerRepository, 
                          MongoTemplate mongoTemplate) {
        this.customerRepository = customerRepository;
        this.mongoTemplate = mongoTemplate;
    }
    
    public Customer createCustomer(Customer customer) {
        return customerRepository.save(customer);
    }
    
    public List<Customer> findByLastName(String lastName) {
        return customerRepository.findByLastName(lastName);
    }
    
    // Using MongoTemplate for complex queries
    public List<Customer> findCustomersWithMultipleCriteria(String lastName, 
                                                         String city, 
                                                         LocalDate minBirthDate) {
        Query query = new Query();
        
        if (lastName != null) {
            query.addCriteria(Criteria.where("lastName").regex(lastName, "i"));
        }
        
        if (city != null) {
            query.addCriteria(Criteria.where("addresses.city").is(city));
        }
        
        if (minBirthDate != null) {
            query.addCriteria(Criteria.where("birthDate").gte(minBirthDate));
        }
        
        return mongoTemplate.find(query, Customer.class);
    }
}
```

### 🧩 Redis Integration

Redis is an in-memory data structure store, used as a database, cache, and message broker.

#### Maven Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

#### Basic Configuration
```properties
# Redis configuration
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.password=password
spring.redis.database=0
spring.redis.timeout=2000
```

#### Redis Configuration Class
```java
@Configuration
@EnableRedisRepositories
public class RedisConfig {
    
    @Bean
    public LettuceConnectionFactory redisConnectionFactory(
            RedisProperties redisProperties) {
        
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration();
        config.setHostName(redisProperties.getHost());
        config.setPort(redisProperties.getPort());
        config.setPassword(RedisPassword.of(redisProperties.getPassword()));
        config.setDatabase(redisProperties.getDatabase());
        
        return new LettuceConnectionFactory(config);
    }
    
    @Bean
    public RedisTemplate<String, Object> redisTemplate(
            RedisConnectionFactory connectionFactory) {
        
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        
        // Configure serializers
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        
        return template;
    }
    
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration cacheConfig = RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10))
                .serializeKeysWith(SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()))
                .disableCachingNullValues();
        
        return RedisCacheManager.builder(connectionFactory)
                .cacheDefaults(cacheConfig)
                .withCacheConfiguration("users", 
                    RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofMinutes(5)))
                .withCacheConfiguration("products", 
                    RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofMinutes(30)))
                .build();
    }
}
```

#### Redis Entity
```java
@RedisHash("session")
public class UserSession implements Serializable {
    @Id
    private String id;
    
    private String username;
    private Set<String> permissions;
    private Date lastAccess;
    
    @TimeToLive
    private Long expiration;
    
    // Getters and setters
}
```

#### Redis Repository
```java
@Repository
public interface UserSessionRepository extends CrudRepository<UserSession, String> {
    List<UserSession> findByUsername(String username);
}
```

#### Using Redis for Caching
```java
@Service
@CacheConfig(cacheNames = "products")
public class ProductService {
    private final ProductRepository productRepository;
    
    @Autowired
    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }
    
    @Cacheable(key = "#id")
    public Product getProduct(Long id) {
        System.out.println("Fetching product from database...");
        return productRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Product not found"));
    }
    
    @CacheEvict(key = "#product.id")
    public Product updateProduct(Product product) {
        return productRepository.save(product);
    }
    
    @CacheEvict(allEntries = true)
    public void clearProductCache() {
        System.out.println("Clearing product cache...");
    }
}
```

#### Using Redis as a Message Broker
```java
@Configuration
public class RedisMessageConfig {
    
    @Bean
    public RedisMessageListenerContainer redisMessageListenerContainer(
            RedisConnectionFactory connectionFactory,
            MessageListenerAdapter listenerAdapter) {
        
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        container.addMessageListener(listenerAdapter, new PatternTopic("notifications"));
        
        return container;
    }
    
    @Bean
    public MessageListenerAdapter listenerAdapter(NotificationReceiver receiver) {
        return new MessageListenerAdapter(receiver, "receiveMessage");
    }
    
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        template.setValueSerializer(new Jackson2JsonRedisSerializer<>(Object.class));
        return template;
    }
}

@Component
public class NotificationReceiver {
    
    public void receiveMessage(String message) {
        System.out.println("Received message: " + message);
        // Process the notification
    }
}

@Service
public class NotificationService {
    private final StringRedisTemplate redisTemplate;
    
    @Autowired
    public NotificationService(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }
    
    public void sendNotification(String message) {
        redisTemplate.convertAndSend("notifications", message);
    }
}
```

### 🛠️ Interview-Ready Insights

✅ **What interviewers look for:**
- Understanding of NoSQL database concepts and use cases
- Knowledge of Spring's MongoDB and Redis integration
- Implementation strategies for common patterns
- Awareness of performance considerations

❌ **Common Mistakes:**
- Using @DBRef unnecessarily (MongoDB)
- Ignoring serialization configuration (Redis)
- Not considering TTL settings for cached items
- Improper indexing strategies for MongoDB
- Using NoSQL databases for relational data without proper planning

📌 **Best Practices:**
- MongoDB:
  - Use embedded documents for one-to-few relationships
  - Use @DBRef only when necessary for one-to-many or many-to-many relationships
  - Create appropriate indexes for frequently queried fields
  - Consider using MongoTemplate for complex queries

- Redis:
  - Configure appropriate serializers for keys and values
  - Set reasonable TTL values for cached items
  - Use cache eviction strategies to manage memory
  - Consider cluster configuration for high availability
  - Implement proper exception handling for Redis operations

## 3. 💻 Complete Integration Example
---------

This example demonstrates a Spring Boot application that uses both a relational database (MySQL) and a NoSQL database (MongoDB) along with Redis for caching.

```java
@SpringBootApplication
public class MultiDatabaseApplication {
    public static void main(String[] args) {
        SpringApplication.run(MultiDatabaseApplication.class, args);
    }
}

// Configuration for MySQL
@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(
    basePackages = "com.example.sql.repository",
    entityManagerFactoryRef = "sqlEntityManagerFactory",
    transactionManagerRef = "sqlTransactionManager"
)
public class MySQLConfig {
    
    @Primary
    @Bean(name = "sqlDataSource")
    @ConfigurationProperties("spring.datasource.mysql")
    public DataSource dataSource() {
        return DataSourceBuilder.create().build();
    }
    
    @Primary
    @Bean(name = "sqlEntityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(
            EntityManagerFactoryBuilder builder,
            @Qualifier("sqlDataSource") DataSource dataSource) {
        
        return builder
                .dataSource(dataSource)
                .packages("com.example.sql.entity")
                .persistenceUnit("sql")
                .properties(getSQLProperties())
                .build();
    }
    
    @Primary
    @Bean(name = "sqlTransactionManager")
    public PlatformTransactionManager transactionManager(
            @Qualifier("sqlEntityManagerFactory") EntityManagerFactory entityManagerFactory) {
        
        return new JpaTransactionManager(entityManagerFactory);
    }
    
    private Map<String, Object> getSQLProperties() {
        Map<String, Object> properties = new HashMap<>();
        properties.put("hibernate.dialect", "org.hibernate.dialect.MySQL8Dialect");
        properties.put("hibernate.hbm2ddl.auto", "update");
        return properties;
    }
}

// MongoDB Configuration
@Configuration
@EnableMongoRepositories(basePackages = "com.example.mongo.repository")
public class MongoConfig {
    
    @Bean
    public MongoCustomConversions mongoCustomConversions() {
        return new MongoCustomConversions(Arrays.asList(
            new DateToLocalDateConverter(),
            new LocalDateToDateConverter()
        ));
    }
    
    // Custom converters for LocalDate
    static class DateToLocalDateConverter implements Converter<Date, LocalDate> {
        @Override
        public LocalDate convert(Date source) {
            return source == null ? null : source.toInstant()
                    .atZone(ZoneId.systemDefault())
                    .toLocalDate();
        }
    }
    
    static class LocalDateToDateConverter implements Converter<LocalDate, Date> {
        @Override
        public Date convert(LocalDate source) {
            return source == null ? null : Date.from(source.atStartOfDay(ZoneId.systemDefault()).toInstant());
        }
    }
}

// Redis Configuration
@Configuration
@EnableCaching
public class RedisConfig {
    
    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory connectionFactory) {
        RedisCacheConfiguration cacheConfig = RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(10))
                .serializeKeysWith(SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()));
        
        return RedisCacheManager.builder(connectionFactory)
                .cacheDefaults(cacheConfig)
                .build();
    }
}

// Service that integrates both data stores
@Service
public class UserOrderService {
    private final UserRepository userRepository;
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    
    @Autowired
    public UserOrderService(UserRepository userRepository,
                          OrderRepository orderRepository,
                          ProductRepository productRepository) {
        this.userRepository = userRepository;
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
    }
    
    @Transactional("sqlTransactionManager")
    public Order createOrder(Long userId, List<OrderItem> items) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));
        
        Order order = new Order();
        order.setUser(user);
        order.setOrderDate(LocalDateTime.now());
        order.setStatus("PENDING");
        
        order = orderRepository.save(order);
        
        for (OrderItem item : items) {
            item.setOrder(order);
        }
        
        order.setItems(items);
        Order savedOrder = orderRepository.save(order);
        
        // Record in MongoDB for analytics
        saveOrderAnalytics(savedOrder);
        
        return savedOrder;
    }
    
    private void saveOrderAnalytics(Order order) {
        OrderAnalytics analytics = new OrderAnalytics();
        analytics.setOrderId(order.getId().toString());
        analytics.setUserId(order.getUser().getId().toString());
        analytics.setOrderDate(order.getOrderDate());
        analytics.setTotalAmount(order.getItems().stream()
                .map(item -> item.getPrice().multiply(new BigDecimal(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add));
        
        List<String> productIds = order.getItems().stream()
                .map(item -> item.getProduct().getId().toString())
                .collect(Collectors.toList());
        analytics.setProductIds(productIds);
        
        orderAnalyticsRepository.save(analytics);
    }
    
    @Cacheable(cacheNames = "userOrders", key = "#userId")
    public List<Order> getUserOrders(Long userId) {
        return orderRepository.findByUserId(userId);
    }
    
    @Cacheable(cacheNames = "productAnalytics", key = "#productId")
    public ProductAnalyticsSummary getProductAnalytics(Long productId) {
        // Get SQL data
        Product product = productRepository.findById(productId)
            .orElseThrow(() -> new EntityNotFoundException("Product not found"));
        
        // Get MongoDB analytics data
        List<OrderAnalytics> analytics = orderAnalyticsRepository
            .findByProductIdsContaining(productId.toString());
        
        // Combine data
        return createAnalyticsSummary(product, analytics);
    }
    
    private ProductAnalyticsSummary createAnalyticsSummary(Product product, 
                                                        List<OrderAnalytics> analytics) {
        // Create summary using data from both sources
        ProductAnalyticsSummary summary = new ProductAnalyticsSummary();
        summary.setProductId(product.getId());
        summary.setProductName(product.getName());
        summary.setCurrentPrice(product.getPrice());
        
        // Calculate analytics
        long totalOrders = analytics.size();
        BigDecimal totalRevenue = analytics.stream()
                .map(OrderAnalytics::getTotalAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        summary.setTotalOrders(totalOrders);
        summary.setTotalRevenue(totalRevenue);
        
        return summary;
    }
}
```

## 4. 🎯 Summary
---------

### Key Takeaways

✅ **Multiple Data Sources**
- Enable separate packages for each data source
- Configure distinct EntityManagerFactory and TransactionManager beans
- Use @Primary for the default data source
- Apply @Qualifier to disambiguate when autowiring
- Specify the transaction manager when crossing data source boundaries

✅ **MongoDB Integration**
- Use @Document and @Id annotations for document mapping
- Apply @Field for custom field names
- Consider embedded documents vs. @DBRef for relationships
- Leverage MongoRepository for common operations
- Use MongoTemplate for complex queries and aggregations

✅ **Redis Integration**
- Configure serializers for keys and values
- Use @RedisHash for Redis entities
- Apply @Cacheable, @CacheEvict, and @CachePut annotations
- Set appropriate TTL values for cached items
- Consider Redis for caching, session management, and messaging

### 📊 Quick Reference Table

| Topic | Key Components | Common Mistakes | Best Practices |
|-------|--------------|----------------|----------------|
| **Multiple Data Sources** | - Separate @EnableJpaRepositories<br>- Multiple EntityManagerFactory beans<br>- Multiple TransactionManager beans | - Missing @Primary annotation<br>- Forgetting @Qualifier<br>- Transaction management issues | - Separate by package structure<br>- Clearly specify persistence unit<br>- Use DTOs for cross-database operations |
| **MongoDB Integration** | - @Document annotation<br>- MongoRepository interface<br>- MongoTemplate<br>- @DBRef for references | - Excessive use of @DBRef<br>- Improper indexing<br>- Relational data modeling | - Use embedded documents appropriately<br>- Create proper indexes<br>- Consider domain-driven document design<br>- Use MongoTemplate for complex queries |
| **Redis Integration** | - RedisTemplate<br>- @RedisHash annotation<br>- @Cacheable annotation<br>- RedisConnectionFactory | - Poor serialization configuration<br>- Missing TTL settings<br>- Not handling connection issues | - Configure proper serializers<br>- Set reasonable TTL values<br>- Use appropriate cache eviction<br>- Consider Redis Cluster for production |

### 🔄 Multiple Database Integration Flow

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│  Spring Service   │     │  Data Sources      │     │  Persistence      │
│  Layer            │     │  Configuration     │     │  Layer            │
└─────────┬─────────┘     └─────────┬─────────┘     └─────────┬─────────┘
          │                         │                         │
          ▼                         ▼                         ▼
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│ @Transactional    │     │ EntityManager     │     │ JPA/MongoDB/Redis │
│ Service Methods   │     │ Factory Beans     │     │ Repositories      │
└─────────┬─────────┘     └─────────┬─────────┘     └─────────┬─────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                                    ▼
                          ┌───────────────────┐
                          │  Multiple         │
                          │  Databases        │
                          └───────────────────┘
```

### 📝 Interview Preparation Tips

1. **Know the configuration steps** for setting up multiple data sources
2. **Understand transaction boundaries** when dealing with multiple databases
3. **Be familiar with document design patterns** for MongoDB
4. **Know when to use embedded documents vs. references** in MongoDB
5. **Understand Redis use cases** beyond simple caching
6. **Be prepared to discuss performance considerations** for each database type
7. **Know how to integrate data** from multiple database types
8. **Understand the monitoring and maintenance aspects** of multiple databases

Remember that interviewers want to see both theoretical knowledge and practical experience. Be ready to discuss real-world scenarios, challenges you've faced, and how you've solved them when working with multiple databases or NoSQL systems.