import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-ifts18')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stock.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # LDAP
    LDAP_HOST = '127.0.0.1'
    LDAP_PORT = 389
    LDAP_BASE_DN = 'dc=ifts18,dc=local'
    LDAP_USERS_DN = 'ou=usuarios,dc=ifts18,dc=local'
    LDAP_GROUPS_DN = 'ou=grupos,dc=ifts18,dc=local'
    LDAP_ADMIN_DN = 'cn=admin,dc=ifts18,dc=local'
    LDAP_ADMIN_PASSWORD = 'admin123'

    # Restricción horaria
    HORA_INICIO = 8
    HORA_FIN = 23