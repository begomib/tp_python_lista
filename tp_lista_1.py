
# lista Begoña Muñoz
#lista 
productos = []

#numeracion de la lista
def productos_de_la_lista(lista):
    if not  lista:
        print ("no hay productos")
        return
   
    print("\n lista de productos")
    print ("*" * 50)
    for i, producto in enumerate(lista, start=1):
        print(f"{i}. Nombre: {producto[0]}")
        print(f"   Categoría: {producto[1]}")
        print(f"   Precio: ${producto[2]}")
        
        print("*" * 50)
    
    else:
        print("\n No existe ese producto.")

# no dejar ingresar productos en blanco
def nombre_producto(prompt):
    while True:
        texto = input(prompt).strip()
        if texto:
            return texto
        else:
            print("No puede quedar vacio.")

# ingresar precio (entero)
def precio_producto(prompt):
    while True:
        try:
            valor = int(input(prompt))
            if valor > 0:
                return valor
            else:
                print("el precio debe ser mayor de cero")
        except ValueError:
            print("el precio debe ser un numero entero.")


# buscar productos por nombre

def buscar_producto(lista):
    busqueda = input("\nIngrese el nombre del producto:").strip()
    if not busqueda:
        print("No puede estar vacío.")
        return
    coincidencias = [p for p in lista if busqueda.lower() in p[0].lower()]

    if coincidencias:
        print("\n Productos encontrados:")
        print("*" * 40)
        for i, producto in enumerate(coincidencias, start=1):
            print(f"{i}. Nombre: {producto[0]}")
            print(f"   Categoría: {producto[1]}")
            print(f"   Precio: ${producto[2]}")
            print("*" * 50)
    else:
        print("\n No se encontraron productos con ese nombre.")


    # Función para eliminar un producto
def borrar_producto(lista):
    productos_de_la_lista(lista)
    if not lista:
        return
    while True:
        try:
            numero = int(input("Ingrese el número del producto a eliminar: "))
            if 1 <= numero <= len(lista):
                eliminado = lista.pop(numero - 1)
                print(f"\n Producto '{eliminado[0]}' eliminado correctamente.")
                break
            else:
                print("error al ingresar el numnero del producto, intente nuevamente")
        except ValueError:
            print("ingresar un número válido.")

## ACÁ SE LLAMA A LA FUNCIÓN DE ARRANQUE
def ingresar_nuevo():
    nombre = nombre_producto("Ingrese el nombre del producto: ")
    categoria = nombre_producto("Ingrese la categoría del producto: ")
    precio = precio_producto("Ingrese el precio del producto: $")
    productos.append([nombre, categoria, precio])
    print(f"\n Producto '{nombre}' agregado correctamente.")

if __name__ == "__main__":
    opcion = ''
    print("\nMenú de opciones: ")
    print("1. Ingresar nuevo producto")
    print("2. Mostrar productos de la lista")
    print("3. Buscar producto por nombre")
    print("4. Borrar un producto")
    print("5. Salir")
    
    while opcion != '5':
        opcion = input("Ingrese opción: ")
        opcion = opcion.strip()
        if opcion == '1':
            ingresar_nuevo()
        elif opcion == '2':
            productos_de_la_lista(productos)
        elif opcion == '3':
            buscar_producto(productos)
        elif opcion == '4':
            borrar_producto(productos)
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")