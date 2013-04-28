from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.exc import *
engine = create_engine('mysql://sman2:sman2@localhost/sman2_alumni.db', convert_unicode=True)
Base = declarative_base()

class Users(Base):
	__tablename__ = "user"
	
	id = Column(Integer, primary_key=True)
	username = Column(String(30), primary_key=True, unique=True)
	fullname = Column(String(30))
	alamat = Column(String(50))
	password = Column(String(30))
	email = Column(String(30), unique=True)
	angkatan = Column(Integer)
	handphone = Column(String(20))
	work = Column(String(20))
	
	def __repr__(self):
		return "('%s', '%s', '%s')" % (self.username, self.fullname, self.angkatan)
	
	def __init__(self, username, fullname, password, email, angkatan, handphone, work):
		self.username = username
		self.fullname = fullname
		self.password = password
		self.email = email
		self.angkatan = angkatan
		self.handphone = handphone
		self.work = work
	
	def dto(self):
		return dict(username = self.username, fullname =  self.fullname , password = self.password,email = self.email, \
					angkatan = self.angkatan, handphone = self.handphone, work = self.work)  
		
class Contact(Base):
	__tablename__ = "contact"

	id = Column(Integer, primary_key=True)
	name = Column(String(30))
	email = Column(String(30))
	handphone = Column(Integer)
	message = Column(String(20))			
	
	def __init__(self, name, email, handphone, message):
		self.name = name	
		self.email = email
		self.handphone = handphone
		self.message = message
		
Session = sessionmaker(bind=engine)
session_db = Session()	
		
	

