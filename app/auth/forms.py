from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Entrar')
	
class RegistrationForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired()])
	email = StringField('Correo electronico', validators=[DataRequired(), Email()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	password2 = PasswordField('Repetir contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Registrar')
	
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Nombre de usuario ya existe')

class UpdatepassForm(FlaskForm):
	oldpassword = PasswordField('Contraseña actual', validators=[DataRequired()])
	password = PasswordField('Contraseña nueva', validators=[DataRequired()])
	password2 = PasswordField('Repetir contraseña nueva', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Cambiar contraseña')