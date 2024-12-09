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
    "pattern": r'^[A-MNPOR-Z]{3}-[0-9]{3}$',
    "forbidden_letters": {'Ñ'},
    "description": "3 letras, guion, 3 números (sin Ñ)"
},
     "Mexico": {
        "pattern": r'^[A-Z]{3}-[0-9]{3}-[A-Z]$',
        "forbidden_letters": {'Ñ'},
        "description": "3 letras, guión, 3 números, guión, 1 letra (sin Ñ)"
    },
    "Honduras": {
        "pattern": r'^[A-Z] [A-Z]{2} [0-9]{4}$',
        "forbidden_letters": {'Q','O','Ñ''U'},
        "description": "3 letras, guión, 3 números, guión, 1 letra (sin Ñ)"
    }
    
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
    # Eliminar guiones para México
    plate = plate.replace('-', '').replace(' ','')
    
    letters = plate[:3]
    number = int(plate[3:6])
    final_letter = plate[6] if len(plate) > 6 else ''
    
    letter_value = sum((ord(c) - ord('A')) * (26 ** (2-i)) for i, c in enumerate(letters))
    
    # Añadir valor de la letra final si existe
    if final_letter:
        letter_value += (ord(final_letter) - ord('A'))
    
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
            country = str(row['País']) if pd.notna(row['País']) else "NA"
            
            # Validar formato según el país
            if not validate_plate_format(plate, country):
                continue
                
            range_start = str(row['Rango_Inicial']).strip().upper() if pd.notna(row['Rango_Inicial']) else "NA"
            range_end = str(row['Rango_Final']).strip().upper() if pd.notna(row['Rango_Final']) else "NA"
            
            range_start_value = alphanumeric_to_number(range_start) if range_start != "NA" else 0
            range_end_value = alphanumeric_to_number(range_end) if range_end != "NA" else float('inf')
            
            if range_start_value <= plate_value <= range_end_value:
                found = True
                
                # Preparar la información de la placa con manejo de valores nulos
                plate_data = {
                    'placa': plate,
                    'pais': country,
                    'departamento': str(row['Departamento']) if pd.notna(row['Departamento']) else "NA",
                    'ciudad': str(row['Ciudad']) if pd.notna(row['Ciudad']) else "NA",
                    'servicio': str(row['Servicio']) if pd.notna(row['Servicio']) else "NA",
                    'color_fondo': str(row['ColorFondo']).strip().lower() if pd.notna(row['ColorFondo']) else "NA",
                    'color_letra': str(row['ColorLetra']).strip().lower() if pd.notna(row['ColorLetra']) else "NA",
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






"""
   
   import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, '..', 'data', 'matriculas_data.xlsx')

def format_matricula(row, columna):
  
    Formatea una matrícula en el formato AAA-000 solo para Colombia
    
    Args:
        row (pd.Series): Fila del DataFrame con información de país y matrícula
        columna (str): Nombre de la columna a formatear ('Rango_Inicial' o 'Rango_Final')
    
    Returns:
        str: Matrícula formateada o sin cambios
   
    # Verificar si el país es Colombia
    if row['País'] == 'Colombia':
        matricula = str(row[columna])
        
        # Verificar si la matrícula tiene al menos 3 caracteres
        if len(matricula) >= 3:
            # Separar los primeros 3 caracteres y el resto
            parte_letras = matricula[:3]
            parte_numeros = matricula[3:]
            
            # Formatear con guión
            return f"{parte_letras}-{parte_numeros}"
    
    # Si no es Colombia o la matrícula es muy corta, devolverla como está
    return str(row[columna])

# Leer el archivo Excel
df = pd.read_excel(csv_path)

 Aplicar el formato a las columnas de Rango_Inicial y Rango_Final
 Usar axis=1 para pasar toda la fila a la función
df['Rango_Inicial'] = df.apply(lambda row: format_matricula(row, 'Rango_Inicial'), axis=1)
df['Rango_Final'] = df.apply(lambda row: format_matricula(row, 'Rango_Final'), axis=1)

# Guardar el DataFrame modificado
df.to_excel(csv_path, index=False)

# Opcional: Mostrar los resultados para verificar
print(df[['País', 'Rango_Inicial', 'Rango_Final']].head())
   
   
   
   
    """









