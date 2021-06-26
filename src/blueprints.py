from src.admin.controllers import admin as admin_module
from src.auth.controllers import auth as auth_module
from src.site.controllers import site as site_module
from src.projects.controllers import projects as projects_module
from src.schedules.controllers import schedules as schedules_module
from src.specimens.controllers import specimens as specimens_module
from src.procedures.controllers import procedures as procedures_module
from src.parameters.controllers import parameters as parameters_module


def register_blueprints(app):
    app.register_blueprint(site_module)
    app.register_blueprint(projects_module)
    app.register_blueprint(procedures_module)
    app.register_blueprint(parameters_module)
    app.register_blueprint(schedules_module)
    app.register_blueprint(specimens_module)
    app.register_blueprint(auth_module)
    app.register_blueprint(admin_module)
