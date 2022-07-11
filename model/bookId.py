from flask import *
import json
import requests
from cnxpool import cnxpool

class BookIdModel:
  def searchid(self,bookId):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor(buffered = True, dictionary = True)	
    try:
      sql ="SELECT bookid, name, category, author, description, image, price, stock, view FROM books WHERE bookid = %s"
      i = int(bookId)
      adr = (i,)
      mycursor.execute(sql,adr)
      result = mycursor.fetchall()
      mycursor.execute("SELECT recomment2.message,recomment2.username,account2.image FROM recomment2 join account2 on recomment2.email = account2.email where recomment2.bookid =%s" , (bookId,))
      result2 = mycursor.fetchall()
      if result2 == []:
        mycursor.execute("SELECT recomment2.message,recomment2.username FROM recomment2 where recomment2.bookid =%s" , (bookId,))
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

    finally:
      mycursor.close()
      cnx.close()	


bookId_model = BookIdModel()

