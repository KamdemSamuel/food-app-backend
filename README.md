# Food App Backend

A robust REST API backend for a food delivery/ordering application built with **Flask** and **Python**, containerized with **Docker** for seamless deployment.

## Overview

The Food App Backend is a comprehensive Flask-based API that powers food ordering and management features. It provides endpoints for managing users, food items, orders, and integrates with a database layer for persistent data storage.

## Tech Stack

- **Framework**: Flask (Python web framework)
- **Database**: Supports both DAO (Data Access Object) and ORM approaches
- **Containerization**: Docker & Docker Compose
- **Dependency Management**: Pipenv
- **Testing**: Python unittest framework

## Project Structure

```
food-app-backend/
├── app.py                          # Main Flask application entry point
├── main.py                         # Alternative entry point with DAO pattern
├── main_orm.py                     # ORM-based implementation
├── requirements.txt                # Python dependencies
├── Pipfile & Pipfile.lock         # Pipenv configuration
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Multi-container orchestration
├── data.json                       # Sample/seed data
├── import_data.py                  # Data import utility
├── run_orm_migrations.py           # Database migration runner
├── business_logic/                 # Core business logic modules
├── dao/                            # Data Access Object implementations
├── orm_dao/                        # ORM-based data access
├── models/                         # Data models
├── database/                       # Database configuration and setup
├── templates/                      # HTML templates (if applicable)
├── tests/                          # Test suites
├── test_business_logic.py          # Business logic tests
└── Exercice_Of_Assigement/         # Assignment-related files
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (for containerized deployment)
- Pipenv or pip

### Installation

#### Option 1: Using Pipenv (Recommended)

```bash
# Clone the repository
git clone https://github.com/KamdemSamuel/food-app-backend.git
cd food-app-backend

# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

#### Option 2: Using pip

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Local Development

```bash
# Using standard Flask entry point
python app.py

# Or using DAO pattern
python main.py

# Or using ORM pattern
python main_orm.py
```

The API will be available at `http://localhost:5000`

#### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build the image manually
docker build -t food-app-backend .
docker run -p 5000:5000 food-app-backend
```

### Database Setup

If using the ORM approach:

```bash
# Run migrations
python run_orm_migrations.py

# Import initial data
python import_data.py
```

## Features

- 🍔 **Food Management**: CRUD operations for food items
- 👥 **User Management**: User registration and profile management
- 🛒 **Order Management**: Create, track, and manage food orders
- 📊 **Data Persistence**: Multiple data access patterns (DAO & ORM)
- 🐳 **Docker Support**: Easy containerization and deployment
- ✅ **Testing**: Comprehensive test suites included

## API Endpoints

The API provides RESTful endpoints for:

- **Food Items**: List, create, read, update, delete menu items
- **Orders**: Create and manage customer orders
- **Users**: User registration and profile management

(For detailed endpoint documentation, refer to the Flask app configuration)

## Testing

Run the test suites to ensure everything works correctly:

```bash
# Run all tests
python -m pytest

# Run business logic tests
python test_business_logic.py

# Run specific test modules
python -m pytest tests/
```

## Development

### Data Access Patterns

The project implements two data access patterns:

1. **DAO Pattern** (`dao/`, `main.py`): Traditional Data Access Object implementation for direct database queries
2. **ORM Pattern** (`orm_dao/`, `main_orm.py`): SQLAlchemy ORM for object-oriented database interactions

Choose the approach that best fits your needs when deploying.

### Adding New Features

1. Create models in the `models/` directory
2. Implement business logic in `business_logic/`
3. Add data access methods in `dao/` or `orm_dao/`
4. Create API endpoints in the main Flask app
5. Add tests to ensure functionality

## Environment Variables

Create a `.env` file in the project root if needed for:

- Database connection strings
- API configuration
- Secret keys
- Other sensitive configurations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:

```bash
# Change the port in app.py or run with a different port
python app.py --port 5001
```

### Database Connection Issues

Ensure database credentials are properly configured in your environment or configuration files.

### Docker Issues

Make sure Docker and Docker Compose are installed:

```bash
docker --version
docker-compose --version
```

## License

This project is open source and available under the MIT License.

## Author

**KamdemSamuel** - [GitHub Profile](https://github.com/KamdemSamuel)

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub Issues](https://github.com/KamdemSamuel/food-app-backend/issues) page.

---

**Created**: June 17, 2025  
**Last Updated**: June 28, 2025
