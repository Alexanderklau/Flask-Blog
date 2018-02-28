# coding : utf-8
__author__ = 'lau.wenbo'
from flask import Flask


app = Flask(__name__)



@app.route('/')
def index():
    return 'hello world!', 400


@app.route('/item/<id>')
def item(id):
    return '<h1>Item: {}</h1>'.format(id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
