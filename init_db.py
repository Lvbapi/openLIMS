from src import db
from src.auth.models import User, Role
import src.site.models as SiteModels
import src.projects.models as ProjectsModels
import src.procedures.models as ProceduresModels
import src.parameters.models as ParametersModels
import src.specimens.models as SpecimensModels
import src.schedules.models as SchedulesModels
import src.auth.models as AuthModels
import src.projects.models as ProjectsModels
from werkzeug.security import generate_password_hash
from datetime import date, timedelta


user = User()
user.email = 'admin@example.com'
user.password = generate_password_hash('admin')

role = Role()
role.name = 'admin'
role.description = ''
db.session.add(role)
user.roles.append(role)
db.session.commit()

role = Role()
role.name = 'manager'
role.description = ''
db.session.add(role)
user.roles.append(role)
db.session.commit()

role = Role()
role.name = 'employee'
role.description = ''
db.session.add(role)
user.roles.append(role)
db.session.add(user)
db.session.commit()

project = ProjectsModels.Projects()
project.name = 'KOMP2'
project.description = 'The Knockout Mouse Phenotyping Program (KOMP2) collaborates with the International Mouse Phenotyping Consortium (IMPC) to knockout and characterize all protein-coding genes in the mouse genome.'
db.session.add(project)
db.session.commit()

specimen = SpecimensModels.Specimens()
specimen.name = 'EXMPL-1'
db.session.add(specimen)
db.session.commit()

specimen = SpecimensModels.Specimens()
specimen.name = 'EXMPL-2'
db.session.add(specimen)
db.session.commit()

specimen = SpecimensModels.Specimens()
specimen.name = 'EXMPL-3'
db.session.add(specimen)
db.session.commit()

specimen_attribute = SpecimensModels.SpecimensAttribute()
specimen_attribute.name = 'sex'
db.session.add(specimen_attribute)
db.session.commit()

specimen_attribute = SpecimensModels.SpecimensAttribute()
specimen_attribute.name = 'genotype'
db.session.add(specimen_attribute)
db.session.commit()

specimen_attribute = SpecimensModels.SpecimensAttribute()
specimen_attribute.name = 'date of birth'
db.session.add(specimen_attribute)
db.session.commit()

specimen_attribute = SpecimensModels.SpecimensAttribute()
specimen_attribute.name = 'date of death'
db.session.add(specimen_attribute)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 1
specimen_value.specimens_attribute_id = 1
specimen_value.value = 'Male'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 1
specimen_value.specimens_attribute_id = 2
specimen_value.value = 'Het'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 1
specimen_value.specimens_attribute_id = 3
specimen_value.value = str((date.today() - timedelta(days=12)).strftime("%Y-%m-%d")) + 'T12:00'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 2
specimen_value.specimens_attribute_id = 1
specimen_value.value = 'Female'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 2
specimen_value.specimens_attribute_id = 2
specimen_value.value = 'Het'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 2
specimen_value.specimens_attribute_id = 3
specimen_value.value = str((date.today() - timedelta(days=9)).strftime("%Y-%m-%d")) + 'T12:00'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 3
specimen_value.specimens_attribute_id = 2
specimen_value.value = 'Hom'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 3
specimen_value.specimens_attribute_id = 1
specimen_value.value = 'Male'
db.session.add(specimen_value)
db.session.commit()

specimen_value = SpecimensModels.SpecimensValue()
specimen_value.specimens_id = 3
specimen_value.specimens_attribute_id = 3
specimen_value.value = str((date.today() - timedelta(days=10)).strftime("%Y-%m-%d")) + 'T12:00'
db.session.add(specimen_value)
db.session.commit()

procedure = ProceduresModels.Procedures()
procedure.project_id = 1
procedure.name = 'Body Weight'
procedure.description = 'The body weight test measures the weight of the mouse in a time series, allowing monitoring of its evolution; also, it is parameter.required in many other procedures.'
db.session.add(procedure)
db.session.commit()

procedure = ProceduresModels.Procedures()
procedure.project_id = 1
procedure.name = 'Fertility'
procedure.description = 'To assess the fertility of homozygous knockout mice.'
db.session.add(procedure)
db.session.commit()

procedure = ProceduresModels.Procedures()
procedure.project_id = 1
procedure.name = 'Open Field'
procedure.description = 'The Open Field test is used to assess anxiety and exploratory behaviors. It is based on the natural tendency of an animal to explore and to protect itself using avoidance which translates to a normal animal spending more time in the periphery of the Open Field arena than in the center (the most anxiogenic area).'
db.session.add(procedure)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Body Weight'
parameter.datatype = 'decimal' 
parameter.datamin = str(2.5)
parameter.datamax = str(90.0)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 2
parameter.name = 'Gross Findings Male'
parameter.datatype = 'option'
parameter.required = 1
db.session.add(parameter)
db.session.flush()

option = SiteModels.Options.get_by_name('Infertile')
if not option:
    option = SiteModels.Options()
option.name = 'Infertile'
db.session.add(option)
db.session.flush()
parameter.options.append(option)
db.session.add(parameter)
db.session.flush()

option = SiteModels.Options.get_by_name('Fertile')
if not option:
    option = SiteModels.Options()
option.name = 'Fertile'
db.session.add(option)
db.session.flush()
parameter.options.append(option)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 2
parameter.name = 'Gross Findings Female'
parameter.datatype = 'option'
parameter.required = 1
db.session.add(parameter)
db.session.flush()

option = SiteModels.Options.get_by_name('Infertile')
if not option:
    option = SiteModels.Options()
option.name = 'Infertile'
db.session.add(option)
db.session.flush()
parameter.options.append(option)
db.session.add(parameter)
db.session.flush()

option = SiteModels.Options.get_by_name('Fertile')
if not option:
    option = SiteModels.Options()
option.name = 'Fertile'
db.session.add(option)
db.session.flush()
parameter.options.append(option)
db.session.add(parameter)
db.session.commit()


parameter = ParametersModels.Parameters()
parameter.procedure_id = 3
parameter.name = 'increment'
parameter.datatype = 'integer' 
parameter.datamin = str(5)
parameter.datamax = str(20)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 3
parameter.name = 'Distance Travelled'
parameter.datatype = 'decimal' 
parameter.datamin = str(5.0)
parameter.datamax = str(25.75)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 3
parameter.name = 'Number of Rears'
parameter.datatype = 'integer' 
parameter.datamin = str(0)
parameter.datamax = str(2000)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 3
parameter.name = 'Whole Arena Resting Time'
parameter.datatype = 'decimal' 
parameter.datamin = str(0.0)
parameter.datamax = str(600.0)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 3
parameter.name = 'Number of Center Entries'
parameter.datatype = 'integer' 
parameter.datamin = str(0)
parameter.datamax = str(1000)
parameter.required = 1
db.session.add(parameter)
db.session.commit()

schedule = SchedulesModels.Schedules()
schedule.start_datetime = str(date.today().strftime("%Y-%m-%d")) + 'T12:00'
schedule.end_datetime = str(date.today().strftime("%Y-%m-%d")) + 'T14:00'
schedule.procedure_id = 1
schedule.users.append(User.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(2))
schedule.specimens.append(SpecimensModels.Specimens.query.get(3))
db.session.add(schedule)
db.session.commit()

schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() + timedelta(days=1)).strftime("%Y-%m-%d")) + 'T12:00'
schedule.end_datetime = str((date.today() + timedelta(days=1)).strftime("%Y-%m-%d")) + 'T14:00'
schedule.procedure_id = 2
schedule.users.append(User.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(2))
schedule.specimens.append(SpecimensModels.Specimens.query.get(3))
db.session.add(schedule)
db.session.commit()

schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() + timedelta(days=2)).strftime("%Y-%m-%d")) + 'T12:00'
schedule.end_datetime = str((date.today() + timedelta(days=2)).strftime("%Y-%m-%d")) + 'T14:00'
schedule.procedure_id = 3
schedule.users.append(User.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(1))
schedule.specimens.append(SpecimensModels.Specimens.query.get(2))
schedule.specimens.append(SpecimensModels.Specimens.query.get(3))
db.session.add(schedule)
db.session.commit()

