from sqlalchemy.orm import Session
from models import Pedido, Menu, Cliente, Ingrediente, pedido_menu, menu_ingrediente

class PedidoCRUD:
    @staticmethod
    def crear_pedido(db: Session, cliente_id: int, items_pedido: list):
        """
        Crea un pedido, calcula el total y DESCUENTA STOCK.
        Si no hay stock suficiente, cancela todo (Rollback) y avisa el error.
        """
        # 1. Verificar Cliente
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise ValueError("El cliente no existe.")

        # Iniciamos una transacción "segura": si algo falla (falta stock), nada se guarda
        try:
            # 2. Instanciar Pedido (el total se calcula abajo)
            nuevo_pedido = Pedido(cliente_id=cliente_id, total=0)
            db.add(nuevo_pedido)
            db.flush()  # Generamos el ID del pedido sin confirmar aún

            total_calculado = 0

            # 3. Procesar cada menú solicitado
            for item in items_pedido:
                menu_id = item['menu_id']
                cantidad_platos = item['cantidad']

                # Obtener objeto Menú
                menu_obj = db.query(Menu).filter(Menu.id == menu_id).first()
                if not menu_obj:
                    raise ValueError(f"El menú con ID {menu_id} no existe.")

                total_calculado += (menu_obj.precio * cantidad_platos)

                # --- LÓGICA DE DESCUENTO DE STOCK ---
                # Buscamos en la tabla intermedia qué ingredientes usa este menú
                # SELECT * FROM menu_ingrediente WHERE menu_id = ...
                ingredientes_receta = db.query(menu_ingrediente).filter(
                    menu_ingrediente.c.menu_id == menu_id
                ).all()

                for ing_asoc in ingredientes_receta:
                    ing_id = ing_asoc.ingrediente_id
                    cantidad_requerida_por_plato = ing_asoc.cantidad_requerida
                    
                    # Total a descontar = receta * cantidad de platos pedidos
                    total_a_descontar = cantidad_requerida_por_plato * cantidad_platos

                    # Traer el ingrediente real para ver su stock
                    ing_obj = db.query(Ingrediente).filter(Ingrediente.id == ing_id).first()
                    
                    if not ing_obj:
                        raise ValueError(f"Ingrediente ID {ing_id} no encontrado en base de datos.")

                    # VALIDACIÓN DE STOCK
                    if ing_obj.stock_actual < total_a_descontar:
                        raise ValueError(
                            f"Stock insuficiente de '{ing_obj.nombre}'. "
                            f"Necesitas {total_a_descontar} {ing_obj.unidad}, "
                            f"pero solo hay {ing_obj.stock_actual}."
                        )

                    # Descontar
                    ing_obj.stock_actual -= total_a_descontar
                
                # --- FIN LÓGICA STOCK ---

                # Insertar relación Pedido-Menu
                stmt = pedido_menu.insert().values(
                    pedido_id=nuevo_pedido.id,
                    menu_id=menu_id,
                    cantidad=cantidad_platos
                )
                db.execute(stmt)

            # 4. Guardar cambios finales
            nuevo_pedido.total = total_calculado
            db.commit()
            db.refresh(nuevo_pedido)
            return nuevo_pedido

        except Exception as e:
            db.rollback() # Si falta stock o hay error, deshacemos todo
            raise e # Re-lanzamos el error para que la App muestre el mensaje

    @staticmethod
    def obtener_pedidos(db: Session):
        return db.query(Pedido).order_by(Pedido.fecha.desc()).all()

    @staticmethod
    def obtener_pedido_por_id(db: Session, pedido_id: int):
        return db.query(Pedido).filter(Pedido.id == pedido_id).first()