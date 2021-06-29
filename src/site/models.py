from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db
from dateutil import parser
from src.projects.models import Projects
from src.procedures.models import Procedures
from src.specimens.models import Specimens
from src.schedules.models import Schedules
from src.parameters.models import Parameters


class Experiments(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  specimen_id = db.Column(db.Integer, db.ForeignKey('specimens.id'), nullable=False)
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
  procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), nullable=False)
  data_points = db.relationship('DataPoints', backref='experiments', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('ExperimentsValue', cascade='all, delete, delete-orphan', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: Value(k,v))

  def __repr__(self):
    return str({'specimen': self.get_specimen().name, 'data': self.data_points})

  def get_date(self):
    schedule = Schedules.query.get(self.schedule_id)
    return schedule.start_datetime

  def get_datetime(self):
    return parser.parse(self.get_date())

  def get_project(self):
    return Projects.query.get(self.project_id)

  def get_procedure(self):
    return Procedures.query.get(self.procedure_id)

  def get_specimen(self):
    return Specimens.query.get(self.specimen_id)

  @classmethod
  def get_by_procedure(cls, procedure_id):
    return cls.query.filter(cls.procedure_id==procedure_id).all()


class ExperimentsAttribute(db.Model):
    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('ExperimentsValue', backref="experiments_attribute", cascade='all, delete, delete-orphan')

  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj


class ExperimentsValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('experiment_id', 'experiment_attribute_id'),
  )
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
  experiment_attribute_id = db.Column(db.Integer, db.ForeignKey('experiments_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('ExperimentsAttribute', uselist=False, 
    foreign_keys=[experiment_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: ExperimentsAttribute.get_or_create(v))

  def __repr__(self):
    return self.value


# --------------------------

class Options(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)

  data_options = db.relationship('DataOptions', backref='options', cascade='all, delete, delete-orphan', lazy=True)

  @classmethod
  def get_by_name(cls, name):
    return cls.query.filter_by(name=name).first()


# --------------------------

class DataPoints(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
  parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), nullable=False)
  data_point_id = db.Column(db.Integer)

  def __repr__(self):
    return str({'parameter': self.get_parameter().name, 'value': self.get_value()}) 

  def get_parameter(self):
    return Parameters.query.filter(Parameters.id==self.parameter_id).first()

  def get_specimen_name(self):
    experiment = Experiments.query.get(self.experiment_id)
    return experiment.get_specimen().name

  def get_value(self):
    data_type = self.get_parameter().get_datatype()
    classInstance = self.get_class_by_string(data_type)
    return classInstance.get_value(self.data_point_id)

  def get_class_by_string(self, data_type):
    lookup = {'Integer': DataIntegers(),
     'Character': DataCharacters(),
     'Boolean': DataBooleans(),
     'Decimal': DataDecimals(),
     'Datetime': DataDatetimes(),
     'Date': DataDates(),
     'Time': DataTimes(),
     'Text': DataTexts(),
     'File': DataFiles(),
     'Option': DataOptions()}
    return lookup[data_type]

  def get_by_value(self, data_type, value):
    classInstance = self.get_class_by_string(data_type)
    stored_value = classInstance.get_by_value(value)
    if not stored_value:
      return None
    return stored_value


class DataIntegers(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Integer, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataCharacters(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.String, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataBooleans(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Boolean, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataDecimals(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Float, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return round(cls.query.get(data_point_id).value, 2)

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataDatetimes(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.DateTime, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataDates(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Date, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataTimes(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Time, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataTexts(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.Text, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataFiles(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  value = db.Column(db.String, unique=True)

  def __repr__(self):
    return str(self.value)

  @classmethod
  def get_value(cls, data_point_id):
    return cls.query.get(data_point_id).value

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(value=value).first()


class DataOptions(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=False)

  def __repr__(self):
    return Options.query.get(self.option_id).name

  @classmethod
  def get_value(cls, data_point_id):
    option_id = cls.query.get(data_point_id).option_id
    return Options.query.get(option_id).name

  @classmethod
  def get_by_value(cls, value):
    return cls.query.filter_by(option_id=value).first()
