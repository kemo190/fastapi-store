from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg

app = FastAPI()

# CORS للسماح للفرونت إند يتواصل
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# الاتصال بقاعدة البيانات
async def get_db():
    return await asyncpg.connect(
        user="postgres", password="Kk112233", 
        database="student_db", host="localhost"
    )

# نموذج البيانات
class Registration(BaseModel):
    name: str
    phone: str
    college: str
    status: str
    year: str = None
    track: str
    city: str

# API للتسجيل
@app.post("/api/register")
async def register(data: Registration):
    conn = await get_db()
    await conn.execute("""
        INSERT INTO students (name, phone, college, status, year, track, city)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, data.name, data.phone, data.college, data.status, data.year, data.track, data.city)
    await conn.close()
    return {"message": "تم الحفظ بنجاح"}

# API لعرض كل الطلاب
@app.get("/api/students")
async def get_students():
    conn = await get_db()
    rows = await conn.fetch("SELECT * FROM students ORDER BY id DESC")
    await conn.close()

    return [
        {
            "name": row["name"],
            "phone": row["phone"],
            "college": row["college"],
            "status": row["status"],
            "year": row["year"],
            "track": row["track"],
            "city": row["city"]
        }
        for row in rows
    ]
