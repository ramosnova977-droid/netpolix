from app.config.db import get_connection

class Video:

    @staticmethod
    def registrar(isan, titulo, anio, duracion, clasificacion_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO video (isan, titulo, anio, duracion, clasificacion_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING isan
            """, (isan, titulo, anio, duracion, clasificacion_id))
            result = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Video registrado", "isan": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def obtener_todos():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT v.isan, v.titulo, v.anio, v.duracion, c.tipo as clasificacion
                FROM video v
                LEFT JOIN clasificacion c ON v.clasificacion_id = c.id
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                {
                    "isan": r[0],
                    "titulo": r[1],
                    "anio": r[2],
                    "duracion": r[3],
                    "clasificacion": r[4]
                }
                for r in rows
            ]
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def obtener_por_isan(isan):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT v.isan, v.titulo, v.anio, v.duracion, c.tipo as clasificacion
                FROM video v
                LEFT JOIN clasificacion c ON v.clasificacion_id = c.id
                WHERE v.isan = %s
            """, (isan,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            if not row:
                return {"error": "Video no encontrado"}
            return {
                "isan": row[0],
                "titulo": row[1],
                "anio": row[2],
                "duracion": row[3],
                "clasificacion": row[4]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def registrar_serie(titulo, temporada):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO serie (titulo, temporada)
                VALUES (%s, %s) RETURNING id
            """, (titulo, temporada))
            result = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Serie registrada", "id": str(result)}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def registrar_coleccion(isan, titulo, volumen):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO coleccion (isan, titulo, volumen)
                VALUES (%s, %s, %s) RETURNING isan
            """, (isan, titulo, volumen))
            result = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Colección registrada", "isan": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def agregar_persona(video_isan, nombre, fecha_nacimiento, rol):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO persona (nombre, fecha_nacimiento)
                VALUES (%s, %s) RETURNING id
            """, (nombre, fecha_nacimiento))
            persona_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO video_persona (video_isan, persona_id, rol)
                VALUES (%s, %s, %s)
            """, (video_isan, persona_id, rol))
            conn.commit()
            cur.close()
            conn.close()
            return {"message": f"{rol} agregado al video"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def agregar_idioma(video_isan, idioma, tipo):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO video_idioma (video_isan, idioma, tipo)
                VALUES (%s, %s, %s)
            """, (video_isan, idioma, tipo))
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Idioma agregado"}
        except Exception as e:
            return {"error": str(e)}