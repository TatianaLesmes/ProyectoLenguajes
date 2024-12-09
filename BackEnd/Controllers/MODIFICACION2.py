import re
import pandas as pd
import os
from typing import Dict, Optional, Union


# Ejemplo de uso para pruebas

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, '..', 'data', 'matriculas_data.xlsx')
    


# Definir las expresiones regulares por país
PLATE_PATTERNS = {
    "Colombia": {
        "pattern": r'^[A-MNPOR-Z]{3}[0-9]{3}$',
        "forbidden_letters": {'Ñ'},
        "description": "3 letras seguidas de 3 números (sin Ñ)"
    },
    "Mexico": {
        "pattern": r'^[A-Z]-\d{3}-[A-Z]{3}$',  # Ejemplo - ajustar según necesidad
        "forbidden_letters": {"Ñ","O",},
        "description": "Una letra, seguida de un guion, tres números, otro guion, y tres letras"
    },
    # Agregar más países según sea necesario
}

def validate_plate_format(plate: str, country: str) -> bool:
    """
    Valida el formato de la placa según el país especificado
    """
    if country not in PLATE_PATTERNS:
        return False
    
    plate = plate.strip().upper()
    country_rules = PLATE_PATTERNS[country]
    
    # Verificar patrón básico
    if not re.match(country_rules["pattern"], plate):
        return False
    
    # Verificar letras prohibidas
    if any(letter in plate for letter in country_rules["forbidden_letters"]):
        return False
    
    return True

def alphanumeric_to_number(plate: str) -> int:
    """
    Convierte una placa alfanumérica en un valor numérico comparable
    """
    letters = plate[:3]
    number = int(plate[3:])
    letter_value = sum((ord(c) - ord('A')) * (26 ** (2-i)) for i, c in enumerate(letters))
    return letter_value * 1000 + number

def get_plate_info(plate: str, color_fondo: str, color_letra: str, excel_path: str) -> Dict[str, Union[str, bool, dict]]:
    """
    Función principal que procesa la información de la placa y retorna un diccionario
    con toda la información necesaria para la API
    """
    response = {
        "success": False,
        "message": "",
        "data": None
    }
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(excel_path)
        
        # Normalizar inputs
        plate = plate.strip().upper()
        color_fondo = color_fondo.strip().lower()
        color_letra = color_letra.strip().lower()
        
        # Convertir placa a valor numérico
        plate_value = alphanumeric_to_number(plate)
        
        found = False
        for index, row in df.iterrows():
            country = row['País']
            
            # Validar formato según el país
            if not validate_plate_format(plate, country):
                continue
                
            range_start = row['Rango_Inicial'].strip().upper()
            range_end = row['Rango_Final'].strip().upper()
            
            range_start_value = alphanumeric_to_number(range_start)
            range_end_value = alphanumeric_to_number(range_end)
            
            if range_start_value <= plate_value <= range_end_value:
                found = True
                
                # Preparar la información de la placa
                plate_data = {
                    'placa': plate,
                    'pais': country,
                    'departamento': row['Departamento'],
                    'ciudad': row['Ciudad'],
                    'servicio': row['Servicio'],
                    'color_fondo': row['ColorFondo'].strip().lower(),
                    'color_letra': row['ColorLetra'].strip().lower(),
                    'rango': f"{range_start} - {range_end}"
                }
                
                # Verificar coincidencia de colores
                if (plate_data['color_fondo'] == color_fondo and 
                    plate_data['color_letra'] == color_letra):
                    response["success"] = True
                    response["message"] = "Placa encontrada con éxito"
                    response["data"] = plate_data
                else:
                    response["message"] = "Los colores no coinciden con los registrados"
                    response["data"] = {
                        "colores_registrados": {
                            "fondo": plate_data['color_fondo'],
                            "letra": plate_data['color_letra']
                        }
                    }
                break
        
        if not found:
            response["message"] = "Placa no encontrada en los rangos registrados"
            
    except FileNotFoundError:
        response["message"] = f"Error: No se pudo encontrar el archivo de datos"
    except Exception as e:
        response["message"] = f"Error al procesar los datos: {str(e)}"
    
    return response

