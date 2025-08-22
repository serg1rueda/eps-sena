from flask import Flask, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import api_blueprint

def create_app():
    """
    Factory function to create Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB
    db.init_app(app)

    # Initialize Swagger
    Swagger(app)

    # Initialize JWT
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # Root route
    @app.route("/")
    def index():
        return jsonify({"msg": "API EPS-SENA funcionando 🚑"})

    return app

# Para ejecutar localmente con python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

# Para Gunicorn en Render
# Gunicorn puede usar: gunicorn "app:create_app()"
