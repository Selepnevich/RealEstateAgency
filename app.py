from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Customers
from FDataBase import FDataBase
import psycopg2 
import psycopg2.extras

# dbase = FDataBase(db)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=('postgresql://postgres:postgres@localhost:5432/DBRealEstateAgency')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "cairocoders-ednalan"
 
DB_HOST = "localhost"
DB_NAME = "DBRealEstateAgency"
DB_USER = "postgres"
DB_PASS = "postgres"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)



db.init_app(app)
migrate = Migrate(app, db)

#Главная страница 
  
@app.route("/", methods=['GET','POST'])
def index():

  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
      fname=request.form['fname']
      lname=request.form['lname']
      email=request.form['email']
      phone=request.form['phone']
      cur.execute('INSERT INTO public."Customers"(fname,lname,email,phone)\
                   VALUES (%s,%s,%s,%s)', \
                  (fname,lname,email,phone))
      conn.commit()
      flash('Ваша заявка отправлена, в течении дня с вами свяжется наш агент')
      return redirect(url_for('index'))
  return render_template('index.html', title ='Главная')   

#Страница недвижимость 

@app.route("/realty")
def realty():
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  s = 'SELECT * FROM public."Realty"'
  cur.execute(s)
  list_realty = cur.fetchall()
  return render_template('realty.html', title ='Недвижимость',\
                         list_realty=list_realty)

@app.route("/clients")
def clients():
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  s = 'SELECT * FROM public."Customers"'
  cur.execute(s)
  list_customers = cur.fetchall()
  return render_template('clients.html', title ='Добавить клиента',\
                         list_customers=list_customers)

@app.route("/add_client", methods=['POST'])
def add_client():
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if request.method == 'POST':
      fname=request.form['fname']
      lname=request.form['lname']
      email=request.form['email']
      phone=request.form['phone']
      cur.execute('INSERT INTO public."Customers" (fname,lname,email,phone)\
                  VALUES (%s,%s,%s,%s)', \
                  (fname,lname,email,phone))
      conn.commit()
      flash('Клиент успешно добавлен')
      return redirect(url_for('add_client'))

@app.route("/list_deal")
def list_deal():
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  s = 'SELECT * FROM public."Deal"'
  cur.execute(s)
  list_deal = cur.fetchall()
  return render_template('list_deal.html', title ='Сделки', list_deal=list_deal )

@app.route("/add_realty")
def add_realty():
  return render_template('list_deal.html', title ='Сделки')

#Вход

@app.route("/login", methods=['POST', 'GET'])
def login(): 
    return render_template('login.html', title="Вход")

@app.route("/registration", methods=['POST', 'GET'])
def registration(): 
    return render_template('registration.html', title="Регистрация")

@app.route("/add_user")
def add_user():
   pass
   

if __name__ == "__main__":
  app.run(debug=True)