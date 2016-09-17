from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Bad Request</h1>',400
if __name__=='__main__':
    app.run(debug=True)