import psycopg2 

from datetime import date

class FDataBase:
  def addrequest(self,fname,lname,email,phone,budget):
        try:
            data_t = date.today()
            self.__cur.execute("INSERT INTO Customers VALUES(NULL, ?, ?, ?, ?, ?)", (fname,lname,email,phone,budget))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Ошибка добавления клиента в БД "+str(e))
            return False