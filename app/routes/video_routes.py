#ROUTES (ENDPOINTS API)
from flask import Blueprint, request, jsonify
from app.controllers.video_controller import *

video_bp = Blueprint('video_bp', __name__)

# 1. LISTAR
@video_bp.route('/videos', methods=['GET'])
def listar():
    data = listar_videos()
    return jsonify({
        "status": "success",
        "data": data
    })


# 2. CREAR
@video_bp.route('/videos', methods=['POST'])
def crear():
    data = request.json
    crear_video(data)
    return jsonify({"message": "Video creado"})


# 3. EDITAR
@video_bp.route('/videos/<isan>', methods=['PUT'])
def editar(isan):
    data = request.json
    editar_video(isan, data)
    return jsonify({"message": "Video actualizado"})

    
# 4. ELIMINAR
@video_bp.route('/videos/<isan>', methods=['DELETE'])
def eliminar(isan):
    eliminar_video(isan)
    return jsonify({"message": "Video eliminado"})


# 5. BUSCAR
@video_bp.route('/videos/buscar', methods=['GET'])
def buscar():
    texto = request.args.get('q')
    return jsonify(buscar_video(texto))