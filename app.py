from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Customers
from FDataBase import FDataBase
import psycopg2 
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from werkzeug.utils import secure_filename
from UserLogin import UserLogin
import re 

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
  if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
  
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

@app.route("/realty", methods=['GET','POST'])
def realty():
  
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  s = f'SELECT * FROM public."Realty"'
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
  
@app.route("/search", methods=['POST'])
def search():
  if request.method == 'POST':
    object_type=request.form['object_type']
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
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM  public."User" WHERE username = %s', (username,))
        account = cur.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('index'))
            else:
                flash('Неверное имя пользователя/пароль')
        else:
            flash('Неверное имя пользователя/пароль')
 
    return render_template('login.html', title="Вход")


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
    
        _hashed_password = generate_password_hash(password)
 
        cursor.execute('SELECT * FROM public."User" WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            flash('Учетная запись уже существует!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Имя пользователя должно содержать только латинские символы и цифры!')
        elif not username or not password:
            flash('Пожалуйста, заполните форму!')
        elif  len(password) < 4:
           flash('Ваш пароль слишком короткий!')
        elif password != password2:
           flash('Пароли не совпадают')
        else:
            cursor.execute('INSERT INTO public."User"( username, password) VALUES (%s,%s)', (username, _hashed_password))
            conn.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('Пожалуйста, заполните форму!')

    return render_template('registration.html', title="Регистрация")

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route("/add_user")
def add_user():
   pass
   
@app.route("/check_user", methods=['GET','POST'])
def check_user():
   pass




if __name__ == "__main__":
  app.run(debug=True)