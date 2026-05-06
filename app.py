from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import logging
import re
import os
from profiles.healthcare import healthcare
from profiles.lawfirm import lawfirm
from profiles.researchlab import researchlab

app = Flask(__name__)

logging.basicConfig(filename = 'honeypot.log',
                    level = logging.INFO,
                    format = '%(asctime)s - %(message)s',
                    force = True)

app.register_blueprint(healthcare, url_prefix = '/healthcare')
app.register_blueprint(lawfirm, url_prefix = '/lawfirm')
app.register_blueprint(researchlab, url_prefix = '/researchlab')

def parse_logs(profile_filter = None):
    hits = []
    login_attempts_list = []
    ips = set()

    try:
        with open('honeypot.log', 'r') as f:
            lines = f.readlines()

        for line in lines:
            if 'Hit:' in line:
                parts = line.strip().split(' - ', 1)
                if len(parts) < 2:
                    continue
                timestamp = parts[0]
                msg = parts[1]

                ip_match = re.search(r'IP: ([\d\.]+)', msg)
                path_match = re.search(r'Hit: (\S+)', msg)
                method_match = re.search(r'Method: (\S+)', msg)

                if ip_match and path_match and method_match:
                    ip = ip_match.group(1)
                    path = path_match.group(1)
                    method = method_match.group(1)

                    if profile_filter and profile_filter not in path:
                        continue
                    ips.add(ip)

                    if '/healthcare' in path:
                        profile = 'healthcare'
                    elif '/lawfirm' in path:
                        profile = 'lawfirm'
                    elif '/researchlab' in path:
                        profile = 'researchlab'
                    else:
                        profile = 'unknown'
                    
                    hits.append({ 'timestamp': timestamp,
                                  'ip': ip,
                                  'path': path,
                                  'method': method,
                                  'profile': profile })
                    
            if 'Login attempt' in line:
                profile_check = f'profile: {profile_filter}' if profile_filter else None
                if profile_check and profile_check not in line:
                    continue

                parts = line.strip().split(' - ', 1)
                if len(parts) < 2:
                    continue
                timestamp = parts[0]
                msg = parts[1]

                ip_match = re.search(r'IP: ([\d\.]+)', msg)
                user_match = re.search(r'user: (\S+)', msg)
                pass_match = re.search(r'password: (.+)', msg)
                
                if user_match and pass_match:
                    login_attempts_list.append({ 'timestamp': timestamp, 
                                                 'ip': ip_match.group(1) if ip_match else 'unknown', 
                                                 'username': user_match.group(1),
                                                 'password': pass_match.group(1) })
    except FileNotFoundError:
        pass
    return hits, login_attempts_list, ips

# severity
def build_alerts(hits, login_attempts_list, ips):
    alerts = []
    ip_hit_counts = {}

    for hit in hits:
        ip = hit['ip']
        path = hit['path']
        ip_hit_counts[ip] = ip_hit_counts.get(ip, 0) + 1

        if any(x in path for x in ['/.env', '/backup.sql', '/config.json', '/db_dump.zip']):
            alerts.append({ 'severity': 'HIGH',
                            'msg': f"{ip} accessed sensitive file: {path}" })
        
        if path.endswith('/admin'):
            alerts.append({ 'severity': 'MEDIUM',
                            'msg': f"{ip} probed admin panel: {path}" })
        
        if any(path.endswith(x) for x in ['.zip', '.sql', '.csv', '.pt']):
            alerts.append({ 'severity': 'MEDIUM',
                            'msg': f"{ip} downloaded file: {path}" })
            
    for ip in ips:
        recent_logins = [l for l in login_attempts_list if l['ip'] == ip]
        if len(recent_logins) >= 5:
            alerts.append({ 'severity': 'HIGH',
                            'msg': f"{ip} made {len(recent_logins)} login attempts" })
    
    for ip, count in ip_hit_counts.items():
        if count >= 3:
            alerts.append({ 'severity': 'LOW',
                            'msg': f"{ip} made {count} requests" })
        
    alerts = sorted(alerts, key = lambda x: ['HIGH', 'MEDIUM', 'LOW'].index(x['severity']))
    return alerts

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    hits, login_attempts_list, ips = parse_logs()
    alerts = build_alerts(hits, login_attempts_list, ips)
    
    return render_template('dashboard.html',
                           hits = hits[-50:],
                           total_hits = len(hits),
                           login_attempts = len(login_attempts_list),
                           login_attempts_list = login_attempts_list[-20:],
                           unique_ips = len(ips),
                           alerts = alerts,
                           alert_count = len(alerts))

@app.route('/dashboard/healthcare')
def dashboard_healthcare():
    hits, login_attempts_list, ips = parse_logs('healthcare')
    alerts = build_alerts(hits, login_attempts_list, ips)

    return render_template('dashboard_healthcare.html',
                           hits = hits[-50:],
                           total_hits = len(hits),
                           login_attempts = len(login_attempts_list),
                           login_attempts_list = login_attempts_list[-20:],
                           unique_ips = len(ips),
                           alerts = alerts,
                           alert_count = len(alerts))

@app.route('/dashboard/lawfirm')
def dashboard_lawfirm():
    hits, login_attempts_list, ips = parse_logs('lawfirm')
    alerts = build_alerts(hits, login_attempts_list, ips)

    return render_template('dashboard_lawfirm.html',
                           hits = hits[-50:],
                           total_hits = len(hits),
                           login_attempts = len(login_attempts_list),
                           login_attempts_list = login_attempts_list[-20:],
                           unique_ips = len(ips),
                           alerts = alerts,
                           alert_count = len(alerts))

@app.route('/dashboard/researchlab')
def dashboard_researchlab():
    hits, login_attempts_list, ips = parse_logs('researchlab')
    alerts = build_alerts(hits, login_attempts_list, ips)

    return render_template('dashboard_researchlab.html',
                           hits = hits[-50:],
                           total_hits = len(hits),
                           login_attempts = len(login_attempts_list),
                           login_attempts_list = login_attempts_list[-20:],
                           unique_ips = len(ips),
                           alerts = alerts,
                           alert_count = len(alerts))

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug = debug)