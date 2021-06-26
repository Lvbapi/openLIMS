from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db
import enum
from src.procedures.models import Procedures



options_parameters = db.Table(
  'options_parameters',
  db.Column('option_id', db.Integer, db.ForeignKey('options.id'), nullable=False),
  db.Column('parameter_id', db.Integer, db.ForeignKey('parameters.id'), nullable=False))


class DataTypes(enum.Enum):
    integer = 'Integer'
    character = 'Character'
    boolean = 'Boolean'
    decimal = 'Decimal'
    datetime = 'DateTime'
    date = 'Date'
    time = 'Time'
    text = 'Text'
    file = 'File'
    option = 'Option'


class Parameters(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), nullable=False)
  name = db.Column(db.String)
  datatype = db.Column(db.Enum(DataTypes), default=DataTypes.character, nullable=False)
  datamin = db.Column(db.String)
  datamax = db.Column(db.String)
  required = db.Column(db.Boolean)
  options = db.relationship('Options', secondary=options_parameters, backref=db.backref('parameters',
    cascade='all, delete', lazy='dynamic'))
  data_points = db.relationship('DataPoints', backref='parameters', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('ParametersValue', cascade='all, delete, delete-orphan', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: Value(k,v))

  def __repr__(self):
    return self.name

  def get_procedure(self):
    return Procedures.query.get(self.procedure_id)

  def get_datatype(self):
    datatype = str(self.datatype).split(".",1)[1].capitalize()
    return datatype


class ParametersAttribute(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('ParametersValue', backref="parameters_attribute", cascade='all, delete, delete-orphan')

  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj
    

class ParametersValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('parameters_id', 'parameters_attribute_id'),
  )
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  parameters_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), nullable=False)
  parameters_attribute_id = db.Column(db.Integer, db.ForeignKey('parameters_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('ParametersAttribute', uselist=False, 
    foreign_keys=[parameters_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: ParametersAttribute.get_or_create(v))

  def __repr__(self):
    return self.value

  @classmethod
  def get_by_uniq_const(cls, parameter_id, attribute_id):
    return cls.query.filter_by(parameters_id=parameter_id, parameters_attribute_id=attribute_id).first()

