from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ecommerce")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]
    payments = db.payments
except Exception as e:
    print("⚠️ Error connecting to MongoDB:", e)

app = FastAPI(title="Payment Service")


class PaymentBase(BaseModel):
    user_id: str
    order_id: str
    amount: float
    method: str = Field(..., description="Payment method (card, paypal, etc.)")

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: str
    status: str
    created_at: datetime

class PaymentUpdate(BaseModel):
    status: str


@app.post("/payments", response_model=PaymentOut, status_code=201)
def create_payment(payload: PaymentCreate):
    doc = {
        "user_id": payload.user_id,
        "order_id": payload.order_id,
        "amount": payload.amount,
        "method": payload.method,
        "status": "PENDING",
        "created_at": datetime.utcnow(),
    }
    res = payments.insert_one(doc)
    return {
        "id": str(res.inserted_id),
        **payload.dict(),
        "status": "PENDING",
        "created_at": doc["created_at"],
    }

@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: str):
    p = payments.find_one({"_id": ObjectId(payment_id)})
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {
        "id": str(p["_id"]),
        "user_id": p["user_id"],
        "order_id": p["order_id"],
        "amount": p["amount"],
        "method": p["method"],
        "status": p["status"],
        "created_at": p["created_at"],
    }

@app.put("/payments/{payment_id}", response_model=dict)
def update_payment(payment_id: str, payload: PaymentUpdate):
    result = payments.update_one({"_id": ObjectId(payment_id)}, {"$set": {"status": payload.status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": f"Payment {payment_id} updated to {payload.status}"}

@app.delete("/payments/{payment_id}", response_model=dict)
def delete_payment(payment_id: str):
    result = payments.delete_one({"_id": ObjectId(payment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": f"Payment {payment_id} deleted successfully"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        db.command("ping")
        return {"db": "ok"}
    except Exception as e:
        return {"db": "error", "details": str(e)}
