from app.config.db import get_connection


# LISTAR CLIENTES
def listar_clientes():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nombre, cedula, fecha_ingreso, puntos, saldo
            FROM cliente
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "id": str(r[0]),
                "nombre": r[1],
                "cedula": r[2],
                "fecha_ingreso": str(r[3]),
                "puntos": r[4],
                "saldo": r[5]
            }
            for r in rows
        ]

    except Exception as e:
        return {"error": str(e)}


# REGISTRAR CLIENTE
def registrar_cliente(data):
    if not data.get("nombre") or not data.get("cedula"):
        return {"error": "Campos obligatorios faltantes"}

    try:
        conn = get_connection()
        cur = conn.cursor()

        referido_por = data.get("referido_por")

        cur.execute("""
            INSERT INTO cliente (nombre, cedula, fecha_ingreso, puntos, saldo, referido_por)
            VALUES (%s, %s, %s, 0, %s, %s) RETURNING id
        """, (
            data["nombre"],
            data["cedula"],
            data["fecha_ingreso"],
            data["saldo"],
            referido_por
        ))

        cliente_id = cur.fetchone()[0]

        if referido_por:
            cur.execute("UPDATE cliente SET puntos = puntos + 1 WHERE id = %s", (referido_por,))

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Cliente registrado", "id": str(cliente_id)}

    except Exception as e:
        return {"error": str(e)}


# VER HISTORIAL DE COMPRAS
def ver_historial(cliente_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, cliente_id, video_isan, tipo, fecha, monto
            FROM alquiler_compra
            WHERE cliente_id = %s
        """, (cliente_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "id": str(r[0]),
                "cliente_id": str(r[1]),
                "video_isan": r[2],
                "tipo": r[3],
                "fecha": str(r[4]),
                "monto": r[5]
            }
            for r in rows
        ]

    except Exception as e:
        return {"error": str(e)}


# ACTUALIZAR PUNTOS
def actualizar_puntos(cliente_id, puntos_a_sumar):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE cliente SET puntos = puntos + %s
            WHERE id = %s RETURNING puntos
        """, (puntos_a_sumar, cliente_id))

        puntos_totales = cur.fetchone()[0]

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

    except Exception as e:
        return {"error": str(e)}


# ALQUILAR O COMPRAR VIDEO
def alquilar_comprar(data):
    if not data.get("cliente_id") or not data.get("video_isan") or not data.get("tipo"):
        return {"error": "Campos obligatorios faltantes"}

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT saldo, puntos FROM cliente WHERE id = %s", (data["cliente_id"],))
        cliente = cur.fetchone()

        if not cliente:
            return {"error": "Cliente no encontrado"}

        saldo = cliente[0]
        puntos = cliente[1]
        monto = data["monto"]

        if saldo < monto:
            return {"error": "Saldo insuficiente"}

        cur.execute("""
            INSERT INTO alquiler_compra (cliente_id, video_isan, tipo, monto)
            VALUES (%s, %s, %s, %s)
        """, (
            data["cliente_id"],
            data["video_isan"],
            data["tipo"],
            monto
        ))

        cur.execute("UPDATE cliente SET saldo = saldo - %s WHERE id = %s", (monto, data["cliente_id"]))

        puntos_a_sumar = 2 if data["tipo"] == "compra" else 1
        nuevos_puntos = puntos + puntos_a_sumar

        video_regalo = False
        if nuevos_puntos >= 20:
            nuevos_puntos = 0
            video_regalo = True

        cur.execute("UPDATE cliente SET puntos = %s WHERE id = %s", (nuevos_puntos, data["cliente_id"]))

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": f"{'Compra' if data['tipo'] == 'compra' else 'Alquiler'} realizado exitosamente",
            "puntos": nuevos_puntos,
            "video_regalo": video_regalo
        }

    except Exception as e:
        return {"error": str(e)}


# CALIFICAR VIDEO
def calificar_video(data):
    if not data.get("cliente_id") or not data.get("video_isan") or not data.get("valor"):
        return {"error": "Campos obligatorios faltantes"}

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO calificacion (cliente_id, video_isan, valor, fecha)
            VALUES (%s, %s, %s, CURRENT_DATE)
        """, (
            data["cliente_id"],
            data["video_isan"],
            data["valor"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Calificación registrada"}

    except Exception as e:
        return {"error": str(e)}


# RECARGAR SALDO (SIMULACIÓN DE PAGO)
def recargar_saldo(data):
    if not data.get("cliente_id") or not data.get("monto"):
        return {"error": "Campos obligatorios faltantes"}

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE cliente SET saldo = saldo + %s
            WHERE id = %s RETURNING saldo
        """, (data["monto"], data["cliente_id"]))

        nuevo_saldo = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": "Pago exitoso",
            "saldo_actual": nuevo_saldo
        }

    except Exception as e:
        return {"error": str(e)}


        #ALO ALO ALO