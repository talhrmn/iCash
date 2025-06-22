# iCash Supermarket Microservices System

A microservices-based system for managing supermarket purchases and analytics, built with Docker and FastAPI.

## Project Overview

This system implements two main microservices:

1. **Cash Register Service**
    - Simulates cashier activity
    - Handles purchase transactions
    - Stores purchase data in PostgreSQL database

2. **Store Analytics Service**
    - Provides real-time analytics
    - Tracks customer loyalty
    - Analyzes product sales


![img.png](img.png)


## System Requirements

- Docker and Docker Compose
- Python 3.8+
- PostgreSQL
- Node.js (for frontend)

## Project Structure

```
.
├── web_client/          # Frontend React application
├── cash_register/       # Cash register microservice
├── store_analytics/     # Store analytics microservice
├── database/            # Database configuration and migrations
├── shared/              # Shared code and models
├── alembic/             # Database migrations
└── docker-compose.yml   # Docker configuration
```

## Setup Instructions

1. **Environment Setup**
    - Copy `.env.example` to `.env` and update the configuration
    - Ensure all required environment variables are set

2. **Database Setup**
    - The system uses PostgreSQL
    - Initial data is loaded from `Products_list.csv` and `Purchases.csv`
    - Database migrations are handled by Alembic

3. **Running the System**
   ```bash
   # Build and start all services
   docker-compose up --build
   
   # Access services:
   # Cash Register API: http://localhost:8000
   # Store Analytics API: http://localhost:8001
   # Frontend (if enabled): http://localhost:3000
   ```

## Features

### Cash Register Service

- Simulates cashier activity
- Handles purchase transactions
- Validates purchase constraints
- Stores purchase data
- Supports UUID4 customer identification

### Store Analytics Service

- Tracks unique buyers across all branches
- Identifies loyal customers (≥3 purchases)
- Calculates top-selling products
- Provides real-time analytics

## API Documentation

### Cash Register API

- **GET /branches**
    - Get list of all branches
- **GET /products**
    - Get list of all products
- **POST /purchases**
    - Create new purchase
        - Required fields: branch_id, user_id, items

### Store Analytics API

- **GET /analytics/customers**
    - Get unique customer count
- **GET /analytics/loyal-customers**
    - Get list of loyal customers
- **GET /analytics/top-products**
    - Get top-selling products

## Data Model

## Database Schema

### Products Table

- `id`: Integer (Primary Key)
- `product_name`: String
- `unit_price`: Float

### Branches Table

- `id`: Integer (Primary Key)

### Purchases Table

- `id`: Integer (Primary Key)
- `supermarket_id`: Integer (Foreign Key to Branches)
- `user_id`: String (UUID4)
- `timestamp`: DateTime
- `total_amount`: Float

### Purchase Items Table

- `purchase_id`: Integer (Foreign Key to Purchases)
- `product_id`: Integer (Foreign Key to Products)
- `quantity`: Integer (Default: 1)
- `unit_price`: Float

### Relationships

- A Purchase belongs to a Branch
- A Purchase has many Purchase Items
- A Purchase Item belongs to a Product
- A Product can be in many Purchase Items
- A Branch can have many Purchases

### Data Model Constraints

- Each customer can buy at most one unit of each product per purchase
- Purchase total is automatically calculated from items
- All timestamps are stored in UTC
- UUID4 is used for customer identification

## Development

### Database Migrations

```bash
docker-compose exec postgres alembic upgrade head
```

### Logging

- Service logs are stored in their respective log directories
- Log levels can be configured via environment variables

### Example images
![img_1.png](img_1.png)