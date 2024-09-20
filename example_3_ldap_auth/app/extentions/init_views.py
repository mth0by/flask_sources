from app import views


def init_appbuilder_views(app):
    """Initialize Web UI views."""

    appbuilder = app.appbuilder

    # Remove the session from scoped_session registry to avoid
    # reusing a session with a disconnected connection
    appbuilder.session.remove()
    appbuilder.add_view_no_menu(views.MyView())