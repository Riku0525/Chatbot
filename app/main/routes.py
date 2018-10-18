from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.main import bp
from app.main.forms import NewbotForm, BotdetailForm
from app.models import User, Bot, Botdetail, Chat, Chatdetail, Service
from app.chat import begin_chat, respond_chat
import sys
import json

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        if user.userlevel == 1:
            return render_template('indexa.html', title='Inicio Administrador', user=user)
        return render_template('indexu.html', title='Chat de Usuario', user=user)
    return render_template('index.html', title='Inicio')

@bp.route('/chatadm')
def chatadm():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('indexu.html', title='Chat de Administrador', user=user)
    
@bp.route('/beginchat', methods=['POST'])
@login_required
def begin_user():
    user = User.query.filter_by(username=current_user.username).first()
    response = begin_chat(user.id, 1, user.get_token())
    message = json.loads(response)
    print(message, file=sys.stderr)
    return jsonify(message)
    
@bp.route('/responduser', methods=['GET'])
@login_required
def respond_user():
    user = User.query.filter_by(username=current_user.username).first()
    response = respond_chat(request.args.get('chat', ''), request.args.get('message', ''), user.get_token())
    message = json.loads(response)
    print(message, file=sys.stderr)
    return jsonify(message)
    
	
@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		users = User.query.all()
		return render_template('users.html', title='Usuarios registrados', users=users)
	return redirect(url_for('main.index'))
	
@bp.route('/newbot', methods=['GET', 'POST'])
@login_required
def newbot():
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		form = NewbotForm()
		if form.validate_on_submit():
			bot = Bot(botname=form.botname.data, botdescription=form.botdescription.data)
			db.session.add(bot)
			db.session.commit()
			flash('Se ha registrado un nuevo Bot en la aplicación')
			return redirect(url_for('main.bot', botname=bot.botname))
		return render_template('newbot.html', title='Registrar nuevo Bot', form=form)
	return redirect(url_for('main.index'))
	
@bp.route('/bots', methods=['GET', 'POST'])
@login_required
def bots():
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		bots = Bot.query.all()
		return render_template('bots.html', title='Bots registrados', bots=bots)
	return redirect(url_for('main.index'))
	
@bp.route('/bot/<botname>', methods=['GET', 'POST'])
@login_required
def bot(botname):
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		bot = Bot.query.filter_by(botname=botname).first_or_404()
		botdetails = bot.detail.all()
		form = BotdetailForm()
		if form.validate_on_submit():
			botdetail = Botdetail(bot_id=bot.id, order=form.sequence.data, mesg=form.mesg.data, post=form.post.data, vali=form.vali.data, next=form.next.data)
			db.session.add(botdetail)
			db.session.commit()
			flash('Se ha registrado una nueva instruccion en el Bot')
			return redirect(url_for('main.bot', botname=bot.botname))
		return render_template('bot.html', title='Mantenimiento de Bot', bot=bot, botdetails=botdetails, form=form)
	return redirect(url_for('main.index'))
	
@bp.route('/instruction/<botname>/<detail>', methods=['GET', 'POST'])
@login_required
def instruction(botname, detail):
    user = User.query.filter_by(username=current_user.username).first()
    if user.userlevel == 1:
        botdetail = Botdetail.query.get(detail)
        form = BotdetailForm()
        if form.validate_on_submit():
            botdetail.order = form.sequence.data
            botdetail.mesg = form.mesg.data
            botdetail.post = form.post.data
            botdetail.vali = form.vali.data
            botdetail.next = form.next.data
            db.session.commit()
            flash('Sus cambios se han guardado.')
            return redirect(url_for('main.instruction', botname=botname, detail=detail))
        elif request.method == 'GET':
            form.sequence.data = botdetail.order
            form.mesg.data = botdetail.mesg
            form.post.data = botdetail.post
            form.vali.data = botdetail.vali
            form.next.data = botdetail.next
        return render_template('detail.html', title='Mantenimiento de instruccion', botdetail=botdetail, form=form, botname=botname)
    return redirect(url_for('main.index'))

@bp.route('/dinstruction/<botname>/<detail>', methods=['GET', 'POST'])
@login_required
def dinstruction(botname, detail):
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		botd = Botdetail.query.get(detail)
		db.session.delete(botd)
		db.session.commit()
		flash('Se ha eliminado una instruccion del Bot')
		return redirect(url_for('main.bot', botname=botname))
	return redirect(url_for('main.index'))
    
@bp.route('/chats', methods=['GET', 'POST'])
@login_required
def chats():
    user = User.query.filter_by(username=current_user.username).first()
    if user.userlevel == 1:
        result = db.session.query(Chat).join(User).join(Bot).with_entities(Chat.timestamp, Chat.id, User.username, Bot.botname).order_by(Chat.id.desc()).all()
        return render_template('chats.html', title='Chats guardados', chats=result)
    return redirect(url_for('main.index'))
    
@bp.route('/detchat/<id>', methods=['GET', 'POST'])
@login_required
def detchat(id):
    user = User.query.filter_by(username=current_user.username).first()
    if user.userlevel == 1:
        chatheader = Chat.query.get(id)
        chatdetail = chatheader.detail.order_by(Chatdetail.order).all()
        service = Service.query.filter_by(chat_id=id).first()
        return render_template('chatdets.html', title='Detalle del Chat', chatdetail=chatdetail, service=service)
    return redirect(url_for('main.index'))
    
@bp.route('/dchat/<id>', methods=['GET', 'POST'])
@login_required
def dchat(id):
    user = User.query.filter_by(username=current_user.username).first()
    if user.userlevel == 1:
        chatdetail = Chatdetail.query.filter_by(chat_id = id)
        if chatdetail:
            for chat in chatdetail: 
                db.session.delete(chat)
        chatd = Chat.query.get(id)
        db.session.delete(chatd)
        db.session.commit()
        flash('Se ha eliminado un registro de Chat')
        return redirect(url_for('main.chats'))
    return redirect(url_for('main.index'))