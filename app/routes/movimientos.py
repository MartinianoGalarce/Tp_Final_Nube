from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Producto, Movimiento
from functools import wraps

mov_bp = Blueprint('movimientos', __name__, url_prefix='/movimientos')

def solo_admin_operador(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.rol not in ['admin', 'operador']:
            flash('No tenés permisos para realizar esta acción.', 'danger')
            return redirect(url_for('stock.listar'))
        return f(*args, **kwargs)
    return decorated

@mov_bp.route('/')
@login_required
def listar():
    movimientos = Movimiento.query.order_by(Movimiento.fecha.desc()).all()
    return render_template('movimientos/listar.html', movimientos=movimientos)

@mov_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@solo_admin_operador
def nuevo():
    productos = Producto.query.all()
    if request.method == 'POST':
        producto_id = int(request.form['producto_id'])
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        observacion = request.form.get('observacion', '')

        producto = Producto.query.get_or_404(producto_id)

        if tipo == 'salida' and producto.stock < cantidad:
            flash('Stock insuficiente para realizar la salida.', 'danger')
            return render_template('movimientos/form.html', productos=productos)

        if tipo == 'entrada':
            producto.stock += cantidad
        else:
            producto.stock -= cantidad

        movimiento = Movimiento(
            producto_id=producto_id,
            tipo=tipo,
            cantidad=cantidad,
            observacion=observacion,
            usuario=current_user.username
        )
        db.session.add(movimiento)
        db.session.commit()
        flash('Movimiento registrado correctamente.', 'success')
        return redirect(url_for('movimientos.listar'))

    return render_template('movimientos/form.html', productos=productos)