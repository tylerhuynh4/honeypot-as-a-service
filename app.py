from flask import Flask
import logging
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

if __name__ == '__main__':
    app.run(debug = True)