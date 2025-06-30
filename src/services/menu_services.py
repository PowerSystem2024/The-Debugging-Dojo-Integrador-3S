from FinalPython.src.database.connection import DatabaseConnection


class MenuService:
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_menu(self):
        """Obtiene todos los items del menú ordenados por categoría y nombre"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, nombre, descripcion, precio, categoria 
                        FROM menu_items 
                        ORDER BY categoria, nombre
                    """)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener menú: {e}")
            return []

    def agregar_item(self, nombre, descripcion, precio, categoria):
        """Agrega un nuevo ítem al menú"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO menu_items 
                        (nombre, descripcion, precio, categoria) 
                        VALUES (%s, %s, %s, %s) RETURNING id""",
                        (nombre, descripcion, precio, categoria)
                    )
                    return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al agregar ítem: {e}")
            return None

    def insertar_menu_ejemplo(self):
        """
        Inserta un menú de ejemplo con 10 platos típicos argentinos
        Útil para pruebas o para inicializar la base de datos
        """
        menu_argentino = [
            # Formato: (nombre, descripción, precio, categoría)
            ("Asado", "Corte de carne vacuna asado a las brasas", 4500, "Carnes"),
            ("Empanadas", "Empanadas de carne cortada a cuchillo", 1200, "Entradas"),
            ("Milanesa con papas fritas", "Milanesa de ternera con papas fritas caseras", 3800, "Carnes"),
            ("Locro", "Guiso tradicional a base de maíz, porotos y carne", 3200, "Guisos"),
            ("Humita en chala", "Pasta de maíz fresca cocida en su propia hoja", 2800, "Vegetariano"),
            ("Provoleta", "Queso provolone derretido con orégano y ají molido", 2500, "Entradas"),
            ("Ñoquis", "Ñoquis de papa con salsa fileto o pesto", 2900, "Pastas"),
            ("Choripán", "Chorizo asado en pan francés con chimichurri", 1800, "Sandwiches"),
            ("Flan con dulce de leche", "Postre tradicional con dulce de leche y crema", 2200, "Postres"),
            ("Alfajor", "Alfajor de maicena relleno de dulce de leche", 800, "Postres")
        ]

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insertar todos los items del menú de ejemplo
                    for item in menu_argentino:
                        cursor.execute(
                            """INSERT INTO menu_items 
                            (nombre, descripcion, precio, categoria) 
                            VALUES (%s, %s, %s, %s)""",
                            item
                        )
                    conn.commit()
                    print("✅ Menú argentino de ejemplo insertado correctamente")
                    return True
        except Exception as e:
            print(f"❌ Error al insertar menú de ejemplo: {e}")
            return False