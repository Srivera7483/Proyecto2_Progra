import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import SessionLocal
from models import Cliente, Menu, Pedido, Ingrediente
# CORRECCIÓN AQUÍ: importamos 'ingredientes_crud' (plural)
from crud import cliente_crud, menu_crud, pedido_crud, ingredientes_crud
from graficos import GestorGraficos

class RestaurantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión - Restaurante Cangri & Sons")
        self.geometry("1100x700")
        
        self.db = SessionLocal()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_clientes = self.tab_view.add("Clientes")
        self.tab_menu = self.tab_view.add("Menú")
        self.tab_ingredientes = self.tab_view.add("Ingredientes")
        self.tab_pedidos = self.tab_view.add("Nuevo Pedido")
        self.tab_estadisticas = self.tab_view.add("Estadísticas")
        
        self.setup_clientes_ui()
        self.setup_menu_ui()
        self.setup_ingredientes_ui()
        self.setup_pedidos_ui()
        self.setup_estadisticas_ui()

    # --- CLIENTES ---
    def setup_clientes_ui(self):
        frame_form = ctk.CTkFrame(self.tab_clientes)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(frame_form, text="Nuevo Cliente", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.entry_nombre = ctk.CTkEntry(frame_form, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=5)
        
        self.entry_email = ctk.CTkEntry(frame_form, placeholder_text="Email")
        self.entry_email.pack(pady=5)
        
        ctk.CTkButton(frame_form, text="Guardar Cliente", command=self.crear_cliente).pack(pady=10)
        
        frame_tabla = ctk.CTkFrame(self.tab_clientes)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree_clientes = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Email"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.pack(fill="both", expand=True)

        ctk.CTkButton(frame_tabla, text="Actualizar Tabla", command=self.cargar_clientes).pack(pady=5)
        self.cargar_clientes()

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        try:
            cliente_crud.ClienteCRUD.crear_cliente(self.db, nombre, email)
            messagebox.showinfo("Éxito", "Cliente creado correctamente")
            self.entry_nombre.delete(0, "end")
            self.entry_email.delete(0, "end")
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        clientes = cliente_crud.ClienteCRUD.obtener_todos(self.db)
        for c in clientes:
            self.tree_clientes.insert("", "end", values=(c.id, c.nombre, c.email))


    # --- MENÚ ---
    def setup_menu_ui(self):
        frame_lista = ctk.CTkFrame(self.tab_menu)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_menu = ttk.Treeview(frame_lista, columns=("ID", "Nombre", "Precio"), show="headings")
        self.tree_menu.heading("ID", text="ID")
        self.tree_menu.heading("Nombre", text="Plato")
        self.tree_menu.heading("Precio", text="Precio")
        self.tree_menu.pack(fill="both", expand=True)

        ctk.CTkButton(self.tab_menu, text="Refrescar Menú", command=self.cargar_menu).pack(pady=10)
        self.cargar_menu()

    def cargar_menu(self):
        for item in self.tree_menu.get_children():
            self.tree_menu.delete(item)
        menus = menu_crud.MenuCRUD.obtener_todos(self.db)
        for m in menus:
            self.tree_menu.insert("", "end", values=(m.id, m.nombre, f"${m.precio}"))

    # --- INGREDIENTES (CORREGIDO) ---
    def setup_ingredientes_ui(self):
        frame_top = ctk.CTkFrame(self.tab_ingredientes)
        frame_top.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_top, text="Control de Stock", font=("Arial", 16, "bold")).pack(side="left", padx=10)
        
        btn_csv = ctk.CTkButton(frame_top, text="📂 Cargar CSV", command=self.cargar_csv_ingredientes)
        btn_csv.pack(side="right", padx=10)

        frame_tabla = ctk.CTkFrame(self.tab_ingredientes)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_ingredientes = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Unidad", "Stock"), show="headings")
        self.tree_ingredientes.heading("ID", text="ID")
        self.tree_ingredientes.heading("Nombre", text="Ingrediente")
        self.tree_ingredientes.heading("Unidad", text="Unidad")
        self.tree_ingredientes.heading("Stock", text="Stock Actual")
        
        self.tree_ingredientes.column("ID", width=50, anchor="center")
        self.tree_ingredientes.column("Stock", width=100, anchor="center")
        self.tree_ingredientes.pack(fill="both", expand=True)

        ctk.CTkButton(self.tab_ingredientes, text="Refrescar Tabla", command=self.refrescar_tabla_ingredientes).pack(pady=5)
        
        self.refrescar_tabla_ingredientes()

    def cargar_csv_ingredientes(self):
        ruta = filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if ruta:
            try:
                # CORRECCIÓN AQUÍ: usamos ingredientes_crud (con s)
                total = ingredientes_crud.IngredienteCRUD.importar_desde_csv(self.db, ruta)
                messagebox.showinfo("Carga Exitosa", f"Se procesaron {total} ingredientes.")
                self.refrescar_tabla_ingredientes()
            except Exception as e:
                messagebox.showerror("Error CSV", str(e))

    def refrescar_tabla_ingredientes(self):
        for item in self.tree_ingredientes.get_children():
            self.tree_ingredientes.delete(item)
        
        # CORRECCIÓN AQUÍ: llamamos al método obtener_todos que agregamos en el paso 1
        items = ingredientes_crud.IngredienteCRUD.obtener_todos(self.db)
        
        for ing in items:
            self.tree_ingredientes.insert("", "end", values=(ing.id, ing.nombre, ing.unidad, ing.stock_actual))


    # --- PEDIDOS ---
    def setup_pedidos_ui(self):
        frame_top = ctk.CTkFrame(self.tab_pedidos)
        frame_top.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_top, text="ID Cliente:").pack(side="left", padx=5)
        self.entry_id_cliente_pedido = ctk.CTkEntry(frame_top, width=60)
        self.entry_id_cliente_pedido.pack(side="left", padx=5)

        ctk.CTkLabel(frame_top, text="ID Menú:").pack(side="left", padx=5)
        self.entry_id_menu_pedido = ctk.CTkEntry(frame_top, width=60)
        self.entry_id_menu_pedido.pack(side="left", padx=5)

        ctk.CTkLabel(frame_top, text="Cantidad:").pack(side="left", padx=5)
        self.entry_cantidad_pedido = ctk.CTkEntry(frame_top, width=60)
        self.entry_cantidad_pedido.pack(side="left", padx=5)

        ctk.CTkButton(frame_top, text="Agregar al Carrito", command=self.agregar_al_carrito).pack(side="left", padx=10)

        self.carrito_items = []
        
        frame_carrito = ctk.CTkFrame(self.tab_pedidos)
        frame_carrito.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame_carrito, text="Carrito de Compras").pack()
        self.text_carrito = ctk.CTkTextbox(frame_carrito, height=150)
        self.text_carrito.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(self.tab_pedidos, text="FINALIZAR PEDIDO", fg_color="green", command=self.finalizar_pedido).pack(pady=10)

    def agregar_al_carrito(self):
        try:
            m_id = int(self.entry_id_menu_pedido.get())
            cant = int(self.entry_cantidad_pedido.get())
            
            menu_obj = self.db.query(Menu).filter(Menu.id == m_id).first()
            if not menu_obj:
                messagebox.showerror("Error", "Menú no existe")
                return

            self.carrito_items.append({'menu_id': m_id, 'cantidad': cant})
            self.text_carrito.insert("end", f"- {menu_obj.nombre} x {cant}\n")
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos")

    def finalizar_pedido(self):
        if not self.carrito_items:
            return
        try:
            c_id = int(self.entry_id_cliente_pedido.get())
            nuevo_pedido = pedido_crud.PedidoCRUD.crear_pedido(self.db, c_id, self.carrito_items)
            
            messagebox.showinfo("Pedido Exitoso", f"Pedido creado! Total: ${nuevo_pedido.total}")
            self.carrito_items = []
            self.text_carrito.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Error al crear pedido", str(e))


    # --- ESTADÍSTICAS ---
    def setup_estadisticas_ui(self):
        self.gestor_graficos = GestorGraficos(self.db)
        
        frame_controles = ctk.CTkFrame(self.tab_estadisticas, height=40)
        frame_controles.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(frame_controles, text="Actualizar Gráficos", command=self.actualizar_graficos).pack(pady=5)

        self.frame_graficos = ctk.CTkFrame(self.tab_estadisticas, fg_color="white")
        self.frame_graficos.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.actualizar_graficos()

    def actualizar_graficos(self):
        self.gestor_graficos.dibujar_grafico_ventas_por_menu(self.frame_graficos)


    def on_close(self):
        print("Cerrando aplicación y base de datos...")
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()