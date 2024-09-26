from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, init_db


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    roles = relationship('Role', secondary='user_roles')

    def __init__(self, username, password):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)


class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))
