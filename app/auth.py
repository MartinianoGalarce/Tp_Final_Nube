from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPException
from flask_login import UserMixin
from datetime import datetime
from app.config import Config

class Usuario(UserMixin):
    def __init__(self, username, rol):
        self.id = username
        self.username = username
        self.rol = rol

def get_hora_actual():
    return datetime.now().hour

def verificar_horario():
    hora = get_hora_actual()
    return Config.HORA_INICIO <= hora < Config.HORA_FIN

def autenticar_ldap(username, password):
    try:
        server = Server(Config.LDAP_HOST, port=Config.LDAP_PORT, get_info=ALL)
        user_dn = f'uid={username},{Config.LDAP_USERS_DN}'
        conn = Connection(server, user=user_dn, password=password)

        if not conn.bind():
            return None, 'Usuario o contraseña incorrectos'

        # Buscar grupos del usuario
        conn_admin = Connection(
            server,
            user=Config.LDAP_ADMIN_DN,
            password=Config.LDAP_ADMIN_PASSWORD
        )
        conn_admin.bind()
        conn_admin.search(
            Config.LDAP_GROUPS_DN,
            f'(member={user_dn})',
            attributes=['cn']
        )

        rol = None
        for entry in conn_admin.entries:
            grupo = entry.cn.value
            if grupo == 'GRP_Admin':
                rol = 'admin'
                break
            elif grupo == 'GRP_Operador':
                rol = 'operador'
                break
            elif grupo == 'GRP_Consulta':
                rol = 'consulta'
                break

        if not rol:
            return None, 'Usuario sin rol asignado'

        return Usuario(username, rol), None

    except LDAPException as e:
        return None, f'Error de conexión LDAP: {str(e)}'