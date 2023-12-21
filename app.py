from flask import Flask, render_template, url_for, jsonify
from sqlalchemy import text
from database import engine

app = Flask(__name__)

# vagas = [
#     {
#         'id': 1,
#         'titulo': 'Analista de Dados',
#         'localidade': 'SC, Brasil',
#         'salario': 'R$ 5.000'
#     },
#     {
#         'id': 2,
#         'titulo': 'Engenheiro de Dados',
#         'localidade': 'SP, Brasil',
#         'salario': 'R$ 10.000'
#     },
#     {
#         'id': 3,
#         'titulo': 'Desenvolvedor Frontend',
#         'localidade': 'SP, Brasil',
#         'salario': 'R$ 3.000'
#     },
#     {
#         'id': 4,
#         'titulo': 'Desenvolvedor Backend',
#         'localidade': 'RJ, Brasil',
#         'salario': 'R$ 4.000'
#     },
#     {
#         'id': 5,
#         'titulo': 'Desenvolvedor Python',
#         'localidade': 'SP, Brasil',
#         'salario': 'R$ 50.000'
#     }
# ]

def load_jobs_from_db():
    with engine.connect() as conn:
        jobs = []
        result = conn.execute(text("SELECT * from jobs"))
        for row in result.all():
            jobs.append(row._asdict())
        return jobs


@app.route("/")
def homepage():
    jobs_list = load_jobs_from_db()
    return render_template("home.html", vagas=jobs_list)


@app.route("/vagas")
def lista_vagas():
    # return jsonify(vagas)
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
