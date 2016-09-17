from flask import Flask
from flask import request
from flask.ext.script import Manager
app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
if __name__=='__main__':
    manager.run()