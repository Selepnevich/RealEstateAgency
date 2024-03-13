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
import datetime

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
  return render_template('index.html', title ='Главная')   


@app.route("/add_ticket", methods=['POST'])
def add_ticket():
   if request.method == 'POST' and 'fname' in request.form  \
    and 'lname' in request.form \
    and 'phone' in request.form:
      cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      fname=request.form['fname']
      lname=request.form['lname']
      email=request.form['email']
      phone=request.form['phone']
      cur.execute(f'SELECT phone FROM public."Customers" WHERE phone= \'{phone}\'')
      list_phone = cur.fetchone()
      if phone!=list_phone:
          # Добавление данных в Таблицу "Клиенты"
          cur.execute('INSERT INTO public."Customers"(fname,lname,email,phone)\
                      VALUES (%s,%s,%s,%s)', \
                      (fname,lname,email,phone))
          conn.commit()

      # Запрос возвращает id Клиента который отправил данные
      customer_id = cur.execute(f'SELECT id FROM public."Customers" WHERE fname = \'{fname}\'')
      customer_id = cur.fetchone()[0]

      #Запрос определяющий агентов с наименьшим количеством запросов
      agent_id = cur.execute('SELECT a.id AS queries_count\
                  FROM public."Agents" as a\
                  LEFT JOIN (\
                      SELECT agent_id, COUNT(*) AS ticket_count\
                      FROM public."Tickets"\
                      GROUP BY agent_id\
                  ) AS t ON a.id = t.agent_id\
                  ORDER BY COALESCE(t.ticket_count, 0)\
                  LIMIT 1')
      agent_id = cur.fetchone()[0]

      #Добавление данных в таблицу "Заявки"
      cur.execute('INSERT INTO public."Tickets"(customer_id,agent_id, tickets_start_date)\
                   VALUES (%s,%s,%s)', \
                  (customer_id, agent_id, datetime.datetime.now()))
      conn.commit()
      flash('Ваша заявка отправлена, в течении дня с вами свяжется наш агент')
      return redirect(url_for('index'))

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
  cur.execute( f'SELECT a.id\
              FROM public."User" as u\
              INNER JOIN public."Profile" as p ON u.id = p.user_id\
              INNER JOIN public."Agents" as a ON a.id = p.agent_id \
              WHERE u.username = \'{session['username']}\'')
  id_agent = cur.fetchone()[0]
  cur.execute(f' SELECT c.id, c.fname, c.lname, c.phone, c.email, t.tickets_start_date \
              FROM public."Tickets" as t\
              INNER JOIN public."Agents" as a ON a.id = t.agent_id\
              INNER JOIN public."Customers" as c ON c.id = t.customer_id\
              WHERE a.id = \'{id_agent}\'')
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
      cur.execute(f'SELECT phone FROM public."Customers" WHERE phone= \'{phone}\'')
      list_phone = cur.fetchone()
      print(list_phone)
      if phone!=list_phone:
          cur.execute('INSERT INTO public."Customers" (fname,lname,email,phone)\
                      VALUES (%s,%s,%s,%s)', \
                      (fname,lname,email,phone))
          conn.commit()
          customer_id = cur.execute(f'SELECT id FROM public."Customers" WHERE fname = \'{fname}\'')
          customer_id = cur.fetchone()[0]
          cur.execute( f'SELECT a.id\
              FROM public."User" as u\
              INNER JOIN public."Profile" as p ON u.id = p.user_id\
              INNER JOIN public."Agents" as a ON a.id = p.agent_id \
              WHERE u.username = \'{session['username']}\'')
          agent_id = cur.fetchone()[0]
          cur.execute('INSERT INTO public."Tickets"(customer_id,agent_id, tickets_start_date)\
                   VALUES (%s,%s,%s)', \
                  (customer_id, agent_id, datetime.datetime.now()))
          conn.commit()
          flash('Клиент успешно добавлен')
          return redirect(url_for('clients'))
      else:
         flash('Невозможно добавить клиента')
  

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
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
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
            #Добавление пользователя
            cursor.execute('INSERT INTO public."User"(username, password) VALUES (%s,%s)', (username, _hashed_password))
            conn.commit()

            #Добавление агента
            cursor.execute('INSERT INTO public."Agents"(fname, lname, email) VALUES (%s,%s,%s)', (fname, lname, email))
            conn.commit()

            user_id = cursor.execute(f'SELECT id FROM public."User" WHERE username= \'{username}\'')
            user_id = cursor.fetchone()[0]
            agent_id = cursor.execute(f'SELECT id FROM public."Agents" WHERE fname= \'{fname}\'')
            agent_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO public."Profile"(user_id, agent_id) VALUES (%s,%s)', (user_id, agent_id))
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
   
@app.route("/profile", methods=['GET','POST'])
def profile():
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  if not {session['username']}:
      return redirect(url_for('login'))
  cur.execute( f'SELECT a.id, u.username, a.fname, a.lname, a.phone, a.email\
              FROM public."User" as u\
              INNER JOIN public."Profile" as p ON u.id = p.user_id\
              INNER JOIN public."Agents" as a ON a.id = p.agent_id \
              WHERE u.username = \'{session['username']}\'')
  data_profile = cur.fetchall()

  cur.execute(f' SELECT c.fname, c.lname, c.phone, c.email, t.tickets_start_date \
              FROM public."Tickets" as t\
              INNER JOIN public."Agents" as a ON a.id = t.agent_id\
              INNER JOIN public."Customers" as c ON c.id = t.customer_id\
              WHERE a.id = \'{data_profile[0][0]}\'')
  data_ticket = cur.fetchall()

  return render_template('profile.html', title="Профиль", data_profile=data_profile, data_ticket=data_ticket)

    



if __name__ == "__main__":
  app.run(debug=True)