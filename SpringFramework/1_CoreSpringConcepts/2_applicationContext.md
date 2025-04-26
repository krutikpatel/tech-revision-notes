# 🌟 Java Spring Framework: Spring Application Context

## 1. 🏛️ Spring Application Context - Fundamentals
---------

The Spring Application Context is a central component of the Spring Framework that represents the IoC (Inversion of Control) container. It's responsible for instantiating, configuring, and assembling beans.

### 📌 What is Spring Application Context?

Spring Application Context is an advanced container that enhances the basic functionality provided by BeanFactory. It's the cornerstone of a Spring application that manages the complete lifecycle of Spring beans.

```
┌────────────────────────────────────────────┐
│             Spring Application             │
│                                            │
│  ┌────────────────────────────────────────┐│
│  │        Application Context             ││
│  │                                        ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐ ││
│  │  │ Bean 1  │  │ Bean 2  │  │ Bean 3  │ ││
│  │  └─────────┘  └─────────┘  └─────────┘ ││
│  │                                        ││
│  └────────────────────────────────────────┘│
└────────────────────────────────────────────┘
```

### 🔄 BeanFactory vs ApplicationContext

While BeanFactory is the basic container, ApplicationContext provides more enterprise-specific functionality:

✅ **ApplicationContext advantages**:
- Event publication
- Internationalization (i18n) support
- Integration with Spring AOP
- Message resource handling
- Application-layer specific contexts

```java
// BeanFactory (basic)
BeanFactory factory = new XmlBeanFactory(new FileSystemResource("beans.xml"));

// ApplicationContext (preferred)
ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
```

### 📌 Key Implementations of ApplicationContext

1. **ClassPathXmlApplicationContext**: Loads context definitions from XML files in the classpath
2. **FileSystemXmlApplicationContext**: Loads context definitions from XML files in the file system
3. **AnnotationConfigApplicationContext**: Loads context definitions from annotated Java classes
4. **WebApplicationContext**: Used in web applications (has a link to the ServletContext)
5. **GenericApplicationContext**: Flexible context implementation that can be configured through reader delegates

```java
// Loading context from XML
ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");

// Loading context from annotated classes
ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);

// Using GenericApplicationContext
GenericApplicationContext context = new GenericApplicationContext();
new XmlBeanDefinitionReader(context).loadBeanDefinitions("applicationContext.xml");
context.refresh();
```

## 2. 🛠️ Working with Application Context
---------

### 📌 Creating and Configuring ApplicationContext

Spring offers several ways to bootstrap and configure an ApplicationContext:

1. **XML-based configuration**:

```java
ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
```

2. **Java-based configuration**:

```java
@Configuration
public class AppConfig {
    @Bean
    public UserService userService() {
        return new UserServiceImpl();
    }
}

// Loading context from Java config
ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
```

3. **Annotation-based configuration**:

```java
@Component
public class UserService {
    // ...
}

// Enable component scanning
@Configuration
@ComponentScan(basePackages = "com.example")
public class AppConfig {
    // ...
}
```

4. **Hybrid configuration** (mixing XML and annotations):

```java
@Configuration
@ImportResource("classpath:applicationContext.xml")
public class AppConfig {
    // Java-based configuration
}
```

### 📌 Getting Beans from ApplicationContext

```java
// By type
UserService userService = context.getBean(UserService.class);

// By name
UserService userService = (UserService) context.getBean("userService");

// By name and type
UserService userService = context.getBean("userService", UserService.class);

// Check if bean exists
boolean exists = context.containsBean("userService");
```

### 📌 ApplicationContext Hierarchies

Application contexts can be organized in parent-child hierarchies, allowing bean definitions to be searched in parent contexts if not found in children.

```java
// Create parent context
ApplicationContext parent = new ClassPathXmlApplicationContext("parent-context.xml");

// Create child context with parent reference
ApplicationContext child = new ClassPathXmlApplicationContext(
    new String[] {"child-context.xml"}, parent);
```

## 3. 🚀 Advanced Features of ApplicationContext
---------

### 📌 Event Publication

The ApplicationContext provides an event propagation mechanism that allows beans to communicate with each other through events.

```java
// Custom event
public class UserCreatedEvent extends ApplicationEvent {
    private User user;
    
    public UserCreatedEvent(Object source, User user) {
        super(source);
        this.user = user;
    }
    
    public User getUser() {
        return user;
    }
}

// Publishing events
@Service
public class UserService {
    @Autowired
    private ApplicationEventPublisher publisher;
    
    public void createUser(User user) {
        // Create user logic...
        publisher.publishEvent(new UserCreatedEvent(this, user));
    }
}

// Handling events
@Component
public class UserEventListener {
    @EventListener
    public void handleUserCreated(UserCreatedEvent event) {
        System.out.println("User created: " + event.getUser().getUsername());
    }
}
```

### 📌 Internationalization Support

ApplicationContext provides support for internationalization:

```java
// Define messages in properties files
// messages_en.properties: greeting=Hello
// messages_fr.properties: greeting=Bonjour

@Configuration
public class I18nConfig {
    @Bean
    public MessageSource messageSource() {
        ResourceBundleMessageSource messageSource = new ResourceBundleMessageSource();
        messageSource.setBasename("messages");
        messageSource.setDefaultEncoding("UTF-8");
        return messageSource;
    }
}

// Using message source
@Service
public class GreetingService {
    @Autowired
    private MessageSource messageSource;
    
    public String getGreeting(Locale locale) {
        return messageSource.getMessage("greeting", null, locale);
    }
}
```

### 📌 Resource Loading

ApplicationContext also acts as a ResourceLoader to access resources:

```java
@Service
public class ResourceService {
    @Autowired
    private ApplicationContext context;
    
    public String readTextFile(String location) throws IOException {
        Resource resource = context.getResource(location);
        try (InputStream is = resource.getInputStream()) {
            return StreamUtils.copyToString(is, StandardCharsets.UTF_8);
        }
    }
}
```

### 📌 Environment Abstraction

The Environment interface represents the environment in which the application is running:

```java
@Component
public class EnvService {
    @Autowired
    private Environment env;
    
    public String getDatabaseUrl() {
        return env.getProperty("database.url");
    }
    
    public boolean isProduction() {
        return env.matchesProfiles("production");
    }
}
```

## 4. ⚠️ Common Mistakes & Best Practices
---------

### ❌ Common Mistakes & Traps

1. **Excessive context creation**: Creating multiple contexts unnecessarily can lead to memory issues
   
2. **Bean overriding without intent**: Accidentally overriding beans due to component scanning

   ```java
   // Class in com.example.service
   @Component("userService")
   public class UserServiceImpl implements UserService { ... }
   
   // Class in com.example.impl (also scanned)
   @Component("userService") // This will override the previous bean!
   public class AnotherUserServiceImpl implements UserService { ... }
   ```

3. **Missing @Configuration annotation**: Causes @Bean methods to be treated as regular methods

   ```java
   // Missing @Configuration!
   public class AppConfig {
       @Bean
       public DataSource dataSource() {
           return new BasicDataSource();
       }
       
       @Bean
       public JdbcTemplate jdbcTemplate() {
           // Without @Configuration, this calls the actual method, not the bean!
           return new JdbcTemplate(dataSource()); 
       }
   }
   ```

4. **Circular dependencies**: Can cause initialization issues
   
5. **Loading incorrect context for environment**: Using a web context in a non-web application

### ✅ Best Practices

1. **Use appropriate context implementation**
   - WebApplicationContext for web applications
   - AnnotationConfigApplicationContext for standalone applications

2. **Prefer Java-based or annotation-based configuration** over XML

3. **Organize contexts properly**
   - Use @ComponentScan with specific packages
   - Group related beans in dedicated @Configuration classes
   
   ```java
   @Configuration
   @ComponentScan(basePackages = {
       "com.example.service",
       "com.example.repository"
   })
   public class AppConfig { ... }
   ```

4. **Follow proper bean naming conventions**
   - Use consistent naming patterns
   - Avoid duplicate bean names across contexts

5. **Manage lifecycle efficiently**
   - Close contexts when no longer needed
   - Use try-with-resources for standalone applications
   
   ```java
   try (ConfigurableApplicationContext context = 
           new AnnotationConfigApplicationContext(AppConfig.class)) {
       // Use context...
   } // Context will be closed automatically
   ```

6. **Use profile-specific configurations**
   
   ```java
   @Configuration
   @Profile("development")
   public class DevConfig {
       @Bean
       public DataSource dataSource() {
           // Development datasource
       }
   }
   
   @Configuration
   @Profile("production")
   public class ProdConfig {
       @Bean
       public DataSource dataSource() {
           // Production datasource
       }
   }
   ```

## 5. 🚀 Integration with Spring Boot
---------

Spring Boot uses ApplicationContext but simplifies its configuration and bootstrapping:

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(MyApplication.class, args);
        // The context is created and configured automatically
    }
}
```

### 📌 Under the Hood

Spring Boot creates an appropriate ApplicationContext based on your application type:
- `AnnotationConfigServletWebServerApplicationContext` for web applications
- `AnnotationConfigApplicationContext` for standalone applications

### 📌 ApplicationContext in Spring Boot Tests

```java
@SpringBootTest
class UserServiceTest {
    @Autowired
    private ApplicationContext context;
    
    @Test
    void contextLoads() {
        assertNotNull(context);
        assertTrue(context.containsBean("userService"));
    }
}
```

## 6. 📝 Summary (Quick Revision)
---------

### 📌 Key Concepts

- **ApplicationContext** is Spring's advanced IoC container that manages the complete lifecycle of beans
- It extends **BeanFactory** and adds enterprise features like event handling, i18n, AOP integration
- Multiple implementations exist for different scenarios (XML, annotation, web applications)
- ApplicationContext can load beans from various sources (XML, Java config, annotations)
- Advanced features include event publication, resource loading, and environment abstraction
- Spring Boot automatically configures an appropriate ApplicationContext

### 📌 Interview Focal Points

- Know the difference between BeanFactory and ApplicationContext
- Understand different ways to bootstrap an ApplicationContext
- Be familiar with context hierarchies and bean lookup rules
- Explain ApplicationContext's role in a Spring application architecture
- Understand how ApplicationContext interacts with other Spring components

## 7. 📊 Quick Reference Tables
---------

### 📌 ApplicationContext Types

| Type | Use Case | When to Use |
|------|----------|-------------|
| ClassPathXmlApplicationContext | XML config from classpath | Older Spring apps, XML config preference |
| FileSystemXmlApplicationContext | XML config from filesystem | External XML config files |
| AnnotationConfigApplicationContext | Java-based & annotation config | Modern Spring apps, no XML |
| WebApplicationContext | Web applications | Any Spring web app |
| XmlWebApplicationContext | XML-based web apps | Older Spring web apps |
| AnnotationConfigWebApplicationContext | Annotation-based web apps | Modern Spring web apps |
| GenericApplicationContext | Advanced customization | Custom loading behavior |

### 📌 Common ApplicationContext Methods

| Method | Purpose | Example Usage |
|--------|---------|---------------|
| getBean() | Retrieve a bean | context.getBean("userService") |
| getBeansOfType() | Get all beans of a type | context.getBeansOfType(UserService.class) |
| containsBean() | Check if bean exists | context.containsBean("userService") |
| getBeanDefinitionNames() | Get all bean names | context.getBeanDefinitionNames() |
| getEnvironment() | Get environment | context.getEnvironment().getProperty("db.url") |
| getResource() | Load a resource | context.getResource("classpath:data.txt") |
| publishEvent() | Publish an event | context.publishEvent(new CustomEvent(this)) |

### 📌 Configuration Approaches Comparison

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| XML-based | Separation from code, no recompilation | Verbose, typo-prone, no compile-time checks | Legacy apps, third-party integration |
| Java-based | Type-safety, refactoring support, IDE help | Requires recompilation, more code | Modern apps, complex configuration |
| Annotation-based | Less code, co-located with beans | Scattered configuration, implicit behavior | Rapid development, simpler apps |
| Hybrid | Flexibility, gradual migration | Complexity, multiple sources of truth | Migration scenarios |

## 8. 🎓 Interview Q&A
---------

### 📌 Common Interview Questions

1. **Q**: What is the difference between BeanFactory and ApplicationContext?
   **A**: ApplicationContext extends BeanFactory, adding enterprise features like event publication, i18n support, integration with AOP, message resource handling, and application-layer contexts. BeanFactory is a basic IoC container, while ApplicationContext is a complete spring module.

2. **Q**: How can you create an ApplicationContext in Spring?
   **A**: Through XML configuration (`ClassPathXmlApplicationContext`), Java-based configuration (`AnnotationConfigApplicationContext`), or in web applications (`WebApplicationContext`). Spring Boot automatically creates the appropriate context with `SpringApplication.run()`.

3. **Q**: How does bean lookup work in a hierarchical ApplicationContext?
   **A**: When a bean is requested, Spring first looks in the current context. If not found, it looks in parent contexts. This allows specialized contexts to override beans from parent contexts while still having access to shared beans.

4. **Q**: How would you handle different environments (dev, test, prod) in Spring?
   **A**: Use Spring's profile feature with `@Profile` annotations on configuration classes, or property placeholders with environment-specific property files. The Environment abstraction in ApplicationContext helps access the active profiles and properties.

5. **Q**: How can beans communicate with each other in an ApplicationContext?
   **A**: Direct method calls (autowiring), through the ApplicationEventPublisher mechanism (event-driven), or using Spring Integration for more complex scenarios.

6. **Q**: What are the ways to bootstrap ApplicationContext in a Spring Boot application?
   **A**: The primary way is `SpringApplication.run(Application.class, args)`. For testing, use `@SpringBootTest`. For advanced scenarios, `SpringApplicationBuilder` provides a fluent API to customize the bootstrap process.

7. **Q**: How would you refresh an ApplicationContext at runtime?
   **A**: Call `refresh()` on `ConfigurableApplicationContext`. However, this is rarely needed and can cause issues with existing beans. A better approach is to use Spring Cloud Config for dynamic property changes or use conditional beans with the Environment abstraction.

---

May your Spring contexts always be properly configured and your beans well-managed! 🌱 Good luck with your interviews! 🍀