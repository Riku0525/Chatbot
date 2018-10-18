from app import app, db
from app.models import User, Bot, Botdetail, Chat, Chatdetail, Service

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Bot': Bot, 'Botdetail': Botdetail, 'Chat':Chat, 'Chatdetail':Chatdetail, 'Service':Service}