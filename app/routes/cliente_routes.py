from flask import Blueprint, request, jsonify
from app.controllers.cliente_controller import *

cliente_bp = Blueprint('cliente_bp', __name__)

# 1. LISTAR de los cliente
@cliente_bp.route('/clientes', methods=['GET'])
def listar():
    data = listar_clientes()
    return jsonify({
        "status": "success",
        "data": data
    })


# 2. REGISTRo cliente
@cliente_bp.route('/clientes', methods=['POST'])
def registrar():
    data = request.json
    resultado = registrar_cliente(data)
    return jsonify(resultado)


# 3. Visualizar HISTORIAL
@cliente_bp.route('/clientes/<int:cliente_id>/historial', methods=['GET'])
def historial(cliente_id):
    data = ver_historial(cliente_id)
    return jsonify({
        "status": "success",
        "data": data
    })


# 4. ACTUALIZAR PUNTOS
@cliente_bp.route('/clientes/<int:cliente_id>/puntos', methods=['PUT'])
def puntos(cliente_id):
    data = request.json
    resultado = actualizar_puntos(cliente_id, data.get("puntos"))
    return jsonify(resultado)

# 5. ALQUILAR O COMPRAR
@cliente_bp.route('/clientes/alquilar-comprar', methods=['POST'])
def alquilar_comprar_video():
    data = request.json
    resultado = alquilar_comprar(data)
    return jsonify(resultado)

# 6. CALIFICAR VIDEO
@cliente_bp.route('/clientes/calificar', methods=['POST'])
def calificar():
    data = request.json
    resultado = calificar_video(data)
    return jsonify(resultado)

# 7. PAGAR (SIMULACIÓN)
@cliente_bp.route('/clientes/pagar', methods=['POST'])
def pagar():
    data = request.json
    resultado = recargar_saldo(data)
    return jsonify(resultado)