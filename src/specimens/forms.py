from wtforms import form, fields, validators


class AddSpecimen(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])

class EditSpecimen(AddSpecimen):
	id = fields.HiddenField()

class AddSpecimenAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')

class EditSpecimenAttribute(AddSpecimenAttribute):
	id = fields.HiddenField()