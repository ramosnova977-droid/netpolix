from flask import Blueprint, jsonify
from app.controllers.gerente_controller import resumen_general, productos_mas_vendidos, clientes_top

gerente_bp = Blueprint('gerente_bp', __name__)

@gerente_bp.route('/gerente/resumen', methods=['GET'])
def resumen():
    return jsonify(resumen_general())

@gerente_bp.route('/gerente/mas-vendidos', methods=['GET'])
def mas_vendidos():
    return jsonify(productos_mas_vendidos())

@gerente_bp.route('/gerente/clientes-top', methods=['GET'])
def top_clientes():
    return jsonify(clientes_top())