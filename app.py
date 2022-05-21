from flask import *
# from flask_cors import CORS
# import mysql.connector
import decimal
import ast
import json
import requests
from cnxpool import cnxpool
from datetime import datetime 
from sqlalchemy import true
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
# CORS(app)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key='yyfgswetjhj'


@app.route('/')
def index():
    return render_template('index.html')
@app.route("/book/<id>")
def book(id):
	return render_template("book.html")
@app.route("/addCart")
def booking():
	return render_template("addCart.html")
@app.route("/api/books")
def books():
  keyword = request.args.get("keyword")
  try:
    if keyword == None:
      cnx=cnxpool.get_connection()
      mycursor=cnx.cursor(buffered = True, dictionary = True)
      mycursor.execute("SELECT bookid, name, category, author, description, image, price, view FROM books WHERE category = '應用科學'")
      result1 = mycursor.fetchall()
      mycursor.execute("SELECT bookid, name, category, author, description, image, price, view FROM books WHERE category = '語文'")
      result2 = mycursor.fetchall()
      mycursor.execute("SELECT bookid, name, category, author, description, image, price, view FROM books WHERE category = '藝術'")
      result3 = mycursor.fetchall()
      mycursor.execute("SELECT bookid, name, category, author, description, image, price, view FROM books WHERE category = '人文'")
      result4 = mycursor.fetchall()
      return {'data1': result1,'data2':result2,'data3':result3,'data4':result4}, 200
    else:
      cnx=cnxpool.get_connection()
      mycursor=cnx.cursor(buffered = True, dictionary = True)
      sql ="SELECT bookid, name, category, author, description, image, price, view FROM books WHERE name LIKE %s"
      adr = ('%'+keyword+'%',)
      mycursor.execute(sql,adr)
      result = mycursor.fetchall()
      return {'data': result}, 200      

  except:
    return {"error": True, "message": "伺服器內部錯誤"}, 500
  finally:
    mycursor.close()
    cnx.close()
  

@app.route("/api/book/<bookId>")
def searchid(bookId):
  try:
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor(buffered = True, dictionary = True)
    sql ="SELECT bookid, name, category, author, description, image, price, view FROM books WHERE bookid = %s"
    i = int(bookId)
    adr = (i,)
    mycursor.execute(sql,adr)
    result = mycursor.fetchall()
    if result != []:
      rl = result[0]
      return {
        "bookid":rl["bookid"],
        "name":rl["name"],
        "category":rl["category"],
        "author":rl["author"],
        "description":rl["description"],
        "image":rl["image"],
        "price":rl["price"],
        "view":rl["view"]
      }, 200 

  except:
    return {"error": True, "message": "伺服器內部錯誤"}, 500
  finally:
    mycursor.close()
    cnx.close()
  
@app.route("/api/user")
def memberinfo():
	if session != {}:
		return jsonify({
			"data":{
				"id":session['id'],
				"name":session['name'],
				"email":session['e_mail']
			}
		}),200	
	else:
		return jsonify({
			"data": None
		}),200		  

@app.route("/api/user", methods=["POST"])
def signup():
	try:
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor() 
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

@app.route("/api/user", methods=["PATCH"])
def signin():
	try:
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor()
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

@app.route("/api/user", methods=["DELETE"])
def signout():
	session.clear()
	return jsonify({
		"ok": True
	})

@app.route("/api/addCart")
def check():
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
			print(myresult)
			print(count)
			if count != 0:
				sql2 = "SELECT id,name,category,author,price,image FROM cart WHERE email = %s"		
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
					}
					i+=1
					list.append(prelist.copy())
				print(myresult2)
			return jsonify({
				"count":count,"data":list
		}),200

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




@app.route("/api/addCart",methods=["POST"])
def addCart():
	if "e_mail" in session :
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)
		req = request.get_json()
		bookid = req["id"]
		email = session['e_mail']
		sql = "SELECT name,category,author,price,image FROM books WHERE bookid = %s"
		adr = (bookid,)	
		mycursor.execute(sql, adr)
		myresult = mycursor.fetchall()
		x = myresult[0]
		name = x['name']
		category = x['category']
		author = x['author']
		price = x['price']
		image = x['image']
		if myresult != []:
			sql = ("INSERT INTO cart(bookid,name,category,author,price,image,email)"
			"VALUES(%s,%s,%s,%s,%s,%s,%s)")		
			adr = (bookid,name,category,author,price,image,email)
			mycursor.execute(sql,adr)
			cnx.commit()
			sql2 = "SELECT id FROM cart WHERE name = %s"
			adr2 = (name,)
			mycursor.execute(sql2,adr2)
			result = mycursor.fetchone()
			print(result)
			cartid = result['id']

			return jsonify({
				"id":cartid,
			"name":name,
			"categoey":category,
			"author":author,
			"price":price,
			"image":image
		})
	else:
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}),403				





app.run(port=3000,debug=True)
# app.run(host='0.0.0.0', port=3000,debug=True)