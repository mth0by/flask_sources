"""Basic authentication backend."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

from flask import Response, request
from flask_appbuilder.const import AUTH_LDAP
from flask_appbuilder.security.sqla.manager import SecurityManager

from flask_login import login_user

from api.auth.extentions.init_auth_manager import get_auth_manager

if TYPE_CHECKING:
    from airflow.providers.fab.auth_manager.models import User

CLIENT_AUTH: tuple[str, str] | Any | None = None

T = TypeVar("T", bound=Callable)


def init_app(_):
    """Initialize authentication backend."""


def auth_current_user() -> User | None:
    """Authenticate and set current user if Authorization header exists."""
    auth = request.authorization
    if auth is None or not auth.username or not auth.password:
        return None

    security_manager = cast(SecurityManager, get_auth_manager())
    user = None
    if security_manager.auth_type == AUTH_LDAP:
        user = get_auth_manager().auth_user_ldap(auth.username, auth.password)
    if user is None:
        user = security_manager.auth_user_db(auth.username, auth.password)
    if user is not None:
        login_user(user, remember=False)
    return user


def requires_authentication(function: T):
    """Decorate functions that require authentication."""

    @wraps(function)
    def decorated(*args, **kwargs):
        if auth_current_user() is not None:
            return function(*args, **kwargs)
        else:
            return Response("Unauthorized", 401, {"WWW-Authenticate": "Basic"})

    return cast(T, decorated)
