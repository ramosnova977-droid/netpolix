from flask import Blueprint, request, jsonify
from app.controllers.venta_controller import comprar_video, alquilar_video, productos_mas_vendidos

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.route('/ventas/comprar', methods=['POST'])
def comprar():
    data = request.json
    resultado = comprar_video(data)
    return jsonify(resultado)

@venta_bp.route('/ventas/alquilar', methods=['POST'])
def alquilar():
    data = request.json
    resultado = alquilar_video(data)
    return jsonify(resultado)

@venta_bp.route('/ventas/mas-vendidos', methods=['GET'])
def mas_vendidos():
    resultado = productos_mas_vendidos()
    return jsonify(resultado)