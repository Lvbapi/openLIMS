from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db


class Projects(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  procedures = db.relationship('Procedures', backref='projects', cascade='all, delete, delete-orphan', lazy=True)
  name = db.Column(db.String)
  description = db.Column(db.String)
  experiments = db.relationship('Experiments', backref='projects', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('ProjectsValue', cascade='all, delete, delete-orphan', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: Value(k,v))

  def __repr__(self):
    return self.name

  @classmethod
  def all(cls):
    return db.session.query(cls).all()


class ProjectsAttribute(db.Model):

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('ProjectsValue', backref="projects_attribute", cascade='all, delete, delete-orphan')

  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj


class ProjectsValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('projects_id', 'projects_attribute_id'),
  )

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  projects_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
  projects_attribute_id = db.Column(db.Integer, db.ForeignKey('projects_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('ProjectsAttribute', uselist=False, 
    foreign_keys=[projects_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: ProjectsAttribute.get_or_create(v))

  def __repr__(self):
    return self.value

  @classmethod
  def get_by_project_id_name(cls, project_id, name):
    attribute = ProjectsAttribute.query.filter_by(name=name)
    return cls.query.filter_by(projects_id=project_id, projects_attribute_id=attribute.id).first()

  @classmethod
  def get_by_uniq_const(cls, project_id, attribute_id):
    return cls.query.filter_by(projects_id=project_id, projects_attribute_id=attribute_id).first()

