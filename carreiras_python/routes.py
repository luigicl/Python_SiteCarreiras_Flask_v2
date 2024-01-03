from flask import Flask, render_template, jsonify, redirect, url_for, request
from carreiras_python import app
from carreiras_python.database import (load_jobs_from_db, load_job_from_db, add_application_to_db, load_applications,
                                       jobs_search)
from carreiras_python.forms import FormApplication, FormSearchApplications, FormSearchJobs
from datetime import datetime
from .gdrive_api_methods import GoogleDriveService

# Making FormSearchJobs available to NAVBAR (all templates, actually)
@app.context_processor
def inject_search_form():
    form = FormSearchJobs()
    return dict(form=form)


@app.route("/")
def homepage():
    jobs_list = load_jobs_from_db()
    return render_template("home.html", jobs=jobs_list)


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
        data = formApplication
        resume_file = formApplication.resume.data
        date = datetime.now()
        file_name = formApplication.email.data + "_" + date.strftime("%Y%m%d%H%M%S") + "_jobID_" + str(job['id'])
        # uploaded_resume_id = upload_file(resume_file, file_name)
        uploaded_resume_id = GoogleDriveService().upload_file(resume_file, file_name)
        add_application_to_db(id, data, date, job['title'], uploaded_resume_id)
        return render_template("apply_confirmation.html", application=data, job=job, date=date)
    return render_template("application_form.html", form=formApplication, job=job)


@app.route("/buscar_inscricoes", methods=["GET", "POST"])
def search_applications():
    formSearchApplications = FormSearchApplications()
    if formSearchApplications.validate_on_submit():
        email = request.form['email']  # executa após submeter o formulário
        applications = my_applications(email)
        return render_template("my_applications.html", applications=applications)
    return render_template("load_applications.html", form=formSearchApplications)


def my_applications(email):
    applications = load_applications(email)
    return applications


@app.route("/busca", methods=["POST"])
def search_jobs():
    form = FormSearchJobs()
    if form.validate_on_submit():
        searched_terms = form.search.data
        jobs = jobs_search(searched_terms)
        return render_template('search.html', form=form, jobs=jobs)
    if not form.validate_on_submit():
        return render_template('search.html', form=form, jobs="")
