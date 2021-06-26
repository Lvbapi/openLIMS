from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db
from colorhash import ColorHash
from dateutil import parser
from src.procedures.models import Procedures
from src.specimens.models import Specimens
from src.auth.models import User


specimens_schedules = db.Table(
  'specimens_schedules',
  db.Column('schedule_id', db.Integer, db.ForeignKey('schedules.id'), nullable=False),
  db.Column('specimen_id', db.Integer, db.ForeignKey('specimens.id'), nullable=False))


users_schedules = db.Table(
  'users_schedules',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
  db.Column('schedule_id', db.Integer, db.ForeignKey('schedules.id'), nullable=False))


class Schedules(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  start_datetime = db.Column(db.String)
  end_datetime = db.Column(db.String)
  specimens = db.relationship('Specimens', secondary=specimens_schedules, backref=db.backref('schedule', lazy='dynamic'))
  users = db.relationship('User', secondary=users_schedules, backref=db.backref('users', lazy='dynamic'))
  procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), nullable=False)
  experiments = db.relationship('Experiments', backref='schedules', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('SchedulesValue', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: Value(k,v))

  def __repr__(self):
    return self.datetime

  def get_procedure(self):
    return Procedures.query.get(self.procedure_id)

  def get_project(self):
    return Procedures.query.get(self.procedure_id).get_project_name()

  def get_project_id(self):
    return Procedures.query.get(self.procedure_id).get_project().id

  def get_converted_datetime(self, parameter):
    return parser.parse(parameter).strftime('%m/%d/%Y %H:%M')

  def set_datetime(self, parameter):
    return parser.parse(parameter).strftime('%Y-%m-%dT%H:%M')

  def get_color(self):
    procedure = self.get_procedure()
    color = ColorHash(procedure.name + str(procedure.id))
    return color.hex

  @classmethod
  def get_user_schedule(cls, user_id):
    return cls.query.filter(cls.users.any(User.id==user_id)).all()

  @classmethod
  def all(cls):
    return db.session.query(cls).all()


class SchedulesAttribute(db.Model):
    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('SchedulesValue', backref="schedules_attribute", cascade='all, delete, delete-orphan')

  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj


class SchedulesValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('schedules_id', 'schedules_attribute_id'),
  )
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  schedules_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
  schedules_attribute_id = db.Column(db.Integer, db.ForeignKey('schedules_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('SchedulesAttribute', uselist=False, 
    foreign_keys=[schedules_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: SchedulesAttribute.get_or_create(v))

  def __repr__(self):
    return self.value

  @classmethod
  def get_by_uniq_const(cls, schedule_id, attribute_id):
    return cls.query.filter_by(schedules_id=schedule_id, schedules_attribute_id=attribute_id).first()
