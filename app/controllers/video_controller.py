from app.models.video import Video
from app.models.calificacion import Calificacion
from app.models.categoria import Categoria

def registrar_video(data):
    if not data.get("isan") or not data.get("titulo") or not data.get("anio") or not data.get("duracion"):
        return {"error": "Campos obligatorios faltantes"}
    return Video.registrar(
        data["isan"], data["titulo"], data["anio"],
        data["duracion"], data.get("clasificacion_id")
    )

def listar_videos():
    return Video.obtener_todos()

def detalle_video(isan):
    video = Video.obtener_por_isan(isan)
    if "error" in video:
        return video
    calificaciones = Calificacion.obtener_calificaciones(isan)
    video["calificaciones"] = calificaciones
    return video

def registrar_serie(data):
    if not data.get("titulo") or not data.get("temporada"):
        return {"error": "Campos obligatorios faltantes"}
    return Video.registrar_serie(data["titulo"], data["temporada"])

def registrar_coleccion(data):
    if not data.get("isan") or not data.get("titulo") or not data.get("volumen"):
        return {"error": "Campos obligatorios faltantes"}
    return Video.registrar_coleccion(data["isan"], data["titulo"], data["volumen"])

def agregar_persona(data):
    if not data.get("video_isan") or not data.get("nombre") or not data.get("rol"):
        return {"error": "Campos obligatorios faltantes"}
    roles_validos = ["actor", "productor", "director"]
    if data["rol"] not in roles_validos:
        return {"error": "Rol inválido. Debe ser actor, productor o director"}
    return Video.agregar_persona(
        data["video_isan"], data["nombre"],
        data.get("fecha_nacimiento"), data["rol"]
    )

def agregar_idioma(data):
    if not data.get("video_isan") or not data.get("idioma") or not data.get("tipo"):
        return {"error": "Campos obligatorios faltantes"}
    tipos_validos = ["original", "subtitulo", "doblaje"]
    if data["tipo"] not in tipos_validos:
        return {"error": "Tipo inválido. Debe ser original, subtitulo o doblaje"}
    return Video.agregar_idioma(data["video_isan"], data["idioma"], data["tipo"])

def listar_categorias():
    return Categoria.obtener_todas()

def registrar_categoria(data):
    if not data.get("nombre"):
        return {"error": "Nombre es obligatorio"}
    return Categoria.registrar(data["nombre"])

def agregar_categoria_video(data):
    if not data.get("video_isan") or not data.get("categoria_id"):
        return {"error": "Campos obligatorios faltantes"}
    return Categoria.agregar_a_video(data["video_isan"], data["categoria_id"])

def videos_por_categoria(categoria_id):
    return Categoria.videos_por_categoria(categoria_id)