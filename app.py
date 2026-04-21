from flask import Flask, render_template, request, send_from_directory
import logging

app = Flask(__name__)

logging.basicConfig(filename = 'honeypot.log',
                    level = logging.INFO,
                    format = '%(asctime)s - %(message)s',
                    force = True)

# reusable log helper 
def log_visit(path):
    logging.info(f"Hit: {path} | IP: {request.remote_addr} | Method: {request.method}")
    for handler in logging.getLogger().handlers:
        handler.flush()

@app.route('/')
def home():
    log_visit('/')
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    log_visit('/login')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.info(f"Login attempt from user: {username} & pwd: {password}")
        for h in logging.getLogger().handlers:
            h.flush()
    return render_template('login.html')

@app.route('/admin')
def admin():
    log_visit('/admin')
    return render_template('admin.html')

@app.route('/patient-records')
def patient_records():
    log_visit('/patient-records')
    return render_template('patient_records.html')

@app.route('/files/<path:filename>')
def static_files(filename):
    log_visit(f'/files/{filename}')
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug = True)