from flask_appbuilder.security.views import AuthLDAPView
from flask_appbuilder.security.sqla.manager import SecurityManager


class LDAPSecurityManager(SecurityManager):
    authldapview = AuthLDAPView
