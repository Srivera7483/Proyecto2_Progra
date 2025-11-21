from database import engine, Base, SessionLocal
from models import Cliente, Ingrediente, Menu, Pedido
# Importar la función de sembrado del nuevo CRUD
from crud.menu_crud import poblar_db_desde_catalogo

def init_db():
    print("Verificando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas.")
    
    # Crear sesión temporal para poblar datos
    db = SessionLocal()
    try:
        poblar_db_desde_catalogo(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()