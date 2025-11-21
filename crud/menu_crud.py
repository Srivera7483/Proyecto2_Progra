from sqlalchemy.orm import Session
from models import Menu, Ingrediente, menu_ingrediente

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, precio: int, items_ingredientes: list):
        """
        Crea un menú y lo asocia con sus ingredientes.
        """
        # Validar nombre único
        if db.query(Menu).filter(Menu.nombre == nombre).first():
            return None

        # Crear objeto Menú
        nuevo_menu = Menu(nombre=nombre, precio=precio)
        db.add(nuevo_menu)
        db.flush()  # Generar ID sin hacer commit final

        # Insertar relaciones en la tabla intermedia
        for item in items_ingredientes:
            stmt = menu_ingrediente.insert().values(
                menu_id=nuevo_menu.id,
                ingrediente_id=item['ingrediente_id'],
                cantidad_requerida=item['cantidad']
            )
            db.execute(stmt)

        db.commit()
        db.refresh(nuevo_menu)
        return nuevo_menu

    @staticmethod
    def obtener_todos(db: Session):
        return db.query(Menu).all()

    @staticmethod
    def eliminar_menu(db: Session, menu_id: int):
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if menu:
            db.delete(menu)
            db.commit()
            return True
        return False

# --- FUNCIÓN PARA INICIALIZAR DATOS (CORREGIDA) ---

def poblar_db_desde_catalogo(db: Session):
    """
    Recorre el catálogo y agrega SOLO los menús que falten en la base de datos.
    """
    print("Verificando catálogo de menús...")

    # Datos extraídos de tu archivo Menu_catalog.py
    datos_iniciales = [
        {
            "nombre": "Sandwich de potito (Esp de la casa)",
            "precio": 2400,
            "receta": [
                ("Intestino de vacuno", "unid", 0.5),
                ("Pan de hamburguesa", "unid", 1),
                ("longaniza", "unid", 0.5),
                ("Cebolla", "unid", 0.5),
            ]
        },
        {
            "nombre": "Completo",
            "precio": 1800,
            "receta": [
                ("Vienesa", "unid", 1),
                ("Pan de completo", "unid", 1),
                ("Palta", "unid", 1),
                ("Tomate", "unid", 1),
            ]
        },
        {
            "nombre": "Cangriburger Simple",
            "precio": 2500,
            "receta": [
                ("Carne de hamburguesa", "unid", 1),
                ("Pan de hamburguesa", "unid", 1),
                ("lechuga", "unidad", 0.5),
                ("Tomate", "unidad", 0.5),
                ("Lamina de cheddar", "unid", 1),
            ]
        },
        {
            "nombre": "Cangriburger Doble",
            "precio": 3500,
            "receta": [
                ("Carne de hamburguesa", "unid", 2),
                ("Pan de hamburguesa", "unid", 1),
                ("lechuga", "unidad", 1),
                ("Tomate", "unidad", 1),
                ("Lamina de cheddar", "unid", 2),
            ]
        },
        {
            "nombre": "Papas fritas (chicas)",
            "precio": 1000,
            "receta": [("Papa", "unid", 2)]
        },
        {
            "nombre": "Papas fritas (medianas)",
            "precio": 2000,
            "receta": [("Papa", "unid", 4)]
        },
        {
            "nombre": "Papas fritas (grandes)",
            "precio": 3000,
            "receta": [("Papa", "unid", 6)]
        },
        {
            "nombre": "Chorrillana simple",
            "precio": 5000,
            "receta": [
                ("Carne de vacuno", "unid", 1),
                ("Papas", "unid", 3),
                ("Cebolla", "unidad", 1),
                ("Huevos", "unidad", 2),
            ]
        },
        {
            "nombre": "Chorrillana XL",
            "precio": 8000,
            "receta": [
                ("Carne de vacuno", "unid", 2),
                ("Papas", "unid", 4),
                ("Cebolla", "unidad", 2),
                ("Huevos", "unidad", 2),
                ("Chorizo", "unid", 1),
                ("Vienesa", "unid", 1),
            ]
        },
        {
            "nombre": "Ensalada mixta",
            "precio": 1800,
            "receta": [
                ("Tomate", "unid", 1),
                ("Lechuga", "unid", 1),
                ("Cebolla", "unid", 0.5),
                ("Huevo", "unid", 1)
            ]
        },
        {
            "nombre": "Empanada frita",
            "precio": 1200,
            "receta": [
                ("Masa de empanada", "unid", 1),
                ("Carne de vacuno", "unid", 0.5),
                ("Cebolla", "unid", 0.5),
                ("Huevo", "unid", 0.25),
            ]
        },
        {
            "nombre": "Empanada de queso",
            "precio": 1000,
            "receta": [
                ("Masa de empanada", "unid", 1),
                ("Queso", "unid", 0.5),
            ]
        },
        {
            "nombre": "Coca-Cola",
            "precio": 1100,
            "receta": [("Coca cola", "unid", 1)]
        },
        {
            "nombre": "Pepsi",
            "precio": 1100,
            "receta": [("Coca cola", "unid", 1)]
        }
    ]

    cont_nuevos = 0
    for menu_data in datos_iniciales:
        # 1. Verificar si el menú YA EXISTE por nombre
        existe = db.query(Menu).filter(Menu.nombre == menu_data["nombre"]).first()
        if existe:
            continue # Si existe, pasamos al siguiente

        # Si no existe, lo creamos
        lista_para_asociar = []

        # 2. Asegurar ingredientes
        for nombre_ing, unidad, cantidad in menu_data["receta"]:
            ing_obj = db.query(Ingrediente).filter(Ingrediente.nombre == nombre_ing).first()
            
            if not ing_obj:
                # Si el ingrediente no existe, lo creamos con stock de prueba (500)
                ing_obj = Ingrediente(nombre=nombre_ing, unidad=unidad, stock_actual=500.0)
                db.add(ing_obj)
                db.flush()
            
            lista_para_asociar.append({
                "ingrediente_id": ing_obj.id, 
                "cantidad": cantidad
            })

        # 3. Crear el menú
        MenuCRUD.crear_menu(db, menu_data["nombre"], menu_data["precio"], lista_para_asociar)
        cont_nuevos += 1
        print(f"Agregado nuevo menú: {menu_data['nombre']}")

    if cont_nuevos > 0:
        db.commit()
        print(f"Se agregaron {cont_nuevos} platos nuevos al menú.")
    else:
        print("El menú ya estaba actualizado.")