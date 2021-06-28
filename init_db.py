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
import random

fakes = 20

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


for i in range(1,fakes):
	specimen = SpecimensModels.Specimens()
	specimen.name = 'EXMPL-' + str(i)
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

for i in range(1,fakes):
	specimen_value = SpecimensModels.SpecimensValue()
	specimen_value.specimens_id = i
	specimen_value.specimens_attribute_id = 1
	specimen_value.value = 'Male' if i%2 == 1 else 'Female'
	db.session.add(specimen_value)
	db.session.commit()

for i in range(1,fakes):
	specimen_value = SpecimensModels.SpecimensValue()
	specimen_value.specimens_id = i
	specimen_value.specimens_attribute_id = 2
	specimen_value.value = 'Het' if i%3 == 1 else 'Hom'
	db.session.add(specimen_value)
	db.session.commit()

for i in range(1,fakes):
	specimen_value = SpecimensModels.SpecimensValue()
	specimen_value.specimens_id = i
	specimen_value.specimens_attribute_id = 3
	specimen_value.value = str((date.today() - timedelta(days=i)).strftime("%Y-%m-%d")) + 'T12:00'
	db.session.add(specimen_value)
	db.session.commit()

procedure = ProceduresModels.Procedures()
procedure.project_id = 1
procedure.name = 'Clinical Chemistry'
procedure.description = 'Clinical chemistry determines biochemical parameters in plasma including enzymatic activity, specific substrates and electrolytes.'
db.session.add(procedure)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Sodium'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mmol/l'
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Potassium'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mmol/l'
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Chloride'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mmol/l'
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Urea (Blood Urea Nitrogen - BUN)'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Creatinine'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Total Protein'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'g/l'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Albumin'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'g/l'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Total Bilirubin'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Calcium'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Phosphorus'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Iron'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Aspartate Aminotransferase'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'U/l'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Alanine Aminotransferase'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'U/l'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Alkaline Phosphatase'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'U/l'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Total Cholesterol'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'HDL-cholesterol'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Triglycerides'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Glucose'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg/dl'
parameter.required = 1
db.session.add(parameter)
db.session.commit()


parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Fructosamine'
parameter.datatype = 'decimal' 
parameter.unit = 'umol/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Lipase'
parameter.datatype = 'decimal' 
parameter.unit = 'U/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Lactate dehydrogenase'
parameter.datatype = 'decimal' 
parameter.unit = 'U/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Alpha-amylase'
parameter.datatype = 'decimal' 
parameter.unit = 'U/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'UIBC (unsaturated iron binding capacity)'
parameter.datatype = 'decimal' 
parameter.unit = 'umol/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'LDL-cholesterol'
parameter.datatype = 'decimal' 
parameter.unit = 'mg/dl'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Free fatty acids'
parameter.datatype = 'decimal' 
parameter.unit = 'mmol/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Glycerol'
parameter.datatype = 'decimal' 
parameter.unit = 'mmol/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Creatine kinase'
parameter.datatype = 'decimal' 
parameter.unit = 'U/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Uric acid'
parameter.datatype = 'decimal' 
parameter.unit = 'umol/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Ferritin'
parameter.datatype = 'decimal' 
parameter.unit = 'ng/ml'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Transferrin'
parameter.datatype = 'decimal' 
parameter.unit = 'mg/dl'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'C-reactive protein'
parameter.datatype = 'decimal' 
parameter.unit = 'mg/l'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Glycosilated hemoglobin A1c (HbA1c)'
parameter.datatype = 'decimal' 
parameter.unit = '%'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Thyroxine'
parameter.datatype = 'decimal' 
parameter.unit = 'ug/dl'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Magnesium'
parameter.datatype = 'decimal' 
parameter.unit = 'mg/dl'
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Cholesterol ratio'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Anesthesia used for blood collection'
parameter.datatype = 'option' 
parameter.datamin = str(0)
parameter.required = 1
db.session.add(parameter)
db.session.flush()

options_list = ['Gas anaesthesia with Isofluorane',
'Injection narcosis with Ketamine (100mg/kg)/Xylazine (10mg/kg)',
'Injection narcosis with Ketamine (100mg/kg)/ Xylazine (10mg/kg )/Antipamezole (Antisedan, 1mg/kg)',
'Injection narcosis with Ketamine (110mg/kg)/Xylazine (11mg/kg)',
'Injection narcosis with Ketamine (110mg/kg)/Xylazine (11mg/kg)/ Antipamezole (Antisedan, 1mg/kg)',
'Injection narcosis with Tribromoethanol (Avertin)',
'Injection narcosis with Sodium Pentobarbital (Pentobarb, 0.1ml)',
'Injection narcosis with Sodium Pentobarbital (Euthatal)',
'No',
'Injection narcosis with Ketamine (137mg/kg)/Xylazine (6.6mg/kg)',
'Injection narcosis with Sodium Pentobarbital (Somnopentyl)']

for opt in options_list:
	option = SiteModels.Options.get_by_name(opt)
	if not option:
	    option = SiteModels.Options()
	option.name = opt
	db.session.add(option)
	db.session.flush()
	parameter.options.append(option)
	db.session.add(parameter)
	db.session.flush()
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Method of blood collection'
parameter.datatype = 'option' 
parameter.datamin = str(0)
parameter.required = 1
db.session.add(parameter)
db.session.flush()

options_list = ['Cardiac puncture',
'Retro-orbital puncture',
'Heart puncture',
'Jugular vein',
'Tail vein']

for opt in options_list:
	option = SiteModels.Options.get_by_name(opt)
	if not option:
	    option = SiteModels.Options()
	option.name = opt
	db.session.add(option)
	db.session.flush()
	parameter.options.append(option)
	db.session.add(parameter)
	db.session.flush()
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Storage temperature from blood collection till measurement'
parameter.datatype = 'decimal' 
parameter.unit = 'C'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 1
parameter.name = 'Anticoagulant'
parameter.datatype = 'character' 
parameter.required = 1
db.session.add(parameter)
db.session.commit()



schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() - timedelta(days=1)).strftime("%Y-%m-%d")) + 'T12:00'
schedule.end_datetime = str((date.today() - timedelta(days=1)).strftime("%Y-%m-%d")) + 'T14:00'
schedule.procedure_id = 1
schedule.users.append(User.query.get(1))
for i in range(1,int(fakes/2)):
	schedule.specimens.append(SpecimensModels.Specimens.query.get(i))
db.session.add(schedule)
db.session.flush()


for specimen in schedule.specimens:
    experiment = SiteModels.Experiments()
    experiment.schedule_id = schedule.id
    experiment.specimen_id = specimen.id
    experiment.project_id = schedule.get_project_id()
    experiment.procedure_id = schedule.procedure_id
    db.session.add(experiment)
    db.session.flush()
    for parameter in schedule.get_procedure().parameters:
        datapoint = SiteModels.DataPoints()
        data_type = parameter.get_datatype()
    
        data_value = round(random.uniform(0.1, 300.0) + (random.choice([1,2,3]) * random.uniform(1,2)), 2)
        classInstance = datapoint.get_by_value(data_type, data_value)
        
        if not classInstance:
            classInstance = datapoint.get_class_by_string(data_type)

            if data_type == 'Option':
                classInstance.option_id = parameter.options[random.choice([1, 2, 3])].id
            elif data_type == 'Datetime':
            	classInstance.value = date.today()
            else:
                classInstance.value = data_value

            db.session.add(classInstance)
            db.session.flush()
        datapoint.experiment_id = experiment.id
        datapoint.parameter_id = parameter.id
        datapoint.data_point_id = classInstance.id
        db.session.add(datapoint)
        db.session.flush()
db.session.commit()



schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() - timedelta(days=2)).strftime("%Y-%m-%d")) + 'T12:00'
schedule.end_datetime = str((date.today() - timedelta(days=2)).strftime("%Y-%m-%d")) + 'T14:00'
schedule.procedure_id = 1
schedule.users.append(User.query.get(1))
for i in range(int(fakes/2), fakes):
	schedule.specimens.append(SpecimensModels.Specimens.query.get(i))
db.session.add(schedule)
db.session.commit()



procedure = ProceduresModels.Procedures()
procedure.project_id = 1
procedure.name = 'Heart Weight'
procedure.description = 'To evaluate cardiac size using heart weight and body weight.'
db.session.add(procedure)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 2
parameter.name = 'Tibia length'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mm'
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 2
parameter.name = 'Body weight'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'g'
parameter.required = 1
db.session.add(parameter)
db.session.commit()

parameter = ParametersModels.Parameters()
parameter.procedure_id = 2
parameter.name = 'Heart weight'
parameter.datatype = 'decimal' 
parameter.datamin = str(0)
parameter.unit = 'mg'
parameter.required = 1
db.session.add(parameter)
db.session.commit()



schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() - timedelta(days=1)).strftime("%Y-%m-%d")) + 'T10:00'
schedule.end_datetime = str((date.today() - timedelta(days=1)).strftime("%Y-%m-%d")) + 'T11:00'
schedule.procedure_id = 2
schedule.users.append(User.query.get(1))
for i in range(1,int(fakes/2)):
	schedule.specimens.append(SpecimensModels.Specimens.query.get(i))
db.session.add(schedule)
db.session.flush()


for specimen in schedule.specimens:
    experiment = SiteModels.Experiments()
    experiment.schedule_id = schedule.id
    experiment.specimen_id = specimen.id
    experiment.project_id = schedule.get_project_id()
    experiment.procedure_id = schedule.procedure_id
    db.session.add(experiment)
    db.session.flush()
    for parameter in schedule.get_procedure().parameters:
        datapoint = SiteModels.DataPoints()
        data_type = parameter.get_datatype()
    
        data_value = round(random.uniform(10.1, 30.0) + (random.choice([1,2,3]) * random.uniform(1,2)), 2)
        classInstance = datapoint.get_by_value(data_type, data_value)
        
        if not classInstance:
            classInstance = datapoint.get_class_by_string(data_type)
            classInstance.value = data_value
            db.session.add(classInstance)
            db.session.flush()
        datapoint.experiment_id = experiment.id
        datapoint.parameter_id = parameter.id
        datapoint.data_point_id = classInstance.id
        db.session.add(datapoint)
        db.session.flush()
db.session.commit()



schedule = SchedulesModels.Schedules()
schedule.start_datetime = str((date.today() + timedelta(days=2)).strftime("%Y-%m-%d")) + 'T10:00'
schedule.end_datetime = str((date.today() + timedelta(days=2)).strftime("%Y-%m-%d")) + 'T11:00'
schedule.procedure_id = 2
schedule.users.append(User.query.get(1))
for i in range(int(fakes/2), fakes):
	schedule.specimens.append(SpecimensModels.Specimens.query.get(i))
db.session.add(schedule)
db.session.commit()

