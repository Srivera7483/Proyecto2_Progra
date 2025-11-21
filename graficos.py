import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Pedido, Menu, pedido_menu   
class GestorGraficos:
    def __init__(self, db: Session):
        self.db = db

    def dibujar_grafico_ventas_por_menu(self, parent_frame):
        """
        Genera un gráfico de barras con los menús más vendidos
        y lo dibuja dentro de 'parent_frame'.
        """
        # 1. Limpiar frame anterior si existe
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # 2. Consulta SQL Agregada: Nombre Menu vs Suma de Cantidades
        # SELECT menus.nombre, SUM(pedido_menu.cantidad) 
        # FROM menus JOIN pedido_menu ... GROUP BY menus.id
        resultados = (
            self.db.query(Menu.nombre, func.sum(pedido_menu.c.cantidad).label("total_vendido"))
            .join(pedido_menu, Menu.id == pedido_menu.c.menu_id)
            .group_by(Menu.nombre)
            .all()
        )

        if not resultados:
            lbl = tk.Label(parent_frame, text="No hay datos suficientes para graficar.")
            lbl.pack()
            return

        # Separar datos para los ejes
        nombres = [r[0] for r in resultados]
        cantidades = [r[1] for r in resultados]

        # 3. Crear Figura Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Colores personalizados
        colores = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722']
        ax.bar(nombres, cantidades, color=colores[:len(nombres)])
        
        ax.set_title("Platos más Vendidos")
        ax.set_ylabel("Cantidad Vendida")
        ax.set_xticklabels(nombres, rotation=20, ha="right")
        
        # Ajustar diseño para que no se corten las etiquetas
        fig.tight_layout()

        # 4. Renderizar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def dibujar_grafico_ingresos(self, parent_frame):
        """
        Genera un gráfico lineal de ingresos totales por pedido (o por día simplificado).
        """
        # Limpiar
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Consulta: Obtener fecha y total de cada pedido
        pedidos = self.db.query(Pedido.fecha, Pedido.total).order_by(Pedido.fecha).all()

        if not pedidos:
            return

        # Procesar datos (Simplificado: Graficamos pedido a pedido secuencialmente)
        fechas = [p.fecha.strftime("%d/%m %H:%M") for p in pedidos]
        ingresos = [p.total for p in pedidos]

        # Crear Figura
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.plot(fechas, ingresos, marker='o', linestyle='-', color='purple')
        
        ax.set_title("Historial de Ingresos por Pedido")
        ax.set_ylabel("Monto ($CLP)")
        ax.tick_params(axis='x', rotation=45)
        
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)