from flask import Flask, render_template
from datetime import datetime
import logging
import re
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

@app.route('/dashboard')
def dashboard():
    hits = []
    login_attempts_list = []
    alerts = []
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
                    ips.add(ip)

                if '/healthcare' in path:
                    profile = 'healthcare'
                elif '/lawfirm' in path:
                    profile = 'lawfirm'
                elif '/research' in path:
                    profile = 'research'
                else:
                    profile = 'unknown'

                hits.append({ 'timestamp': timestamp,
                              'ip': ip,
                              'path': path,
                              'method': method,
                              'profile': profile })
            
            if 'Login attempt' in line:
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
            for ip in ips:
                recent = [l for l in login_attempts_list if l['ip'] == ip]
                if len(recent) >= 5:
                    alerts.append(f"Alert!: {ip} made {len(recent)} login attempts")
        
    except FileNotFoundError:
        pass

    return render_template('dashboard.html',
                           hits = hits[-50:],
                           total_hits = len(hits),
                           login_attempts = len(login_attempts_list),
                           login_attempts_list = login_attempts_list[-20:],
                           unique_ips = len(ips),
                           alerts = alerts,
                           alert_count = len(alerts))

if __name__ == '__main__':
    app.run(debug = True)