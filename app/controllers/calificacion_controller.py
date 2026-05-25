from app.models.calificacion import Calificacion

def calificar(data):
    if not data.get("cliente_id") or not data.get("video_isan") or not data.get("valor"):
        return {"error": "Campos obligatorios faltantes"}
    return Calificacion.calificar(data["cliente_id"], data["video_isan"], data["valor"])

def obtener_calificaciones(video_isan):
    return Calificacion.obtener_calificaciones(video_isan)