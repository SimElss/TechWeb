from database import Base 
from sqlalchemy import Column, ForeignKey, Integer, String

class Users(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, index=True) #primary key and indexable
    username = Column(String(50), unique = True) #unique but cannot be the primary key as the id is
    hashed_pw = Column(String(50))


    
class Admins(Base):
    __tablename__ = 'admins'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key = True, index = True)