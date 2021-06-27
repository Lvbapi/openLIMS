# Import flask dependencies
import os
from flask import (
    Blueprint, request, render_template,
    redirect, url_for, jsonify)
from src import db, app
import src.site.models as SiteModels
import src.site.forms as SiteForms
from src.schedules.models import Schedules
from flask_admin import helpers
from werkzeug.utils import secure_filename
from src.helpers.decorators import check_login, check_admin
from src.helpers.utils import slugify, get_iqr_range
from flask_login import current_user
from src.procedures.models import Procedures
from src.parameters.models import Parameters


site = Blueprint('site', __name__, url_prefix='')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@site.route('/', methods=['GET'])
def index():
    return render_template("/site/welcome.html")


@site.route('/dashboard', methods=['GET'])
@check_login
def dashboard():
    data = {'projects': SiteModels.Projects.query.all(), 'schedules': Schedules().get_user_schedule(current_user.get_id())}
    return render_template("/site/dashboard.html", data=data)


@site.route('/experiments/', methods=['GET'])
@check_login
def experiments():
    experiments = SiteModels.Experiments.query.all()
    attributes = SiteModels.ExperimentsAttribute.query.all()
    if request.args.get('ajax'):
        data = []
        for experiment in experiments:
            data_set = [experiment.get_datetime().strftime('%m/%d/%Y %H:%M'),
                experiment.get_project().name,
                experiment.get_procedure().name,
                experiment.get_specimen().name]
            for attribute in attributes:
                data_set.append(experiment.attributes.get(attribute.name).value)
            data_set.append(render_template('/site/experiments/view_data.html', experiment_id=experiment.id))
            data.append(data_set)
        return jsonify({'data': data})
    return render_template("/site/experiments/index.html", experiments=experiments, attributes=attributes)


@site.route('/experiments/<int:experiment_id>', methods=['GET'])
@check_login
def experiments_view(experiment_id):
    experiment = SiteModels.Experiments.query.get(experiment_id)
    return render_template("/site/experiments/view.html", experiment=experiment)


@site.route('/data/collect/<int:schedule_id>/', methods=['GET', 'POST'])
@check_login
def collect_data(schedule_id):
    schedule = Schedules.query.get(schedule_id)
    if request.method == 'POST':
        for specimen in schedule.specimens:
            experiment = SiteModels.Experiments()
            experiment.schedule_id = schedule_id
            experiment.specimen_id = specimen.id
            experiment.project_id = schedule.get_project_id()
            experiment.procedure_id = schedule.procedure_id
            db.session.add(experiment)
            db.session.flush()
            for parameter in schedule.get_procedure().parameters:
                datapoint = SiteModels.DataPoints()
                data_type = parameter.get_datatype()
                
                if data_type == 'File':
                    classInstance = datapoint.get_class_by_string(data_type)
                    file = request.files.get('[' + parameter.name + '][' + str(specimen.id) + ']')
                    if file and allowed_file(file.filename):
                        slug = slugify(experiment.get_procedure().name) + "/"
                        if not os.path.exists(app.config['UPLOAD_FOLDER'] + slug):
                            os.makedirs(app.config['UPLOAD_FOLDER'] + slug)
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + slug, filename))
                        classInstance.value = slug + filename
                    else:
                        classInstance.value = None
                else:
                    data_value = request.form.get('[' + parameter.name + '][' + str(specimen.id) + ']')
                    classInstance = datapoint.get_by_value(data_type, data_value)
                    
                    if not classInstance:
                        classInstance = datapoint.get_class_by_string(data_type)

                        if data_type == 'Option':
                            classInstance.option_id = data_value
                        else:
                            classInstance.value = data_value

                        db.session.add(classInstance)
                        db.session.flush()
                    datapoint.experiment_id = experiment.id
                    datapoint.parameter_id = parameter.id
                    datapoint.data_point_id = classInstance.id
                    db.session.add(datapoint)
                    db.session.flush()
        db.session.commit()
        return redirect(url_for('schedules.view', schedule_id=schedule_id))
        
    return render_template("/site/collect_data.html", schedule=schedule)


@site.route('/data/<int:procedure_id>/', methods=['GET'])
@check_login
def procedure_data(procedure_id):
    experiments = SiteModels.Experiments.get_by_procedure(procedure_id)
    procedure = Procedures.query.get(procedure_id)
    if request.args.get('ajax'):
        data = []
        for experiment in experiments:
            data_set = [experiment.get_specimen().name]
            for data_point in experiment.data_points:
                data_set.append(str(data_point.get_value()))
            data.append(data_set)
        return jsonify({'data': data})
    return render_template("/site/procedure_data.html", experiments=experiments, procedure=procedure)


@site.route('/outliers/<int:parameter_id>/', methods=['GET'])
@check_login
def outliers(parameter_id):
    parameter = Parameters.query.get(parameter_id)
    data_points = []
    for point in parameter.data_points:
        data_points.append(float(point.get_value()))
    data = get_iqr_range(data_points)
    return render_template("/site/outliers.html", data=data, parameter=parameter)
