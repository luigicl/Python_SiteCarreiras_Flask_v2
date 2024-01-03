""" FORMULÁRIOS DO SITE """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, URL, length, Optional
from carreiras_python.database import load_applications


class FormApplication(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(message="Verifique o e-mail digitado")])
    full_name = StringField("Nome completo", validators=[DataRequired()])
    linkedin = StringField("Linkedin", validators=[Optional(), URL(message="Verifique a URL do Linkedin digitada")])
    github = StringField("Github", validators=[Optional(), URL(message="Verifique a URL do Github digitada")])
    comments = TextAreaField("Fale sobre você", validators=[length(max=1000)])
    resume = FileField("Currículo", validators=[FileAllowed(['pdf'], 'Somente arquivo PDF')])
    confirmation_button = SubmitField("Inscrever-se")


class FormSearchApplications(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(message="Verifique o e-mail digitado")])
    confirmation_button = SubmitField("Buscar")

    def validate_email(self, email):  # o nome da função tem que ser validate_nomedocampo a ser validado
        if not len(load_applications(email.data)):
            raise ValidationError("Não inscrições para o e-mail informado.")


class FormSearchJobs(FlaskForm):
    search = StringField("Busca", validators=[DataRequired()])
    search_button = SubmitField("Buscar")
