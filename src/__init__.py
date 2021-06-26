from flask import Flask
import os
from flask_htmlmin import HTMLMIN
from flask_sqlalchemy import SQLAlchemy

__version__ = (0, 0, 1, 'alpha')


def create_app(TESTING=False):
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['TESTING'] = TESTING

    return app



application = app = create_app()
db = SQLAlchemy(app)

HTMLMIN(app)

import src.site.models as SiteModels
import src.projects.models as ProjectsModels
import src.procedures.models as ProceduresModels
import src.parameters.models as ParametersModels
import src.specimens.models as SpecimensModels
import src.schedules.models as SchedulesModels
import src.auth.models as AuthModels

db.create_all()

from src.blueprints import register_blueprints

register_blueprints(app)


from src.helpers import filters, processors, decorators, error_handlers

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])