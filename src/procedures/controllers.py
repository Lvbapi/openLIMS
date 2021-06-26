# Import flask dependencies
import os
from flask import (
    Blueprint, request, render_template,
    redirect, url_for)
from src import db
import src.procedures.models as ProcedureModels
import src.procedures.forms as ProcedureForms
from flask_admin import helpers
from src.helpers.decorators import check_login, check_admin


procedures = Blueprint('procedures', __name__, url_prefix='/procedures')


@procedures.route('/', methods=['GET'])
@check_login
def index():
    procedures = ProcedureModels.Procedures.query.all()
    attributes = ProcedureModels.ProceduresAttribute.query.all()
    return render_template("procedures/index.html", procedures=procedures, attributes=attributes)


@procedures.route('/<int:procedure_id>', methods=['GET'])
@check_login
def view(procedure_id):
    procedure = ProcedureModels.Procedures.query.get(procedure_id)
    return render_template("procedures/view.html", procedure=procedure)


@procedures.route('/add', methods=['GET', 'POST'])
@check_login
def add():
    attributes = ProcedureModels.ProceduresAttribute.query.all()
    form = ProcedureForms.AddProcedures(request.form)
    if request.method == 'POST':
        procedure = ProcedureModels.Procedures()
        procedure.project_id = request.form.get('project_id')
        procedure.name = request.form.get('name')
        procedure.description = request.form.get('description')
        db.session.add(procedure)
        db.session.flush()
        for attribute in attributes:
            procedure_attribute = ProcedureModels.ProceduresValue()
            procedure_attribute.procedures_id = procedure.id
            procedure_attribute.procedures_attribute_id = attribute.id
            procedure_attribute.value = request.form.get(attribute.name)
            db.session.add(procedure_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('procedures.index'))

    return render_template("procedures/add_or_edit.html", form=form, attributes=attributes)


@procedures.route('/edit/<int:procedure_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit(procedure_id):
    attributes = ProcedureModels.ProceduresAttribute.query.all()
    procedure = ProcedureModels.Procedures.query.get(procedure_id)
    form = ProcedureForms.EditProcedure(request.form, obj=procedure)
    if request.method == 'POST':
        procedure.start_datetime = request.form.get('start_datetime')
        procedure.end_datetime = request.form.get('end_datetime')
        procedure.procedure_id = request.form.get('procedure_id')
        for specimen in request.form.getlist('specimens'):
            procedure.specimens.append(Specimens.query.get(specimen))
        for user in request.form.getlist('users'):
            procedure.users.append(User.query.get(user))
        db.session.add(procedure)
        db.session.flush()
        for attribute in attributes:
            procedure_attribute = ProcedureModels.ProceduresValue.get_by_uniq_const(procedure_id, attribute.id)
            if not procedure_attribute:
                procedure_attribute = ProcedureModels.ProceduresValue()
            procedure_attribute.procedures_id = procedure.id
            procedure_attribute.procedures_attribute_id = attribute.id
            procedure_attribute.value = request.form.get(attribute.name)
            db.session.add(procedure_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('procedures.index'))

    return render_template("procedures/add_or_edit.html", form=form, attributes=attributes, edit=1, procedure=procedure)


@procedures.route('/delete/<int:procedure_id>', methods=['GET'])
@check_login
@check_admin
def delete(procedure_id):
    procedure = ProcedureModels.Procedures.query.get_or_404(procedure_id)
    db.session.delete(procedure)
    db.session.commit()
    return redirect(url_for('procedures.index'))


@procedures.route('/attribute_add', methods=['GET', 'POST'])
@check_login
def attribute_add():
    form = ProcedureForms.AddProceduresAttribute(request.form)
    if helpers.validate_form_on_submit(form):
        attribute = ProcedureModels.ProceduresAttribute()
        form.populate_obj(attribute)
        db.session.add(attribute)
        db.session.commit()
        return redirect(url_for('procedures.index'))

    return render_template("procedures/add_or_edit_attribute.html", form=form)


@procedures.route('/attribute/edit/<int:procedure_attribute_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def attribute_edit(procedure_attribute_id):
    procedure_attribute = ProcedureModels.ProceduresAttribute.query.get(procedure_attribute_id)
    form = ProcedureForms.EditProceduresAttribute(request.form, obj=procedure_attribute)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(procedure_attribute)
        db.session.add(procedure_attribute)
        db.session.commit()
        return redirect(url_for('procedures.index'))

    return render_template("procedures/add_or_edit_attribute.html", form=form, edit=1, procedure_attribute_id=procedure_attribute_id)


@procedures.route('/attribute/delete/<int:procedure_attribute_id>', methods=['GET'])
@check_login
@check_admin
def attribute_delete(procedure_attribute_id):
    procedure_attribute = ProcedureModels.ProceduresAttribute.query.get_or_404(procedure_attribute_id)
    db.session.delete(procedure_attribute)
    db.session.commit()
    return redirect(url_for('procedures.index'))
