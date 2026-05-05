from flask import Flask
import logging
from profiles.healthcare import healthcare

app = Flask(__name__)

logging.basicConfig(filename = 'honeypot.log',
                    level = logging.INFO,
                    format = '%(asctime)s - %(message)s',
                    force = True)

app.register_blueprint(healthcare)

if __name__ == '__main__':
    app.run(debug = True)