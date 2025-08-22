from flask import Blueprint, request, jsonify
from models import db, Usuario, Rol, Paciente, Medico, Cita, Formula, Laboratorio
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

api_blueprint = Blueprint("api", __name__)

# --------------------
# AUTENTICACIÓN / AUTH
# --------------------
@api_blueprint.route("/auth/login", methods=["POST"])
def login():
    """
    Login y generación de JWT
    ---
    tags:
      - auth
    parameters:
      - in: body
        name: body
        schema:
          properties:
            correo:
              type: string
            contrasena:
              type: string
    responses:
      200:
        description: Token JWT
    """
    data = request.json or {}
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    if not correo or not contrasena:
        return jsonify({"msg": "correo y contrasena son requeridos"}), 400

    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"msg": "credenciales inválidas"}), 401

    # incluir rol en claims para verificación sencilla
    user_rol = usuario.rol.nombre if usuario.rol else None
    additional_claims = {"rol": user_rol, "correo": usuario.correo}
    access_token = create_access_token(identity=usuario.id, additional_claims=additional_claims, expires_delta=timedelta(hours=8))

    return jsonify({"access_token": access_token, "rol": user_rol, "usuario_id": usuario.id}), 200

# helper para chequear rol
def require_role(claims, roles_allowed):
    rol = claims.get("rol")
    return rol in roles_allowed

# --------------------
# Ejemplo: obtener usuarios (solo ADMIN)
# --------------------
@api_blueprint.route("/usuarios", methods=["GET"])
@jwt_required()
def get_usuarios():
    """
    Obtener usuarios (solo ADMIN)
    ---
    security:
      - bearerAuth: []
    tags:
      - usuarios
    responses:
      200:
        description: Lista de usuarios
    """
    claims = get_jwt()
    if not require_role(claims, ["ADMIN"]):
        return jsonify({"msg": "sin permiso (ADMIN requerido)"}), 403

    usuarios = Usuario.query.all()
    lista = [{"id": u.id, "nombre": u.nombre_completo, "correo": u.correo, "rol": u.rol.nombre if u.rol else None} for u in usuarios]
    return jsonify(lista), 200

# --------------------
# Endpoints públicos/otros protegidos (ejemplos)
# --------------------
@api_blueprint.route("/citas", methods=["POST"])
@jwt_required()
def crear_cita():
    """
    Crear cita (cualquier usuario autenticado puede crear; en prod validar permisos)
    ---
    security:
      - bearerAuth: []
    tags:
      - citas
    parameters:
      - in: body
        name: body
        schema:
          properties:
            paciente_id:
              type: integer
            medico_id:
              type: integer
            fecha:
              type: string
            notas:
              type: string
    responses:
      201:
        description: Cita creada
    """
    data = request.json or {}
    paciente_id = data.get("paciente_id")
    medico_id = data.get("medico_id")
    fecha = data.get("fecha")
    if not (paciente_id and medico_id and fecha):
        return jsonify({"msg": "paciente_id, medico_id y fecha son requeridos"}), 400

    cita = Cita(paciente_id=paciente_id, medico_id=medico_id, fecha=fecha, notas=data.get("notas"))
    db.session.add(cita)
    db.session.commit()
    return jsonify({"msg": "Cita creada", "id": cita.id}), 201

@api_blueprint.route("/citas", methods=["GET"])
@jwt_required()
def listar_citas():
    """
    Listar citas (cualquier usuario autenticado)
    ---
    security:
      - bearerAuth: []
    tags:
      - citas
    responses:
      200:
        description: Lista de citas
    """
    citas = Cita.query.all()
    result = []
    for c in citas:
        result.append({
            "id": c.id,
            "paciente_id": c.paciente_id,
            "medico_id": c.medico_id,
            "fecha": c.fecha.strftime("%Y-%m-%d %H:%M") if c.fecha else None,
            "estado": c.estado
        })
    return jsonify(result), 200

# --------------------
# Rutas adicionales CRUD (puedes expandirlas)
# --------------------
# ejemplo simple crear usuario (no requiere ADMIN pero en prod sí)
@api_blueprint.route("/usuarios", methods=["POST"])
def crear_usuario_public():
    data = request.json or {}
    nombre = data.get("nombre_completo")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    rol_id = data.get("rol_id")
    if not all([nombre, correo, contrasena, rol_id]):
        return jsonify({"msg": "nombre_completo, correo, contrasena y rol_id son requeridos"}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({"msg": "correo ya registrado"}), 400

    usuario = Usuario(nombre_completo=nombre, correo=correo, rol_id=rol_id)
    usuario.set_password(contrasena)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"msg": "Usuario creado", "id": usuario.id}), 201
