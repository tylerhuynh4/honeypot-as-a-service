from flask import Flask, render_template, request
import logging

app = Flask(__name__)

logging.basicConfig(filename='honeypot.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    force=True)

# reusable log helper 
def log_visit(path):
    logging.info(f"Hit: {path} | IP: {request.remote_addr} | Method: {request.method}")
    for handler in logging.getLogger().handlers:
        handler.flush()

@app.route('/')
def home():
    log_visit('/')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    log_visit('/login')
    return render_template('login.html')

@app.route('/admin')
def admin():
    log_visit('/admin')
    return render_template('admin.html')

@app.route('/patient-records')
def patient_records():
    log_visit('/patient-records')
    return render_template('patient_records.html')

if __name__ == '__main__':
    app.run(debug = True)