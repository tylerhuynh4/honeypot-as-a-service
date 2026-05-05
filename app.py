from flask import Flask
import logging
from profiles.healthcare import healthcare
from profiles.lawfirm import lawfirm

app = Flask(__name__)

logging.basicConfig(filename = 'honeypot.log',
                    level = logging.INFO,
                    format = '%(asctime)s - %(message)s',
                    force = True)

app.register_blueprint(healthcare, url_prefix = '')
app.register_blueprint(lawfirm, url_prefix = '/lawfirm')

if __name__ == '__main__':
    app.run(debug = True)