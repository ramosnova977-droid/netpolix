from app.models.venta import Venta

def comprar_video(data):
    if not data.get("cliente_id") or not data.get("video_isan"):
        return {"error": "Campos obligatorios faltantes"}
    envio_dvd = data.get("envio_dvd", False)
    return Venta.comprar(data["cliente_id"], data["video_isan"], envio_dvd)

def alquilar_video(data):
    if not data.get("cliente_id") or not data.get("video_isan") or not data.get("tipo_alquiler"):
        return {"error": "Campos obligatorios faltantes"}
    return Venta.alquilar(data["cliente_id"], data["video_isan"], data["tipo_alquiler"])

def productos_mas_vendidos():
    return Venta.mas_vendidos()