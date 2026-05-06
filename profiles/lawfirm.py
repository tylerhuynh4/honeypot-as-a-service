from flask import Blueprint, render_template, request, send_from_directory 
import logging 

lawfirm = Blueprint('lawfirm', __name__)

# reusable logger
def log_visit(path):
    msg = f"Hit: /lawfirm{path} | IP: {request.remote_addr} | Method: {request.method}"
    logging.info(msg)
    for h in logging.getLogger().handlers:
        h.flush()

@lawfirm.route('/', strict_slashes = False)
def home():
    log_visit('/')
    return render_template('lawfirm/login.html')

@lawfirm.route('/login', methods = ['GET', 'POST'])
def login():
    log_visit('/login')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Login attempt | profile: lawfirm | IP: {request.remote_addr} | user: {username} | password: {password}")
        for h in logging.getLogger().handlers:
            h.flush()
    return render_template('lawfirm/login.html')

@lawfirm.route('/client-portal')
def client_portal():
    log_visit('/client-portal')
    return render_template('lawfirm/client_portal.html')

@lawfirm.route('/case-files')
def case_files():
    log_visit('/case-files')
    return render_template('lawfirm/case_files.html')

@lawfirm.route('/admin')
def admin():
    log_visit('/admin')
    return render_template('lawfirm/admin.html')

@lawfirm.route('/contracts')
def contracts():
    log_visit('/contracts')
    return render_template('lawfirm/contracts.html')

@lawfirm.route('/archive')
def archive():
    log_visit('/archive')
    return render_template('lawfirm/archive.html')

@lawfirm.route('/client-list')
def client_list():
    log_visit('/client-list')
    return render_template('lawfirm/client_list.html')

@lawfirm.route('/.env')
def env():
    log_visit('/.env')
    return send_from_directory('static/lawfirm', '.env')


@lawfirm.route('/document-upload', methods = ['GET', 'POST'])
def document_upload():
    log_visit('/document-upload')
    if request.method == 'POST':
        # doesn't actually save anything
        filename = request.files.get('file').filename if 'file' in request.files else 'unknown'
        logging.info(f"Document upload attempt | profile: lawfirm | IP: {request.remote_addr} | filename: {filename}")
    return render_template('lawfirm/document_upload.html')

@lawfirm.route('/firm-files/<path:filename>')
def files(filename):
    log_visit(f'/firm-files/{filename}')
    as_attachment = filename.endswith('.pdf')
    return send_from_directory('static/lawfirm', filename, as_attachment = as_attachment)