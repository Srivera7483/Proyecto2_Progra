Sistema de Gestión de Restaurante "Cangri & sons™"

Evaluación 3 - Programación II - Ingeniería Civil en Informática

Descripción del Proyecto

Este proyecto es una solución de software de escritorio desarrollada para optimizar la gestión operativa de un restaurante. A diferencia de versiones anteriores, esta iteración (Ev3) implementa una arquitectura robusta basada en Persistencia de Datos y Patrones de Diseño.

El sistema permite administrar clientes, controlar el stock de ingredientes basado en recetas, tomar pedidos y generar boletas en PDF automáticamente.

Características Técnicas (Requisitos Ev3)

Persistencia de Datos: Uso de SQLAlchemy (ORM) con base de datos SQLite. Los datos no se pierden al cerrar el programa.

Interfaz Gráfica Moderna: Implementada con CustomTkinter para una experiencia de usuario limpia y responsiva (Modo Oscuro/Claro).

Gestión de Inventario: Carga inicial masiva desde csv y descuento automático de stock al generar ventas (Relación N:M entre Menús e Ingredientes).

Generación de Documentos: Creación de boletas detalladas en formato PDF usando el patrón Facade.

Validaciones: Control de errores en inputs de usuario (Regex para correos, validación de tipos numéricos, stock negativo).

🛠️ Instalación y Ejecución

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1. Prerrequisitos

Asegúrate de tener Python 3.10 o superior instalado.

2. Clonar el Repositorio

git clone <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DE_LA_CARPETA>


3. Instalar Dependencias

Se recomienda usar un entorno virtual.

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Instalar librerías
pip install -r requirements.txt


4. Ejecutar la Aplicación

python main.py

Nota: Al ejecutar por primera vez, el sistema creará automáticamente el archivo restaurante.sqlite y cargará el stock inicial desde ingredientes_menu.csv.

Estructura del Proyecto

El código está organizado siguiendo el principio de separación de responsabilidades:

├── crud/                   # Lógica de Negocio (Create, Read, Update, Delete)
│   ├── cliente_crud.py
│   ├── ingrediente_crud.py
│   └── ...
├── models.py               # Modelos ORM (Clases mapeadas a tablas)
├── database.py             # Configuración de conexión a BD
├── BoletaFacade.py         # Patrón Facade para generación de PDFs
├── main.py                 # Punto de entrada y GUI (Vista)
├── ingredientes_menu.csv   # Datos semilla para el inventario
└── requirements.txt        # Lista de dependencias


Patrones de Diseño Aplicados

Facade (BoletaFacade.py): Simplifica la compleja librería FPDF, proveyendo una interfaz simple para imprimir boletas.

MVC (Implícito): Separación clara entre los Modelos (models.py), la Lógica de Control (crud/) y la Vista (main.py).

Autores

Equipo de Desarrollo:

Sebastian Rivera

Simón Molina

Pablo Urra

Asignatura: Programación II
Universidad Católica de Temuco
Fecha: Noviembre 2025
