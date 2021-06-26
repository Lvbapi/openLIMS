# Import flask dependencies
import os
from flask import (
    Blueprint, request, render_template,
    redirect, url_for)
from src import db
import src.specimens.models as SpecimensModels
import src.specimens.forms as SpecimensForms
from flask_admin import helpers
from src.helpers.decorators import check_login, check_admin


specimens = Blueprint('specimens', __name__, url_prefix='/specimens')


@specimens.route('/', methods=['GET'])
@check_login
def index():
    specimens = SpecimensModels.Specimens.query.all()
    attributes = SpecimensModels.SpecimensAttribute.query.all()
    return render_template("/specimens/index.html", specimens=specimens, attributes=attributes)


@specimens.route('/view/<int:specimen_id>', methods=['GET'])
@check_login
def view(specimen_id):
    specimen = SpecimensModels.Specimens.query.get_or_404(specimen_id)
    attributes = SpecimensModels.SpecimensAttribute.query.all()
    return render_template("/specimens/view.html", specimen=specimen, attributes=attributes)


@specimens.route('/add', methods=['GET', 'POST'])
@check_login
def add():
    attributes = SpecimensModels.SpecimensAttribute.query.all()
    form = SpecimensForms.EditSpecimen(request.form)
    if request.method == 'POST':
        specimen = SpecimensModels.Specimens()
        specimen.name = request.form.get('name')
        db.session.add(specimen)
        db.session.flush()
        for attribute in attributes:
            specimen_attribute = SpecimensModels.SpecimensValue()
            specimen_attribute.specimens_id = specimen.id
            specimen_attribute.specimens_attribute_id = attribute.id
            specimen_attribute.value = request.form.get(attribute.name)
            db.session.add(specimen_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('specimens.index'))

    return render_template("/specimens/add_or_edit.html", form=form, attributes=attributes)


@specimens.route('/edit/<int:specimen_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit(specimen_id):
    attributes = SpecimensModels.SpecimensAttribute.query.all()
    specimen = SpecimensModels.Specimens.query.get(specimen_id)
    form = SpecimensForms.EditSpecimen(request.form, obj=specimen)
    if request.method == 'POST':
        specimen.name = request.form.get('name')
        db.session.add(specimen)
        db.session.flush()
        for attribute in attributes:
            specimen_attribute = SpecimensModels.SpecimensValue.get_by_uniq_const(specimen_id, attribute.id)
            if not specimen_attribute:
                specimen_attribute = SpecimensModels.SpecimensValue()
            specimen_attribute.specimens_id = specimen.id
            specimen_attribute.specimens_attribute_id = attribute.id
            specimen_attribute.value = request.form.get(attribute.name)
            db.session.add(specimen_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('specimens.index'))

    return render_template("specimens/add_or_edit.html", form=form, attributes=attributes, edit=1, specimen=specimen)


@specimens.route('/delete/<int:specimen_id>', methods=['GET'])
@check_login
@check_admin
def delete(specimen_id):
    specimen = SpecimensModels.Specimens.query.get_or_404(specimen_id)
    db.session.delete(specimen)
    db.session.commit()
    return redirect(url_for('specimens.index'))


@specimens.route('/attribute_add', methods=['GET', 'POST'])
@check_login
def attribute_add():
    form = SpecimensForms.AddSpecimenAttribute(request.form)
    if helpers.validate_form_on_submit(form):
        attribute = SpecimensModels.SpecimensAttribute()
        form.populate_obj(attribute)
        db.session.add(attribute)
        db.session.commit()
        return redirect(url_for('specimens.index'))

    return render_template("specimens/add_or_edit_attribute.html", form=form)


@specimens.route('/attribute/edit/<int:specimen_attribute_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def attribute_edit(specimen_attribute_id):
    specimen_attribute = SpecimensModels.SpecimensAttribute.query.get(specimen_attribute_id)
    form = SpecimensForms.EditSpecimenAttribute(request.form, obj=specimen_attribute)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(specimen_attribute)
        db.session.add(specimen_attribute)
        db.session.commit()
        return redirect(url_for('specimens.index'))

    return render_template("specimens/add_or_edit_attribute.html", form=form, edit=1, specimen_attribute_id=specimen_attribute_id)


@specimens.route('/attribute/delete/<int:specimen_attribute_id>', methods=['GET'])
@check_login
@check_admin
def attribute_delete(specimen_attribute_id):
    specimen_attribute = SpecimensModels.SpecimensAttribute.query.get_or_404(specimen_attribute_id)
    db.session.delete(specimen_attribute)
    db.session.commit()
    return redirect(url_for('specimens.index'))
