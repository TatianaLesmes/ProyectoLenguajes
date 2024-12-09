from flask import Blueprint, jsonify, request
from Controllers.Expresiones_Regulares import sumar, restar, verificar_placa

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/sumar', methods=['POST'])
def route_sumar():
    data = request.get_json()
    result = sumar(data['a'], data['b'])
    return jsonify({'result': result})

@routes_bp.route('/restar', methods=['POST'])
def route_restar():
    data = request.get_json()
    result = restar(data['a'], data['b'])
    return jsonify({'result': result})


    
@routes_bp.route('/verificar_placa', methods=['POST'])
def route_verificar_placa():
    data = request.get_json()
    placa = data.get('placa', '')
    if not placa:
        return jsonify({"error": "Se debe proporcionar una placa."}), 400
    
    # Llamar a la función del controlador para verificar la placa
    result, status_code = verificar_placa(placa)
    
    return jsonify(result), status_code