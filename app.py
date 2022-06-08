from flask import *
# from flask_cors import CORS
# import mysql.connector
from pip._vendor import cachecontrol
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import boto3
import decimal
import ast
import json
import requests
from cnxpool import cnxpool
from datetime import datetime 
from sqlalchemy import true
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
# CORS(app)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key='yyfgswetjhj'
ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
s3 = boto3.client('s3',
                    aws_access_key_id = ACCESS_KEY_ID,
                    aws_secret_access_key = ACCESS_SECRET_KEY,
                     )

BUCKET_NAME='aws-test-learn-s3'



@app.route('/')
def index():
    return render_template('index.html')
@app.route("/book/<id>")
def book(id):
	return render_template("book.html")
@app.route("/addCart")
def booking():
	return render_template("addCart.html")
@app.route("/account")
def account():
	return render_template("account.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")		
@app.route("/api/books")
def books():
	try:
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)
		keyword = request.args.get("keyword")
		if keyword == None:
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
			sql ="SELECT bookid, name, category, author, description, image, price, view FROM books WHERE name LIKE %s"
			adr = ('%'+ keyword +'%',)
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
		mycursor.execute("SELECT recomment.message,recomment.username,account.image FROM recomment join account on recomment.email = account.email where recomment.bookid =%s" , (bookId,))
		result2 = mycursor.fetchall()
		if result2 == []:
			mycursor.execute("SELECT recomment.message,recomment.username FROM recomment where recomment.bookid =%s" , (bookId,))
			result2 = mycursor.fetchall()
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
				"view":rl["view"],
				"data":result2
			}, 200 



	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

	# finally:
	# 		mycursor.close()
	# 		cnx.close()



  
@app.route("/api/user")
def memberinfo():
	if session != {}:
		return jsonify({
			"data":{
				# "id":session['id'],
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
# @login_is_required
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

@app.route("/api/addCart", methods=["DELETE"])
def deleteBook():
	try:
		if session != {}:
			cnx=cnxpool.get_connection()
			mycursor=cnx.cursor()			
			req = request.get_json()
			deleteBookId = req["deleteBookId"]		
			sql2 = "SELECT price FROM cart where id = %s"
			adr2 = (deleteBookId,)
			mycursor.execute(sql2, adr2)
			myresult = mycursor.fetchone()
			sql = "DELETE FROM cart where id = %s"
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



@app.route('/api/accountPic' ,methods=['POST'])
def update_pic():
	img = request.files['file']
	email = session["e_mail"]
	if(len(request.files) != 0):
		img = request.files['file']
		filename = secure_filename(img.filename)
		print('圖檔',img)
		print('圖檔名稱',filename)
	try:
		s3.upload_fileobj(img,BUCKET_NAME,filename)
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500
	try:
		cnx = cnxpool.get_connection()
		mycursor=cnx.cursor(dictionary = True)
		sql = ("INSERT INTO account (email, image)"
		"VALUES (%s, %s) ON duplicate KEY UPDATE"
		"`email` =VALUES(`email`),`image`=VALUES(`image`)")
		adr = (email, "https://d1kfzndf9j846w.cloudfront.net/"+filename)
		mycursor.execute(sql,adr)
		cnx.commit()
	except:
		cnx.rollback()
		return {"error": True, "message": "伺服器內部錯誤"}, 500
	finally:
		mycursor.close()
		cnx.close()
				
	return {'ok': True}, 200

@app.route('/api/accountPic', methods=['GET'])
def get_pic():
		try:
				cnx = cnxpool.get_connection()
				cursor = cnx.cursor(buffered = True, dictionary = True)
				email = session["e_mail"]
				name = session["name"]
				sql = ("SELECT image FROM account WHERE email = %s")
				adr = (email,)
				cursor.execute(sql,adr)
				result = cursor.fetchall()			

		except:
				return {"error": True, "message": "伺服器內部錯誤"}, 500
		finally:
				cursor.close()
				cnx.close()

		return {'data': result,'name':name,'email':email}, 200
	


@app.route("/api/orders",methods=["POST"])
def createBook():
	try:
		if session != {}:
			cnx=cnxpool.get_connection()
			mycursor=cnx.cursor()			
			partnerKey = os.getenv("PARTNERKEY")
			req = request.get_json()
			prime = req["prime"]
			email = req["email"]
			phone = req["phone"]
			address = req["address"]
			sql = "SELECT name,author,price from cart WHERE email = %s" 
			adr = (email,)
			mycursor.execute(sql, adr)
			myresult = mycursor.fetchall()
			pricetotal = 0
			for i in myresult:	
				price	= i[2]
				pricetotal += price
			number = datetime.now().strftime('%Y%m%d%H%M%S')
			username = req["username"]
			if phone !="":
				header = {
					"content-type": "application/json",
					"x-api-key": partnerKey
				}
				my_data = {
						"prime": prime,
						"partner_key": partnerKey,
						"merchant_id": "d29553883_CTBC",
						"details":"TapPay Test",
						"amount": pricetotal,
						"cardholder": {
							"phone_number": phone,
							"name": username,
							"email": email,
						},
						"remember": True
					}
				response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', json = my_data, headers=header)
				data = response.json()
				status = data["status"]
				rec_trade_id = data["rec_trade_id"]
				if status == 0:
					for i in myresult:	
						name = i[0]
						author = i[1]
						price	= i[2]
						sql2 = ("INSERT INTO orderhistory(number,name,author,price,username,email,phone,address,status,rec_trade_id)" 
						" VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")		
						adr2 = (number,name,author,price,username,email,phone,address,status,rec_trade_id)
						mycursor.execute(sql2,adr2)
						cnx.commit()
						mycursor.execute("DELETE FROM cart where email= %s",(email,))
						cnx.commit()
					return jsonify({
						"data": {
							"number": number,
							"payment": {
							 "status":status,
							 "message": "付款成功"
						}
						}
					})
				else:
					sql2 = ("INSERT INTO orderhistory(number,name,author,price,username,email,phone,address,status)" 
					" VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")		
					adr2 = (number,name,author,price,username,email,phone,address,status)
					mycursor.execute(sql2,adr2)
					cnx.commit()
					return jsonify({
						"data": {
							"number": number,
							"payment": {
							 "status":status,
							 "message": "付款失敗"
						}
						}
					})					
			else:
				return jsonify({
					"error": True,
					"message": "建立失敗，資料沒輸入"
				}),400				
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
		if cnx.in_transaction:
			cnx.rollback()
		cnx.close()



@app.route("/api/refund",methods=["POST"])
def refund():
	try:
		req = request.get_json()
		orderNumber = req["orderNumber"]
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)			
		partnerKey = os.getenv("PARTNERKEY")
		mycursor.execute("SELECT rec_trade_id FROM orderhistory WHERE number = %s" ,(orderNumber,))
		myresult = mycursor.fetchall()
		print(myresult)
		rec_trade_id = myresult[0]["rec_trade_id"]
		header = {
		"content-type": "application/json",
		"x-api-key": partnerKey
		}
		my_data = {
			"partner_key": partnerKey,
			"rec_trade_id": rec_trade_id,
		}
		response = requests.post('https://sandbox.tappaysdk.com/tpc/transaction/refund', json = my_data, headers=header)
		data = response.json()
		print(data)
		status = data["status"]
		if status == 0:
			return jsonify({
				"data": {
					"status":status,
					"message": "退款成功"
				}
			})
		else:
			return jsonify({
				"data": {
					"status":status,
					"message": "退款失敗"
				}
			})
	except:
		return jsonify({
			"error": True,
			"message": "伺服器內部錯誤"
		}),500	
	finally:
		if cnx.in_transaction:
			cnx.rollback()
		cnx.close()				



@app.route("/api/orders/<orderNumber>")
def thankyouPage(orderNumber):
	try:
		if session != {}:
			cnx=cnxpool.get_connection()
			mycursor=cnx.cursor()
			sql = "SELECT number FROM orderhistory WHERE number = %s" 
			adr = (orderNumber,)
			mycursor.execute(sql, adr)
			myresult = mycursor.fetchall()
			x = myresult[0]
			x.__str__()
			number = x[0]
			return jsonify({
				"data":{"number":number}
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


@app.route('/api/hidtory', methods=['GET'])
def history():
	if session != {}:
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)
		email = session["e_mail"]
		sql = "SELECT number,name,author,price FROM orderhistory WHERE email = %s" 
		adr = (email,)
		mycursor.execute(sql, adr)
		myresult = mycursor.fetchall()
		return jsonify({
			"data":myresult
		})


@app.route('/api/recomment' ,methods=['POST'])
def input_message():
	x = request.form
	bookid = request.form['bookid']
	message = request.form['message']	

	try:
		if session != {}:
			username = session["name"]
			email = session["e_mail"]	
			cnx = cnxpool.get_connection()
			mycursor=cnx.cursor(dictionary = True)
			mycursor.execute("INSERT INTO recomment (bookid, username, email, message) VALUES (%s,%s,%s,%s)", (bookid,username,email,message))
		else:
				return jsonify({
					"error": True,
					"message": "未登入系統，拒絕存取"
				}),403			
	except:
		cnx.rollback()
		return {"error": True, "message": "伺服器內部錯誤"}, 500
	finally:
		mycursor.close()
		cnx.commit()
		cnx.close()
				
	return {'ok': True}, 200
	


# app.run(port=3000)
app.run(host='0.0.0.0', port=3000)