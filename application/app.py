# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
from flask import Flask, render_template
from application import public, service
from application.extensions import (
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)


def create_app(config_object="application.settings"):
    """按照说明创建应用程序工厂 here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: 要使用的配置对象
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    # register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)
    # configure_logger(app)
    return app


def register_extensions(app):
    """注册 Flask 扩展。"""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """注册 Flask 蓝图。"""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(service.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """注册错误处理程序."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

