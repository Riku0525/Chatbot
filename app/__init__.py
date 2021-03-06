from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Es necesario iniciar sesión para acceder al contenido."
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
app.config.update(
    MAIL_SERVER= 'smtp-mail.outlook.com',
    MAIL_PORT= 587,
    MAIL_USE_SSL= False,
    MAIL_USE_TLS= True,
    MAIL_USERNAME= 'riku0525@hotmail.com',
    MAIL_PASSWORD= 'Kaiser12'
    )
mail = Mail(app)

from app.main import bp as main_bp
app.register_blueprint(main_bp, url_prefix='/main')

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import models, routes, email