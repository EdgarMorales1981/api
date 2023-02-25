import psycopg2

import uuid
import cloudinary
import cloudinary.uploader
import uvicorn
from fastapi import FastAPI, status, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Servicio(BaseModel):
    id: str = None
    nombre: str
    descripcion: str
    foto: str
    precio: str

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


@app.get("/status")
def check_status():
    return {"status": "ok"}

@app.get("/servicios{id}",status_code=status.HTTP_200_OK)
async def serviciosOne(id:str):
    conn = psycopg2.connect(
        database="vfvxprgv",
        user='vfvxprgv',
        password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
        host="mahmud.db.elephantsql.com"
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM contenedor WHERE ID = '{id}' ")
    rows = cur.fetchall()

    formatted_datos = []
    for row in rows:
        formatted_datos.append(
            Servicio(id=row[0], nombre=row[1], descripcion=row[2],foto=row[3],precio=row[4])
        )

    cur.close()
    conn.close()
    return formatted_datos

@app.get("/servicios",status_code=status.HTTP_200_OK)
async def servicios():
    conn = psycopg2.connect(
        database="vfvxprgv",
        user='vfvxprgv',
        password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
        host="mahmud.db.elephantsql.com"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM contenedor ORDER BY id DESC")
    rows = cur.fetchall()

    formatted_datos = []
    for row in rows:
        formatted_datos.append(
            Servicio(id=row[0], nombre=row[1], descripcion=row[2],foto=row[3],precio=row[4])
        )

    cur.close()
    conn.close()
    return formatted_datos

@app.post("/servicios",status_code=status.HTTP_201_CREATED)
async def create_servicio(file:UploadFile, nombre:str = Form(), descripcion: str = Form(), precio: str = Form()):
        result = cloudinary.uploader.upload(file.file)
        url =result.get("url")
        id = uuid.uuid4()
        foto = url
        conn = psycopg2.connect(
            database="vfvxprgv",
            user='vfvxprgv',
            password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
            host="mahmud.db.elephantsql.com"
        )
        cur = conn.cursor()
        cur.execute(f"INSERT INTO contenedor (id, nombre,descripcion, foto, precio) VALUES  ('{id}','{nombre}','{descripcion}','{foto}','{precio}')")
        conn.commit()
        cur.close()
        conn.close()
        return {"id": id, "nombre": nombre, "descripcion": descripcion, "foto": foto, "precio": precio}


@app.put("/servicios/{id}",status_code=status.HTTP_200_OK)
async def editar(id:str, file:UploadFile, nombre:str = Form(), descripcion: str = Form(), precio: str = Form()):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    foto=url
    conn = psycopg2.connect(
        database="vfvxprgv",
        user='vfvxprgv',
        password='u1Ququtd0f-27eKTgXwzlrHTpwaYqVUE',
        host="mahmud.db.elephantsql.com"
    )


    cur = conn.cursor()
    cur.execute(
        f"UPDATE contenedor SET nombre='{nombre}',descripcion='{descripcion}', foto='{foto}', precio='{precio}' WHERE id='{id}'")
    conn.commit()
    cur.close()
    conn.close()
    return  {"id": id, "nombre": nombre, "descripcion": descripcion, "foto": foto, "precio": precio}




if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8000)