import re
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

# Definir las provincias y sus respectivas letras
provincias = {
    'Azuay': 'A', 'Bolívar': 'B', 'Carchi': 'C', 'Esmeraldas': 'E', 'Guayas': 'G', 'Chimborazo': 'H',
    'Imbabura': 'I', 'Santo Domingo de los Tsáchilas': 'J', 'Sucumbíos': 'K', 'Loja': 'L', 'Manabí': 'M',
    'Napo': 'N', 'El Oro': 'O', 'Pichincha': 'P', 'Orellana': 'Q', 'Los Ríos': 'R', 'Pastaza': 'S',
    'Tungurahua': 'T', 'Cañar': 'U', 'Morona Santiago': 'V', 'Galápagos': 'W', 'Cotopaxi': 'X', 'Santa Elena': 'Y', 'Zamora Chinchipe': 'Z'
}

# Letras válidas para la primera letra de la placa (correspondiente a las provincias)
letras_validas = set(provincias.values())

# Expresión regular combinada para placas con formato general
expresion_combinada = r"^[A-Z](?![AUZEXM])[B-Y][A-Z]{2}\d{4}$|^[A-Z][A-U,Z,E,X,M][A-Z]{2}\d{4}$"

# Definir las letras según el tipo de vehículo
letras_particular = set("BCDFGHIJKLNOPQRSTVWY")  # Vehículos particulares
letras_servicio_publico = set("AUZEXM")  # Vehículos de servicio público

# Función corregida
def verificar_placa(placa):
    placa = placa.upper()  # Convertir la placa a mayúsculas para asegurar la validación

    # Validar que la primera letra de la placa corresponde a una provincia válida
    if placa[0] not in letras_validas:
        return {"error": "La primera letra de la placa no corresponde a una provincia válida."}, 400

    # Validar placas con guión y longitud de 8 caracteres
    if len(placa) == 8 and '-' in placa:
        partes = placa.split('-')
        if len(partes) == 2:
            letras, numeros = partes
            if len(letras) == 3 and len(numeros) == 4 and letras.isalpha() and numeros.isdigit():
                if placa[1] in letras_particular:
                    tipo_vehiculo = "Particular"
                elif placa[1] in letras_servicio_publico:
                    tipo_vehiculo = "Servicio Público"
                else:
                    return {"error": "Formato incorrecto para Carro Particular o Servicio Público."}, 400
                
                # Obtener la provincia
                provincia = [prov for prov, letra in provincias.items() if letra == placa[0]][0]
                
                # Retornar la respuesta con los detalles
                return {
                    "placa": placa,
                    "tipo_vehiculo": tipo_vehiculo,
                    "provincia": provincia,
                    "pais": "Ecuador"
                }, 200
            else:
                return {"error": "Formato incorrecto: Verifique que tenga 3 letras, un guion y 4 números."}, 400

    # Validar con expresión regular combinada
    if re.match(expresion_combinada, placa):
        if placa[1] in letras_particular:
            tipo_vehiculo = "Particular"
        elif placa[1] in letras_servicio_publico:
            tipo_vehiculo = "Servicio Público"
        else:
            tipo_vehiculo = "Desconocido"
        
        provincia = [prov for prov, letra in provincias.items() if letra == placa[0]][0]
        return {
            "placa": placa,
            "tipo_vehiculo": tipo_vehiculo,
            "provincia": provincia,
            "pais": "Ecuador"
        }, 200
    else:
        return {"error": "La placa no es válida según las reglas establecidas."}, 400
