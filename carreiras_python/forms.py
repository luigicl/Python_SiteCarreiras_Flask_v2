""" FORMULÁRIOS DO SITE """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, URL, length, Optional
from carreiras_python.database import load_my_applications


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
        if not len(load_my_applications(email.data)):
            raise ValidationError("Não inscrições para o e-mail informado.")


class FormSearchJobs(FlaskForm):
    search = StringField("Busca", validators=[DataRequired()])
    search_button = SubmitField("Buscar")


class FormCreateJob(FlaskForm):
    job_title = StringField("Título da Vaga", validators=[DataRequired()])
    responsabilities = TextAreaField("Responsabilidades", validators=[DataRequired(), length(max=2000)])
    requirements = TextAreaField("Requisitos", validators=[DataRequired(), length(max=2000)])
    location = StringField("Localidade", validators=[DataRequired()])
    salary = IntegerField("Salário", validators=[Optional()])
    currency = SelectField("Moeda",
                           choices=[
                               ('BRL', 'BRASIL - REAL'),
                               ('USD', 'ESTADOS UNIDOS - DÓLAR'),
                               ('EUR', 'ZONA DO EURO - EURO'),
                               ('GBP', 'REINO UNIDO - LIBRA ESTERLINA'),
                               ('ARS', 'ARGENTINA - PESO'),
                               ('ZAR', 'ÁFRICA DO SUL - RAND'),
                               ('AUD', 'AUSTRÁLIA - DÓLAR AUSTRALIANO'),
                               ('BOB', 'BOLÍVIA - BOLIVIANO'),
                               ('CAD', 'CANADÁ - DÓLAR CANADENSE'),
                               ('CLP', 'CHILE - PESO CHILENO'),
                               ('CNY', 'CHINA - YUAN'),
                               ('COP', 'COLÔMBIA - PESO COLOMBIANO'),
                               ('DKK', 'DINAMARCA - COROA DINAMARQUESA'),
                               ('HKD', 'HONG KONG - DÓLAR DE HONG KONG'),
                               ('INR', 'ÍNDIA - RUPIA INDIANA'),
                               ('IDR', 'INDONÉSIA - RUPIA INDONÉSIA'),
                               ('ILS', 'ISRAEL - SHEKEL NOVO'),
                               ('JPY', 'JAPÃO - IENE'),
                               ('MYR', 'MALÁSIA - RINGGIT'),
                               ('MXN', 'MÉXICO - PESO NOVO MEXICANO'),
                               ('NOK', 'NORUEGA - COROA NORUEGUESA'),
                               ('NZD', 'NOVA ZELÂNDIA - DÓLAR DA NOVA ZELÂNDIA'),
                               ('KRW', 'REPÚBLICA DA CORÉIA - WON SUL-COREANO'),
                               ('RUB', 'RÚSSIA - RUBLO'),
                               ('SGD', 'SINGAPURA - DÓLAR DE SINGAPURA'),
                               ('SEK', 'SUÉCIA - COROA SUECA'),
                               ('CHF', 'SUÍÇA - FRANCO SUÍÇO'),
                               ('TWD', 'TAIWAN - DÓLAR TAIWANÊS')
                           ])
    confirmation_button = SubmitField("Cadastrar")


class FormDelete(FlaskForm):
    delete_button = SubmitField("Excluir")
