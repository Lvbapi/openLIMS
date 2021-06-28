from wtforms import form, fields, validators
from src.procedures.models import Procedures
from wtforms_alchemy import QuerySelectField


class AddParameters(form.Form):
	procedure_id = QuerySelectField('Procedure', query_factory=lambda: Procedures.query)
	name = fields.StringField('Name', validators=[validators.required()])
	datatype = fields.SelectField('Data Type', choices=[('integer', 'Integer'),
		('character', 'Character'), ('boolean', 'Boolean'), ('decimal', 'Decimal'),
		('datetime', 'DateTime'), ('date', 'Date'), ('time', 'Time'), ('text', 'Text'),
		('file', 'File'), ('option', 'Option')])
	datamin = fields.StringField('Min Value or Length')
	datamax = fields.StringField('Max Value or Length')
	unit = fields.StringField('Unit')
	required = fields.BooleanField('Required')


class EditParameters(AddParameters):
	id = fields.HiddenField()


class AddParametersAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')


class EditParametersAttribute(AddParametersAttribute):
	id = fields.HiddenField()
