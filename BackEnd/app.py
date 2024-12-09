from flask import Flask
from flask_cors import CORS
from Routes.route import routes_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones cross-origin

app.register_blueprint(routes_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)