from flask import *
from controller.api_books import api_books
from controller.api_book_bookId import api_book_bookId
from controller.api_cartCount import api_cartCount
from controller.api_user import api_user
from controller.api_addCart import api_addCart
from controller.api_accountPic import api_accountPic
from controller.api_orders import api_orders
from controller.api_refund import api_refund
from controller.api_history import api_history
from controller.api_recomment import api_recomment


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key='yyfgswetjhj'

app.register_blueprint(api_books)
app.register_blueprint(api_book_bookId)
app.register_blueprint(api_cartCount)
app.register_blueprint(api_user)
app.register_blueprint(api_addCart)
app.register_blueprint(api_accountPic)
app.register_blueprint(api_orders)
app.register_blueprint(api_refund)
app.register_blueprint(api_history)
app.register_blueprint(api_recomment)



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
	
		
	
app.run(host='0.0.0.0', port=3000)