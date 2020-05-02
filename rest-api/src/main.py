from flask import Flask
from flask_cors import CORS

from models import init_models
from routes import init_routes

def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some-secret-key'

    cors = CORS(app)
    app.run()

if __name__ == "__main__":
    main()