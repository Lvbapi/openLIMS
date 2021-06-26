from wtforms import form, fields, validators


class AddExperimentsAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')
	