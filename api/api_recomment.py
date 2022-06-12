from flask import *
import json
from cnxpool import cnxpool





api_recomment=Blueprint("api_recomment", __name__, template_folder="templates")


@api_recomment.route('/api/recomment' ,methods=['POST'])
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