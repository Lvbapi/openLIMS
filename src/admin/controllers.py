# Import flask dependencies
from datetime import datetime

import flask_login as login
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_admin import helpers
from werkzeug.security import generate_password_hash
from src import db
import src.admin.forms as AdminForms
from src.auth.models import Role, User
from src.helpers.decorators import check_admin, check_login, has_role
import src.site.models as SiteModels

# Create blog blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


# Create the user routes
@admin.route('/user', defaults={'pages': 1}, methods=['GET'])
@admin.route('/user/<int:pages>', methods=['GET'])
@check_login
@check_admin
def user_list(pages):
    order = 'users_' + request.args[
        'sort'] if 'sort' in request.args else 'users_id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    users = User.get_sortable_list(order, direction, pages)

    return render_template("admin/users/list.html", users=users)


@admin.route('/user/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_user():
    form = AdminForms.CreateUserForm(request.form)
    if helpers.validate_form_on_submit(form):
        user = User()
        form.populate_obj(user)
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.user_list'))

    return render_template("admin/users/user.html", form=form)


@admin.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_user(user_id):
    user = User.query.get(user_id)
    old_pass = user.password
    user.password = None
    last_login = user.last_login_ip
    form = AdminForms.EditUserForm(request.form, obj=user)
    if helpers.validate_form_on_submit(form):

        form.populate_obj(user)

        if user.password == '':
            user.password = old_pass
        else:
            user.password = generate_password_hash(user.password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.user_list'))

    return render_template("admin/users/user.html", form=form, user=user)


@admin.route('/user/delete/<int:user_id>', methods=['GET'])
@check_login
@check_admin
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.user_list'))


# Create the role routes
@admin.route('/role', defaults={'pages': 1}, methods=['GET'])
@admin.route('/role/<int:pages>', methods=['GET'])
@check_login
@check_admin
def role_list(pages):
    order = request.args['sort'] if 'sort' in request.args else 'id'
    direction = request.args['d'] if 'd' in request.args else 'desc'
    roles = Role.get_sortable_list(order, direction, pages)

    return render_template("admin/roles/list.html", roles=roles)


@admin.route('/role/create', methods=['GET', 'POST'])
@check_login
@check_admin
def create_role():
    form = AdminForms.CreateRoleForm(request.form)
    if helpers.validate_form_on_submit(form):
        role = Role()
        form.populate_obj(role)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('admin.role_list'))

    return render_template("admin/roles/role.html", form=form)


@admin.route('/role/edit/<int:role_id>', methods=['GET', 'POST'])
@check_login
@check_admin
def edit_role(role_id):
    role = Role.query.get(role_id)
    form = AdminForms.EditRoleForm(request.form, obj=role)
    if helpers.validate_form_on_submit(form):
        form.populate_obj(role)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('admin.role_list'))

    return render_template("admin/roles/role.html", form=form)


@admin.route('/role/delete/<int:role_id>', methods=['GET'])
@check_login
@check_admin
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('admin.role_list'))
