#!/usr/bin/env python
import os
from flask import Flask
from config import app_config


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(app_config.get(env))

    from harvestapi.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/harvest')

    from harvestapi.model import db
    db.init_app(app)

    return app


env_name = os.getenv('FLASK_ENV')
application = create_app(env_name)

if __name__ == "__main__":
    apps = application
    apps.run()


