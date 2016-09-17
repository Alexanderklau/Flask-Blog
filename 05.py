from flask import Flask
from flask import request
from flask import abort
app = Flask(__name__)

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello,%s</h1>' % user.name
if __name__=='__main__':
    app.run(debug=True)