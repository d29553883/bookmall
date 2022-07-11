from flask import *
import json
from cnxpool import cnxpool

class RecommentModel:
  def input_message(self):
    x = request.form
    bookid = request.form['bookid']
    message = request.form['message']	
    cnx = cnxpool.get_connection()
    mycursor=cnx.cursor(dictionary = True)
    try:
      if session != {}:
        username = session["name"]
        email = session["e_mail"]	
        mycursor.execute("INSERT INTO recomment2 (bookid, username, email, message) VALUES (%s,%s,%s,%s)", (bookid,username,email,message))
        cnx.commit()
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
      cnx.close()
          
    return {'ok': True}, 200

recomment_model = RecommentModel()