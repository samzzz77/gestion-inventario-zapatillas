import sqlite3
from datetime import date

# 1. Conectarse a la base de datos local
conexion = sqlite3.connect("mi_negocio.db")
cursor = conexion.cursor()

# 2. Crear las tablas de Productos, Clientes y Ventas
cursor.executescript('''
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    marca TEXT NOT NULL,
    costo INT NOT NULL,
    precio_sugerido INT NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contacto TEXT
);

CREATE TABLE IF NOT EXISTS ventas (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha TEXT NOT NULL,
    precio_venta INT NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
''')

# 3. Insertar datos iniciales
cursor.execute("SELECT COUNT(*) FROM productos")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO productos (modelo, marca, costo, precio_sugerido, stock) VALUES (?, ?, ?, ?, ?)", [
        ('Maxima', 'Joma', 35000, 55000, 7),
        ('Dribling', 'Joma', 40000, 60000, 5),
        ('Mercurial Vapor', 'Nike', 55000, 85000, 4)
    ])
    
    cursor.executemany("INSERT INTO clientes (nombre, contacto) VALUES (?, ?)", [
        ('Benjamín', '@benja_fb'),
        ('Carlos', '+56912345678')
    ])
    
    cursor.executemany("INSERT INTO ventas (id_producto, id_cliente, fecha, precio_venta) VALUES (?, ?, ?, ?)", [
        (1, 1, '2026-04-15', 55000),
        (2, 2, '2026-04-18', 58000)
    ])
    conexion.commit()

# --- FUNCIONES DEL MENÚ ---

def mostrar_reporte():
    consulta_ganancias = '''
        SELECT 
            p.modelo, 
            p.marca, 
            v.precio_venta, 
            p.costo, 
            (v.precio_venta - p.costo) AS ganancia_neta
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto
    '''
    cursor.execute(consulta_ganancias)
    resultados = cursor.fetchall()

    print("\n=======================================")
    print("   REPORTE DE GANANCIAS AUTOMÁTICO     ")
    print("=======================================")
    total_ganado = 0
    for fila in resultados:
        modelo, marca, precio_v, costo, ganancia = fila
        print(f"Zapato: {marca} {modelo} | Vendido: ${precio_v:,} | Costo: ${costo:,} | GANANCIA: ${ganancia:,}")
        total_ganado += ganancia
    print("---------------------------------------")
    print(f"GANANCIAS TOTALES: ${total_ganado:,}")
    print("=======================================\n")

def registrar_venta():
    print("\n--- REGISTRAR NUEVA VENTA ---")
    cursor.execute("SELECT id_producto, marca, modelo, precio_sugerido, stock FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos disponibles.")
        return

    print("Productos disponibles:")
    for prod in productos:
        print(f"[{prod[0]}] {prod[1]} {prod[2]} - Precio Sugerido: ${prod[3]:,} (Stock: {prod[4]})")

    try:
        id_prod = int(input("\nIngresa el ID del producto vendido: "))
        precio_real = int(input("Ingresa el precio final de venta ($): "))
        
        fecha_hoy = str(date.today())
        
        # Registrar la venta (asignamos cliente 1 por defecto)
        cursor.execute(
            "INSERT INTO ventas (id_producto, id_cliente, fecha, precio_venta) VALUES (?, ?, ?, ?)",
            (id_prod, 1, fecha_hoy, precio_real)
        )
        
        # Descontar 1 del stock
        cursor.execute("UPDATE productos SET stock = stock - 1 WHERE id_producto = ?", (id_prod,))
        conexion.commit()
        print("¡Venta registrada con éxito!\n")
    except ValueError:
        print("Error: Ingresa valores numéricos válidos.\n")

# --- MENÚ PRINCIPAL ---
while True:
    print("=== SISTEMA DE GESTIÓN DE ZAPATILLAS ===")
    print("1. Ver reporte de ganancias")
    print("2. Registrar una nueva venta")
    print("3. Salir")
    
    opcion = input("Selecciona una opción (1-3): ")
    
    if opcion == "1":
        mostrar_reporte()
    elif opcion == "2":
        registrar_venta()
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.\n")

conexion.close()