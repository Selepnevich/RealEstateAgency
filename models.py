from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import date 

db=SQLAlchemy()

class Customers(db.Model):
  __tablename__='Customers'
  id=Column(Integer,primary_key=True, autoincrement=True)
  fname=Column(String(40), nullable=False)
  lname=Column(String(40), nullable=False)
  email=Column(String(40))
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

    def __repr__(self):
        return f"Realty(object_type='{self.object_type}', location='{self.location}', " \
               f"price='{self.price}', area={self.area}, num_rooms={self.num_rooms}, " \
               f"description='{self.description}')"


class Agents(db.Model):
    __tablename__ = 'Agents'
    id = Column(Integer, primary_key=True)
    fname = Column(String(40), nullable=False)
    lname = Column(String(40), nullable=False)
    email = Column(String(40))
    phone = Column(Integer, nullable=False)
    salary = Column(Integer, nullable=False)

    def __init__(self,fname,lname,email,phone,salary):
      self.fname=fname
      self.lname=lname
      self.email=email
      self.phone=phone
      self.salary=salary

    def __repr__(self):
        return f"Agents(id={self.id}, fname='{self.fname}', lname='{self.lname}', " \
               f"email='{self.email}', phone={self.phone}, salary={self.salary})"


class Deal(db.Model):
    __tablename__ = 'Deal'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    realty_id = Column(Integer, ForeignKey('Realty.id'), nullable=False)
    agent_id = Column(Integer, ForeignKey('Agents.id'), nullable=False)
    deal_date = Column(Date, nullable=False, default=date.today())
    price = Column(Integer, nullable=False)

    customer = relationship("Customers")
    realty = relationship("Realty")
    agent = relationship("Agents")

    def __init__(self,customer_id,realty_id,agent_id,deal_date,price):
      self.customer_id=customer_id
      self.realty_id=realty_id
      self.agent_id=agent_id
      self.deal_date=deal_date
      self.price=price

    def __repr__(self):
        return f"Deal(id={self.id}, " \
               f"customer_id={self.customer_id}, " \
               f"realty_id={self.realty_id}, " \
               f"agent_id={self.agent_id}, " \
               f"deal_date='{self.deal_date}', " \
               f"price={self.price})"


class Reviews(db.Model):
    __tablename__ = 'Reviews'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    realty_id = Column(Integer, ForeignKey('Realty.id'), nullable=False)
    rating = Column(Integer, CheckConstraint("num_rooms>0 and num_rooms<6"))
    comment = Column(Text)

    customer = relationship("Customers")
    realty = relationship("Realty")

    def __init__(self,customer_id,realty_id,rating,comment):
      self.customer_id=customer_id
      self.realty_id=realty_id
      self.rating=rating
      self.comment=comment

    def __repr__(self):
        return f"Reviews(id={self.id}, " \
               f"customer_id={self.customer_id}, " \
               f"realty_id={self.realty_id}, " \
               f"rating={self.rating}, " \
               f"comment='{self.comment}')"