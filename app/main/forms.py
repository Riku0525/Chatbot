from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import Bot
	
class NewbotForm(FlaskForm):
	botname = StringField('Nombre del Bot', validators=[DataRequired()])
	botdescription = TextAreaField('Descripcion del Bot', validators=[DataRequired()])
	submit = SubmitField('Crear Bot')
	
	def validate_botname(self, botname):
		bot = Bot.query.filter_by(botname=botname.data).first()
		if bot is not None:
			raise ValidationError('Nombre de Bot ya existe')

class BotdetailForm(FlaskForm):
	sequence = IntegerField('Secuencia', validators=[DataRequired()], render_kw={'class': 'form-control input-sm'})
	mesg = TextAreaField('Mensaje', validators=[DataRequired()], render_kw={'class': 'form-control input-lg'})
	post = TextAreaField('Posterior', validators=[DataRequired()], render_kw={'class': 'form-control input-lg'})
	vali = TextAreaField('Validaciones', render_kw={'class': 'form-control input-lg'})
	next = IntegerField('Instruccion Siguiente', render_kw={'class': 'form-control input-sm'})
	submit = SubmitField('Agregar instruccion', render_kw={'class': 'btn btn-default'})