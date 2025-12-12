import sqlite3
import sys

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    _C = True
except Exception:
    _C = False
    class _Fake:
        RESET_ALL = ""
    Fore = Style = _Fake()

DB = "inventario.db"


def conectar(path=DB):
    return sqlite3.connect(path)

#creacion de base de datos:
def crear_tabla(con):
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
        """
    )
    con.commit()

#registrar productos
def registrar(con):
    nombre = input("Nombre: ").strip()
    if not nombre:
        print(Fore.RED + "Nombre vacío." + Style.RESET_ALL)
        return
    descripcion = input("Descripción: ").strip()
    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
    except ValueError:
        print(Fore.RED + "Cantidad o precio inválido." + Style.RESET_ALL)
        return
    categoria = input("Categoría: ").strip()
    cur = con.cursor()
    cur.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                (nombre, descripcion, cantidad, precio, categoria))
    con.commit()
    print(Fore.GREEN + "Registrado." + Style.RESET_ALL)

# mostrar lista de productos
def mostrar_lista(con):
    cur = con.cursor()
    cur.execute("SELECT id, nombre, cantidad, precio FROM productos ORDER BY id")
    filas = cur.fetchall()
    if not filas:
        print(Fore.YELLOW + "Sin productos." + Style.RESET_ALL)
        return
    print(Fore.CYAN + "--- Lista de productos ---" + Style.RESET_ALL)
    for f in filas:
        id_col = Fore.MAGENTA + str(f[0]) + Style.RESET_ALL
        nombre_col = Fore.GREEN + f[1] + Style.RESET_ALL
        cantidad_col = Fore.YELLOW + f"cantidad:{f[2]}" + Style.RESET_ALL
        precio_col = Fore.LIGHTBLUE_EX + f"precio $ {f[3]}" + Style.RESET_ALL
        print(f"{id_col} | {nombre_col} | {cantidad_col} | {precio_col}")

# buscar productos por nombre
def buscar_nombre(con):
    nombre_buscar = input("Nombre: ").strip()
    if not nombre_buscar:
        print(Fore.RED + "Nombre vacío." + Style.RESET_ALL)
        return
    cur = con.cursor()
    cur.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
    filas = cur.fetchall()
    if not filas:
        print(Fore.YELLOW + "No encontrado." + Style.RESET_ALL)
        return
    print(Fore.CYAN + "--- Resultados ---" + Style.RESET_ALL)
    for fila in filas:
        id_col = Fore.MAGENTA + str(fila[0]) + Style.RESET_ALL
        nombre_col = Fore.GREEN + fila[1] + Style.RESET_ALL
        desc_col = Fore.WHITE + (fila[2] or '-') + Style.RESET_ALL
        cantidad_col = Fore.YELLOW + f"c:{fila[3]}" + Style.RESET_ALL
        precio_col = Fore.LIGHTBLUE_EX + f"$ {fila[4]}" + Style.RESET_ALL
        cat_col = Fore.LIGHTCYAN_EX + (fila[5] or '-') + Style.RESET_ALL
        print(f"{id_col} | {nombre_col} | {desc_col} | {cantidad_col} | {precio_col} | {cat_col}")

# actualizar productos por nombre
def actualizar(con):
    nombre_buscar = input("Nombre del producto a actualizar: ").strip()
    if not nombre_buscar:
        print(Fore.RED + "Nombre vacío." + Style.RESET_ALL)
        return
    cur = con.cursor()
    cur.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
    filas = cur.fetchall()
    if not filas:
        print(Fore.YELLOW + "No existe." + Style.RESET_ALL)
        return
    if len(filas) > 1:
        print(Fore.CYAN + "Hay varios productos con ese nombre:" + Style.RESET_ALL)
        for f in filas:
            print(f"  {f[0]}: {f[1]}")
        try:
            id_ = int(input("Ingrese el ID del producto a actualizar: "))
        except ValueError:
            print(Fore.RED + "ID inválido." + Style.RESET_ALL)
            return
        fila = next((f for f in filas if f[0] == id_), None)
        if not fila:
            print(Fore.RED + "ID no encontrado en los resultados." + Style.RESET_ALL)
            return
    else:
        fila = filas[0]
        id_ = fila[0]
    
    nombre = input("Nombre (vacío = sin cambio): ").strip()
    descripcion = input("Descripción (vacío = sin cambio): ").strip()
    cantidad_s = input("Cantidad (vacío = sin cambio): ").strip()
    precio_s = input("Precio (vacío = sin cambio): ").strip()
    categoria = input("Categoría (vacío = sin cambio): ").strip()
    
    nombre = nombre or fila[1]
    descripcion = descripcion or fila[2]
    try:
        cantidad = int(cantidad_s) if cantidad_s else fila[3]
        precio = float(precio_s) if precio_s else fila[4]
    except ValueError:
        print(Fore.RED + "Cantidad o precio inválido. Cancelado." + Style.RESET_ALL)
        return
    categoria = categoria or fila[5]
    
    cur.execute("UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?",
                (nombre, descripcion, cantidad, precio, categoria, id_))
    con.commit()
    print(Fore.GREEN + "Actualizado." + Style.RESET_ALL)

# eliminar productos por nombre
def eliminar(con):
    nombre_buscar = input("Nombre del producto a eliminar: ").strip()
    if not nombre_buscar:
        print(Fore.RED + "Nombre vacío." + Style.RESET_ALL)
        return
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM productos WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
    filas = cur.fetchall()
    if not filas:
        print(Fore.YELLOW + "No existe." + Style.RESET_ALL)
        return
    if len(filas) > 1:
        print(Fore.CYAN + "Hay varios productos con ese nombre:" + Style.RESET_ALL)
        for f in filas:
            print(f"  {f[0]}: {f[1]}")
        try:
            id_ = int(input("Ingrese el ID del producto a eliminar: "))
        except ValueError:
            print(Fore.RED + "ID inválido." + Style.RESET_ALL)
            return
        fila = next((f for f in filas if f[0] == id_), None)
        if not fila:
            print(Fore.RED + "ID no encontrado en los resultados." + Style.RESET_ALL)
            return
    else:
        fila = filas[0]
        id_ = fila[0]
    
    ok = input(f"Eliminar {fila[1]}? (s/n): ").lower()
    if ok != 's':
        print(Fore.YELLOW + "Cancelado." + Style.RESET_ALL)
        return
    cur.execute("DELETE FROM productos WHERE id = ?", (id_,))
    con.commit()
    print(Fore.GREEN + "Eliminado." + Style.RESET_ALL)

# reporte de productos por cantidad maxima
def reporte(con):
    try:
        lim = int(input("Límite cantidad: "))
    except ValueError:
        print("Límite inválido.")
        return
    cur = con.cursor()
    cur.execute("SELECT id, nombre, cantidad FROM productos WHERE cantidad <= ? ORDER BY cantidad", (lim,))
    filas = cur.fetchall()
    if not filas:
        print("Ninguno." )
        return
    for f in filas:
        print(f"{f[0]}: {f[1]} | c:{f[2]}")
        
# menú principal
def menu():
    con = conectar()
    crear_tabla(con)
    if '--init' in sys.argv:
        print(Fore.CYAN + "BD lista." + Style.RESET_ALL)
        con.close()
        return
    ops = {
        '0': ('Registrar', registrar),
        '1': ('Mostrar lista', mostrar_lista),
        '2': ('Buscar por nombre', buscar_nombre),
        '3': ('Actualizar por nombre', actualizar),
        '4': ('Eliminar por nombre', eliminar),
         '4': ('Consulta productos por cantidad maxima', reporte),
        '6': ('Salir', None)
    }
    while True:
        print('')
        if _C:
            print(Fore.BLUE + '=== Menú Inventario ===' + Style.RESET_ALL)
        else:
            print('=== Menú Inventario ===')
        for k in sorted(ops.keys()):
            print(k + ") " + ops[k][0])
        sel = input('Opción: ').strip()
        if sel == '0':
            print(Fore.GREEN + 'Saliendo...' + Style.RESET_ALL)
            break
        act = ops.get(sel)
        if not act:
            print(Fore.RED + 'Opción inválida.' + Style.RESET_ALL)
            continue
        func = act[1]
        if func:
            func(con)
    con.close()


if __name__ == '__main__':
    menu()
