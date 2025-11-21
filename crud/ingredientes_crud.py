import csv
from sqlalchemy.orm import Session
from models import Ingrediente

class IngredienteCRUD:
    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, unidad: str, stock: float):
        # Buscar si ya existe
        existente = db.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()
        if existente:
            existente.stock_actual += stock
            # Si el CSV trae unidad, actualizamos, si no, mantenemos la que tenía
            if unidad:
                existente.unidad = unidad
            db.commit()
            db.refresh(existente)
            return existente
        else:
            nuevo = Ingrediente(nombre=nombre, unidad=unidad, stock_actual=stock)
            db.add(nuevo)
            db.commit()
            db.refresh(nuevo)
            return nuevo

    @staticmethod
    def obtener_todos(db: Session):
        """Esta es la función que te faltaba y causaba el error AttributeError"""
        return db.query(Ingrediente).all()

    @staticmethod
    def actualizar_stock(db: Session, ingrediente_id: int, cantidad: float):
        ing = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ing:
            ing.stock_actual = cantidad
            db.commit()
            return ing
        return None

    @staticmethod
    def importar_desde_csv(db: Session, ruta_archivo: str):
        count = 0
        with open(ruta_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    nombre = row["nombre"]
                    unidad = row["unidad"]
                    cantidad = float(row["cantidad"])
                    
                    IngredienteCRUD.crear_ingrediente(db, nombre, unidad, cantidad)
                    count += 1
                except ValueError:
                    continue
        return count