from flask import *
import json
import requests
from cnxpool import cnxpool

class AddCartModel:
  def check(self):
    try:
      cnx=cnxpool.get_connection()
      mycursor=cnx.cursor()
      if "e_mail" in session :
        email = session['e_mail']
        sql = "SELECT count(*) FROM cart WHERE email = %s"
        adr = (email,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        count = myresult[0][0]
        if count != 0:
          sql2 = "SELECT id,name,category,author,price,image,stock FROM cart WHERE email = %s"		
          adr2 = (email,)
          mycursor.execute(sql2, adr2)
          myresult2 = mycursor.fetchall()
          list = []
          i = 0
          while i<count:
            prelist= {
              "id":myresult2[i][0],
              "name":myresult2[i][1],
              "category":myresult2[i][2],
              "author":myresult2[i][3],
              "price":myresult2[i][4],
              "image":myresult2[i][5],
              "stock":myresult2[i][6],
            }
            i+=1
            list.append(prelist.copy())
          return jsonify({
            "count":count,"data":list
        }),200
        else:
          return jsonify({
            "data":None
          })		

      else:
        return jsonify({
          "error": True,
          "message": "未登入系統，拒絕存取"
        }),403
    except:
      return jsonify({
        "error": True,
        "message": "伺服器內部錯誤"
      }),500
    finally:
      mycursor.close()
      cnx.close()

  def addCart(self):
    if "e_mail" in session :
      cnx=cnxpool.get_connection()
      mycursor=cnx.cursor(buffered = True, dictionary = True)
      req = request.get_json()
      bookid = req["id"]
      email = session['e_mail']
      sql = "SELECT name,category,author,price,image,stock FROM books WHERE bookid = %s"
      adr = (bookid,)	
      mycursor.execute(sql, adr)
      myresult = mycursor.fetchall()
      x = myresult[0]
      name = x['name']
      category = x['category']
      author = x['author']
      price = x['price']
      image = x['image']
      stock = x['stock']
      if myresult != []:
        sql = ("INSERT INTO cart(bookid,name,category,author,price,image,email,stock)"
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")		
        adr = (bookid,name,category,author,price,image,email,stock)
        mycursor.execute(sql,adr)
        cnx.commit()
        sql2 = "SELECT id FROM cart WHERE name = %s"
        adr2 = (name,)
        mycursor.execute(sql2,adr2)
        result = mycursor.fetchone()
        cartid = result['id']

        return jsonify({
          "id":cartid,
        "name":name,
        "category":category,
        "author":author,
        "price":price,
        "image":image
      })
    else:
      return jsonify({
        "error": True,
        "message": "未登入系統，拒絕存取"
      }),403


  def deleteBook(self):
    try:
      if session != {}:
        cnx=cnxpool.get_connection()
        mycursor=cnx.cursor()			
        req = request.get_json()
        deleteBookId = req["deleteBookId"]		
        sql2 = "SELECT price FROM cart WHERE id = %s"
        adr2 = (deleteBookId,)
        mycursor.execute(sql2, adr2)
        myresult = mycursor.fetchone()
        sql = "DELETE FROM cart WHERE id = %s"
        adr = (deleteBookId,)
        mycursor.execute(sql, adr)
        cnx.commit()		
        return jsonify({
          "ok": True,
          "price":myresult[0]
        })
      else:
        return jsonify({
          "error": True,
          "message": "未登入系統，拒絕存取"
        }),403
    finally:
      if cnx.in_transaction:
        cnx.rollback()
      cnx.close()	


addCart_model = AddCartModel()