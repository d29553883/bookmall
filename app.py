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
from flask_oauthlib.client import OAuth
import os
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

oauth = OAuth(app)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SERCET = os.getenv("GOOGLE_CLIENT_SERCET")
google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SERCET,
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

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
		
@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))	
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect('/')
@app.route('/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    # 此處可使用 user_info 中的資訊，如 user_info.data['email'] 等
    email = user_info.data['email']
    session["e_mail"] = email
    session["name"] = email.replace('@gmail.com', '')
    return redirect('/')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
app.run(host='0.0.0.0', port=3000)