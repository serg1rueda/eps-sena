from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.Text, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())

    rol = db.relationship("Rol", backref="usuarios", lazy=True)

    # helpers
    def set_password(self, plain):
        self.contrasena_hash = generate_password_hash(plain)

    def check_password(self, plain) -> bool:
        return check_password_hash(self.contrasena_hash, plain)

class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), unique=True)
    documento = db.Column(db.String(40), unique=True)
    fecha_nac = db.Column(db.Date)
    telefono = db.Column(db.String(30))

    usuario = db.relationship("Usuario", backref="paciente", uselist=False)

class Medico(db.Model):
    __tablename__ = "medicos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), unique=True)
    especialidad = db.Column(db.String(80))

    usuario = db.relationship("Usuario", backref="medico", uselist=False)

class Cita(db.Model):
    __tablename__ = "citas"
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey("medicos.id"), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Enum("PROGRAMADA", "CANCELADA", "ATENDIDA"), default="PROGRAMADA")
    notas = db.Column(db.Text)

    paciente = db.relationship("Paciente", backref="citas")
    medico = db.relationship("Medico", backref="citas")

class Formula(db.Model):
    __tablename__ = "formulas"
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey("citas.id"), nullable=False)
    medicamento = db.Column(db.Text, nullable=False)
    dosis = db.Column(db.Text, nullable=False)
    instrucciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())

    cita = db.relationship("Cita", backref="formulas")

class Laboratorio(db.Model):
    __tablename__ = "laboratorios"
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey("citas.id"), nullable=False)
    examen = db.Column(db.Text, nullable=False)
    resultado = db.Column(db.Text)
    fecha_resultado = db.Column(db.DateTime)
    observaciones = db.Column(db.Text)

    cita = db.relationship("Cita", backref="laboratorios")
