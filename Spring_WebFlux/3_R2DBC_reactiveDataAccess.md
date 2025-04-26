# R2DBC for Reactive Data Access in Spring WebFlux 🚀

This guide will help you understand R2DBC for reactive data access in Spring WebFlux with practical examples for your upcoming interviews.

## 1. 🌐 Introduction to R2DBC
---------

R2DBC (Reactive Relational Database Connectivity) is a specification and set of libraries that enables reactive programming against traditional relational databases.

### Why R2DBC?

Traditional JDBC is:
- Blocking and synchronous
- Thread-per-connection model
- Cannot be used effectively in reactive applications

R2DBC provides:
- Non-blocking database drivers
- Reactive streams support
- Fully asynchronous data access
- Integration with Spring's reactive stack

📌 **Key Insight**: R2DBC brings reactive programming to relational databases, similar to what Reactive Streams did for application-level processing.

```
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │
│  Spring WebFlux     │     │  Spring WebFlux     │
│      with           │     │      with           │
│  Spring Data R2DBC  │     │  Spring Data JPA    │
│                     │     │                     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
┌──────────▼──────────┐     ┌──────────▼──────────┐
│                     │     │                     │
│       R2DBC         │     │       JDBC          │
│  (Non-blocking)     │     │     (Blocking)      │
│                     │     │                     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
┌──────────▼──────────┐     ┌──────────▼──────────┐
│                     │     │                     │
│  Relational Database│     │  Relational Database│
│                     │     │                     │
└─────────────────────┘     └─────────────────────┘
```

✅ **Interview Tip**: Highlight that R2DBC enables end-to-end reactive programming from the web layer through to the database, eliminating blocking operations throughout the stack.

## 2. 🧩 Important R2DBC Classes & Interfaces
---------

### Core R2DBC Interfaces:

1. **ConnectionFactory**: Entry point to create connections
2. **Connection**: Represents a database connection
3. **Statement**: Used to execute SQL statements
4. **Result**: Represents query results
5. **Row**: Represents a single row in a result
6. **Batch**: For executing batch operations

### Spring Data R2DBC Key Components:

1. **R2dbcEntityTemplate**: Core class for R2DBC operations
2. **DatabaseClient**: Provides a fluent API for database interactions
3. **ReactiveCrudRepository**: Repository interface for CRUD operations
4. **R2dbcRepository**: Extended repository with additional features
5. **R2dbcTransactionManager**: Manages reactive transactions

📊 **Class Relationship Diagram**:

```
┌────────────────────┐     ┌───────────────────────┐
│                    │     │                       │
│  R2dbcRepository   │────►│  ReactiveCrudRepository│
│                    │     │                       │
└────────────────────┘     └───────────┬───────────┘
                                       │
                                       │
┌────────────────────┐     ┌───────────▼───────────┐
│                    │     │                       │
│ R2dbcEntityTemplate│────►│     DatabaseClient    │
│                    │     │                       │
└────────┬───────────┘     └───────────┬───────────┘
         │                             │
         │                             │
┌────────▼───────────┐     ┌───────────▼───────────┐
│                    │     │                       │
│ R2dbcTransactionManager  │    ConnectionFactory   │
│                    │     │                       │
└────────────────────┘     └───────────────────────┘
```

✅ **Best Practice**: Understand the relationship between these components to effectively work with R2DBC and explain them during interviews.

## 3. ⚙️ Setting Up R2DBC with Spring Boot
---------

### Maven Dependencies:

```xml
<dependencies>
    <!-- Spring WebFlux -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    
    <!-- Spring Data R2DBC -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-r2dbc</artifactId>
    </dependency>
    
    <!-- H2 Database Driver for R2DBC -->
    <dependency>
        <groupId>io.r2dbc</groupId>
        <artifactId>r2dbc-h2</artifactId>
        <scope>runtime</scope>
    </dependency>
    
    <!-- PostgreSQL Driver for R2DBC -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>r2dbc-postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

### Configuration Properties:

```properties
# application.properties

# R2DBC Configuration
spring.r2dbc.url=r2dbc:postgresql://localhost:5432/mydatabase
spring.r2dbc.username=postgres
spring.r2dbc.password=secret

# Connection Pool Configuration
spring.r2dbc.pool.enabled=true
spring.r2dbc.pool.initial-size=5
spring.r2dbc.pool.max-size=10
```

### Java Configuration:

```java
@Configuration
public class R2dbcConfig extends AbstractR2dbcConfiguration {
    
    @Value("${spring.r2dbc.url}")
    private String url;
    
    @Value("${spring.r2dbc.username}")
    private String username;
    
    @Value("${spring.r2dbc.password}")
    private String password;
    
    @Override
    @Bean
    public ConnectionFactory connectionFactory() {
        return ConnectionFactories.get(
            ConnectionFactoryOptions.builder()
                .option(DRIVER, "postgresql")
                .option(HOST, "localhost")
                .option(PORT, 5432)
                .option(USER, username)
                .option(PASSWORD, password)
                .option(DATABASE, "mydatabase")
                .build());
    }
    
    @Bean
    ReactiveTransactionManager transactionManager(ConnectionFactory connectionFactory) {
        return new R2dbcTransactionManager(connectionFactory);
    }
}
```

❌ **Common Mistake**: Using the wrong R2DBC URL format. R2DBC URLs use the format `r2dbc:{driver}://{host}:{port}/{database}` instead of JDBC's `jdbc:` format.

✅ **Interview Insight**: Explain that Spring Boot's auto-configuration simplifies R2DBC setup, but understanding the manual configuration demonstrates deeper knowledge.

## 4. 📝 Domain Model & Repository
---------

### Entity Class:

```java
@Data
@Table("users")
public class User {
    
    @Id
    private Long id;
    
    private String name;
    
    private String email;
    
    @Column("created_at")
    private LocalDateTime createdAt;
    
    // Constructors, getters and setters
}
```

### Repository Interface:

```java
@Repository
public interface UserRepository extends ReactiveCrudRepository<User, Long> {
    
    // Find by email
    Mono<User> findByEmail(String email);
    
    // Find by name containing string
    Flux<User> findByNameContainingIgnoreCase(String name);
    
    // Custom query example
    @Query("SELECT * FROM users WHERE created_at > :date")
    Flux<User> findUsersCreatedAfter(LocalDateTime date);
    
    // Count by example
    Mono<Long> countByEmailEndingWith(String emailDomain);
}
```

✅ **Best Practice**: Unlike JPA, R2DBC entities don't support entity relationships (no @OneToMany, etc.) directly. You'll need to handle relationships manually with joins or multiple queries.

❌ **Interview Trap**: Don't expect all JPA features to be available in R2DBC. Be ready to explain the limitations and differences.

## 5. 🔨 Using R2dbcEntityTemplate
---------

R2dbcEntityTemplate provides a more flexible alternative to repositories for advanced database operations.

```java
@Service
public class UserService {
    
    private final R2dbcEntityTemplate template;
    
    public UserService(R2dbcEntityTemplate template) {
        this.template = template;
    }
    
    // Find with criteria
    public Flux<User> findUsersByNameOrEmail(String term) {
        Criteria criteria = Criteria.where("name").like("%" + term + "%")
            .or(Criteria.where("email").like("%" + term + "%"));
            
        Query query = Query.query(criteria);
        
        return template.select(User.class)
                      .matching(query)
                      .all();
    }
    
    // Insert user
    public Mono<User> createUser(User user) {
        return template.insert(User.class)
                      .using(user);
    }
    
    // Update user
    public Mono<User> updateUser(User user) {
        return template.update(User.class)
                      .matching(Query.query(Criteria.where("id").is(user.getId())))
                      .apply(Update.update("name", user.getName())
                                 .set("email", user.getEmail()));
    }
    
    // Delete user
    public Mono<Void> deleteUser(Long id) {
        return template.delete(User.class)
                      .matching(Query.query(Criteria.where("id").is(id)))
                      .all()
                      .then();
    }
}
```

📌 **Key Insight**: R2dbcEntityTemplate provides a bridge between the flexibility of SQL and the convenience of object mapping.

✅ **Interview Tip**: Show how R2dbcEntityTemplate allows for more complex queries than repositories while still maintaining the reactive programming model.

## 6. 🚀 Performing CRUD Operations
---------

### Service Layer Implementation:

```java
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    
    // Create
    @Override
    public Mono<User> createUser(User user) {
        return userRepository.save(user);
    }
    
    // Read
    @Override
    public Mono<User> getUserById(Long id) {
        return userRepository.findById(id)
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }
    
    @Override
    public Flux<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    // Update
    @Override
    public Mono<User> updateUser(Long id, User userDetails) {
        return userRepository.findById(id)
            .flatMap(existingUser -> {
                existingUser.setName(userDetails.getName());
                existingUser.setEmail(userDetails.getEmail());
                return userRepository.save(existingUser);
            })
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }
    
    // Delete
    @Override
    public Mono<Void> deleteUser(Long id) {
        return userRepository.findById(id)
            .flatMap(user -> userRepository.delete(user))
            .switchIfEmpty(Mono.error(new UserNotFoundException(id)));
    }
}
```

### Controller Layer:

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<User> createUser(@RequestBody User user) {
        return userService.createUser(user);
    }
    
    @GetMapping("/{id}")
    public Mono<User> getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }
    
    @GetMapping
    public Flux<User> getAllUsers() {
        return userService.getAllUsers();
    }
    
    @PutMapping("/{id}")
    public Mono<User> updateUser(@PathVariable Long id, @RequestBody User user) {
        return userService.updateUser(id, user);
    }
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public Mono<Void> deleteUser(@PathVariable Long id) {
        return userService.deleteUser(id);
    }
}
```

❌ **Common Mistake**: Using `block()` or other blocking calls within reactive chains, which defeats the purpose of reactive programming.

✅ **Best Practice**: Use `flatMap()` when your operation returns another Publisher (like a Mono or Flux) and `map()` for simple transformations.

## 7. 🔄 Transaction Management
---------

Reactive transaction management in R2DBC is handled differently than in traditional JDBC/JPA.

### Declarative Transaction Management:

```java
@Service
public class TransferService {
    
    private final AccountRepository accountRepository;
    
    public TransferService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }
    
    @Transactional // Reactive transaction
    public Mono<TransferResult> transferFunds(Long fromId, Long toId, BigDecimal amount) {
        return accountRepository.findById(fromId)
            .flatMap(fromAccount -> {
                if (fromAccount.getBalance().compareTo(amount) < 0) {
                    return Mono.error(new InsufficientFundsException());
                }
                
                fromAccount.setBalance(fromAccount.getBalance().subtract(amount));
                return accountRepository.save(fromAccount)
                    .flatMap(saved -> accountRepository.findById(toId)
                        .flatMap(toAccount -> {
                            toAccount.setBalance(toAccount.getBalance().add(amount));
                            return accountRepository.save(toAccount);
                        })
                        .thenReturn(new TransferResult(fromId, toId, amount, true)));
            });
    }
}
```

### Programmatic Transaction Management:

```java
@Service
public class TransferService {
    
    private final AccountRepository accountRepository;
    private final TransactionalOperator transactionalOperator;
    
    public TransferService(
            AccountRepository accountRepository,
            ReactiveTransactionManager transactionManager) {
        this.accountRepository = accountRepository;
        this.transactionalOperator = TransactionalOperator.create(transactionManager);
    }
    
    public Mono<TransferResult> transferFunds(Long fromId, Long toId, BigDecimal amount) {
        Mono<TransferResult> transfer = accountRepository.findById(fromId)
            .flatMap(fromAccount -> {
                if (fromAccount.getBalance().compareTo(amount) < 0) {
                    return Mono.error(new InsufficientFundsException());
                }
                
                fromAccount.setBalance(fromAccount.getBalance().subtract(amount));
                return accountRepository.save(fromAccount)
                    .flatMap(saved -> accountRepository.findById(toId)
                        .flatMap(toAccount -> {
                            toAccount.setBalance(toAccount.getBalance().add(amount));
                            return accountRepository.save(toAccount);
                        })
                        .thenReturn(new TransferResult(fromId, toId, amount, true)));
            });
        
        // Apply transaction operator
        return transfer.as(transactionalOperator::transactional);
    }
}
```

📌 **Key Insight**: Transactions in reactive programming maintain the non-blocking nature while ensuring atomicity of operations.

❌ **Interview Trap**: Be aware that reactive transactions work differently from imperative ones. In reactive code, the transaction is only committed when the Mono/Flux completes successfully.

## 8. 🧪 Testing R2DBC Repositories
---------

### Unit Testing with TestContainers:

```java
@DataR2dbcTest
@Testcontainers
public class UserRepositoryTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");
    
    @DynamicPropertySource
    static void registerPgProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.r2dbc.url", 
            () -> String.format("r2dbc:postgresql://%s:%d/%s", 
                postgres.getHost(), 
                postgres.getFirstMappedPort(), 
                postgres.getDatabaseName()));
        registry.add("spring.r2dbc.username", postgres::getUsername);
        registry.add("spring.r2dbc.password", postgres::getPassword);
    }
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    public void shouldSaveAndFindUser() {
        // Create test user
        User user = new User();
        user.setName("Test User");
        user.setEmail("test@example.com");
        user.setCreatedAt(LocalDateTime.now());
        
        // Save and verify
        StepVerifier.create(userRepository.save(user))
            .expectNextMatches(saved -> saved.getId() != null && 
                             saved.getName().equals("Test User"))
            .verifyComplete();
        
        // Find and verify
        StepVerifier.create(userRepository.findByEmail("test@example.com"))
            .expectNextMatches(found -> found.getName().equals("Test User"))
            .verifyComplete();
    }
}
```

### Integration Testing:

```java
@SpringBootTest
@Testcontainers
public class UserServiceIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13");
    
    @DynamicPropertySource
    static void registerPgProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.r2dbc.url", 
            () -> String.format("r2dbc:postgresql://%s:%d/%s", 
                postgres.getHost(), 
                postgres.getFirstMappedPort(), 
                postgres.getDatabaseName()));
        registry.add("spring.r2dbc.username", postgres::getUsername);
        registry.add("spring.r2dbc.password", postgres::getPassword);
    }
    
    @Autowired
    private UserService userService;
    
    @Test
    public void testCreateAndGetUser() {
        User user = new User();
        user.setName("Integration Test");
        user.setEmail("integration@test.com");
        
        // Create user
        User savedUser = userService.createUser(user).block();
        assertNotNull(savedUser.getId());
        
        // Get user
        User foundUser = userService.getUserById(savedUser.getId()).block();
        assertEquals("Integration Test", foundUser.getName());
    }
}
```

✅ **Best Practice**: Use StepVerifier for testing reactive code to verify the sequence of events in a reactive stream.

❌ **Common Mistake**: Using `block()` in tests unnecessarily. While sometimes convenient for assertion, prefer using StepVerifier for more robust reactive tests.

## 9. 📊 Advanced R2DBC Techniques
---------

### Custom SQL Operations:

```java
@Repository
public class CustomUserRepository {
    
    private final DatabaseClient databaseClient;
    
    public CustomUserRepository(DatabaseClient databaseClient) {
        this.databaseClient = databaseClient;
    }
    
    public Flux<User> findUsersByComplex(String search, LocalDateTime since) {
        String sql = """
            SELECT * FROM users 
            WHERE (name ILIKE :search OR email ILIKE :search) 
            AND created_at > :since
            ORDER BY created_at DESC
            """;
        
        return databaseClient.sql(sql)
            .bind("search", "%" + search + "%")
            .bind("since", since)
            .map((row, metadata) -> {
                User user = new User();
                user.setId(row.get("id", Long.class));
                user.setName(row.get("name", String.class));
                user.setEmail(row.get("email", String.class));
                user.setCreatedAt(row.get("created_at", LocalDateTime.class));
                return user;
            })
            .all();
    }
    
    public Mono<Integer> batchUpdateUsers(List<User> users) {
        return Flux.fromIterable(users)
            .flatMap(user -> 
                databaseClient.sql("UPDATE users SET name = :name, email = :email WHERE id = :id")
                    .bind("id", user.getId())
                    .bind("name", user.getName())
                    .bind("email", user.getEmail())
                    .fetch()
                    .rowsUpdated()
            )
            .reduce(0, Integer::sum);
    }
}
```

### Handling Large Result Sets:

```java
@Service
public class ReportService {
    
    private final DatabaseClient databaseClient;
    
    public ReportService(DatabaseClient databaseClient) {
        this.databaseClient = databaseClient;
    }
    
    public Flux<UserActivity> streamUserActivity() {
        return databaseClient.sql("""
                SELECT u.id, u.name, u.email, count(l.id) as login_count
                FROM users u
                LEFT JOIN logins l ON u.id = l.user_id
                GROUP BY u.id, u.name, u.email
                """)
            .map((row, metadata) -> {
                UserActivity activity = new UserActivity();
                activity.setUserId(row.get("id", Long.class));
                activity.setName(row.get("name", String.class));
                activity.setEmail(row.get("email", String.class));
                activity.setLoginCount(row.get("login_count", Integer.class));
                return activity;
            })
            .all()
            // Use backpressure to prevent overwhelming consumers
            .limitRate(100);
    }
}
```

✅ **Interview Insight**: When dealing with large result sets in reactive applications, techniques like `limitRate()` help implement backpressure to prevent overwhelming downstream components.

📌 **Key Pattern**: For advanced operations, combining DatabaseClient with manual mapping provides maximum flexibility.

## 10. 📝 Summary of R2DBC with Spring WebFlux
---------

R2DBC provides a reactive API for relational databases, making it possible to build fully reactive applications with Spring WebFlux from the HTTP layer all the way to the database.

Key points to remember:

1. **Purpose**: Enables non-blocking database access for reactive applications
2. **Key Components**: ConnectionFactory, R2dbcEntityTemplate, ReactiveCrudRepository
3. **Programming Model**: Returns Mono/Flux instead of direct values or collections
4. **Limitations**: No built-in support for entity relationships like JPA
5. **Transactions**: Supports both declarative and programmatic reactive transactions
6. **Testing**: Use StepVerifier for testing reactive streams
7. **Advanced Usage**: DatabaseClient for complex queries and manual mapping

✅ **Interview Ready!**: When discussing R2DBC in interviews, emphasize how it completes the reactive stack for web applications and enables handling more concurrent users with fewer resources.

## 11. 📊 Summary Table
---------

| Topic | Key Points | Interview Focus |
|-------|------------|-----------------|
| **Purpose of R2DBC** | Non-blocking database access for reactive applications | Contrast with JDBC's blocking nature |
| **Core Components** | ConnectionFactory, R2dbcEntityTemplate, ReactiveCrudRepository | Class responsibilities and relationships |
| **Entity Mapping** | Uses @Table, @Id, @Column annotations | Limitations compared to JPA |
| **Repository Pattern** | ReactiveCrudRepository returns Mono/Flux | Method naming conventions |
| **Template API** | R2dbcEntityTemplate for flexible operations | When to use over repositories |
| **Transaction Management** | @Transactional or TransactionalOperator | How reactive transactions differ |
| **SQL Operations** | Use DatabaseClient for custom SQL | Manual row mapping techniques |
| **Testing** | StepVerifier for reactive assertions | Testing without blocking |
| **Connection Pooling** | Configure pool size based on workload | Performance considerations |
| **Best Practices** | Never block, use flatMap, handle errors reactively | Common anti-patterns |

✅ **Final Interview Tip**: In an interview, be prepared to discuss not just how R2DBC works, but when you would choose it over traditional JPA. Being able to articulate the tradeoffs demonstrates engineering maturity.