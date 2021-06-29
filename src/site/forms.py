from wtforms import form, fields, validators
from wtforms_alchemy import QuerySelectField
from src.parameters.models import Parameters


class AddExperimentsAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')
	

def parameters_limited():
	return Parameters.query.filter(Parameters.datatype.in_(['decimal', 'integer']))

class ChartForm(form.Form):
	parameter_id_a = QuerySelectField('Parameter A', query_factory=parameters_limited)
	parameter_id_b = QuerySelectField('Parameter B', query_factory=parameters_limited)