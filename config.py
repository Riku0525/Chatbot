import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kaiser-12'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_TLS = False
    MAIL_USE_SSL= True
    MAIL_USERNAME = 'abg.ansconta@gmail.com'
    MAIL_PASSWORD = 'Kaiser123'   
    MAIL_DEFAULT_SENDER = 'riku0525@hotmail.com'
    ADMINS = ['abg.ansconta@gmail.com']
    LANGUAGES = ['es']
    CHATS_PER_PAGE = 25