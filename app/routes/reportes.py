from flask import Blueprint, render_template, Response
from flask_login import login_required
from app.models import Producto, Movimiento
import csv
import io

rep_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@rep_bp.route('/')
@login_required
def index():
    productos = Producto.query.all()
    movimientos = Movimiento.query.order_by(Movimiento.fecha.desc()).limit(50).all()
    return render_template('reportes/index.html', productos=productos, movimientos=movimientos)

@rep_bp.route('/exportar/productos')
@login_required
def exportar_productos():
    productos = Producto.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nombre', 'Descripcion', 'Stock', 'Precio', 'Categoria', 'Creado en'])
    for p in productos:
        writer.writerow([p.id, p.nombre, p.descripcion, p.stock, p.precio, p.categoria, p.creado_en])
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=productos.csv'}
    )

@rep_bp.route('/exportar/movimientos')
@login_required
def exportar_movimientos():
    movimientos = Movimiento.query.order_by(Movimiento.fecha.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Producto', 'Tipo', 'Cantidad', 'Observacion', 'Usuario', 'Fecha'])
    for m in movimientos:
        writer.writerow([m.id, m.producto.nombre, m.tipo, m.cantidad, m.observacion, m.usuario, m.fecha])
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=movimientos.csv'}
    )