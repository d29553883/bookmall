from flask import *
import json
from cnxpool import cnxpool


class HistoryModel:
  def history(self):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor(buffered = True, dictionary = True)  
    try:
      if session != {}:
        email = session["e_mail"]
        sql = "SELECT number,name,author,price,count FROM orderhistory WHERE email = %s" 
        adr = (email,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        return jsonify({
          "data":myresult
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



history_model = HistoryModel()