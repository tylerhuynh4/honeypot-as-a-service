from flask import Blueprint, render_template, request, send_from_directory 
import logging

healthcare = Blueprint('healthcare', __name__)

# reusable log helper
def log_visit(path):
    msg = f"Hit: {path} | IP: {request.remote_addr} | Method: {request.method}"
    logging.info(msg)
    for h in logging.getLogger().handlers:
        h.flush()

@healthcare.route('/')
def home():
    log_visit('/')
    return render_template('healthcare/login.html')

@healthcare.route('/login', methods = ['GET', 'POST'])
def login():
    log_visit('/login')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Login attempt | user: {username} | password: {password}")
        for h in logging.getLogger().handlers:
            h.flush()
    return render_template('healthcare/login.html')

@healthcare.route('/admin')
def admin():
    log_visit('/admin')
    return render_template('healthcare/admin.html')

@healthcare.route('/patient-records')
def patient_records():
    log_visit('/patient-records')
    return render_template('healthcare/patient_records.html')

@healthcare.route('/files/<path:filename>')
def files(filename):
    log_visit(f'/files/{filename}')
    return send_from_directory('static/healthcare', filename)