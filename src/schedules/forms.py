from wtforms import form, fields, validators
import src.schedules.models as SchedulesModels
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
from src.auth.models import User
from src.specimens.models import Specimens


def specimens():
    return Specimens.all()

def users():
    return User.all()


class AddSchedule(form.Form):
	start_datetime = fields.StringField('Start DateTime', validators=[validators.required()])
	end_datetime = fields.StringField('End DateTime', validators=[validators.required()])
	specimens = QuerySelectMultipleField('Specimens', query_factory=specimens, allow_blank=False)
	users = QuerySelectMultipleField('Assigned To', query_factory=users, allow_blank=False)
	procedure_id = QuerySelectField('Procedure', query_factory=lambda: SchedulesModels.Procedures.query)
	

class EditSchedule(AddSchedule):
	id = fields.HiddenField()


class AddSchedulesAttribute(form.Form):
	name = fields.StringField('Name', validators=[validators.required()])
	submit = fields.SubmitField('Submit')

class EditSchedulesAttribute(AddSchedulesAttribute):
	id = fields.HiddenField()