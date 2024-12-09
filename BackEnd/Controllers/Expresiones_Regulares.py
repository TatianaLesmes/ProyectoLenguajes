import re
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(current_dir, '..', 'data', 'matriculas_data.xlsx')

def validate_plate(plate):
    """
    Valida que la placa tenga el formato correcto:
    - 3 letras seguidas de 3 números
    - No acepta las letras Ñ, Q, O
    """
    # Convertir a mayúsculas y eliminar espacios
    plate = plate.strip().upper()
    
    # Patrón regex corregido que acepta 3 letras (excluyendo Ñ, Q, O) seguidas de 3 números
    pattern = r'^[A-P-N-Z]{3}[0-9]{3}$'
    
    if not re.match(pattern, plate):
        return False
    
    # Verificar que no contenga las letras prohibidas
    forbidden_letters = {'Ñ', 'Q', 'O'}
    if any(letter in plate[:3] for letter in forbidden_letters):
        return False
        
    return True

def alphanumeric_to_number(plate):
    """Convierte una placa alfanumérica como AAA000 en un valor comparable numéricamente."""
    letters = plate[:3]  # Tres primeras letras
    number = int(plate[3:])  # Los últimos tres dígitos como número
    
    # Convierte las letras a un valor numérico basado en su posición en el alfabeto
    letter_value = sum((ord(c) - ord('A')) * (26 ** (2-i)) for i, c in enumerate(letters))
    
    return letter_value * 1000 + number

def process_plate_data(plate, color_fondo_input, color_letra_input, csv_path):
    # Validar formato de la placa
    if not validate_plate(plate):
        print("Error: Formato de placa inválido. Debe contener 3 letras seguidas de 3 números.")
        print("Las letras Ñ, Q y O no están permitidas.")
        return
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(csv_path)
        
        # Normaliza la placa (sin espacios, todo en mayúsculas)
        plate = plate.strip().upper()
        
        # Convierte la placa a su valor numérico
        plate_value = alphanumeric_to_number(plate)
        
        found = False
        # Buscar la fila que contiene la placa
        for index, row in df.iterrows():
            # Normaliza los rangos (sin espacios, todo en mayúsculas)
            range_start = row['Rango_Inicial'].strip().upper()
            range_end = row['Rango_Final'].strip().upper()
            
            # Convierte los rangos a sus valores numéricos
            range_start_value = alphanumeric_to_number(range_start)
            range_end_value = alphanumeric_to_number(range_end)
            
            # Verificamos si la placa está dentro del rango
            if range_start_value <= plate_value <= range_end_value:
                found = True
                # Extraer información de la fila
                result = {
                    'País': row['País'],
                    'Departamento': row['Departamento'],
                    'Ciudad': row['Ciudad'],
                    'Servicio': row['Servicio'],
                    'Color de fondo': row['ColorFondo'].strip().lower(),
                    'Color de letra': row['ColorLetra'].strip().lower(),
                    'Rango': f"{range_start} - {range_end}",
                    'Placa': plate
                }
                
                # Validar si los colores corresponden
                if (result['Color de fondo'] == color_fondo_input.strip().lower() and
                    result['Color de letra'] == color_letra_input.strip().lower()):
                    print("\nInformación de la placa:")
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    print("\nError: Los colores ingresados no coinciden con los registrados para esta placa.")
                    print(f"Colores registrados: Fondo {result['Color de fondo']}, Letra {result['Color de letra']}")
                break
        
        if not found:
            print("\nError: Placa no encontrada en los rangos registrados.")
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo Excel en la ruta: {csv_path}")
    except Exception as e:
        print(f"Error al procesar los datos: {str(e)}")


# Llamada a la función con las entradas
plate_input = "AGK498"  # Placa a buscar
color_fondo_input = "Amarillo"  # Color de fondo ingresado por el usuario
color_letra_input = "Negro"  # Color de letra ingresado por el usuario

process_plate_data(plate_input, color_fondo_input, color_letra_input, csv_path)
