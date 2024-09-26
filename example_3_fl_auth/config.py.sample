from pathlib import Path

"""
It’s set to 'dev' to provide a convenient value during development,
but it should be overridden with a random value when deploying.
"""
SECRET_KEY = "dev"

BASEDIR = Path(__file__).absolute()
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# region Authentication

AUTH_LDAP_SERVER = "ldap://ldap.forumsys.com"
# AUTH_ROLES_MAPPING = {
#     "CN=fab_users,OU=groups,DC=example,dc=org": ["User"],
#     "CN=fab_admins,OU=groups,DC=example,dc=org": ["Admin"],
# }
AUTH_LDAP_USER_BASE_TEMPLATE="uid={},dc=example,dc=com"
AUTH_LDAP_SEARCH_FILTER = "(objectClass=person)"

# endregion