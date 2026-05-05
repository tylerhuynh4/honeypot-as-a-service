from flask import Blueprint, render_template, request, send_from_directory
import logging

researchlab = Blueprint('researchlab', __name__)

def log_visit(path):
    msg = f"Hit: {path} | IP: {request.remote_addr} | Method: {request.method}"
    logging.info(msg)
    for h in logging.getLogger().handlers:
        h.flush()

@researchlab.route('/login', methods = ['GET', 'POST'])
def login():
    log_visit('/login')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Login attempt | user: {username} | password: {password}")
        for h in logging.getLogger().handlers:
            h.flush()
    return render_template('researchlab/login.html')

@researchlab.route('/admin')
def admin():
    log_visit('/admin')
    return render_template('researchlab/admin.html')

@researchlab.route('/datasets')
def datasets():
    log_visit('/datasets')
    return render_template('researchlab/datasets.html')

@researchlab.route('/models')
def models():
    log_visit('/models')
    return render_template('researchlab/models.html')

@researchlab.route('/lab-files/<path:filename>')
def files(filename):
    log_visit(f'/lab-files/{filename}')
    as_attachment = filename.endswith('.pdf')
    return send_from_directory('static/researchlab', filename, as_attachment = as_attachment)