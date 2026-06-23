from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from app.auth import autenticar_ldap, verificar_horario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not verificar_horario():
            flash('Acceso restringido: solo se permite entre las 8:00 y las 18:00 hs.', 'danger')
            return render_template('login.html')

        usuario, error = autenticar_ldap(username, password)

        if error:
            flash(error, 'danger')
            return render_template('login.html')

        session['rol'] = usuario.rol
        login_user(usuario)
        flash(f'Bienvenido {username} — Rol: {usuario.rol}', 'success')
        return redirect(url_for('stock.listar'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))