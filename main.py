from fastapi import FastAPI, UploadFile,Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import cloudinary
import cloudinary.uploader
import uuid
headers={"content-type":"utf-8"}
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloudinary.config(
     cloud_name="ejmorales",
     api_key="485664484772281",
     api_secret="zTuUNkCS6RX3kmizDQCIpo3Qf3c"
 )


class Servicio(BaseModel):
    id: str = None
    nombre: str
    descripcion: str
    foto: str
    precio: str
@app.get("/")
async def index():
    content = {"message": "!Hello World"}
    return JSONResponse(content=content,headers=headers)
@app.get("/servicios")
async def servicios():
    conn = psycopg2.connect(
        database="vfvxprgv",
        user='vfvxprgv',
        password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
        host="mahmud.db.elephantsql.com"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM contenedor ORDER BY id DESC")
    rows= cur.fetchall()
    content = [{
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "foto": row[3],
        "precio": row[4]
    } for row in  rows]
    cur.close()
    conn.close()
    return JSONResponse(content=content,headers=headers,media_type="application/json")

@app.get("/servicios/buscar/{id}")
async def servicios_buscar(id: str):
    conn = psycopg2.connect(
    database="vfvxprgv",
    user='vfvxprgv',
     password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
    host="mahmud.db.elephantsql.com"
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM contenedor WHERE id = '{id}'")
    rows = cur.fetchall()
    content = [{
        "id": row[0],
        "nombre": row[1],
        "descripcion": row[2],
        "foto": row[3],
        "precio": row[4]
    } for row in rows]
    cur.close()
    conn.close()
    return JSONResponse(content=content, headers=headers, media_type="application/json")

@app.post("/servicios/crear")
async def crear_servicio(file: UploadFile, nombre: str = Form(), descripcion: str = Form(), precio: str = Form()):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("secure_url")
    id = uuid.uuid4()
    foto = url
    conn = psycopg2.connect(
        database="vfvxprgv",
        user='vfvxprgv',
        password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
        host="mahmud.db.elephantsql.com"
    )
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO contenedor (id, nombre,descripcion, foto, precio) VALUES  ('{id}','{nombre}','{descripcion}','{foto}','{precio}')")
    conn.commit()
    cur.close()
    conn.close()
    return JSONResponse(content={"message": "Servicio creado"}, headers=headers, media_type="application/json")


