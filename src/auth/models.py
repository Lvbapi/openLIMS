from src import db
from flask_security import RoleMixin
from flask_login import UserMixin


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other and
                self.name != getattr(other, 'name', None))

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name.replace('_', ' ')

    @classmethod
    def get_role(cls, name):
        return Role.query.filter_by(name=name).first()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    registered_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    registered_ip = db.Column(db.String(255))
    last_login_ip = db.Column(db.String(255))

    def __repr__(self):
        return self.get_display_name()

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_roles(self):
        return self.roles

    def get_display_name(self):
        return self.email.split("@")[0]

    def is_admin(self):
        return True if 'admin' in self.roles else False

    def has_role(self, role):
        return True if role in self.roles else False

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.query(cls).get(user_id)

    @classmethod
    def get_user_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()
