from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Cliente
class ClienteCRUD:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, email: str):
        if not nombre or not email:
            raise ValueError("Nombre y email son obligatorios")
        
        # Uso de lambda/filter sugerido en pauta para validación simple en memoria (opcional, ya que SQL lo hace mejor)
        # Aquí confiamos en la DB, pero manejamos el error
        try:
            nuevo_cliente = Cliente(nombre=nombre, email=email)
            db.add(nuevo_cliente)
            db.commit()
            db.refresh(nuevo_cliente)
            return nuevo_cliente
        except IntegrityError:
            db.rollback()
            raise ValueError("El correo electrónico ya está registrado.")

    @staticmethod
    def obtener_todos(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def eliminar_cliente(db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            # Validación de la pauta: "Impedir eliminar clientes con pedidos"
            if cliente.pedidos: 
                raise ValueError("No se puede eliminar un cliente con pedidos asociados.")
            db.delete(cliente)
            db.commit()
            return True
        return False