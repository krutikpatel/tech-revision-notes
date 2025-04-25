# Java Collections: Interview Preparation Guide 🧠

## 1. 📚 List Implementations
---------

### ArrayList vs LinkedList 📌

#### ArrayList ✅
- **Implementation**: Backed by a resizable array
- **Random Access**: O(1) - direct indexing
- **Insertion/Deletion**: O(n) in worst case (requires shifting elements)
- **Memory**: More efficient for storage, less overhead per element

```java
List<String> names = new ArrayList<>();  // Initial capacity 10
List<String> names = new ArrayList<>(100);  // Specify initial capacity
```

#### LinkedList ✅
- **Implementation**: Doubly-linked list (nodes with prev/next pointers)
- **Random Access**: O(n) - must traverse the list
- **Insertion/Deletion**: O(1) at known position (just relink nodes)
- **Memory**: Higher overhead (each element has next/prev references)

```java
List<String> queue = new LinkedList<>();
// LinkedList also implements Queue and Deque
LinkedList<String> linkedList = new LinkedList<>();
linkedList.addFirst("First");  // Deque operation
linkedList.addLast("Last");    // Deque operation
```

#### When to Choose Each ⚡
- **ArrayList**: Default choice for most use cases
  - Random access needs
  - Mostly read operations
  - Infrequent insertions/deletions
- **LinkedList**: Special cases
  - Frequent insertions/deletions in the middle
  - Implementing queue/deque behavior
  - No random access needed

### Vector and Stack (Legacy) 📌

#### Vector ✅
- **Similar to**: ArrayList but synchronized (thread-safe)
- **Performance**: Slower than ArrayList due to synchronization
- **Growth**: Grows by doubling size (versus 50% for ArrayList)

```java
Vector<Integer> vector = new Vector<>();  // Synchronized
```

#### Stack ✅
- **Extends**: Vector
- **Implementation**: LIFO (Last-In-First-Out) structure
- **Methods**: push(), pop(), peek()

```java
Stack<String> stack = new Stack<>();
stack.push("Element");
String top = stack.peek();  // View top without removing
String popped = stack.pop();  // Remove and return top
```

#### Modern Alternatives ⚡
- Use `ArrayList` instead of `Vector`
- Use `ArrayDeque` instead of `Stack`
- Use `Collections.synchronizedList()` if thread safety needed

### Performance Characteristics 📊

```
Operation       ArrayList    LinkedList    Vector
----------      ---------    ----------    ------
get(index)      O(1)         O(n)          O(1)
add(E)          O(1)*        O(1)          O(1)*
add(index, E)   O(n)         O(n)**        O(n)
remove(index)   O(n)         O(n)**        O(n)
Iterator.remove O(n)         O(1)          O(n)
Memory          Low          High          Low

* Amortized - occasional O(n) when resizing
** O(1) if position is known (e.g., using ListIterator)
```

### Common Mistakes ❌
- Using LinkedList for random access operations
- Using Vector/Stack in modern applications
- Not specifying initial capacity for ArrayList with known size
- Using index-based operations on LinkedList

### Best Practices ✨
- Use ArrayList by default
- Use LinkedList for queue/deque implementations
- Specify initial capacity for ArrayList when size is known
- Use modern alternatives to legacy classes


## 2. 🔍 Set Implementations
---------

### HashSet vs LinkedHashSet vs TreeSet 📌

#### HashSet ✅
- **Implementation**: Backed by HashMap
- **Order**: No guaranteed order
- **Performance**: O(1) for add, remove, contains
- **Use Case**: When element order doesn't matter

```java
Set<String> uniqueNames = new HashSet<>();
uniqueNames.add("Alice");  // Returns true (added)
uniqueNames.add("Alice");  // Returns false (already exists)
```

#### LinkedHashSet ✅
- **Implementation**: HashSet with linked list
- **Order**: Maintains insertion order
- **Performance**: O(1) for add, remove, contains (slightly slower than HashSet)
- **Use Case**: When preserving insertion order is important

```java
Set<String> orderedSet = new LinkedHashSet<>();
orderedSet.add("B");
orderedSet.add("A");
orderedSet.add("C");
// Iteration order: B, A, C (insertion order)
```

#### TreeSet ✅
- **Implementation**: Red-black tree (balanced binary search tree)
- **Order**: Elements sorted by natural order or custom Comparator
- **Performance**: O(log n) for add, remove, contains
- **Use Case**: When sorted order is required

```java
Set<String> sortedSet = new TreeSet<>();
sortedSet.add("B");
sortedSet.add("A");
sortedSet.add("C");
// Iteration order: A, B, C (sorted)

// Custom ordering
Set<Person> personsByAge = new TreeSet<>(
    Comparator.comparing(Person::getAge)
);
```

### EnumSet 📌
- **Specialized for**: Enum types
- **Implementation**: Bit vector (extremely efficient)
- **Performance**: Near-constant time operations
- **Memory**: Highly optimized for enums

```java
enum Day { MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY }

// Create a set with specific enum values
EnumSet<Day> weekdays = EnumSet.range(Day.MONDAY, Day.FRIDAY);

// Create a set with all enum values
EnumSet<Day> allDays = EnumSet.allOf(Day.class);

// Create an empty set
EnumSet<Day> noDays = EnumSet.noneOf(Day.class);
```

### Uniqueness and Hashing 📌
- Sets store unique elements (no duplicates)
- Uniqueness determined by:
  - `equals()` method for value equality
  - `hashCode()` method for hash-based sets (HashSet, LinkedHashSet)
  - `compareTo()` or `Comparator` for TreeSet

```java
// Custom class needs proper equals() and hashCode()
public class Employee {
    private int id;
    private String name;
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employee = (Employee) o;
        return id == employee.id && Objects.equals(name, employee.name);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }
}
```

### Common Mistakes ❌
- Forgetting to override both `equals()` and `hashCode()` methods
- Modifying elements after adding to HashSet/LinkedHashSet
- Using TreeSet without comparable elements or Comparator
- Using HashSet when order matters

### Best Practices ✨
- Always override both `equals()` and `hashCode()` for custom classes
- Use LinkedHashSet when needing to maintain insertion order
- Use TreeSet when a sorted set is required
- Use EnumSet for sets of enum values


## 3. 🗺️ Map Implementations
---------

### HashMap vs LinkedHashMap vs TreeMap 📌

#### HashMap ✅
- **Implementation**: Hash table with buckets
- **Order**: No guaranteed order
- **Performance**: O(1) average for put, get, remove
- **Use Case**: General-purpose key-value storage

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
int aliceScore = scores.get("Alice");  // 95
```

#### LinkedHashMap ✅
- **Implementation**: HashMap with doubly-linked list
- **Order**: Maintains insertion order (by default)
- **Can also**: Maintain access order (LRU cache)
- **Performance**: O(1) for operations (slightly slower than HashMap)

```java
// Insertion-order
Map<String, Integer> orderedScores = new LinkedHashMap<>();

// Access-order (LRU cache behavior)
Map<String, Integer> lruCache = new LinkedHashMap<>(16, 0.75f, true);
```

#### TreeMap ✅
- **Implementation**: Red-black tree
- **Order**: Keys sorted by natural order or custom Comparator
- **Performance**: O(log n) for operations
- **Use Case**: When sorted key order is required

```java
Map<String, Integer> sortedScores = new TreeMap<>();
sortedScores.put("Charlie", 80);
sortedScores.put("Alice", 95);
sortedScores.put("Bob", 87);
// Keys are iterated in order: Alice, Bob, Charlie
```

### IdentityHashMap, WeakHashMap 📌

#### IdentityHashMap ✅
- **Key Equality**: Uses reference equality (==) instead of equals()
- **Use Case**: When reference identity matters, not object equality

```java
Map<String, Integer> identityMap = new IdentityHashMap<>();
String a = new String("key");
String b = new String("key");
identityMap.put(a, 1);
identityMap.put(b, 2);
// Size is 2 because a and b are different objects
```

#### WeakHashMap ✅
- **Key References**: Weak references that allow garbage collection
- **Use Case**: Caches where entry lifetime depends on external references

```java
Map<Object, String> weakMap = new WeakHashMap<>();
Object key = new Object();
weakMap.put(key, "Value");
// Entry will be removed when 'key' is eligible for garbage collection
key = null;  // Entry will be removed on next GC cycle
```

### EnumMap 📌
- **Specialized for**: Enum keys
- **Implementation**: Array-based (very efficient)
- **Performance**: Constant time operations
- **Memory**: Much more efficient than HashMap for enum keys

```java
enum Day { MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY }

EnumMap<Day, String> schedule = new EnumMap<>(Day.class);
schedule.put(Day.MONDAY, "Work");
schedule.put(Day.SATURDAY, "Leisure");
```

### Common Mistakes ❌
- Using mutable objects as keys in hash-based maps
- Forgetting that WeakHashMap entries can disappear
- Not considering insertion order when it matters
- Using HashMap when sorted keys are needed

### Best Practices ✨
- Use immutable objects as keys for hash-based maps
- Use LinkedHashMap for predictable iteration order
- Use specialized maps (EnumMap) when appropriate
- Consider TreeMap when range queries are needed


## 4. 🔄 Queue and Deque
---------

### ArrayDeque 📌
- **Implementation**: Resizable circular array
- **Performance**: O(1) for add/remove at both ends
- **Use Cases**: Stack, Queue, or general Deque implementation
- **Advantages**: More efficient than Stack or LinkedList

```java
// As a stack (LIFO)
Deque<String> stack = new ArrayDeque<>();
stack.push("A");          // addFirst()
stack.push("B");
String top = stack.pop(); // removeFirst()

// As a queue (FIFO)
Queue<String> queue = new ArrayDeque<>();
queue.offer("A");         // addLast()
queue.offer("B");
String first = queue.poll(); // removeFirst()
```

### PriorityQueue 📌
- **Implementation**: Binary heap (complete binary tree)
- **Order**: Natural order or custom Comparator
- **Performance**: O(log n) for offer/poll, O(1) for peek
- **Use Case**: When processing elements by priority

```java
// Min heap (smallest element first)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(2);
minHeap.offer(8);
int smallest = minHeap.poll();  // Returns 2

// Max heap (largest element first)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
maxHeap.offer(5);
maxHeap.offer(2);
maxHeap.offer(8);
int largest = maxHeap.poll();  // Returns 8

// With custom priority
PriorityQueue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparing(Task::getPriority)
);
```

### Queue Operations 📌

#### Basic Operations 📊

```
Method Pair     | Throws Exception | Returns Special Value
--------------- | ---------------- | ---------------------
Insert          | add(e)           | offer(e) - returns boolean
Remove          | remove()         | poll() - returns null if empty
Examine         | element()        | peek() - returns null if empty
```

#### Deque Operations 📊

```
Operation  | First Element (Head)     | Last Element (Tail)
---------- | ----------------------- | ------------------------
Insert     | addFirst(e)/offerFirst(e) | addLast(e)/offerLast(e)
Remove     | removeFirst()/pollFirst() | removeLast()/pollLast()
Examine    | getFirst()/peekFirst()    | getLast()/peekLast()
```

### Common Mistakes ❌
- Using Stack instead of ArrayDeque for LIFO behavior
- Assuming PriorityQueue iteration reveals sorted order
- Using exception-throwing methods without checking emptiness
- Forgetting that Queue is an interface, not a concrete class

### Best Practices ✨
- Use ArrayDeque instead of Stack
- Use offer/poll/peek methods to avoid exceptions
- Specify initial capacity for ArrayDeque when size is known
- Use PriorityQueue for maintaining elements in priority order


## 5. 💡 Interview-Ready Insights
---------

### Collection Selection Decision Tree 🌳

```
Need key-value pairs? → Yes → Need sorted keys? → Yes → TreeMap
                       |                        → No → Need insertion order? → Yes → LinkedHashMap
                       |                                                     → No → HashMap
                       |
                       → No → Need unique elements? → Yes → Need sorted elements? → Yes → TreeSet
                                                    |                             → No → Need insertion order? → Yes → LinkedHashSet
                                                    |                                                          → No → HashSet
                                                    |
                                                    → No → Need random access? → Yes → ArrayList
                                                                              → No → Need FIFO/queue? → Yes → ArrayDeque/LinkedList
                                                                                                      → No → Need priority? → Yes → PriorityQueue
                                                                                                                            → No → ArrayDeque
```

### Thread Safety Considerations ⚡
- All standard collections are not thread-safe
- Legacy collections (Vector, Hashtable) are thread-safe but less efficient
- For thread safety, use:
  - `Collections.synchronizedXxx()` methods
  - Concurrent collections from `java.util.concurrent`

### Performance Tips 🚀
- Size ArrayList/ArrayDeque appropriately when size is known
- Consider load factor for hash-based collections
- Use specialized collections (EnumSet, EnumMap) when applicable
- Choose the right collection based on your access patterns

### Common Interview Questions 🎯
1. "Compare ArrayList vs LinkedList performance"
2. "What happens if you modify a HashMap key after insertion?"
3. "How would you implement an LRU cache in Java?"
4. "When would you use TreeMap instead of HashMap?"
5. "Why should you implement both equals() and hashCode()?"


## 6. 📝 Summary
---------

### List Implementations
- **ArrayList**: Array-based, O(1) access, best for random access
- **LinkedList**: Node-based, O(1) insertion/deletion at ends, implements Deque
- **Vector/Stack**: Legacy, synchronized, use modern alternatives

### Set Implementations
- **HashSet**: Unordered, O(1) operations
- **LinkedHashSet**: Maintains insertion order, O(1) operations
- **TreeSet**: Sorted order, O(log n) operations
- **EnumSet**: Ultra-efficient for enum types

### Map Implementations
- **HashMap**: Unordered, O(1) operations
- **LinkedHashMap**: Maintains insertion/access order, O(1) operations
- **TreeMap**: Sorted keys, O(log n) operations
- **WeakHashMap**: Allows key garbage collection
- **IdentityHashMap**: Uses reference equality (==)
- **EnumMap**: Efficient for enum keys

### Queue/Deque Implementations
- **ArrayDeque**: Double-ended queue, O(1) operations at both ends
- **PriorityQueue**: Heap-based priority queue, O(log n) for offer/poll
- **LinkedList**: Can be used as a Queue/Deque


## 7. 📊 Quick Reference Table
---------

### List Implementations

| Implementation | Order           | get()  | add()  | insert() | delete() | Memory     | Thread-Safe |
|----------------|-----------------|--------|--------|----------|----------|------------|-------------|
| ArrayList      | Insertion       | O(1)   | O(1)*  | O(n)     | O(n)     | Low        | No          |
| LinkedList     | Insertion       | O(n)   | O(1)   | O(1)**   | O(1)**   | High       | No          |
| Vector         | Insertion       | O(1)   | O(1)*  | O(n)     | O(n)     | Low        | Yes         |

*Amortized
**When position is known

### Set Implementations

| Implementation | Order           | add()  | remove() | contains() | Memory     | Thread-Safe |
|----------------|-----------------|--------|----------|------------|------------|-------------|
| HashSet        | None            | O(1)   | O(1)     | O(1)       | Medium     | No          |
| LinkedHashSet  | Insertion       | O(1)   | O(1)     | O(1)       | High       | No          |
| TreeSet        | Sorted          | O(log n)| O(log n)| O(log n)   | Medium     | No          |
| EnumSet        | Natural (enum)  | O(1)   | O(1)     | O(1)       | Very Low   | No          |

### Map Implementations

| Implementation | Key Order       | put()  | get()  | remove() | Memory     | Thread-Safe |
|----------------|-----------------|--------|--------|----------|------------|-------------|
| HashMap        | None            | O(1)   | O(1)   | O(1)     | Medium     | No          |
| LinkedHashMap  | Insertion/Access| O(1)   | O(1)   | O(1)     | High       | No          |
| TreeMap        | Sorted          | O(log n)| O(log n)| O(log n)| Medium    | No          |
| WeakHashMap    | None            | O(1)   | O(1)   | O(1)     | Medium     | No          |
| IdentityHashMap| None            | O(1)   | O(1)   | O(1)     | Medium     | No          |
| EnumMap        | Natural (enum)  | O(1)   | O(1)   | O(1)     | Very Low   | No          |

### Queue/Deque Implementations

| Implementation | Ordering       | offer() | poll() | peek() | Special Feature   | Thread-Safe |
|----------------|----------------|---------|--------|--------|-------------------|-------------|
| ArrayDeque     | FIFO/LIFO      | O(1)    | O(1)   | O(1)   | Both ends O(1)    | No          |
| PriorityQueue  | Priority       | O(log n)| O(log n)| O(1)  | Priority ordering | No          |
| LinkedList     | FIFO/LIFO      | O(1)    | O(1)   | O(1)   | Node-based        | No          |

Use this compact reference to quickly select the appropriate collection for your specific needs during interviews and real-world coding tasks!