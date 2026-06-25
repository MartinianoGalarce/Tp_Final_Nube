from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, default=0.0)
    categoria = db.Column(db.String(50))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    movimientos = db.relationship('Movimiento', backref='producto', lazy=True, cascade='all, delete-orphan')

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    observacion = db.Column(db.String(200))
    usuario = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)