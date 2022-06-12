from flask import *
import json
import requests
from cnxpool import cnxpool



api_books=Blueprint("api_books", __name__, template_folder="templates")


@api_books.route("/api/books")
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