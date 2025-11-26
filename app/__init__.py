import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from elasticsearch import Elasticsearch



def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])
    # return 'ro'


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = _l("Please log in to access this page.")
mail = Mail()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    app.elasticsearch = (
        Elasticsearch(
            [app.config["ELASTICSEARCH_URL"]],
            verify_certs=False,
            ssl_show_warn=False
        )
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp

    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        if os.environ.get("SENDGRID_API_KEY"):
            from app.email import SendGridHandler

            sendgrid_handler = SendGridHandler(
                api_key=os.environ.get("SENDGRID_API_KEY"),
                from_email=app.config["MAIL_USERNAME"],
                to_emails=app.config["ADMINS"],
                subject="PaperLight Failure",
            )

            sendgrid_handler.setLevel(logging.ERROR)
            sendgrid_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            app.logger.addHandler(sendgrid_handler)

        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/paperlight.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("PaperLight startup")

    return app


from app import models
