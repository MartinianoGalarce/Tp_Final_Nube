from flask import Flask
from flask_login import LoginManager
from app.models import db
from app.config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debés iniciar sesión para acceder.'

    from app.auth import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        # Guardamos el rol en sesión, lo recuperamos acá
        from flask import session
        rol = session.get('rol', 'consulta')
        return Usuario(user_id, rol)

    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.routes.stock import stock_bp
    from app.routes.movimientos import mov_bp
    from app.routes.reportes import rep_bp
    from app.routes import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(mov_bp)
    app.register_blueprint(rep_bp)

    return app