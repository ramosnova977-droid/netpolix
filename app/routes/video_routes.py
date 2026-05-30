from flask import Blueprint, request, jsonify
from app.controllers.video_controller import (
    registrar_video, listar_videos, detalle_video,
    registrar_serie, registrar_coleccion, agregar_persona,
    agregar_idioma, listar_categorias, registrar_categoria,
    agregar_categoria_video, videos_por_categoria
)

video_bp = Blueprint('video_bp', __name__)

@video_bp.route('/videos', methods=['GET'])
def listar():
    return jsonify(listar_videos())

@video_bp.route('/videos', methods=['POST'])
def registrar():
    data = request.json
    return jsonify(registrar_video(data))

@video_bp.route('/videos/<string:isan>', methods=['GET'])
def detalle(isan):
    return jsonify(detalle_video(isan))

@video_bp.route('/videos/series', methods=['POST'])
def serie():
    data = request.json
    return jsonify(registrar_serie(data))

@video_bp.route('/videos/colecciones', methods=['POST'])
def coleccion():
    data = request.json
    return jsonify(registrar_coleccion(data))

@video_bp.route('/videos/personas', methods=['POST'])
def persona():
    data = request.json
    return jsonify(agregar_persona(data))

@video_bp.route('/videos/idiomas', methods=['POST'])
def idioma():
    data = request.json
    return jsonify(agregar_idioma(data))

@video_bp.route('/categorias', methods=['GET'])
def categorias():
    return jsonify(listar_categorias())

@video_bp.route('/categorias', methods=['POST'])
def nueva_categoria():
    data = request.json
    return jsonify(registrar_categoria(data))

@video_bp.route('/categorias/video', methods=['POST'])
def categoria_video():
    data = request.json
    return jsonify(agregar_categoria_video(data))

@video_bp.route('/categorias/<int:categoria_id>/videos', methods=['GET'])
def videos_categoria(categoria_id):
    return jsonify(videos_por_categoria(categoria_id))