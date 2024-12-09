from flask import Flask
from flask_cors import CORS
from Routes.route import routes_bp

app = Flask(__name__)

# Configuración simple de CORS para desarrollo
CORS(app, supports_credentials=True)

# Registrar el blueprint con prefijo /api
app.register_blueprint(routes_bp, url_prefix='/api')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)