from flask import Flask
from flask_fontawesome import FontAwesome
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail
from flask_ckeditor import CKEditor
from .config import Config

fa = FontAwesome()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
login.login_message_category = 'info'
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
mail = Mail()
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    fa.init_app(app)
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    
    from app.public import public
    app.register_blueprint(public)
    
    from app.admin import admin
    app.register_blueprint(admin)
    
    from app.auth import auth
    app.register_blueprint(auth)
    
    from app.post import post
    app.register_blueprint(post)
    
    from app.errors import error
    app.register_blueprint(error)
    
    return app

from app import models
