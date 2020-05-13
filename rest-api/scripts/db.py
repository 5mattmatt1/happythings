#!/usr/bin/python3

import os
from argparse import ArgumentParser

from flask import Flask
from flask_migrate import init, migrate, upgrade

from dotenv import load_dotenv

import sys

# TODO: Bit clunky to call from anywhere other than top level...
sys.path.extend(["src"])

from models import init_models
from routes import init_routes

def main():
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'some-secret-key'

    init_models(app)
    with app.app_context():
        argparser = ArgumentParser()
        argparser.add_argument('command', choices=['init', 'migrate', 'upgrade'])
        vargs = argparser.parse_args()
        
        if vargs.command == 'init':
            init()
        elif vargs.command == 'migrate':
            migrate()
        elif vargs.command == 'upgrade':
            upgrade()

if __name__ == "__main__":
    main()