from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField("Usuario", validators=[DataRequired()])
    password=PasswordField("Contraseña", validators=[DataRequired()])
    remember_me=BooleanField("Recuérdame")
    submit=SubmitField("Iniciar sesión")

class SignUpForm(FlaskForm):
    username=StringField("Usuario", validators=[DataRequired()])
    email=StringField("Correo", validators=[DataRequired()])
    password=PasswordField("Contraseña", validators=[DataRequired()])
    submit=SubmitField("Registrar")


class ContactForm(FlaskForm):
    name=StringField("Nombre", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    number=StringField("Número", validators=[DataRequired()])
    submit=SubmitField("Registrar")