from wtforms import form, fields, validators


class AddProjects(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	description = fields.TextAreaField('Description')


class EditProjectsForm(AddProjects):
	id = fields.HiddenField()


class AddProjectsAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')


class EditProjectsAttribute(AddProjectsAttribute):
	id = fields.HiddenField()
