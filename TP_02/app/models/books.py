from database import Base 
from sqlalchemy import Column, ForeignKey, Integer, String

class Books(Base):
    __tablename__= 'books'

    id = Column(Integer, primary_key= True, index = True)

    title = Column(String(50))
    author = Column(String(50))
    editor = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.id'))
        #foreing key to the user that posted. Incase of user deletion, do NOT ERASE the lign. 
        #Otherwise the user's IDs will change.s