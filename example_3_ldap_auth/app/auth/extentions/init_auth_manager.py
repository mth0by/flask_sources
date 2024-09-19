from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder import SQLA, AppBuilder
from app.auth.security import LDAPSecurityManager

auth_manager: SecurityManager | None = None


# def get_auth_manager_cls() -> type[SecurityManager]:
#     """
#     Return just the auth manager class without initializing it.
#
#     Useful to save execution time if only static methods need to be called.
#     """
#
#     auth_manager_cls = conf.getimport(section="core", key="auth_manager")
#
#     if not auth_manager_cls:
#         raise AirflowConfigException(
#             "No auth manager defined in the config. "
#             "Please specify one using section/key [core/auth_manager]."
#         )
#
#     return auth_manager_cls


def init_auth_manager(appbuilder: AppBuilder) -> SecurityManager:
    """
    Initialize the auth manager.

    Import the user manager class and instantiate it.
    """
    global auth_manager
    auth_manager_cls = LDAPSecurityManager
    auth_manager = auth_manager_cls(appbuilder)
    return auth_manager


def get_auth_manager() -> SecurityManager:
    """Return the auth manager, provided it's been initialized before."""
    if auth_manager is None:
        raise RuntimeError(
            "Auth Manager has not been initialized yet. "
            "The `init_auth_manager` method needs to be called first."
        )
    return auth_manager


def is_auth_manager_initialized() -> bool:
    """Return whether the auth manager has been initialized."""
    return auth_manager is not None
