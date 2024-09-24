from re import search

from ldap3 import Connection, Server
from flask import current_app
from flask_login import logout_user

from werkzeug.exceptions import Unauthorized

def get_ldap_connection():
    server = Server(current_app.config.get('AUTH_LDAP_SERVER'))
    connection = Connection(server)
    connection.bind()

    return connection

def do_login(username, password):
    from ldap3 import Connection, Server
    from flask import current_app

    server = Server(current_app.config.get("AUTH_LDAP_SERVER"))
    user_base_dn = current_app.config.get("AUTH_LDAP_USER_BASE_TEMPLATE").format(
        username)
    connection = Connection(server, user=user_base_dn, password=password)
    if not connection.bind():
        raise Unauthorized(
            description="Ошибка при проверке имени пользователя и пароля в AD."
        )

    search_result = connection.search(
        search_base=user_base_dn,
        search_filter=current_app.config.get("AUTH_LDAP_SEARCH_FILTER"),
    )
    if search_result is None:
        raise Unauthorized(description="Недостаточно прав доступа.")

    return search_result


def do_logout():
    logout_user()
