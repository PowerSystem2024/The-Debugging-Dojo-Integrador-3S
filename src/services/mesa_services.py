class MesaService:
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_mesas_disponibles(self):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero, capacidad 
                        FROM mesas 
                        WHERE disponible = TRUE
                        ORDER BY capacidad, numero
                    """)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener mesas: {e}")
            return []

    def asignar_mesa_automatica(self, personas):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero, capacidad 
                        FROM mesas 
                        WHERE disponible = TRUE AND capacidad >= %s
                        ORDER BY capacidad, numero
                        LIMIT 1
                    """, (personas,))
                    mesa = cursor.fetchone()
                    if mesa:
                        numero, capacidad = mesa
                        cursor.execute(
                            "UPDATE mesas SET disponible = FALSE WHERE numero = %s",
                            (numero,)
                        )
                        conn.commit()
                        return {
                            'numero': numero,
                            'capacidad': capacidad,
                            'mensaje': f"Mesa {numero} asignada (para {capacidad} personas)"
                        }
                    return {
                        'error': "No hay mesas disponibles para ese tamaño de grupo"
                    }
        except Exception as e:
            print(f"Error al asignar mesa: {e}")
            return {'error': str(e)}
