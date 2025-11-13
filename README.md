# 💳 Payment Service — FastAPI + MongoDB Atlas (Render Deployment)

## 🧩 Overview
This microservice handles **payment operations** (create, read, update, delete).  
It connects to **MongoDB Atlas** and is deployed using **Docker** on **Render**.

---

## 🚀 Features
- Full **CRUD** for payments (`/payments`)
- Health check endpoint: `/health/db`
- Secure **environment-based configuration**
- **Dockerized** for easy deployment
- Deployed live on Render:  
  👉 [https://payment-service-g6iu.onrender.com](https://payment-service-g6iu.onrender.com)

---

## ⚙️ Environment Variables
| Variable | Description | Example |
|-----------|--------------|----------|
| `MONGO_URI` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster0.mongodb.net/` |
| `DB_NAME` | Database name | `ecommerce` |
| `PORT` *(optional)* | Server port | `8000` |

> 🔒 Make sure to store sensitive data (like `MONGO_URI`) in `.env` — do **not** commit it.

---

## 🧱 Local Development

### 1️⃣ Clone the repo
```bash
git clone <your_repo_url>
cd payment-service
