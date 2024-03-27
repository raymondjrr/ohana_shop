from flask import Flask

app = Flask(__name__, static_url_path='/static')
# need this secret key for SESSION to work
app.secret_key='py is life'