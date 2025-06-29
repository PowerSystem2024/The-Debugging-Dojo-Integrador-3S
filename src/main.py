# src/main.py
from src.services.cliente_service import ClienteService
from src.services.mozo_service import MozoService
from src.services.menu_services import MenuService
from src.services.mesa_services import MesaService
from src.database.database_setup import initialize_database


def mostrar_menu_principal():
    print("\n=== RESTAURANTE ===")
    print("1. Registrar cliente")
    print("2. Asignar mesa")
    print("3. Ver menú")
    print("4. Listar clientes")
    print("5. Listar mesas disponibles")
    print("6. Cargar menú de ejemplo")
    print("7. Recrear base de datos")  # Nueva opción para emergencias
    print("8. Salir")


def main():
    # Inicializar base de datos al comenzar
    initialize_database()

    # Inicializar servicios
    cliente_service = ClienteService()
    mesa_service = MesaService()
    mozo_service = MozoService()
    menu_service = MenuService()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- REGISTRAR CLIENTE ---")
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")
            cliente_id = cliente_service.registrar_cliente(nombre, telefono)
            if cliente_id:
                print(f"Cliente registrado con ID: {cliente_id}")

        elif opcion == "2":
            print("\n--- ASIGNACIÓN AUTOMÁTICA DE MESA ---")
            try:
                personas = int(input("¿Para cuántas personas? "))
                resultado = mesa_service.asignar_mesa_automatica(personas)
                if 'error' in resultado:
                    print(f"\n✖ {resultado['error']}")
                else:
                    print(f"\n✔ {resultado['mensaje']}")
                    print(f"   Capacidad: {resultado['capacidad']} personas")
            except ValueError:
                print("Error: Ingrese un número válido de personas")

        elif opcion == "3":
            print("\n--- MENÚ ---")
            menu = menu_service.obtener_menu()
            if not menu:  # Si el menú está vacío
                print("El menú está vacío. ¿Desea cargar el menú de ejemplo? (s/n)")
                if input().lower() == 's':
                    if menu_service.insertar_menu_ejemplo():
                        menu = menu_service.obtener_menu()

            # Mostrar el menú organizado por categorías
            categorias = {}
            for item in menu:
                if item[4] not in categorias:  # item[4] es la categoría
                    categorias[item[4]] = []
                categorias[item[4]].append(item)

            for categoria, items in categorias.items():
                print(f"\n{categoria.upper()}:")
                for item in items:
                    print(f"  {item[1]} - ${item[3]:.2f}")  # item[1] = nombre, item[3] = precio
                    print(f"    {item[2]}")  # item[2] = descripción

        elif opcion == "4":
            print("\n--- CLIENTES REGISTRADOS ---")
            clientes = cliente_service.listar_clientes()
            if clientes:
                for cliente in clientes:
                    print(f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | Tel: {cliente['telefono']}")
            else:
                print("No hay clientes registrados")

        elif opcion == "5":
            print("\n--- MESAS DISPONIBLES ---")
            mesas = mesa_service.obtener_mesas_disponibles()
            if mesas:
                print("Número | Capacidad")
                print("------------------")
                for numero, capacidad in mesas:
                    print(f"{numero:6} | {capacidad:8}")
            else:
                print("No hay mesas disponibles actualmente")

        elif opcion == "6":  # Nueva opción para cargar menú de ejemplo
            print("\n--- CARGAR MENÚ DE EJEMPLO ---")
            confirmacion = input("¿Está seguro que desea cargar el menú de ejemplo? (s/n): ")
            if confirmacion.lower() == 's':
                if menu_service.insertar_menu_ejemplo():
                    print("✅ Menú argentino cargado exitosamente")
                else:
                    print("❌ Error al cargar el menú de ejemplo")

        elif opcion == "7":  # Nueva opción para recrear DB
            print("\n⚠️ ADVERTENCIA: Esto borrará y recreará toda la estructura de la base de datos")
            confirm = input("¿Está ABSOLUTAMENTE seguro? (s/n): ")
            if confirm.lower() == 's':
                from src.database.database_setup import DatabaseSetup
                db_setup = DatabaseSetup()
                if db_setup.create_database_structure():
                    db_setup.insert_initial_data()
                    print("✅ Base de datos recreada exitosamente")

        elif opcion == "8":
            print("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()
