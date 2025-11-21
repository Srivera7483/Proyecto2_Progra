import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nombre de la base de datos SQLite
DATABASE_URL = "sqlite:///restaurante.db"

# Crear motor
engine = create_engine(DATABASE_URL, echo=False)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Generador de dependencias para obtener la sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()