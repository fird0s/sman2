from sqlalchemy import Column, String, Integer, create_engine, TEXT, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.exc import *
engine = create_engine('mysql://fird0s:a@localhost/sman2_alumni', convert_unicode=True)
Base = declarative_base()

class Users(Base):
	__tablename__ = "sman2_user"
	
	id = Column(Integer, primary_key=True)
	username = Column(String(30), primary_key=True, unique=True)
	fullname = Column(String(30))
	alamat = Column(String(50))
	password = Column(String(30))
	email = Column(String(30), unique=True)
	angkatan = Column(Integer)
	handphone = Column(String(20))
	work = Column(String(20))
	ip = Column(String(100))
	status = Column(String(100))

	def __repr__(self):
		return "('%s', '%s', '%s')" % (self.username, self.fullname, self.angkatan)
	
	def __init__(self, username, fullname, password, email, angkatan, handphone, work, ip, status):
		self.username = username
		self.fullname = fullname
		self.password = password
		self.email = email
		self.angkatan = angkatan
		self.handphone = handphone
		self.work = work
		self.ip = ip
		self.status = status	
	def dto(self):
		return dict(username = self.username, fullname =  self.fullname , password = self.password,email = self.email, \
					angkatan = self.angkatan, handphone = self.handphone, work = self.work)  
		
class Contact(Base):
	__tablename__ = "sman2_contact"

	id = Column(Integer, primary_key=True)
	name = Column(String(30))
	email = Column(String(30))
	handphone = Column(Integer)
	message = Column(TEXT)			
	
	def __init__(self, name, email, handphone, message):
		self.name = name	
		self.email = email
		self.handphone = handphone
		self.message = message
		
		
class Berita(Base):
	__tablename__ = "sman2_berita"
	
	id = Column(Integer, primary_key=True)
	judul = Column(String(100))
	content = Column(TEXT)		
	user_adder = Column(String(100))
	time = Column(DATE)
	
		
class Log(Base):
	__tablename__ = "sman2_log"
	
	id = Column(Integer, primary_key=True)
	request = Column(String(400))		
	ip = Column(String(100))		
	time = Column(DATE)
	referer = Column(TEXT)
		
class Admin(Base):
	__tablename__ = "sman2_admin"
		
	id = Column(Integer, primary_key=True)
	nama = Column(String(100))			
	password = Column(String(100))
	ip = Column(String(100))

			
Session = sessionmaker(bind=engine)
session_db = Session()	
		
#Base.metadata.create_all(engine) this for create your database and 
#please setting databasename 'sman2_alumni' and user = 'fird0s' and pass = 'a'

