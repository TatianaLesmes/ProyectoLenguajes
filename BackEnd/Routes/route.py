# routes.py
from flask import Blueprint, jsonify, request
from Controllers.MODIFICACION2 import get_plate_info
import os

routes_bp = Blueprint('routes', __name__)

# Obtener la ruta del archivo Excel desde una variable de entorno o configuración
EXCEL_PATH = os.getenv('EXCEL_PATH', 'data/matriculas_data.xlsx')

@routes_bp.route('/validate-plate', methods=['POST'])
def validate_plate_route():
    try:
        data = request.get_json()
        
        # Verificar que el cuerpo de la solicitud no sea None
        if not data:
            return jsonify({
                'success': False,
                'message': 'El cuerpo de la solicitud es requerido'
            }), 400
        
        # Verificar que todos los campos necesarios estén presentes
        required_fields = ['placa', 'color_fondo', 'color_letra']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Los siguientes campos son requeridos: {", ".join(missing_fields)}'
            }), 400

        # Validar que los campos no estén vacíos
        empty_fields = [field for field in required_fields if not str(data[field]).strip()]
        if empty_fields:
            return jsonify({
                'success': False,
                'message': f'Los siguientes campos no pueden estar vacíos: {", ".join(empty_fields)}'
            }), 400

        # Llamar a la función de validación con la ruta del Excel
        result = get_plate_info(
            data['placa'],
            data['color_fondo'],
            data['color_letra'],
            EXCEL_PATH
        )
        
        # Determinar el código de estado HTTP basado en el resultado
        status_code = 200 if result['success'] else 404 if "no encontrada" in result['message'] else 400
        
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        }), 500