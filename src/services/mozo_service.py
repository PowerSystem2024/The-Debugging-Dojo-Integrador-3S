from src.database.connection import DatabaseConnection
import random


class MozoService:
    def __init__(self):
        self.db = DatabaseConnection()

    def asignar_mozo(self):
        """Asigna un mozo disponible de forma aleatoria y lo marca como no disponible"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, nombre FROM mozos WHERE disponible = TRUE"
                    )
                    mozos = cursor.fetchall()

                    if mozos:
                        mozo = random.choice(mozos)
                        # Actualizar estado
                        cursor.execute(
                            "UPDATE mozos SET disponible = FALSE WHERE id = %s",
                            (mozo[0],)
                        )
                        conn.commit()
                        return {"id": mozo[0], "nombre": mozo[1]}
                    else:
                        print("No hay mozos disponibles.")
                        return None
        except Exception as e:
            print(f"Error al asignar mozo: {e}")
            return None

    def liberar_mozo(self, mozo_id):
        """Libera un mozo específico, marcándolo como disponible nuevamente"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE mozos SET disponible = TRUE WHERE id = %s",
                        (mozo_id,)
                    )
                    conn.commit()
                    print(f"Mozo con ID {mozo_id} liberado.")
                    return True
        except Exception as e:
            print(f"Error al liberar mozo: {e}")
            return False

    def liberar_todos_los_mozos(self):
        """Libera todos los mozos, marcándolos como disponibles"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE mozos SET disponible = TRUE")
                    conn.commit()
                    print("Todos los mozos han sido liberados.")
                    return True
        except Exception as e:
            print(f"Error al liberar mozos: {e}")
            return False
