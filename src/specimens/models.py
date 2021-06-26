from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from src import db


class Specimens(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  experiments = db.relationship('Experiments', backref='specimens', cascade='all, delete, delete-orphan', lazy=True)

  attribute_values = db.relationship('SpecimensValue', cascade='all, delete, delete-orphan', 
    collection_class=attribute_mapped_collection('_attribute_name'))

  attributes = association_proxy('attribute_values', 'value', 
    creator=lambda k, v: SpecimensValue(k,v))

  def __repr__(self):
    return self.name

  @classmethod
  def all(cls):
    return db.session.query(cls).all()


class SpecimensAttribute(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False, unique=True)

  values = db.relationship('SpecimensValue', backref="specimens_attribute", cascade='all, delete, delete-orphan')

  @classmethod
  def get_or_create(cls, name, *arg, **kw):
    with db.session.no_autoflush:
      q = cls.query.filter_by(name=name)
      obj = q.first()
      if not obj:
        obj = cls(name, *arg, **kw)
        db.session.add(obj)
    return obj


class SpecimensValue(db.Model):
  __table_args__ = (
    db.UniqueConstraint('specimens_id', 'specimens_attribute_id'),
  )
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  specimens_id = db.Column(db.Integer, db.ForeignKey('specimens.id'), nullable=False)
  specimens_attribute_id = db.Column(db.Integer, db.ForeignKey('specimens_attribute.id'), nullable=False)
  value = db.Column(db.String)

  # Relationship to use in association proxy
  _attribute = db.relationship('SpecimensAttribute', uselist=False, 
    foreign_keys=[specimens_attribute_id], lazy='joined')

  # Expose attribute name as proxy
  _attribute_name = association_proxy('_attribute', 'name', 
    creator=lambda v: SpecimensAttribute.get_or_create(v))

  def __repr__(self):
    return self.value

  @classmethod
  def get_by_uniq_const(cls, specimen_id, attribute_id):
    return cls.query.filter_by(specimens_id=specimen_id, specimens_attribute_id=attribute_id).first()
