from wtforms import form, fields, validators
from src.projects.models import Projects
from wtforms_alchemy import QuerySelectField


class AddProcedures(form.Form):
	project_id = QuerySelectField('Project', query_factory=lambda: Projects.query)
	name = fields.StringField('Name', validators=[validators.required()])
	description = fields.TextAreaField('Description')


class EditProcedure(AddProcedures):
	id = fields.HiddenField()


class AddProceduresAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')


class EditProceduresAttribute(AddProceduresAttribute):
	id = fields.HiddenField()
