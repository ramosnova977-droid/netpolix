from flask import Blueprint, request, jsonify
from app.controllers.calificacion_controller import calificar, obtener_calificaciones

calificacion_bp = Blueprint('calificacion_bp', __name__)

@calificacion_bp.route('/calificaciones', methods=['POST'])
def nueva_calificacion():
    data = request.json
    resultado = calificar(data)
    return jsonify(resultado)

@calificacion_bp.route('/calificaciones/<string:video_isan>', methods=['GET'])
def ver_calificaciones(video_isan):
    resultado = obtener_calificaciones(video_isan)
    return jsonify(resultado)


#alo alo alo