from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db
from src.projects.models import Projects


class Procedures(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
  name = db.Column(db.String)
  description = db.Column(db.String)
  parameters = db.relationship('Parameters', backref='procedures', cascade='all, delete, delete-orphan', lazy=True)
  schedules = db.relationship('Schedules', backref='procedures', cascade='all, delete, delete-orphan', lazy=True)
  experiments = db.relationship('Experiments', backref='procedures', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('ProceduresValue', cascade='all, delete, delete-orphan', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: Value(k,v))

  def __str__(self):
    return Projects.query.get(self.project_id).name + ": " + self.name

  def __repr__(self):
    return Projects.query.get(self.project_id).name + ": " + self.name

  def get_project(self):
    return Projects.query.get(self.project_id)

  def get_project_name(self):
    return Projects.query.get(self.project_id).name

  @classmethod
  def all(cls):
    return db.session.query(cls).all()


class ProceduresAttribute(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('ProceduresValue', backref="procedures_attribute", cascade='all, delete, delete-orphan')
  
  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj
    

class ProceduresValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('procedures_id', 'procedures_attribute_id'),
  )
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  procedures_id = db.Column(db.Integer, db.ForeignKey('procedures.id'), nullable=False)
  procedures_attribute_id = db.Column(db.Integer, db.ForeignKey('procedures_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('ProceduresAttribute', uselist=False, 
    foreign_keys=[procedures_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: ProceduresAttribute.get_or_create(v))

  def __repr__(self):
    return self.value

  @classmethod
  def get_by_uniq_const(cls, procedure_id, attribute_id):
    return cls.query.filter_by(procedures_id=procedure_id, procedures_attribute_id=attribute_id).first()

