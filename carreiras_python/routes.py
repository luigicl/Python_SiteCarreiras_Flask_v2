import json
from flask import Flask, render_template, jsonify, redirect, url_for, request, session
from carreiras_python import app
from carreiras_python.database import (load_jobs_from_db, load_job_from_db, add_application_to_db, load_my_applications,
                                       jobs_search, add_new_job_to_db, delete_a_job, delete_a_application,
                                       load_applications_from_db, load_application_by_id, check_application)
from carreiras_python.forms import FormApplication, FormSearchApplications, FormSearchJobs, FormCreateJob, FormDelete
from datetime import datetime
from carreiras_python.gdrive_api_methods import GoogleDriveService


# Making FormSearchJobs available to NAVBAR (all templates, actually)
@app.context_processor
def inject_search_form():
    form = FormSearchJobs()
    return dict(form=form)


@app.route("/")
def homepage():
    jobs_list = load_jobs_from_db()
    return render_template("home.html", jobs=jobs_list, button_name="Detalhes")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/admin/cadastrar_vaga", methods=["GET", "POST"])
def create_job():
    formCreateJob = FormCreateJob(currency=None)  # setting a default value when instantiating
    if formCreateJob.validate_on_submit():
        date = datetime.now()
        add_new_job_to_db(formCreateJob, date)
        message = "Vaga cadastrada com sucesso"
        formCreateJob = FormCreateJob(formdata=None)
        return render_template("create_job.html", form=formCreateJob, message=message)
    return render_template("create_job.html", form=formCreateJob)


@app.route("/admin/excluir_vaga", methods=["GET", "POST"])
def jobs_to_delete():
    jobs_list = load_jobs_from_db()
    message = session.get('message', None)
    session.pop('message', None)
    return render_template("delete_job.html", jobs=jobs_list, button_name="Excluir",
                           message=message)


@app.route("/admin/excluir_vaga/excluir")
def delete_job():
    job_id = request.args.get("job_to_delete")
    if job_id:
        delete_a_job(job_id)
        session['message'] = job_id
        return redirect(url_for("jobs_to_delete"))


@app.route("/admin/excluir_inscricao/excluir")
def delete_application():
    application_id = request.args.get("application_to_delete")
    resume_id = request.args.get("resume_id")
    if application_id:
        application = load_application_by_id(application_id)
        email = application[0]['email']
        delete_a_application(application_id, resume_id)
        applications = my_applications(email)
        if applications:
            message = "Inscrição removida com sucesso."
            return render_template("my_applications.html", applications=applications, message=message)
        else:
            return redirect(url_for("search_applications"))


@app.route("/vagas")
def list_jobs():
    jobs_list = load_jobs_from_db()
    return jsonify(jobs_list)


@app.route("/vaga/<id>", methods=["GET", "POST"])
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Vaga não encontrada", 404
    return render_template("job_page.html", job=job)


@app.route("/inscricao/<id>", methods=["GET", "POST"])
def apply_to_job(id):
    job = load_job_from_db(id)
    formApplication = FormApplication()
    if formApplication.validate_on_submit():  # executa após submeter o formulário
        is_subscribed = check_application(id, formApplication.email.data)
        if is_subscribed:
            message = "Já existe uma inscrição para esta vaga com este e-mail."
            return render_template("application_form.html", form=formApplication, job=job, message=message)
        else:
            resume_file = formApplication.resume.data
            date = datetime.now()
            file_name = formApplication.email.data + "_" + date.strftime("%Y%m%d%H%M%S") + "_jobID_" + str(job['id'])
            if resume_file:
                uploaded_resume_id = GoogleDriveService().upload_file(resume_file, file_name)
            else:
                uploaded_resume_id = ""
            add_application_to_db(id, formApplication, date, job['title'], uploaded_resume_id)
            return render_template("apply_confirmation.html", application=formApplication, job=job, date=date)
    return render_template("application_form.html", form=formApplication, job=job)


@app.route("/buscar_inscricoes", methods=["GET", "POST"])
def search_applications():
    formSearchApplications = FormSearchApplications()
    message = session.get('message', None)
    session.pop('message', None)
    if formSearchApplications.validate_on_submit():
        email = request.form['email']  # executa após submeter o formulário
        applications = my_applications(email)
        return render_template("my_applications.html", applications=applications)
    return render_template("load_my_applications.html", form=formSearchApplications, message=message)


def my_applications(email):
    applications = load_my_applications(email)
    return applications


@app.route("/busca", methods=["POST"])
def search_jobs():
    form = FormSearchJobs()
    if form.validate_on_submit():
        searched_terms = form.search.data
        jobs = jobs_search(searched_terms)
        return render_template('search.html', form=form, jobs=jobs, button_name="Detalhes")
    if not form.validate_on_submit():
        return render_template('search.html', form=form, jobs="")


@app.route("/admin/candidaturas")
def list_applications():
    applications_list = load_applications_from_db()
    return render_template("load_all_applications.html", applications=applications_list)
