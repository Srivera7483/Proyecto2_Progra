from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  

# --- TABLAS DE ASOCIACIÓN (Muchos a Muchos con cantidad extra) ---

# Tabla intermedia: Ingredientes dentro de un Menú (con cantidad requerida)
menu_ingrediente = Table(
    'menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad_requerida', Float, nullable=False)
)

# Tabla intermedia: Menús dentro de un Pedido (con cantidad comprada)
pedido_menu = Table(
    'pedido_menu', Base.metadata,
    Column('pedido_id', Integer, ForeignKey('pedidos.id'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('cantidad', Integer, nullable=False) 
)

# --- MODELOS PRINCIPALES ---

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relación: Un cliente tiene muchos pedidos
    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    unidad = Column(String, nullable=True) # ej: kg, lt, unid
    stock_actual = Column(Float, default=0.0)

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)
    
    # Relación: Muchos a Muchos con Ingredientes
    ingredientes = relationship("Ingrediente", secondary=menu_ingrediente, backref="menus_que_lo_usan")

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Integer, default=0)
    
    # Clave foránea del cliente
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")
    
    # Relación: Muchos a Muchos con Menu
    items = relationship("Menu", secondary=pedido_menu, backref="pedidos_donde_aparece")