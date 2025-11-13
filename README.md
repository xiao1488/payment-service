# Payment Service — FastAPI + MongoDB Atlas (Render Deployment)

## Overview
This microservice handles payment operations (create, read, update, delete).
It connects to MongoDB Atlas and is deployed using Docker on Render.

## Features
- CRUD operations for payments
- `/health/db` endpoint to verify MongoDB connectivity
- Secure environment configuration (no exposed `.env`)

## Environment Variables
| Name | Description |
|------|--------------|
| `MONGO_URI` | MongoDB Atlas connection string |
| `DB_NAME` | Database name (e.g., ecommerce) |

## Local Run
```bash
docker build -t payment-service .
docker run -p 8000:8000 -e MONGO_URI="mongodb://localhost:27017" -e DB_NAME="ecommerce" payment-service