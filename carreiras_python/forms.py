""" FORMULÁRIOS DO SITE """
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, URL, length


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(message="Verifique o e-mail digitado")])
    full_name = StringField("Nome completo", validators=[DataRequired()])
    linkedin = StringField("Linkedin", validators=[DataRequired(), URL(message="Verifique a URL do Linkedin digitada")])
    github = StringField("Github", validators=[DataRequired(), URL(message="Verifique a URL do Github digitada")])
    comments = TextAreaField("Fale sobre você", validators=[length(max=1000)])
    confirmation_button = SubmitField("Inscrever-se")

    # def validate_email(self, email):  # o nome da função tem que ser validate_nomedocampo a ser validado
    #     usuario = Usuario.query.filter_by(email=email.data).first()  # campo email da classe Usuario
    #     if not usuario:
    #         raise ValidationError("Usuário inexistente. Crie uma conta para continuar.")


