from app.config.db import get_connection

# LISTAR VIDEOS
def listar_videos():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                v.isan,
                v.titulo_original,
                v.anio,
                v.duracion,
                c.tipo as clasificacion
            FROM video v
            JOIN clasificacion c ON v.clasificacion_id = c.id
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


# CREAR VIDEO
def crear_video(data):
    if not data.get("isan") or not data.get("titulo_original"):
        return {"error": "Campos obligatorios faltantes"}

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO video (isan, titulo_original, anio, duracion)
        VALUES (%s, %s, %s, %s)
    """, (
        data["isan"],
        data["titulo_original"],
        data["anio"],
        data["duracion"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Video creado"}


# EDITAR VIDEO
def editar_video(isan, data):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
    UPDATE video
    SET
        titulo_original = %s,
        anio = %s,
        duracion = %s
    WHERE isan = %s
    """

    cur.execute(sql, (
        data["titulo_original"],
        data["anio"],
        data["duracion"],
        isan
    ))

    conn.commit()

    cur.close()
    conn.close()

    return True


# ELIMINAR VIDEO
def eliminar_video(isan):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM video WHERE isan = %s",
        (isan,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return True


# BUSCAR VIDEO
def buscar_video(texto):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM video
        WHERE titulo_original ILIKE %s
    """, (f"%{texto}%",))

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return resultados


