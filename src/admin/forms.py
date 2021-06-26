from wtforms import form, fields, validators
from wtforms.widgets import TextArea
from src.auth.models import Role
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
import src.site.models as SiteModels


def roles():
    return Role.all()


class CreateUserForm(form.Form):
    email = fields.StringField('Email', validators=[validators.required()])
    password = fields.StringField('Password')

    roles = QuerySelectMultipleField('User Roles', query_factory=roles,
                                     allow_blank=False)

    active = fields.BooleanField()
    submit = fields.SubmitField('Submit')


class EditUserForm(CreateUserForm):
    id = fields.HiddenField()


class CreateRoleForm(form.Form):
    name = fields.StringField('Name', validators=[validators.required()])
    description = fields.StringField('Description', validators=[validators.required()])
    submit = fields.SubmitField('Submit')


class EditRoleForm(CreateRoleForm):
    id = fields.HiddenField()
