# Import flask dependencies
from flask import (
    Blueprint, request, render_template,
    redirect, url_for)
from src import db
import src.projects.models as ProjectsModels
import src.projects.forms as ProjectsForms
from flask_admin import helpers
from src.helpers.decorators import check_login, check_admin

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('/', methods=['GET'])
@check_login
def index():
    projects = ProjectsModels.Projects.query.all()
    attributes = ProjectsModels.ProjectsAttribute.query.all()
    return render_template("/projects/index.html", projects=projects, attributes=attributes)


@projects.route('/<int:project_id>', methods=['GET'])
@check_login
def view(project_id):
    project = ProjectsModels.Projects.query.get(project_id)
    return render_template("/projects/view.html", project=project)


@projects.route('/add', methods=['GET', 'POST'])
@check_login
def add():
    attributes = ProjectsModels.ProjectsAttribute.query.all()
    form = ProjectsForms.AddProjects(request.form)
    if request.method == 'POST':
        project = ProjectsModels.Projects()
        form.populate_obj(project)
        db.session.add(project)
        db.session.flush()
        for attribute in attributes:
            project_attribute = ProjectsModels.ProjectsValue()
            project_attribute.projects_id = project.id
            project_attribute.projects_attribute_id = attribute.id
            project_attribute.value = request.form.get(attribute.name)
            db.session.add(project_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('projects.index'))

    return render_template("projects/add_or_edit.html", form=form, attributes=attributes)


@projects.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit(project_id):
    attributes = ProjectsModels.ProjectsAttribute.query.all()
    project = ProjectsModels.Projects.query.get(project_id)
    form = ProjectsForms.EditProjectsForm(request.form, obj=project)
    if request.method == 'POST':
        form.populate_obj(project)
        db.session.add(project)
        db.session.flush()
        for attribute in attributes:
            project_attribute = ProjectsModels.ProjectsValue.get_by_uniq_const(project_id, attribute.id)
            if not project_attribute:
                project_attribute = ProjectsModels.ProjectsValue()
            project_attribute.projects_id = project.id
            project_attribute.projects_attribute_id = attribute.id
            project_attribute.value = request.form.get(attribute.name)
            db.session.add(project_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('projects.index'))

    return render_template("projects/add_or_edit.html", form=form, attributes=attributes, edit=1, project=project)


@projects.route('/delete/<int:project_id>', methods=['GET'])
@check_login
@check_admin
def delete(project_id):
    project = ProjectsModels.Projects.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects.index'))


@projects.route('/attribute/add', methods=['GET', 'POST'])
@check_login
def attribute_add():
    form = ProjectsForms.AddProjectsAttribute(request.form)
    if helpers.validate_form_on_submit(form):
        attribute = ProjectsModels.ProjectsAttribute()
        form.populate_obj(attribute)
        db.session.add(attribute)
        db.session.commit()
        return redirect(url_for('projects.index'))

    return render_template("projects/add_or_edit_attribute.html", form=form)


@projects.route('/attribute/edit/<int:project_attribute_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def attribute_edit(project_attribute_id):
    project_attribute = ProjectsModels.ProjectsAttribute.query.get(project_attribute_id)
    form = ProjectsForms.EditProjectsAttribute(request.form, obj=project_attribute)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(project_attribute)
        db.session.add(project_attribute)
        db.session.commit()
        return redirect(url_for('projects.index'))

    return render_template("projects/add_or_edit_attribute.html", form=form, edit=1, project_attribute_id=project_attribute_id)


@projects.route('/attribute/delete/<int:project_attribute_id>', methods=['GET'])
@check_login
@check_admin
def attribute_delete(project_attribute_id):
    project_attribute = ProjectsModels.ProjectsAttribute.query.get_or_404(project_attribute_id)
    db.session.delete(project_attribute)
    db.session.commit()
    return redirect(url_for('projects.index'))
