from app.config.db import get_connection

class Gerente:

    @staticmethod
    def resumen():
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM cliente")
            total_clientes = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM video")
            total_videos = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM venta")
            total_ventas = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM alquiler")
            total_alquileres = cur.fetchone()[0]

            cur.execute("SELECT COALESCE(SUM(precio), 0) FROM venta")
            ingresos_ventas = cur.fetchone()[0]

            ingresos_alquileres = total_alquileres * 3.5

            cur.close()
            conn.close()

            return {
                "total_clientes": total_clientes,
                "total_videos": total_videos,
                "total_ventas": total_ventas,
                "total_alquileres": total_alquileres,
                "ingresos_ventas": float(ingresos_ventas),
                "ingresos_alquileres": ingresos_alquileres,
                "ingresos_totales": float(ingresos_ventas) + ingresos_alquileres
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def mas_vendidos():
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT video_isan, COUNT(*) as total
                FROM venta
                GROUP BY video_isan
                ORDER BY total DESC
                LIMIT 10
            """)
            ventas = cur.fetchall()

            cur.execute("""
                SELECT video_isan, COUNT(*) as total
                FROM alquiler
                GROUP BY video_isan
                ORDER BY total DESC
                LIMIT 10
            """)
            alquileres = cur.fetchall()

            cur.close()
            conn.close()

            return {
                "mas_vendidos": [{"video_isan": r[0], "total": r[1]} for r in ventas],
                "mas_alquilados": [{"video_isan": r[0], "total": r[1]} for r in alquileres]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def clientes_con_mas_puntos():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, cedula, puntos, saldo
                FROM cliente
                ORDER BY puntos DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                {
                    "id": str(r[0]),
                    "nombre": r[1],
                    "cedula": r[2],
                    "puntos": r[3],
                    "saldo": float(r[4])
                }
                for r in rows
            ]
        except Exception as e:
            return {"error": str(e)}