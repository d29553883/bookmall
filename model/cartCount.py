from flask import *
import json
import requests
from cnxpool import cnxpool

class CartCountModel:
  def cartCount(self):
    cnx=cnxpool.get_connection()
    mycursor=cnx.cursor()
    try:
      if session != {}:
        email = session["e_mail"]
        mycursor.execute("SELECT count(name) FROM cart WHERE email = %s " ,(email,))
        myresult = mycursor.fetchall()
        return jsonify({
          "count":myresult[0]
        }),200
      else:
        return jsonify({
          "error": True,
          "message": "未登入系統，拒絕存取"
        }),403
    except:
      return jsonify({
        "error": True,
        "message": "伺服器崩潰"
      }),500
    finally:
      mycursor.close()
      cnx.close()



cartCount_model = CartCountModel()