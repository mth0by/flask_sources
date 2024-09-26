from ldap3 import Connection, Server, Tls, BASE
from ssl import PROTOCOL_TLSv1_2

from flask import current_app
from flask_login import logout_user

from werkzeug.exceptions import Unauthorized

DEFAULT_CIPHERS = ":".join([
    "AES256-GCM-SHA384",
    "AES128-GCM-SHA256",
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "AES128-CCM-SHA256",
    "ECDHE-ECDSA-AES128-CBC-SHA256",
    "ECDHE-RSA-AES128-CBC-SHA256",
])


def get_ldap_connection():
    server = Server(current_app.config.get('AUTH_LDAP_SERVER'))
    connection = Connection(server)
    connection.bind()

    return connection

def get_user_roles(entry: object) -> list[str]:
    # TODO: role mapping with domain struct
    role_mapping = current_app.config.get('AUTH_ROLES_MAPPING')
    # ldap_group_name_re = r"^OU=([\w\s--]+),.*$"
    for uid in entry.uid.values:
        # group_name_match = re.match(ldap_group_name_re, dn)
        # ldap_group: str = group_name_match.group(1)
        ldap_group: str = uid
        for ldap_map_role, service_role in role_mapping.items():
            if ldap_group == ldap_map_role:
                yield from role_mapping[ldap_map_role]

def do_login(username, password):
    ldap_tls_settings = Tls(
        validate=False, ciphers=DEFAULT_CIPHERS, version=PROTOCOL_TLSv1_2)
    server = Server(current_app.config.get("AUTH_LDAP_SERVER"),
                    tls=ldap_tls_settings)
    user_base_dn = current_app.config.get(
        "AUTH_LDAP_USER_BASE_TEMPLATE").format(username)
    connection = Connection(server, user=user_base_dn, password=password)
    # connection.start_tls()
    if not connection.bind():
        raise Unauthorized(
            description="Проверка имени пользователя или пароля не пройдена.")

    search_result = connection.search(
        search_base=user_base_dn,
        search_filter=current_app.config.get("AUTH_LDAP_SEARCH_FILTER"),
        search_scope=BASE,
        attributes=['*'],
    )
    if not search_result:
        raise Unauthorized(description="Недостаточно прав доступа.")
    entry = connection.entries[0]
    # connection.unbind()

    return entry


def do_logout():
    logout_user()
