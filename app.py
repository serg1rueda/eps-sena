from flask import Flask, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB
    db.init_app(app)

    # Swagger
    Swagger(app)

    # JWT
    jwt = JWTManager(app)

    # Blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({"msg": "API EPS-SENA funcionando 🚑"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
