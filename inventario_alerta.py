import sqlite3

# 1. Conexión a la base de datos del segundo proyecto
conexion = sqlite3.connect("inventario_alertas.db")
cursor = conexion.cursor()

# 2. Crear la tabla de productos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    marca TEXT NOT NULL,
    costo INT NOT NULL,
    precio INT NOT NULL,
    stock INT NOT NULL
)
''')

# 3. Datos iniciales de prueba
# (Puedes cambiar estos valores por los tuyos)
cursor.execute("SELECT COUNT(*) FROM productos")
if cursor.fetchone()[0] == 0:
    cursor.executemany('''
        INSERT INTO productos (modelo, marca, costo, precio, stock) 
        VALUES (?, ?, ?, ?, ?)
    ''', [
        ('Top Flex', 'Joma', 35000, 55000, 8),
        ('Regate Rebound', 'Joma', 40000, 60000, 2),   # ALERTA (<= 3)
        ('Mercurial Vapor', 'Nike', 55000, 85000, 1), # ALERTA (<= 3)
        ('Predator', 'Adidas', 50000, 78000, 5)
    ])
    conexion.commit()

# 4. Consultar todo el inventario
cursor.execute("SELECT modelo, marca, stock FROM productos")
productos = cursor.fetchall()

# 5. Mostrar inventario y evaluar Alerta de Stock Bajo
print("===========================================")
print("   CONTROL DE INVENTARIO Y ALERTAS         ")
print("===========================================")

LIMITE_ALERTA = 3
alertas_detectadas = 0

for prod in productos:
    modelo, marca, stock = prod
    
    # Evaluar la condición de stock bajo
    if stock <= LIMITE_ALERTA:
        print(f"[⚠️ ALERTA STOCK BAJO] {marca} {modelo} -> Quedan solo {stock} unidades")
        alertas_detectadas += 1
    else:
        print(f"[OK - Stock Normal]   {marca} {modelo} -> {stock} unidades disponibles")

print("-------------------------------------------")
if alertas_detectadas > 0:
    print(f"⚠️ Atención: Tienes {alertas_detectadas} producto(s) por reponer urgente.")
else:
    print("✅ Todo tu stock está al día.")
print("===========================================")

conexion.close()