# Import flask dependencies
import os
from flask import (
    Blueprint, request, render_template,
    redirect, url_for)
from src import db
import src.schedules.models as SchedulesModels
import src.schedules.forms as SchedulesForms
from flask_admin import helpers
from src.helpers.decorators import check_login, check_admin
from src.auth.models import User
from src.specimens.models import Specimens



schedules = Blueprint('schedules', __name__, url_prefix='/schedules')


@schedules.route('/', methods=['GET'])
@check_login
def index():
    schedules = SchedulesModels.Schedules.query.all()
    attributes = SchedulesModels.SchedulesAttribute.query.all()
    return render_template("/schedules/index.html", schedules=schedules, attributes=attributes)


@schedules.route('/calendar', methods=['GET'])
@check_login
def calendar():
    schedules = SchedulesModels.Schedules.query.all()
    return render_template("/schedules/calendar.html", schedules=schedules)



@schedules.route('/view/<int:schedule_id>', methods=['GET'])
@check_login
def view(schedule_id):
    schedule = SchedulesModels.Schedules.query.get(schedule_id)
    return render_template("/schedules/view.html", schedule=schedule)


@schedules.route('/update/', methods=['POST'])
@check_login
def update():
    if request.method == 'POST':
        schedule_data = request.get_json()
        print(schedule_data)
        schedule = SchedulesModels.Schedules.query.get(schedule_data['schedule_id'])
        if schedule:
            schedule.start_datetime = schedule.set_datetime(schedule_data['start_datetime'])
            schedule.end_datetime = schedule.set_datetime(schedule_data['end_datetime'])
            db.session.add(schedule)
            db.session.commit()
            return 'ok'
        return 'failed'
    return redirect(url_for('schedules.index'))


@schedules.route('/add', methods=['GET', 'POST'])
@check_login
def add():
    attributes = SchedulesModels.SchedulesAttribute.query.all()
    form = SchedulesForms.AddSchedule(request.form)
    if request.method == 'POST':
        schedule = SchedulesModels.Schedules()
        schedule.start_datetime = request.form.get('start_datetime')
        schedule.end_datetime = request.form.get('end_datetime')
        schedule.procedure_id = request.form.get('procedure_id')
        for specimen in request.form.getlist('specimens'):
            schedule.specimens.append(Specimens.query.get(specimen))
        for user in request.form.getlist('users'):
            schedule.users.append(User.query.get(user))
        db.session.add(schedule)
        db.session.flush()
        for attribute in attributes:
            schedule_attribute = SchedulesModels.SchedulesValue()
            schedule_attribute.schedules_id = schedule.id
            schedule_attribute.schedules_attribute_id = attribute.id
            schedule_attribute.value = request.form.get(attribute.name)
            db.session.add(schedule_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('schedules.index'))

    return render_template("schedules/add_or_edit.html", form=form, attributes=attributes)


@schedules.route('/edit/<int:schedule_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit(schedule_id):
    attributes = SchedulesModels.SchedulesAttribute.query.all()
    schedule = SchedulesModels.Schedules.query.get(schedule_id)
    form = SchedulesForms.EditSchedule(request.form, obj=schedule)
    if request.method == 'POST':
        schedule.start_datetime = request.form.get('start_datetime')
        schedule.end_datetime = request.form.get('end_datetime')
        schedule.procedure_id = request.form.get('procedure_id')
        for specimen in request.form.getlist('specimens'):
            schedule.specimens.append(Specimens.query.get(specimen))
        for user in request.form.getlist('users'):
            schedule.users.append(User.query.get(user))
        db.session.add(schedule)
        db.session.flush()
        for attribute in attributes:
            schedule_attribute = SchedulesModels.SchedulesValue.get_by_uniq_const(schedule_id, attribute.id)
            if not schedule_attribute:
                schedule_attribute = SchedulesModels.SchedulesValue()
            schedule_attribute.schedules_id = schedule.id
            schedule_attribute.schedules_attribute_id = attribute.id
            schedule_attribute.value = request.form.get(attribute.name)
            db.session.add(schedule_attribute)
            db.session.flush()
        db.session.commit()
        return redirect(url_for('schedules.index'))

    return render_template("schedules/add_or_edit.html", form=form, attributes=attributes, edit=1, schedule=schedule)


@schedules.route('/delete/<int:schedule_id>', methods=['GET'])
@check_login
@check_admin
def delete(schedule_id):
    schedule = SchedulesModels.Schedules.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for('schedules.index'))


@schedules.route('/attribute/add', methods=['GET', 'POST'])
@check_login
def attribute_add():
    form = SchedulesForms.AddSchedulesAttribute(request.form)
    if helpers.validate_form_on_submit(form):
        attribute = SchedulesModels.SchedulesAttribute()
        form.populate_obj(attribute)
        db.session.add(attribute)
        db.session.commit()
        return redirect(url_for('schedules.index'))

    return render_template("schedules/add_or_edit_attribute.html", form=form)


@schedules.route('/attribute/edit/<int:schedule_attribute_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def attribute_edit(schedule_attribute_id):
    schedule_attribute = SchedulesModels.SchedulesAttribute.query.get(schedule_attribute_id)
    form = SchedulesForms.EditSchedulesAttribute(request.form, obj=schedule_attribute)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(schedule_attribute)
        db.session.add(schedule_attribute)
        db.session.commit()
        return redirect(url_for('schedules.index'))

    return render_template("schedules/add_or_edit_attribute.html", form=form, edit=1, schedule_attribute_id=schedule_attribute_id)


@schedules.route('/attribute/delete/<int:schedule_attribute_id>', methods=['GET'])
@check_login
@check_admin
def attribute_delete(schedule_attribute_id):
    schedule_attribute = SchedulesModels.SchedulesAttribute.query.get_or_404(schedule_attribute_id)
    db.session.delete(schedule_attribute)
    db.session.commit()
    return redirect(url_for('schedules.index'))
