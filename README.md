# Evaluer - Academic Grading System

A modern, sophisticated grading system for academic institutions using Hive LMS. This system provides automated grade calculation, manual assessment capabilities, and comprehensive grade management following SOLID principles and cloud-native patterns.

## Architecture Overview

The system implements a hierarchical grading model where:
- **Response-Level Grading**: Manual quality assessment of redo submissions (1-5 scale)
- **Exercise-Level Calculation**: Automated aggregation of response grades
- **Module-Level Aggregation**: Weighted combination of exercise scores
- **Subject-Level Reporting**: Overall course performance metrics
- **Overall Student Grading**: Cross-subject aggregated performance scores

## Key Features

- ✅ **Hierarchical Grading System**: Exercise → Module → Subject → Overall grade calculation
- ✅ **Configurable Weight System**: Custom weights for subjects, modules, and exercises with environment defaults
- ✅ **Overall Student Scoring**: Configurable cross-subject grade aggregation with weighted or equal methods
- ✅ **Intelligent Response Classification**: Auto-detection of redo vs auto-check responses
- ✅ **File Caching**: 20-minute TTL with invalidation on new submissions
- ✅ **Real-time Grade Calculation**: Immediate updates after manual grading
- ✅ **Full Hive Sync**: Complete data synchronization with Hive LMS
- ✅ **RESTful API**: FastAPI-based endpoints for all operations
- ✅ **Async Architecture**: High-performance async/await patterns
- ✅ **Redis Caching**: File and data caching for optimal performance
- ✅ **PostgreSQL Storage**: Robust relational data persistence

## Tech Stack

- **Backend**: FastAPI with async/await
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **Caching**: Redis for files and computed data
- **Migration**: Alembic for database versioning
- **Deployment**: Docker with cloud-native patterns
- **Integration**: Hive LMS REST API client

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd evaluer

# Copy environment configuration
cp .env.example .env

# Edit .env with your Hive credentials and database settings
```

### 2. Development with Docker Compose

```bash
# Start all services (PostgreSQL, Redis, API)
docker-compose up -d

# View logs
docker-compose logs -f evaluer-api
```

### 3. Local Development Setup

```bash
# Install dependencies
poetry install

# Start PostgreSQL and Redis (via Docker or locally)
docker-compose up -d postgres redis

# Run database migrations
poetry run alembic upgrade head

# Start the API server
poetry run uvicorn evaluer.api.app:app --reload
```

### 4. Initial Data Sync

```bash
# Full sync from Hive LMS
curl -X POST http://localhost:8000/api/sync/full

# Or sync specific student
curl -X POST http://localhost:8000/api/sync/student/{student_id}
```

## API Endpoints

### Student Operations
- `GET /api/v1/students` - List all students
- `GET /api/v1/students/{id}/grading` - Student grading overview with overall grade
- `GET /api/v1/students/{id}/overall` - Student overall grading view
- `POST /api/v1/students/{id}/recalculate-overall` - Recalculate overall grade only
- `POST /api/v1/students/{id}/recalculate-all` - Recalculate all grades for student

### Grading Operations
- `GET /api/v1/exercises` - List all exercises  
- `GET /api/v1/exercises/{id}/redo-responses` - Redo responses needing grades
- `PATCH /api/v1/responses/{id}/grade` - Submit manual grade (1-5)
- `GET /api/v1/responses/{assignment_id}/{response_id}/files` - Get response files

### Data Synchronization
- `POST /api/v1/sync/full` - Complete sync from Hive
- `POST /api/v1/sync/student/{id}` - Sync specific student data

### System Health
- `GET /` - API status
- `GET /health` - Health check

## Grading Workflow

### 1. Data Sync
The system syncs data from Hive LMS including:
- Students (clearance level HANICH)
- Assignments and responses
- Exercise/module/subject hierarchy
- Response classifications (Redo, AutoCheck, etc.)

### 2. Grade Calculation Rules

**Response Classification:**
- **AutoCheck responses**: Automatic pass/fail scoring
- **Redo responses**: Require manual 1-5 quality assessment
- **Other responses**: Informational only

**Calculation Hierarchy:**
1. **Exercise Grade**: Average of redo response quality scores × 20
2. **Module Grade**: Weighted average of exercise grades
3. **Subject Grade**: Weighted average of module grades
4. **Overall Grade**: Weighted or equal average of subject grades (configurable)

**Weight Configuration:**
- **Default weights**: System-wide defaults via environment variables
- **Custom weights**: Entity-specific weights in database
- **Auto-normalization**: Weights automatically normalized to 100%
- **Fallback behavior**: Equal distribution when no weights specified

### 3. Manual Grading Process
1. Select student from student list
2. Navigate to subject → module → exercise
3. View redo responses requiring assessment
4. Access student files (cached for 20 minutes)
5. Assign quality grade (1-5 scale)
6. System automatically recalculates all dependent grades (exercise → module → subject → overall)

## Configuration

### Weight Management
Weights can be configured at multiple levels:
- **Default weights**: Set via environment variables for system-wide defaults
- **Custom weights**: Stored in the `weight_configurations` table for specific entities
- **Auto-completion**: System automatically normalizes weights to 100% when partially defined
- Database direct updates (future admin interface planned)
- Migration scripts for institutional defaults
- API endpoints (future feature)

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# Redis
REDIS_URL=redis://host:port/db

# Hive LMS
HIVE_BASE_URL=https://your-hive-instance
HIVE_USERNAME=your-username  
HIVE_PASSWORD=your-password

# Application
DEBUG=false
FILE_CACHE_TTL=1200  # 20 minutes

# Default Weight Configuration
DEFAULT_SUBJECT_WEIGHT=25.00      # Default weight for subjects (0.01-100.00)
DEFAULT_MODULE_WEIGHT=33.33       # Default weight for modules (0.01-100.00)
DEFAULT_EXERCISE_WEIGHT=10.00     # Default weight for exercises (0.01-100.00)

# Overall Grading Configuration
ENABLE_OVERALL_GRADING=true                           # Enable/disable overall grading
OVERALL_GRADE_CALCULATION_METHOD=weighted_average     # Method: weighted_average or equal_weight
```

## Database Schema

### Core Tables
- `students` - Student information from Hive
- `subjects` - Course subjects with optional weights
- `modules` - Subject modules with optional weights  
- `exercises` - Module exercises with optional weights
- `assignments` - Student-exercise assignments
- `assignment_responses` - Response submissions and grades
- `student_grades` - Calculated grades at each level
- `weight_configurations` - Configurable weight settings

### Key Relationships
- Student → Assignments → Responses (1:N:N)
- Subject → Modules → Exercises (1:N:N) 
- Responses → Manual Grades → Calculated Grades (1:1:N)

## Performance Considerations

### Caching Strategy
- **File Cache**: 20-minute TTL, invalidated on new submissions
- **API Response Cache**: Hive data with configurable TTL
- **Computed Grades**: Stored in database, recalculated on changes

### Scalability Patterns
- Async/await throughout for non-blocking I/O
- Connection pooling for database and Redis
- Bulk operations for large dataset sync
- Pagination support for large result sets

## Monitoring and Observability

### Health Checks
- Database connectivity
- Redis availability  
- Hive LMS API status
- Grade calculation consistency

### Logging
- Structured logging with timestamps
- API request/response logging
- Grade calculation audit trail
- Sync operation status tracking

## Security Considerations

### Data Protection
- Student data handling following privacy requirements
- Secure credential management via environment variables
- Database connection encryption
- API rate limiting and authentication (future)

### Access Control
- Currently open access (institutional network assumption)
- Future: Role-based permissions for graders/administrators
- Audit logging for grade changes and access

## Development Guidelines

### Code Organization
```
evaluer/
├── api/           # FastAPI routes and models
├── cache/         # Redis configuration and utilities
├── clients/       # External API clients (Hive)
├── core/          # Settings and shared models
├── database/      # SQLAlchemy models and config
├── repositories/  # Data access layer
├── services/      # Business logic layer
└── main.py        # Legacy CLI interface
```

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- Performance tests for grade calculations
- Mock Hive API for testing

### Contributing
1. Follow async/await patterns throughout
2. Use type hints for all function signatures
3. Implement proper error handling and logging
4. Add tests for new functionality
5. Update documentation for API changes

## Deployment

### Production Deployment
```bash
# Build production image
docker build -t evaluer:latest .

# Run with production settings
docker run -d \
  --name evaluer-api \
  -p 8000:8000 \
  -e DATABASE_URL=your-prod-db \
  -e REDIS_URL=your-prod-redis \
  evaluer:latest
```

### Environment-Specific Configs
- Development: Docker Compose with local services
- Staging: Kubernetes deployment with external databases
- Production: Cloud-native deployment with managed services

## Future Enhancements

### Planned Features
- [ ] Web-based admin interface for weight configuration
- [ ] Real-time notifications for grading deadlines
- [ ] Advanced analytics and reporting dashboards
- [ ] Bulk grading operations and CSV exports
- [ ] Grade history and audit trail interface
- [ ] Student self-service grade viewing
- [ ] Integration with additional LMS platforms

### Performance Optimizations
- [ ] Database query optimization and indexing
- [ ] Advanced caching strategies
- [ ] Background job processing for heavy operations
- [ ] API response compression and CDN integration

## Support

For technical support or questions:
- Review API documentation at `/docs` when running
- Check logs via `docker-compose logs evaluer-api`
- Verify environment configuration in `.env`
- Ensure Hive LMS connectivity and credentials

## License

[Add your license information here]
