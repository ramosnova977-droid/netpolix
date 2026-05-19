from app.config.db import get_connection

class Cliente:
    def __init__(self, nombre, cedula, fecha_ingreso, puntos=0, saldo=0.0, referido_id=None):
        self.nombre = nombre
        self.cedula = cedula
        self.fecha_ingreso = fecha_ingreso
        self.puntos = puntos
        self.saldo = saldo
        self.referido_id = referido_id

    @staticmethod
    def registrar(nombre, cedula, fecha_ingreso, saldo, referido_id=None):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO cliente (nombre, cedula, fecha_ingreso, puntos, saldo, referido_id)
               VALUES (%s, %s, %s, 0, %s, %s) RETURNING id""",
            (nombre, cedula, fecha_ingreso, saldo, referido_id)
        )
        cliente_id = cur.fetchone()[0]
        
        # referido 1 point
        if referido_id:
            cur.execute("UPDATE cliente SET puntos = puntos + 1 WHERE id = %s", (referido_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        return cliente_id

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, cedula, fecha_ingreso, puntos, saldo FROM cliente")
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return clientes

    @staticmethod
    def obtener_por_id(cliente_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, cedula, fecha_ingreso, puntos, saldo FROM cliente WHERE id = %s", (cliente_id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        return cliente

    @staticmethod
    def actualizar_puntos(cliente_id, puntos_a_sumar):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE cliente SET puntos = puntos + %s WHERE id = %s RETURNING puntos", (puntos_a_sumar, cliente_id))
        puntos_totales = cur.fetchone()[0]
        
        # 20 puntos se regala un video
        if puntos_totales >= 20:
            cur.execute("UPDATE cliente SET puntos = 0 WHERE id = %s", (cliente_id,))
            conn.commit()
            cur.close()
            conn.close()
            return {"puntos": 0, "video_regalo": True}
        
        conn.commit()
        cur.close()
        conn.close()
        return {"puntos": puntos_totales, "video_regalo": False}