
import json
from cnxpool import cnxpool



cnx = cnxpool.get_connection()
mycursor=cnx.cursor(dictionary = True)
with open('book.json',encoding="utf-8") as f:
  data = json.load(f)
  try:
    for i in data:
      sql = ("INSERT INTO books (bookid, name, category, author, description, image, price, view, stock)"
      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
      adr = (i["id"],i["title"],i["category"],i["author"],i["book_intro"],i["cover"],i["price"],i["view"],100)
      mycursor.execute(sql,adr)
      cnx.commit()
  except:
    cnx.rollback()
    print("伺服器內部錯誤",500)   
  finally:
    mycursor.close()
    cnx.close()
    
