# 🚀 Core Spring Boot Concepts for Interviews

## 1. 🔄 Spring Boot Autoconfiguration
---------

Spring Boot Autoconfiguration is a key feature that automatically configures your Spring application based on the dependencies present in your classpath. It reduces boilerplate configuration, allowing you to focus on business logic.

### 📌 How Autoconfiguration Works

Spring Boot uses a combination of conditional annotations, property defaults, and component scanning to automatically configure your application:

```
┌───────────────────┐     ┌─────────────────┐     ┌───────────────────┐
│ Classpath Scanning│────▶│ Condition Check │────▶│ Bean Registration │
└───────────────────┘     └─────────────────┘     └───────────────────┘
```

The autoconfiguration process follows these steps:

1. Spring Boot scans for dependencies in your classpath
2. It evaluates conditions to determine which configurations to apply
3. It creates and registers beans based on those conditions
4. Your application starts with a pre-configured environment

### 📌 Enabling Autoconfiguration

Autoconfiguration is enabled via the `@EnableAutoConfiguration` annotation, which is included in `@SpringBootApplication`:

```java
@SpringBootApplication  // Includes @EnableAutoConfiguration
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

### 📌 Conditional Annotations

Spring Boot uses various conditional annotations to determine when to apply autoconfiguration:

```java
// Apply this configuration only if DataSource class is on classpath
@ConditionalOnClass(DataSource.class)
public class DataSourceAutoConfiguration {
    // Configuration code
}

// Apply only if this bean is not already defined
@ConditionalOnMissingBean(name = "dataSource")
public DataSource dataSource() {
    // Bean definition
}

// Apply only if this property exists
@ConditionalOnProperty(name = "spring.datasource.url")
public DataSource dataSource() {
    // Bean definition
}
```

Common conditional annotations include:
- `@ConditionalOnClass` / `@ConditionalOnMissingClass`
- `@ConditionalOnBean` / `@ConditionalOnMissingBean`
- `@ConditionalOnProperty`
- `@ConditionalOnWebApplication` / `@ConditionalOnNotWebApplication`
- `@ConditionalOnExpression` (SpEL expressions)

### 📌 Viewing Auto-configurations

To see which auto-configurations are being applied or excluded:

```yaml
# application.properties or application.yml
debug=true  # Enables auto-configuration report
```

This will show a report in the logs when your application starts:

```
=========================
AUTO-CONFIGURATION REPORT
=========================

Positive matches:
-----------------
   DataSourceAutoConfiguration matched:
      - @ConditionalOnClass found required class 'javax.sql.DataSource' (OnClassCondition)

Negative matches:
-----------------
   MongoAutoConfiguration did not match:
      - @ConditionalOnClass did not find required class 'com.mongodb.MongoClient' (OnClassCondition)
```

### 📌 Customizing Auto-configuration

You can exclude specific auto-configurations:

```java
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class MyApplication {
    // Application code
}
```

Or in properties:

```yaml
spring:
  autoconfigure:
    exclude:
      - org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
```

### ❌ Common Mistakes

1. **Overriding auto-configuration unintentionally** - Creating beans without understanding which auto-configurations are active
2. **Not excluding conflicting auto-configurations** - When you want custom behavior
3. **Assuming auto-configuration will cover everything** - Some scenarios still require explicit configuration

### ✅ Best Practices

1. **Review the auto-configuration report** - Use `debug=true` to understand what's being configured
2. **Leverage property customization first** - Before creating custom beans
3. **Use starter dependencies** - To bring in related groups of auto-configurations
4. **Create custom auto-configurations for reusable modules** - When developing shared components

## 2. 🌈 Spring Profiles
---------

Spring Profiles allow you to define different sets of beans and configurations for different environments (development, testing, production).

### 📌 Defining Profiles

You can define profiles using annotations on configuration classes:

```java
@Configuration
@Profile("development")
public class DevelopmentConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}

@Configuration
@Profile("production")
public class ProductionConfig {
    @Bean
    public DataSource dataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setUrl("jdbc:mysql://prod-server:3306/mydb");
        // Set other properties
        return dataSource;
    }
}
```

You can also apply profiles to individual beans:

```java
@Component
public class MyService {
    @Bean
    @Profile("development")
    public DevToolsBean devTools() {
        return new DevToolsBean();
    }
    
    @Bean
    @Profile("production")
    public MonitoringBean monitoring() {
        return new MonitoringBean();
    }
}
```

### 📌 Activating Profiles

Activate profiles in several ways:

**1. In application.properties/yml:**
```yaml
spring:
  profiles:
    active: development
```

**2. As command-line arguments:**
```
java -jar app.jar --spring.profiles.active=production
```

**3. As environment variables:**
```
export SPRING_PROFILES_ACTIVE=production
java -jar app.jar
```

**4. Programmatically:**
```java
SpringApplication app = new SpringApplication(MyApplication.class);
app.setAdditionalProfiles("production");
app.run(args);
```

### 📌 Profile Groups

Spring Boot 2.4+ introduced profile groups to activate multiple profiles at once:

```yaml
spring:
  profiles:
    group:
      production: prod-db,prod-mq,monitoring
      development: dev-db,dev-mq,debug
```

### 📌 Default Profile

If no profile is specified, Spring uses the "default" profile:

```java
@Profile("default")
@Configuration
public class DefaultConfig {
    // Default configuration
}
```

### ❌ Common Mistakes

1. **Misconfiguring active profiles** - Especially in complex deployment pipelines
2. **Profile collision** - When multiple profiles define the same bean
3. **Not having sensible defaults** - Applications should work reasonably without any profile
4. **Using too many or overly specific profiles** - Leading to configuration fragmentation

### ✅ Best Practices

1. **Use consistent naming conventions** - Like "dev", "test", "prod"
2. **Limit profiles to environment-specific concerns** - Don't overuse for application features
3. **Leverage profile groups** - To simplify activation of related profiles
4. **Include validation logic** - To verify environment-specific configurations are complete

## 3. 📝 Spring Boot Properties & YAML Configuration
---------

Spring Boot provides a flexible property management system to configure your application through various sources.

### 📌 Property Sources

Spring Boot loads properties in the following order (later sources override earlier ones):

1. Default properties in Spring Boot
2. `@PropertySource` annotations
3. `application.properties` or `application.yml` in config directory
4. `application.properties` or `application.yml` in classpath
5. Profile-specific properties (e.g., `application-dev.properties`)
6. Command-line arguments
7. OS environment variables

### 📌 Property File Formats

**Properties format:**
```properties
server.port=8080
spring.datasource.url=jdbc:mysql://localhost/test
spring.datasource.username=dbuser
spring.datasource.password=dbpass
```

**YAML format:**
```yaml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost/test
    username: dbuser
    password: dbpass
```

### 📌 Accessing Properties

**1. Using @Value:**
```java
@Component
public class MyComponent {
    @Value("${server.port}")
    private int serverPort;
    
    @Value("${app.default-timeout:30}")
    private int timeout;  // With default value
}
```

**2. Using Environment:**
```java
@Component
public class MyComponent {
    @Autowired
    private Environment env;
    
    public void doSomething() {
        String dbUrl = env.getProperty("spring.datasource.url");
        int port = env.getProperty("server.port", Integer.class, 8080);
    }
}
```

**3. Using @ConfigurationProperties:**
```java
@Component
@ConfigurationProperties(prefix = "app.mail")
public class MailProperties {
    private String host;
    private int port = 25;  // Default value
    private String username;
    private String password;
    
    // Getters and setters
}
```

### 📌 Profile-Specific Properties

You can define profile-specific properties in separate files:

```
application.yml              # Common properties
application-dev.yml          # Development properties
application-prod.yml         # Production properties
```

Or within the same YAML file using document separators:

```yaml
# Common properties
spring:
  application:
    name: my-app

---
# Development profile
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:h2:mem:testdb

---
# Production profile
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:mysql://prod-server/mydb
```

### 📌 Property Binding and Conversion

Spring Boot automatically converts properties to appropriate types:

```yaml
app:
  server:
    port: 8080               # Converted to int
    active: true             # Converted to boolean
    timeout: 10s             # Converted to Duration
    max-file-size: 10MB      # Converted to DataSize
    hosts:                   # Converted to List<String>
      - host1.example.com
      - host2.example.com
```

### 📌 Configuration Metadata

Create a `META-INF/spring-configuration-metadata.json` file to provide IDE hints:

```json
{
  "properties": [
    {
      "name": "app.mail.host",
      "type": "java.lang.String",
      "description": "Mail server host name."
    }
  ]
}
```

### ❌ Common Mistakes

1. **Hardcoding sensitive information** - Passwords, API keys, etc. in property files
2. **Ignoring property binding failures** - Missing error handling for invalid properties
3. **Not using relaxed binding** - Unaware that camelCase, kebab-case, etc. are equivalent
4. **Misconfiguring property sources order** - Leading to unexpected overrides

### ✅ Best Practices

1. **Externalize sensitive properties** - Use environment variables or secure vaults
2. **Group related properties** - Using `@ConfigurationProperties` for type-safety
3. **Provide sensible defaults** - So application works with minimal configuration
4. **Document custom properties** - With configuration metadata
5. **Validate properties** - Using `@Validated` with `@ConfigurationProperties`

```java
@Component
@ConfigurationProperties(prefix = "app.connection")
@Validated
public class ConnectionProperties {
    @NotNull
    private String host;
    
    @Min(1000)
    @Max(65535)
    private int port = 8080;
    
    // Getters and setters
}
```

## 4. 📊 Summary Tables for Quick Revision
---------

### 📌 Spring Boot Autoconfiguration

| Concept | Description | Example |
|---------|-------------|---------|
| Enabling | Automatic with `@SpringBootApplication` | `@SpringBootApplication` includes `@EnableAutoConfiguration` |
| Conditional Annotations | Control when configurations activate | `@ConditionalOnClass`, `@ConditionalOnProperty` |
| Viewing | Debug output of auto-configurations | Set `debug=true` in properties |
| Customizing | Override or exclude auto-configurations | `@SpringBootApplication(exclude={...})` |
| Creating Custom | Create reusable auto-configurations | Create configuration class and register in `META-INF/spring.factories` |

### 📌 Spring Profiles

| Concept | Description | Example |
|---------|-------------|---------|
| Defining | Mark beans/configs for specific environments | `@Profile("development")` |
| Activating | Set which profiles are active | `spring.profiles.active=dev,debug` |
| Default | Used when no profile specified | `@Profile("default")` |
| Profile Groups | Activate multiple profiles at once | `spring.profiles.group.production=prod-db,prod-mq` |
| Profile-specific Properties | Configure per environment | `application-{profile}.properties` |

### 📌 Spring Boot Properties

| Concept | Description | Example |
|---------|-------------|---------|
| Property Sources | Where properties come from | Config files, env vars, command line |
| Formats | Properties or YAML | `.properties` or `.yml` files |
| Accessing | How to use properties in code | `@Value`, `Environment`, `@ConfigurationProperties` |
| Binding | Convert string properties to types | Duration, DataSize, List conversions |
| Validation | Verify property values | `@Validated` with JSR-303 annotations |

## 5. 🚀 Quick Concept Summary
---------

### 📌 Spring Boot Autoconfiguration

- **Purpose**: Automatically configure applications based on classpath contents
- **How it works**: Uses conditional logic to determine when to apply configurations
- **Benefits**: Reduces boilerplate, speeds up development, enforces conventions
- **Customization**: Can be overridden or excluded when needed
- **Key point**: Understand the conditions that trigger auto-configurations

### 📌 Spring Profiles

- **Purpose**: Environment-specific configurations and behavior
- **How it works**: Conditionally activates beans based on active profiles
- **Benefits**: Clean separation of environment concerns
- **Activation**: Multiple methods (properties, command line, environment variables)
- **Key point**: Profile groups simplify managing related profiles

### 📌 Spring Boot Properties

- **Purpose**: External application configuration
- **How it works**: Loads properties from various sources in defined precedence
- **Benefits**: Type-safe configuration, environment abstraction
- **Formats**: Supports properties and YAML with hierarchical configuration
- **Key point**: `@ConfigurationProperties` provides type-safety and validation

## 6. 🎯 Interview Q&A
---------

### 📌 Spring Boot Autoconfiguration Questions

**Q1: What is Spring Boot Autoconfiguration and how does it work?**

A: Spring Boot Autoconfiguration automatically configures your Spring application based on the dependencies in your classpath. It works by using conditional annotations to check if certain classes or properties exist, then registers appropriate beans. This happens through configuration classes defined in `META-INF/spring.factories` that are loaded when `@EnableAutoConfiguration` is used.

**Q2: How would you disable a specific auto-configuration?**

A: You can disable specific auto-configurations in three ways:
1. Using the `exclude` attribute on `@SpringBootApplication`: 
   ```java
   @SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
   ```
2. In properties:
   ```yaml
   spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
   ```
3. Programmatically:
   ```java
   SpringApplication app = new SpringApplication(MyApp.class);
   Set<String> excludes = new HashSet<>();
   excludes.add(DataSourceAutoConfiguration.class.getName());
   app.setExcludedSources(excludes);
   app.run(args);
   ```

**Q3: How would you create a custom auto-configuration?**

A: To create a custom auto-configuration:
1. Create a configuration class with appropriate `@Conditional` annotations
2. Add a `META-INF/spring.factories` file in your JAR:
   ```properties
   org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
   com.example.MyAutoConfiguration
   ```
3. Use proper `@AutoConfigureBefore` or `@AutoConfigureAfter` to control ordering
4. Provide sensible defaults but allow property overrides

### 📌 Spring Profiles Questions

**Q1: How do you activate multiple Spring profiles?**

A: You can activate multiple profiles by separating them with commas:
```yaml
spring.profiles.active=dev,debug,local
```
Or with profile groups in Spring Boot 2.4+:
```yaml
spring.profiles.group.development=dev,debug,local
```
Then activate with:
```yaml
spring.profiles.active=development
```

**Q2: What's the difference between `spring.profiles.active` and `spring.profiles.include`?**

A: `spring.profiles.active` specifies which profiles are primarily active, while `spring.profiles.include` adds additional profiles regardless of what's active. Included profiles have lower precedence than active profiles if there are conflicts.

**Q3: How would you conditionally create a bean based on multiple profiles?**

A: You can use SpEL expressions with `@Profile`:
```java
@Bean
@Profile("production & !legacy")  // Active in production but not if legacy is also active
public DataSource dataSource() {
    // Bean definition
}
```

### 📌 Spring Boot Properties Questions

**Q1: What's the difference between `@Value` and `@ConfigurationProperties`?**

A: 
- `@Value` is for injecting single properties with SpEL support
- `@ConfigurationProperties` binds entire groups of properties to structured objects
- `@ConfigurationProperties` offers relaxed binding, type conversion, and validation
- `@ConfigurationProperties` is more maintainable for related properties

**Q2: How can you handle property validation in Spring Boot?**

A: Add validation annotations to `@ConfigurationProperties` classes:
```java
@Component
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {
    @NotEmpty
    private String name;
    
    @Min(1) @Max(10)
    private int retryCount;
    
    // Getters and setters
}
```

**Q3: Explain property binding relaxation in Spring Boot.**

A: Spring Boot supports multiple formats for the same property name:
- `app.retryCount` (camelCase)
- `app.retry-count` (kebab-case)
- `app.retry_count` (snake_case)
- `APP_RETRY_COUNT` (uppercase with underscores, for environment variables)

All these will bind to the same property `retryCount` in your `@ConfigurationProperties` class.

---

These concepts are foundational to developing with Spring Boot. Understanding them thoroughly will serve you well in your interview and future Java development. Good luck! 🍀