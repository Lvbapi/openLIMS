from datetime import datetime
from src.procedures.models import Procedures
from src.projects.models import Projects
from src import app


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.context_processor
def get_projects():
	return {'get_projects': Projects.query.all()}
