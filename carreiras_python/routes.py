from flask import Flask, render_template, jsonify, redirect, url_for
from carreiras_python import app
from carreiras_python.database import load_jobs_from_db, load_job_from_db
from carreiras_python.forms import FormLogin


@app.route("/")
def homepage():
    jobs_list = load_jobs_from_db()
    return render_template("home.html", vagas=jobs_list)


@app.route("/vagas")
def listar_vagas():
    jobs_list = load_jobs_from_db()
    return jsonify(jobs_list)


@app.route("/vaga/<id>", methods=["GET", "POST"])
def mostrar_vaga(id):
    # vaga = load_job_from_db(id)
    # if not vaga:
    #     return "Vaga não encontrada", 404
    # return render_template("includes/job_page.html", vaga=vaga)
    vaga = load_job_from_db(id)
    if not vaga:
        return "Vaga não encontrada", 404
    return render_template("job_page.html", vaga=vaga)


@app.route("/inscricao/<id>", methods=["GET", "POST"])
def fazer_inscricao(id):
    vaga = load_job_from_db(id)

    formlogin = FormLogin()

    if formlogin.validate_on_submit():  # executa após submeter o formulário
        return render_template("includes/teste.html")
    # if not formlogin.validate_on_submit():
    #     return render_template("job_page.html", form=formlogin, vaga=vaga, scroll="inscricao")
    jobs_list = load_jobs_from_db()
    return render_template("apply.html", form=formlogin, vaga=vaga, scroll='inscricao')


@app.route("/teste")
def teste():
    return render_template("teste.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
