from app.config.db import get_connection

class Categoria:

    @staticmethod
    def obtener_todas():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM categoria")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [{"id": r[0], "nombre": r[1]} for r in rows]
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def registrar(nombre):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO categoria (nombre)
                VALUES (%s) RETURNING id
            """, (nombre,))
            result = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Categoría registrada", "id": result}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def agregar_a_video(video_isan, categoria_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM video_categoria WHERE video_isan = %s
            """, (video_isan,))
            count = cur.fetchone()[0]
            if count >= 3:
                return {"error": "Un video puede tener máximo 3 categorías"}
            cur.execute("""
                INSERT INTO video_categoria (video_isan, categoria_id)
                VALUES (%s, %s)
            """, (video_isan, categoria_id))
            conn.commit()
            cur.close()
            conn.close()
            return {"message": "Categoría agregada al video"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def videos_por_categoria(categoria_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT v.isan, v.titulo, v.anio, v.duracion
                FROM video v
                JOIN video_categoria vc ON v.isan = vc.video_isan
                WHERE vc.categoria_id = %s
            """, (categoria_id,))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                {
                    "isan": r[0],
                    "titulo": r[1],
                    "anio": r[2],
                    "duracion": r[3]
                }
                for r in rows
            ]
        except Exception as e:
            return {"error": str(e)}