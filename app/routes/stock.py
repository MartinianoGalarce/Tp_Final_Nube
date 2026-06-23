from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Producto
from functools import wraps

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

def solo_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.rol != 'admin':
            flash('No tenés permisos para realizar esta acción.', 'danger')
            return redirect(url_for('stock.listar'))
        return f(*args, **kwargs)
    return decorated

@stock_bp.route('/')
@login_required
def listar():
    productos = Producto.query.all()
    return render_template('stock/listar.html', productos=productos)

@stock_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@solo_admin
def nuevo():
    if request.method == 'POST':
        producto = Producto(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            stock=int(request.form['stock']),
            precio=float(request.form['precio']),
            categoria=request.form['categoria']
        )
        db.session.add(producto)
        db.session.commit()
        flash('Producto creado correctamente.', 'success')
        return redirect(url_for('stock.listar'))
    return render_template('stock/form.html', producto=None)

@stock_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@solo_admin
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.stock = int(request.form['stock'])
        producto.precio = float(request.form['precio'])
        producto.categoria = request.form['categoria']
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('stock.listar'))
    return render_template('stock/form.html', producto=producto)

@stock_bp.route('/eliminar/<int:id>')
@login_required
@solo_admin
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('stock.listar'))