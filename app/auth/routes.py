from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, UpdatepassForm
from app.models import User
from app.chat import loginUser, logoutUser
import json
import requests
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o Contraseña invalidos')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        loginUser(form.username.data, form.password.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Inicio de sesión', form=form)
	
@bp.route('/logout')
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    logoutUser(user.get_token())
    logout_user()
    return redirect(url_for('main.index'))
	
@bp.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, userlevel=2)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Gracias, se ha registrado un usuario')
		return redirect(url_for('main.index'))
	return render_template('register.html', title='Registro', form=form)
	
@bp.route('/regadm', methods=['GET', 'POST'])
@login_required
def registeradministrator():
	user = User.query.filter_by(username=current_user.username).first()
	if user.userlevel == 1:
		form = RegistrationForm()
		if form.validate_on_submit():
			user = User(username=form.username.data, email=form.email.data, userlevel=1)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Se ha registrado un nuevo administrador')
			return redirect(url_for('main.index'))
		return render_template('registera.html', title='Registro de Administrador', form=form)
	return redirect(url_for('main.index'))
	
@bp.route('/options', methods=['GET', 'POST'])
@login_required
def options():
	user = User.query.filter_by(username=current_user.username).first()
	form = UpdatepassForm()
	if form.validate_on_submit():
		if user is None or not user.check_password(form.oldpassword.data):
			flash('Contraseña acutal erronea')
			return redirect(url_for('auth.opciones'))
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Contraseña actualizada')
		return redirect(url_for('auth.login'))
	return render_template('options.html', title='Opciones', user=user, form=form)