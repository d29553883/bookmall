from flask import *
import boto3
import json
import requests
from cnxpool import cnxpool
from werkzeug.utils import secure_filename
import os


ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
s3 = boto3.client('s3',
                    aws_access_key_id = ACCESS_KEY_ID,
                    aws_secret_access_key = ACCESS_SECRET_KEY,
                     )

BUCKET_NAME='aws-test-learn-s3'



api_accountPic=Blueprint("api_accountPic", __name__, template_folder="templates")


@api_accountPic.route('/api/accountPic' ,methods=['POST'])
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
		sql = ("INSERT INTO account2 (email, image)"
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



@api_accountPic.route('/api/accountPic', methods=['GET'])
def get_pic():
	try:
		cnx = cnxpool.get_connection()
		cursor = cnx.cursor(buffered = True, dictionary = True)
		email = session["e_mail"]
		name = session["name"]
		sql = ("SELECT image FROM account2 WHERE email = %s")
		adr = (email,)
		cursor.execute(sql,adr)
		result = cursor.fetchall()		
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500
	finally:
		cursor.close()
		cnx.close()

	return {'data': result,'name':name,'email':email}, 200