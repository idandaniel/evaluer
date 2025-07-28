# Copilot Instructions for Python/FastAPI Development

## Core Principles

### Code Quality Standards
- Write self-documenting code that explains itself through clear naming and structure
- Never add comments to code - the code should be readable and self-explanatory
- Follow the principle that good code is its own documentation
- Code should read like a well-written story that explains what the system does
- Prefer explicit over implicit (Zen of Python principle)
- Simple is better than complex (Zen of Python principle)
- Readability counts more than cleverness

## Python Best Practices (Pythonic Code)

### Dictionary and Data Access
- Always use `.get()` method on dictionaries instead of direct key access to avoid KeyError
- Use `dict.get(key, default_value)` to provide fallback values
- Use `dict.setdefault(key, default)` for conditional insertion
- Prefer `dict.pop(key, default)` over checking key existence then deleting
- Use dictionary comprehensions for transforming dictionaries: `{k: v.upper() for k, v in data.items()}`
- Use `collections.ChainMap` for combining multiple dictionaries
- Use `**kwargs` unpacking for dictionary merging in Python 3.9+: `{**dict1, **dict2}`

### String Handling Best Practices
- Always use f-strings for string formatting, never % formatting or .format()
- Use triple quotes for multi-line strings, not string concatenation
- Use `str.join()` for concatenating multiple strings, never use + in loops
- Use `str.strip()`, `str.lstrip()`, `str.rstrip()` for whitespace removal
- Use `str.startswith()` and `str.endswith()` instead of slicing for prefix/suffix checks
- Use `str.partition()` or `str.rpartition()` for splitting strings at first/last occurrence
- Use raw strings (r"") for regex patterns and Windows paths
- Use `str.casefold()` for case-insensitive comparisons, not `str.lower()`

### List and Sequence Operations
- Use list comprehensions instead of map() and filter() when readable
- Use generator expressions for memory-efficient iteration: `(x for x in items if condition)`
- Use `enumerate()` instead of `range(len())` for indexed iteration
- Use `zip()` for parallel iteration over multiple sequences
- Use `itertools.zip_longest()` when sequences have different lengths
- Use slice assignment for list modification: `items[2:4] = new_items`
- Use `list.extend()` instead of += for adding multiple items
- Use `collections.deque` for frequent insertions/deletions at both ends
- Use `bisect` module for maintaining sorted lists

### Set Operations and Membership Testing
- Use sets for membership testing (O(1)) instead of lists (O(n))
- Use set comprehensions: `{item.lower() for item in items}`
- Use set operations: `set1 & set2` (intersection), `set1 | set2` (union), `set1 - set2` (difference)
- Use `frozenset` for immutable sets that can be dictionary keys or set elements
- Use `any()` and `all()` functions for boolean operations on sequences

### General Python Guidelines
- Use list comprehensions and generator expressions when they improve readability
- Prefer `enumerate()` over manual indexing: `for i, item in enumerate(items)` not `for i in range(len(items))`
- Use `zip()` for parallel iteration: `for a, b in zip(list1, list2)`
- Leverage `collections.defaultdict`, `collections.Counter`, and other specialized containers
- Use `pathlib.Path` instead of `os.path` for all file operations
- Prefer f-strings for string formatting: `f"Hello {name}"` not `"Hello {}".format(name)`
- Use context managers (`with` statements) for all resource management
- Implement `__str__` and `__repr__` methods for custom classes
- Use type hints consistently throughout the codebase
- Follow PEP 8 naming conventions strictly

### Advanced Python Patterns
- Use `@property` decorator for computed attributes instead of getter methods
- Use `@classmethod` for alternative constructors
- Use `@staticmethod` for utility functions that belong to the class
- Use `__slots__` for memory-efficient classes with fixed attributes
- Use `dataclasses` for simple data containers instead of regular classes
- Use `functools.cached_property` for expensive computed properties
- Use `functools.lru_cache` for memoizing expensive function calls
- Use `functools.partial` for creating specialized versions of functions
- Use `contextlib.contextmanager` for creating custom context managers

### None Handling and Optional Values
- Use `is None` and `is not None` for None comparisons, never `== None`
- Use the walrus operator `:=` for assignment within expressions (Python 3.8+)
- Use `or` for providing default values: `value = user_input or default_value`
- Use `and` for conditional execution: `items and process_items(items)`
- Be careful with falsy values (0, [], "", etc.) when using `or` for defaults

### Boolean and Logical Operations
- Use implicit boolean evaluation: `if items:` instead of `if len(items) > 0:`
- Use `not` operator for negation: `if not items:` instead of `if len(items) == 0:`
- Use `in` and `not in` for membership testing
- Use boolean short-circuiting: `condition1 and condition2` stops at first False

### Exception Handling Best Practices
- Catch specific exceptions, never use bare `except:`
- Use exception chaining with `raise ... from ...` to preserve stack traces
- Use `finally` blocks for cleanup that must always happen
- Use `else` clause in try-except for code that should run only if no exception occurred
- Create custom exception hierarchies for domain-specific errors
- Use `contextlib.suppress` for ignoring specific exceptions when appropriate

### Error Handling
- Use specific exception types rather than generic `Exception`
- Implement proper exception hierarchies for domain-specific errors
- Use `try`/`except`/`else`/`finally` appropriately
- Prefer EAFP (Easier to Ask for Forgiveness than Permission) over LBYL (Look Before You Leap)
- Never use bare `except:` clauses - always specify the exception type
- Use exception chaining with `raise ... from ...` to preserve original error context
- Use `contextlib.suppress()` for situations where you want to ignore specific exceptions

### File and Path Operations
- Always use `pathlib.Path` instead of `os.path` for cross-platform compatibility
- Use context managers for file operations: `with open(file) as f:`
- Use `Path.read_text()` and `Path.write_text()` for simple file operations
- Use `Path.glob()` and `Path.rglob()` for pattern matching
- Use `Path.exists()`, `Path.is_file()`, `Path.is_dir()` for path checking
- Use `/` operator for path joining: `path / "subdir" / "file.txt"`
- Use `Path.resolve()` to get absolute paths
- Use `Path.stem` and `Path.suffix` for filename manipulation

### Async/Await Best Practices
- Use `async def` and `await` for all I/O bound operations
- Use `asyncio.gather()` for concurrent execution of multiple async operations
- Use `asyncio.create_task()` for running async functions concurrently
- Use `async with` for async context managers
- Use `async for` for async iterators
- Never use `time.sleep()` in async code - use `asyncio.sleep()`
- Use `asyncio.run()` as the main entry point for async programs
- Use `asyncio.Queue` for async producer-consumer patterns

### Memory and Performance Optimization
- Use generators and `yield` for large datasets to avoid loading everything into memory
- Use `__slots__` for classes with many instances to reduce memory usage
- Use `sys.intern()` for frequently used strings to save memory
- Use `weakref` module for avoiding circular references
- Use `functools.lru_cache` for expensive function calls
- Use `itertools` functions for efficient iteration patterns
- Use `operator` module functions instead of lambda for simple operations
- Profile code with `cProfile` and `memory_profiler` before optimizing

### Imports and Module Organization  
- Import modules in the standard order: stdlib, third-party, local
- Use absolute imports instead of relative imports when possible
- Import only what you need: `from module import specific_function`
- Never use wildcard imports: avoid `from module import *`
- Use `importlib` for dynamic imports when necessary
- Group imports logically and separate groups with blank lines
- Use `if TYPE_CHECKING:` for type-only imports to avoid circular imports

### Type Hints and Annotations
- Use type hints for all function parameters and return values
- Use `typing.Optional[T]` or `T | None` (Python 3.10+) for optional parameters
- Use `typing.Union[A, B]` or `A | B` (Python 3.10+) for multiple possible types
- Use `typing.List[T]`, `typing.Dict[K, V]` or built-in `list[T]`, `dict[K, V]` (Python 3.9+)
- Use `typing.Protocol` for structural typing (duck typing with types)
- Use `typing.TypeVar` for generic types
- Use `typing.Final` for constants that should never change
- Use `typing.Literal` for string literals that have specific allowed values

### Data Structures and Algorithms
- Choose appropriate data structures (sets for membership testing, deques for queue operations)
- Use `itertools` for efficient iteration patterns
- Implement `__slots__` for memory-efficient classes when appropriate
- Prefer immutable data structures when possible
- Use `collections.namedtuple` or `typing.NamedTuple` for simple data structures
- Use `collections.defaultdict` with factory functions for nested dictionaries
- Use `collections.OrderedDict` when insertion order matters (Python <3.7)
- Use `heapq` module for priority queues and finding top-k elements
- Use `bisect` module for maintaining sorted sequences
- Use `array.array` for homogeneous numeric data to save memory

### Object-Oriented Programming Best Practices
- Use composition over inheritance whenever possible
- Implement `__eq__`, `__hash__`, and `__repr__` methods consistently
- Use `@property` for computed attributes and data validation
- Use `@classmethod` for alternative constructors
- Use `@staticmethod` for utility functions that belong conceptually to the class
- Implement `__enter__` and `__exit__` for custom context managers
- Use `super()` properly in inheritance hierarchies
- Follow the Liskov Substitution Principle in inheritance
- Use abstract base classes (`abc.ABC`) to define interfaces

### Functional Programming Patterns
- Use `map()`, `filter()`, and `reduce()` judiciously (prefer comprehensions when readable)
- Use `functools.partial` for creating specialized versions of functions
- Use `functools.wraps` when creating decorators to preserve metadata
- Use `functools.singledispatch` for function overloading based on type
- Use closures and nested functions for encapsulation
- Avoid side effects in functions when possible (pure functions)
- Use `itertools` functions like `chain`, `cycle`, `repeat` for complex iterations

### Function Design
- Keep functions small and focused on a single responsibility
- Use keyword-only arguments for complex functions: `def func(*, arg1, arg2)`
- Implement proper default arguments (avoid mutable defaults like `[]` or `{}`)
- Use `*args` and `**kwargs` judiciously, document their purpose
- Return early to reduce nesting and improve readability
- Use descriptive parameter names that explain their purpose
- Limit function parameters to 3-5 for better maintainability
- Use type hints for all parameters and return values
- Prefer returning data structures over multiple return values
- Use generator functions (`yield`) for producing sequences

## FastAPI Best Practices

### Application Structure
- Use dependency injection for all external dependencies
- Implement proper middleware for cross-cutting concerns (logging, CORS, authentication)
- Use Pydantic models for all request/response validation with custom validators
- Implement proper error handling with custom exception handlers
- Use background tasks for non-blocking operations
- Organize routes into separate router modules by domain/resource
- Use dependency override for testing different implementations
- Implement proper startup and shutdown event handlers

### Request/Response Handling
- Use Pydantic models with Field() for validation and documentation
- Implement custom validators using `@validator` and `@root_validator`
- Use Response models to define API contracts explicitly
- Implement proper serialization for datetime and custom types
- Use status_code parameter in route decorators for clarity
- Handle file uploads with proper validation and size limits
- Use streaming responses for large data transfers

### Dependency Injection Patterns
- Create reusable dependencies for common operations (database sessions, authentication)
- Use dependency classes for complex injection logic
- Implement proper dependency scoping (singleton, per-request)
- Use `Annotated` for dependency documentation and reuse
- Create dependency hierarchies for role-based access control
- Use dependency override for testing and configuration switching

### API Design
- Implement proper HTTP status codes for all scenarios
- Use appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Implement proper pagination for list endpoints with limit/offset or cursor-based pagination
- Use query parameters for filtering and sorting with proper validation
- Implement proper versioning strategy (URL path or header-based)
- Use consistent resource naming conventions (plural nouns)
- Implement proper HATEOAS principles where appropriate
- Use proper HTTP headers for caching, content negotiation, and metadata

### Input Validation and Sanitization
- Use Pydantic Field() with constraints (min_length, max_length, regex)
- Implement custom validators for business logic validation
- Use constr, conint, confloat for constrained types
- Validate nested objects and arrays properly
- Implement proper email, URL, and other format validations
- Use enum classes for limited choice fields
- Implement proper file type and size validation for uploads

### Security
- Implement proper authentication and authorization
- Use dependency injection for security requirements
- Validate all input data using Pydantic models
- Implement rate limiting where appropriate
- Use HTTPS in production with proper SSL/TLS configuration
- Implement CORS policies correctly for cross-origin requests
- Use secure headers (HSTS, X-Frame-Options, CSP)
- Implement proper password hashing with bcrypt or argon2
- Use JWT tokens with proper expiration and refresh mechanisms
- Validate and sanitize all user inputs to prevent injection attacks
- Implement proper session management
- Use environment variables for sensitive configuration

### Performance
- Implement async/await properly for I/O operations
- Use connection pooling for database connections
- Implement proper caching strategies (in-memory, Redis, CDN)
- Use streaming responses for large data transfers
- Implement proper logging without performance impact
- Use database indexing appropriately
- Implement request/response compression when beneficial
- Use lazy loading for expensive operations
- Profile and monitor application performance regularly
- Use OpenAPI annotations for automatic documentation
- Implement proper response models for all endpoints
- Use descriptive names for endpoints and parameters
- Include examples in Pydantic models
- Document error responses and status codes
- Use proper docstrings for complex business logic
- Include API versioning information in documentation
- Provide clear examples for authentication and authorization

## Design Patterns and Architectural Principles

### Common Design Patterns
- **Repository Pattern**: Abstract data access layer from business logic
- **Factory Pattern**: Create objects without specifying exact classes
- **Builder Pattern**: Construct complex objects step by step
- **Strategy Pattern**: Encapsulate algorithms and make them interchangeable
- **Observer Pattern**: Define subscription mechanism for object state changes
- **Command Pattern**: Encapsulate requests as objects for queuing and logging
- **Singleton Pattern**: Ensure class has only one instance (use sparingly)
- **Dependency Injection**: Provide dependencies from external sources

### Concurrency and Threading
- Use `asyncio` for I/O-bound concurrent operations
- Use `concurrent.futures.ThreadPoolExecutor` for CPU-bound tasks in async context
- Use `threading.Lock` and `threading.RLock` for thread synchronization
- Use `queue.Queue` for thread-safe communication between threads
- Avoid global variables in multi-threaded code
- Use `threading.local()` for thread-local storage
- Understand GIL limitations for CPU-bound tasks
- Use `multiprocessing` for true parallelism when needed

### Testing Best Practices
- Write tests first (TDD) or immediately after implementation
- Use `pytest` as the testing framework with proper fixtures
- Test one thing at a time with descriptive test names
- Use dependency injection to make code testable
- Mock external dependencies using `unittest.mock` or `pytest-mock`
- Use parametrized tests for testing multiple scenarios
- Implement integration tests for critical paths
- Use test databases and cleanup after tests
- Achieve high test coverage but focus on critical paths
- Use factories for creating test data consistently

## Clean Code Principles

### Functions and Methods
- Functions should do one thing and do it well
- Function names should be verbs, class names should be nouns
- Functions should be small (ideally under 20 lines)
- Avoid deep nesting (max 3 levels)
- Use early returns to reduce complexity

### Classes and Objects
- Classes should have a single responsibility
- Use composition over inheritance
- Implement proper encapsulation
- Keep interfaces minimal and focused
- Make dependencies explicit through constructor injection

### Variables and Naming
- Use intention-revealing names
- Avoid mental mapping and abbreviations
- Use searchable names for important concepts
- Use pronounceable names
- Distinguish names meaningfully

### Code Organization
- Organize code into logical modules and packages
- Keep related functionality together
- Separate concerns properly
- Use consistent indentation and formatting
- Remove dead code immediately

## SOLID Principles

### Single Responsibility Principle (SRP)
- Each class should have only one reason to change
- Separate business logic from data access
- Isolate different concerns into different modules

### Open/Closed Principle (OCP)
- Classes should be open for extension but closed for modification
- Use abstraction to enable extensibility
- Implement plugin architectures where appropriate

### Liskov Substitution Principle (LSP)
- Derived classes must be substitutable for their base classes
- Maintain behavioral contracts in inheritance hierarchies
- Use abstract base classes to define contracts

### Interface Segregation Principle (ISP)
- Clients should not depend on interfaces they don't use
- Create small, focused interfaces
- Use Protocol classes for interface definitions

### Dependency Inversion Principle (DIP)
- High-level modules should not depend on low-level modules
- Both should depend on abstractions
- Abstractions should not depend on details

## REST API Best Practices

### Resource Design
- Use nouns for resource names, not verbs
- Use plural nouns for collections
- Implement proper resource hierarchies
- Use consistent naming conventions

### HTTP Methods
- GET for retrieving data (idempotent)
- POST for creating resources
- PUT for updating entire resources (idempotent)
- PATCH for partial updates
- DELETE for removing resources (idempotent)

### Status Codes
- 200 OK for successful GET, PUT, PATCH
- 201 Created for successful POST
- 204 No Content for successful DELETE
- 400 Bad Request for validation errors
- 401 Unauthorized for authentication failures
- 403 Forbidden for authorization failures
- 404 Not Found for missing resources
- 409 Conflict for resource conflicts
- 422 Unprocessable Entity for semantic errors
- 500 Internal Server Error for server errors

### Response Design
- Use consistent response formats
- Include proper metadata (pagination, timestamps)
- Implement proper error response formats
- Use JSON as the primary data format
- Include resource URLs in responses

### API Versioning
- Version APIs from the start
- Use URL versioning or header versioning consistently
- Maintain backward compatibility
- Provide migration guides for breaking changes

## Three-Layer Architecture

### Presentation Layer (API/Controllers)
- Handle HTTP requests and responses
- Perform input validation and serialization
- Delegate business logic to service layer
- Handle authentication and authorization
- Transform data for client consumption

### Business Logic Layer (Services)
- Implement all business rules and logic
- Coordinate between different domain entities
- Handle complex validations and calculations
- Manage transactions and business workflows
- Remain independent of data access details

### Data Access Layer (Repositories/DAL)
- Handle all database operations
- Implement data mapping and transformation
- Manage database connections and transactions
- Provide abstraction over data storage
- Implement caching strategies

## Dependency Injection

### Implementation Strategy
- Use constructor injection as the primary method
- Implement dependency interfaces/protocols
- Use dependency injection containers (like FastAPI's Depends)
- Avoid service locator pattern
- Make dependencies explicit and testable

### Best Practices
- Inject interfaces, not concrete implementations
- Use factory patterns for complex object creation
- Implement proper lifetime management (singleton, transient, scoped)
- Avoid circular dependencies
- Use dependency injection for configuration as well

## Testable Code Design

### Code Structure for Testing
- Write pure functions wherever possible
- Avoid static dependencies and global state
- Use dependency injection to enable mocking
- Separate side effects from business logic
- Make async code testable with proper abstractions

### Design Patterns for Testability
- Use repository pattern for data access
- Implement command and query separation
- Use factory patterns for object creation
- Implement proper error handling that can be tested
- Design with test doubles in mind

### Testable Architecture
- Keep business logic independent of frameworks
- Use abstractions for external dependencies
- Implement proper separation of concerns
- Design for integration testing
- Make configuration testable

## Code Organization Rules

### File and Module Structure
- One class per file (with exceptions for small related classes)
- Use meaningful module names that reflect functionality
- Organize imports in standard order (standard library, third-party, local)
- Keep module interfaces minimal and focused
- Use `__all__` to explicitly define public module interface
- Implement proper `__init__.py` files for packages
- Use relative imports within packages sparingly and only for closely related modules

### Package Organization
- Group related functionality into packages
- Use `__init__.py` files to define package interfaces
- Implement proper package-level imports
- Avoid circular imports between packages
- Use namespace packages for large distributed systems
- Implement proper package versioning and metadata
- Use `setup.py` or `pyproject.toml` for package configuration

### Configuration Management
- Use environment variables for configuration
- Implement configuration validation using Pydantic
- Separate configuration from code
- Use dependency injection for configuration access
- Implement different configuration profiles (dev, test, prod)
- Use configuration files (YAML, JSON) for complex settings
- Never hardcode secrets or sensitive data in source code
- Use configuration management tools like `python-dotenv`

### Logging Best Practices
- Use the standard `logging` module, never print() for production code
- Configure logging at application startup, not in modules
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include contextual information in log messages
- Use structured logging (JSON) for production systems
- Implement proper log rotation and retention policies
- Use correlation IDs for tracking requests across services
- Never log sensitive data (passwords, tokens, personal information)
- Use lazy evaluation for expensive log message formatting
- Implement different log formats for development and production

### Code Quality and Linting
- Use `black` for consistent code formatting
- Use `isort` for import sorting
- Use `pylint` or `flake8` for linting
- Use `mypy` for static type checking
- Use `bandit` for security linting
- Implement pre-commit hooks for automated checks
- Use `pytest-cov` for test coverage reporting
- Set up continuous integration for code quality checks
- Use `pre-commit` framework for git hooks
- Implement code review processes and standards

### Database Best Practices
- Use SQLAlchemy ORM for database operations
- Implement proper database migrations using Alembic
- Use database connection pooling for performance
- Implement proper transaction management
- Use database indexes appropriately for query performance
- Implement soft deletes instead of hard deletes when appropriate
- Use database constraints to enforce data integrity
- Implement proper backup and recovery procedures
- Use read replicas for scaling read operations
- Implement database monitoring and alerting

### Microservices and Distributed Systems
- Design services around business capabilities
- Implement proper service discovery and registration
- Use API gateways for external communication
- Implement circuit breakers for fault tolerance
- Use distributed tracing for debugging
- Implement proper service-to-service authentication
- Use message queues for asynchronous communication
- Implement proper data consistency patterns
- Use health checks for service monitoring
- Implement graceful shutdown procedures

### Security Best Practices
- Never trust user input - validate and sanitize everything
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Use HTTPS for all external communications
- Implement rate limiting to prevent abuse
- Use secure headers (HSTS, CSP, X-Frame-Options)
- Implement proper password policies and hashing
- Use secure session management
- Implement proper CORS policies
- Regular security audits and dependency updates
- Use environment variables for secrets, never hardcode
- Implement proper logging for security events
- Use principle of least privilege for access control

### Performance Optimization
- Profile before optimizing - measure, don't guess
- Use appropriate data structures for the use case
- Implement caching strategies at multiple levels
- Use database indexes and query optimization
- Implement pagination for large datasets
- Use async/await for I/O-bound operations
- Use connection pooling for database and HTTP connections
- Implement proper memory management
- Use generators for large data processing
- Monitor application performance continuously
- Use CDNs for static content delivery
- Implement proper load balancing strategies

Remember: The goal is to write code that is self-explanatory, maintainable, and follows established patterns that any Python developer can understand immediately. Code should read like well-written prose that tells a story about what the system does.
