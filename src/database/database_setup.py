# src/database/database_setup.py
from src.database.connection import DatabaseConnection

class DatabaseSetup:
    def __init__(self):
        self.db = DatabaseConnection()

    def check_database_exists(self):
        """Verifica si las tablas necesarias existen"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' 
                            AND table_name = 'clientes'
                        )
                    """)
                    return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al verificar base de datos: {e}")
            return False

    def create_database_structure(self):
        """Crea toda la estructura de la base de datos"""
        sql_commands = [
            # Secuencia y tabla de clientes
            """
            CREATE SEQUENCE IF NOT EXISTS clientes_id_seq
                START WITH 1
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1
            """,
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER NOT NULL DEFAULT nextval('clientes_id_seq'),
                nombre VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            """,
            # Secuencia y tabla de mozos
            """
            CREATE SEQUENCE IF NOT EXISTS mozos_id_seq
                START WITH 1
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1
            """,
            """
            CREATE TABLE IF NOT EXISTS mozos (
                id INTEGER NOT NULL DEFAULT nextval('mozos_id_seq'),
                nombre VARCHAR(100) NOT NULL,
                disponible BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (id)
            """,
            # Secuencia y tabla de menu_items
            """
            CREATE SEQUENCE IF NOT EXISTS menu_items_id_seq
                START WITH 1
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1
            """,
            """
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER NOT NULL DEFAULT nextval('menu_items_id_seq'),
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                precio NUMERIC(10,2) NOT NULL,
                categoria VARCHAR(50),
                PRIMARY KEY (id)
            )
            """,
            # Secuencia y tabla de mesas
            """
            CREATE SEQUENCE IF NOT EXISTS mesas_id_seq
                START WITH 1
                INCREMENT BY 1
                NO MINVALUE
                NO MAXVALUE
                CACHE 1
            """,
            """
            CREATE TABLE IF NOT EXISTS mesas (
                id INTEGER NOT NULL DEFAULT nextval('mesas_id_seq'),
                numero INTEGER NOT NULL UNIQUE,
                capacidad INTEGER NOT NULL,
                disponible BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (id)
            )
            """
        ]

        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    for command in sql_commands:
                        cursor.execute(command)
                    conn.commit()
                print("✅ Estructura de base de datos verificada/creada correctamente")
                return True
        except Exception as e:
            print(f"❌ Error al crear estructura de base de datos: {e}")
            return False

    def insert_initial_data(self):
        """Inserta datos iniciales esenciales"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insertar mesas básicas si no existen
                    cursor.execute("SELECT COUNT(*) FROM mesas")
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("""
                            INSERT INTO mesas (numero, capacidad) 
                            VALUES 
                                (1, 2), (2, 2), (3, 4), (4, 4), (5, 4),
                                (6, 6), (7, 6), (8, 8), (9, 8), (10, 10)
                        """)
                        conn.commit()
                        print("✅ Mesas iniciales creadas correctamente")
                    return True
        except Exception as e:
            print(f"❌ Error al insertar datos iniciales: {e}")
            return False

def initialize_database():
    """Función principal para inicializar la base de datos"""
    db_setup = DatabaseSetup()
    if not db_setup.check_database_exists():
        print("⚙️ Configurando base de datos por primera vez...")
        if db_setup.create_database_structure():
            db_setup.insert_initial_data()
