from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date 
import enum

db=SQLAlchemy()

class Customers(db.Model):
  __tablename__='Customers'
  id=Column(Integer,primary_key=True, autoincrement=True)
  fname=Column(String(40), nullable=False)
  lname=Column(String(40), nullable=False)
  email=Column(String(40), nullable=False, unique=True)
  phone=Column(String(30), unique=True)
 
  def __init__(self,fname,lname,email,phone):
    self.fname=fname
    self.lname=lname
    self.email=email
    self.phone=phone

class Realty(db.Model):
    __tablename__ = 'Realty'
    id=Column(Integer, primary_key=True)
    object_type=Column(String(40), nullable=False)
    location=Column(String(255), nullable=False)
    price=Column(String(10), nullable=False)
    square=Column(String(10), nullable=False)
    num_rooms=Column(Integer, CheckConstraint("num_rooms>0 and num_rooms<21"))
    description=Column(Text, nullable=False)

    def __init__(self,object_type,location,price,area,num_rooms):
      self.object_type=object_type
      self.location=location
      self.price=price
      self.area=area
      self.num_rooms=num_rooms



class Agents(db.Model):
    __tablename__ = 'Agents'
    id = Column(Integer, primary_key=True)
    fname = Column(String(40), nullable=False)
    lname = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False)
    phone = Column(String(30), unique=True)
    salary = Column(Integer)

    def __init__(self,fname,lname,email,phone,salary):
      self.fname=fname
      self.lname=lname
      self.email=email
      self.phone=phone
      self.salary=salary



class Tickets(db.Model):
    __tablename__ = 'Tickets'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('Agents.id'), nullable=False)
    tickets_start_date = Column(Date, nullable=False, default=date.today())

    customer = relationship("Customers")
    realty = relationship("Realty")

    def __init__(self,customer_id,agent_id,tickets_start_date):
      self.customer_id=customer_id
      self.agent_id=agent_id
      self.tickets_start_date=tickets_start_date

class Operations(db.Model):
    __tablename__ = 'Operations'
    id = Column(Integer, primary_key=True)
    operation_type = Column(String (20), nullable=False)

    def __init__(self,operation_type):
       self.operation_type=operation_type


class Contract(db.Model):
    __tablename__ = 'Contract'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    realty_id = Column(Integer, ForeignKey('Realty.id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('Agents.id'), nullable=False)
    operations_id = Column(Integer, ForeignKey('Operations.id'), nullable=False)
    contract_start_date = Column(Date, nullable=False, default=date.today())
    contract_end_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)

    customer = relationship("Customers")
    realty = relationship("Realty")
    agent = relationship("Agents")

    def __init__(self,customer_id,realty_id,agent_id,operations_id,contract_start_date,contract_end_date,price):
      self.customer_id=customer_id
      self.realty_id=realty_id
      self.agent_id=agent_id
      self.operations_id=operations_id
      self.contract_start_date=contract_start_date
      self.contract_end_date=contract_end_date
      self.price=price

class User(db.Model):
   __tablename__ = 'User'
   id = Column(Integer, primary_key=True)
   username = Column(String(40), nullable=False)
   password = Column(Text, nullable=False)

   def __init__(self, username, password):
      self.username=username
      self.password=password

class Profile(db.Model):
  __tablename__ = 'Profile'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
  agent_id = Column(Integer, ForeignKey('Agents.id'), nullable=False)

  customer = relationship("Customers")
  agent = relationship("Agents")

  def __init__(self,customer_id,agent_id):
    self.customer_id=customer_id
    self.agent_id=agent_id