# Import flask dependencies
import os
from flask import (
    Blueprint, request, render_template,
    redirect, url_for)
from src import db
import src.site.models as SiteModels
import src.parameters.models as ParameterModels
import src.parameters.forms as ParameterForms
from flask_admin import helpers
from src.helpers.decorators import check_login, check_admin


parameters = Blueprint('parameters', __name__, url_prefix='/parameters')


@parameters.route('/', methods=['GET'])
@check_login
def index():
    parameters = ParameterModels.Parameters.query.all()
    attributes = ParameterModels.ParametersAttribute.query.all()
    return render_template("parameters/index.html", parameters=parameters, attributes=attributes)


@parameters.route('/<int:parameter_id>', methods=['GET'])
@check_login
def view(parameter_id):
    parameter = ParameterModels.Parameters.query.get(parameter_id)
    return render_template("parameters/view.html", parameter=parameter)


@parameters.route('/add', methods=['GET', 'POST'])
@check_login
def add():
    attributes = ParameterModels.ParametersAttribute.query.all()
    form = ParameterForms.AddParameters()
    if request.method == 'POST':
        parameter = ParameterModels.Parameters()
        parameter.procedure_id = request.form.get('procedure_id')
        parameter.name = request.form.get('name')
        parameter.datatype = request.form.get('datatype')
        parameter.datamin = request.form.get('datamin')
        parameter.datamax = request.form.get('datamax')
        parameter.unit = request.form.get('unit')
        parameter.required = 1 if request.form.get('required') == 'y' else 0
        db.session.add(parameter)
        db.session.flush()
        options_list = request.form.getlist('option[]');
        if(options_list):
            for options in options_list:
                option = SiteModels.Options.get_by_name(options)
                if not option:
                    option = SiteModels.Options()
                option.name = options
                db.session.add(option)
                db.session.flush()
                parameter.options.append(option)
                db.session.add(parameter)
                db.session.flush()
        for attribute in attributes:
            parameter_attribute = ParameterModels.ParametersValue()
            parameter_attribute.parameters_id = parameter.id
            parameter_attribute.parameters_attribute_id = attribute.id
            parameter_attribute.value = request.form.get(attribute.name)
            db.session.add(parameter_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('parameters.index'))

    return render_template("parameters/add_or_edit.html", form=form, attributes=attributes)


@parameters.route('/edit/<int:parameter_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit(parameter_id):
    attributes = ParameterModels.ParametersAttribute.query.all()
    parameter = ParameterModels.Parameters.query.get(parameter_id)
    form = ParameterForms.AddParameters(request.form, obj=parameter)
    if request.method == 'POST':
        parameter.procedure_id = request.form.get('procedure_id')
        parameter.name = request.form.get('name')
        parameter.datatype = request.form.get('datatype')
        parameter.datamin = request.form.get('datamin')
        parameter.datamax = request.form.get('datamax')
        parameter.unit = request.form.get('unit')
        parameter.required = 1 if request.form.get('required') == 'y' else 0
        db.session.add(parameter)
        db.session.flush()
        options_list = request.form.getlist('option[]');
        if(options_list):
            for options in options_list:
                option = SiteModels.Options.get_by_name(options)
                if not option:
                    option = SiteModels.Options()
                option.name = options
                db.session.add(option)
                db.session.flush()
                parameter.options.append(option)
                db.session.add(parameter)
                db.session.flush()
        for attribute in attributes:
            parameter_attribute = ParameterModels.ParametersValue.get_by_uniq_const(parameter_id, attribute.id)
            if not parameter_attribute:
                parameter_attribute = ParameterModels.ParametersValue()
            parameter_attribute.parameters_id = parameter.id
            parameter_attribute.parameters_attribute_id = attribute.id
            parameter_attribute.value = request.form.get(attribute.name)
            db.session.add(parameter_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('parameters.index'))

    return render_template("parameters/add_or_edit.html", form=form, attributes=attributes, edit=1, parameter=parameter)


@parameters.route('/delete/<int:procedure_id>', methods=['GET'])
@check_login
@check_admin
def delete(procedure_id):
    procedure = ProcedureModels.Procedures.query.get_or_404(procedure_id)
    db.session.delete(procedure)
    db.session.commit()
    return redirect(url_for('procedures.index'))


@parameters.route('/attribute_add', methods=['GET', 'POST'])
@check_login
def attribute_add():
    form = ParameterForms.AddParametersAttribute(request.form)
    if helpers.validate_form_on_submit(form):
        attribute = ParameterModels.ParametersAttribute()
        form.populate_obj(attribute)
        db.session.add(attribute)
        db.session.commit()
        return redirect(url_for('parameters.index'))

    return render_template("parameters/add_or_edit_attribute.html", form=form)


@parameters.route('/attribute/edit/<int:parameter_attribute_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def attribute_edit(parameter_attribute_id):
    parameter_attribute = ParameterModels.ParametersAttribute.query.get(parameter_attribute_id)
    form = ParameterForms.EditParametersAttribute(request.form, obj=parameter_attribute)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(parameter_attribute)
        db.session.add(parameter_attribute)
        db.session.commit()
        return redirect(url_for('parameters.index'))

    return render_template("parameters/add_or_edit_attribute.html", form=form, edit=1, parameter_attribute_id=parameter_attribute_id)


@parameters.route('/attribute/delete/<int:parameter_attribute_id>', methods=['GET'])
@check_login
@check_admin
def attribute_delete(parameter_attribute_id):
    parameter_attribute = ParameterModels.ParametersAttribute.query.get_or_404(parameter_attribute_id)
    db.session.delete(parameter_attribute)
    db.session.commit()
    return redirect(url_for('parameters.index'))
