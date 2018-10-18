from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin
import base64
import os

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    userlevel = db.Column(db.Integer)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration =(db.Column(db.DateTime))
    chats = db.relationship('Chat', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
		
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
		
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
        
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Bot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	botname = db.Column(db.String(64), index=True, unique=True)
	botdescription = db.Column(db.String(500))
	chats = db.relationship('Chat', backref='bot', lazy='dynamic')
	detail = db.relationship('Botdetail', backref='bot', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.botname)
		
class Botdetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'), index=True)
    order = db.Column(db.Integer, index=True)
    action = db.Column(db.String(250))
    mesg = db.Column(db.String(250))
    post = db.Column(db.String(250))
    vali = db.Column(db.String(250))
    next = db.Column(db.Integer)
    chats = db.relationship('Chat', backref='botdetail', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.mesg)
        
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vars = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bot_id = db.Column(db.Integer, db.ForeignKey('bot.id'))
    botdetail_id = db.Column(db.Integer, db.ForeignKey('botdetail.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    detail = db.relationship('Chatdetail', backref='chat', lazy='dynamic')
    service = db.relationship('Service', backref='chat', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.id)	
	
class Chatdetail(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), index=True)
	order = db.Column(db.Integer, index=True)
	message = db.Column(db.String(150))
	author = db.Column(db.String(64))
	
	def __repr__(self):
		return '<User {}>'.format(self.chat_id)
		
@login.user_loader
def load_user(id):
	return User.query.get(int(id))
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    bot = db.Column(db.String(150))
    var = db.Column(db.String(150))
    email = db.Column(db.String(150))
    status = db.Column(db.Integer)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), index=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.id)	