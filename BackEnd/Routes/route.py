from flask import Blueprint, jsonify, request
from Controllers.Expresiones_Regulares import sumar, restar

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