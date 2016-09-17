from flask import Flask
from flask import request
from flask import redirect
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('http://www.cuit.edu.cn')
if __name__=='__main__':
    app.run(debug=True)