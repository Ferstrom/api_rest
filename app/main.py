from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Crear instancia de FastAPI
app = FastAPI()

# Configuración de la conexión a PostgreSQL
DATABASE_URL = "postgresql://user:JB8ziPCn40pW6DHpipN3rgbpSB5QpfMU@dpg-csc0qulds78s73cdlldg-a.oregon-postgres.render.com/db_agenda_u1pv"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir los modelos
Base = declarative_base()

# Definición del modelo de la tabla 'personas'
class Persona(Base):
    __tablename__ = "personas"
    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de ejemplo para insertar una persona
@app.post("/personas/")
def crear_persona(nombre: str, telefono: str, db: Session = Depends(get_db)):
    nueva_persona = Persona(nombre=nombre, telefono=telefono)
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)
    return nueva_persona

# Ruta para obtener todas las personas
@app.get("/personas/")
def obtener_personas(db: Session = Depends(get_db)):
    personas = db.query(Persona).all()
    return personas

# Ruta principal
@app.get("/")
async def root():
    return {"message": "Bienvenido a mi FastAPI"}
