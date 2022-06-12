from flask import *
import json
import requests
from cnxpool import cnxpool


api_book_bookId=Blueprint("api_book_bookId", __name__, template_folder="templates")


@api_book_bookId.route("/api/book/<bookId>")
def searchid(bookId):
	try:
		cnx=cnxpool.get_connection()
		mycursor=cnx.cursor(buffered = True, dictionary = True)
		sql ="SELECT bookid, name, category, author, description, image, price, stock, view FROM books WHERE bookid = %s"
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
				"stock":rl["stock"],
				"view":rl["view"],
				"data":result2
			}, 200 


	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500