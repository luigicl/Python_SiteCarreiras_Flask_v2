from flask import Flask, render_template, url_for, jsonify
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__)


@app.route("/")
def homepage():
    jobs_list = load_jobs_from_db()
    return render_template("home.html", vagas=jobs_list)


@app.route("/vagas")
def listar_vagas():
    jobs_list = load_jobs_from_db()
    return jsonify(jobs_list)


@app.route("/vaga/<id>")
def mostrar_vaga(id):
    vaga = load_job_from_db(id)
    return render_template("vaga.html", vaga=vaga)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
