from flask import *
import json
import requests
from cnxpool import cnxpool

class UserModel:
  def memberinfo(self):
    if session != {}:
      return jsonify({
        "data":{
          "name":session['name'],
          "email":session['e_mail']
        }
      }),200	
    else:
      return jsonify({
        "data": None
      }),200


  def signup(self):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor() 	
    try:
      req = request.get_json()
      e_mail = req["email"]
      sql = "SELECT email FROM member WHERE email = %s"
      adr = (e_mail, )
      mycursor.execute(sql, adr)
      myresult = mycursor.fetchall()
      if myresult != [] :
        response= make_response(jsonify({
          "error": True,
          "message": "此email已存在"
        }),400)
        return response
      else:
        Name = req["name"]
        e_mail = req["email"]
        passWord = req["password"]
        mycursor.execute("INSERT INTO member(name, email, password) VALUES(%s, %s, %s)",(Name, e_mail, passWord))
        cnx.commit()
        return jsonify({
          "ok": True
        })
    except:
      return jsonify({
        "error": True,
        "message": "伺服器崩潰"
      }),500
    finally:
      if cnx.in_transaction:
        cnx.rollback()
      cnx.close()
      

  def signin(self):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor()	
    try:
      req = request.get_json()
      e_mail = req["email"]
      passWord = req["password"]
      sql = "SELECT email,password FROM member WHERE email = %s AND password = %s"
      adr = (e_mail,passWord, )
      mycursor.execute(sql, adr)
      myresult = mycursor.fetchall()
      if myresult != []:
        sql2 = "SELECT id,name,email FROM member WHERE email = %s"
        adr2 = (e_mail,)
        mycursor.execute(sql2, adr2)
        myresult = mycursor.fetchall()
        x = myresult[0]
        x.__str__()
        session['id']= int(x[0])
        session["name"]= x[1]
        session["e_mail"]= x[2]
        return jsonify({
          "ok": True
        })
      else:
        return jsonify({
          "error": True,
          "message": "帳號或密碼錯誤"
        }),400
    except:
      return jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
      }),500
    finally:
      if cnx.in_transaction:
        cnx.rollback()
      cnx.close()

  def signout(self):
    session.clear()
    return jsonify({
      "ok": True
    })




user_model = UserModel()