# src/services/clientes_service.py
from src.database.connection import DatabaseConnection  # Importa la conexión desde el proyecto principal

class ClienteService:
    def __init__(self):
        self.db = DatabaseConnection()

    def registrar_cliente(self, nombre, telefono):
        """Registra un nuevo cliente en la base de datos"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s) RETURNING id",
                        (nombre, telefono)
                    )
                    return cursor.fetchone()[0]  # Retorna el ID del nuevo cliente
        except Exception as e:
            print(f"Error al registrar cliente: {e}")
            return None

    def listar_clientes(self):
        """Lista todos los clientes registrados"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre, telefono FROM clientes")
                    columns = [desc[0] for desc in cursor.description]
                    return [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            return []