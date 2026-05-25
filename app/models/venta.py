from app.config.db import get_connection

PRECIO_VENTA = 10
PRECIO_ALQUILER = 5
PUNTOS_PARA_REGALO = 20

class Venta:

    @staticmethod
    def comprar(cliente_id, video_isan, envio_dvd=False):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT saldo, puntos FROM cliente WHERE id = %s", (cliente_id,))
            cliente = cur.fetchone()

            if not cliente:
                return {"error": "Cliente no encontrado"}

            saldo, puntos = cliente

            if saldo < PRECIO_VENTA:
                return {"error": "Saldo insuficiente"}

            # Registrar venta
            cur.execute("""
                INSERT INTO venta (cliente_id, video_isan, precio, envio_dvd)
                VALUES (%s, %s, %s, %s)
            """, (cliente_id, video_isan, PRECIO_VENTA, envio_dvd))

            # Descontar saldo
            cur.execute("UPDATE cliente SET saldo = saldo - %s WHERE id = %s", (PRECIO_VENTA, cliente_id))

            # Sumar 2 puntos por compra
            nuevos_puntos = puntos + 2
            video_regalo = False
            if nuevos_puntos >= PUNTOS_PARA_REGALO:
                nuevos_puntos = 0
                video_regalo = True

            cur.execute("UPDATE cliente SET puntos = %s WHERE id = %s", (nuevos_puntos, cliente_id))

            conn.commit()
            cur.close()
            conn.close()

            return {
                "message": "Compra exitosa",
                "puntos": nuevos_puntos,
                "video_regalo": video_regalo,
                "envio_dvd": envio_dvd
            }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def alquilar(cliente_id, video_isan, tipo_alquiler):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT saldo, puntos FROM cliente WHERE id = %s", (cliente_id,))
            cliente = cur.fetchone()

            if not cliente:
                return {"error": "Cliente no encontrado"}

            saldo, puntos = cliente

            if saldo < PRECIO_ALQUILER:
                return {"error": "Saldo insuficiente"}

            # Registrar alquiler
            cur.execute("""
                INSERT INTO alquiler (cliente_id, video_isan, tipo_alquiler, fecha)
                VALUES (%s, %s, %s, CURRENT_DATE)
            """, (cliente_id, video_isan, tipo_alquiler))

            # Descontar saldo
            cur.execute("UPDATE cliente SET saldo = saldo - %s WHERE id = %s", (PRECIO_ALQUILER, cliente_id))

            # Sumar 1 punto por alquiler
            nuevos_puntos = puntos + 1
            video_regalo = False
            if nuevos_puntos >= PUNTOS_PARA_REGALO:
                nuevos_puntos = 0
                video_regalo = True

            cur.execute("UPDATE cliente SET puntos = %s WHERE id = %s", (nuevos_puntos, cliente_id))

            conn.commit()
            cur.close()
            conn.close()

            return {
                "message": "Alquiler exitoso",
                "puntos": nuevos_puntos,
                "video_regalo": video_regalo
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
                "mas_vendidos": [{"video_isan": r[0], "total_ventas": r[1]} for r in ventas],
                "mas_alquilados": [{"video_isan": r[0], "total_alquileres": r[1]} for r in alquileres]
            }

        except Exception as e:
            return {"error": str(e)}