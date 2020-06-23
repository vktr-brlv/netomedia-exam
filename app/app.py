from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/intense')
def intense():
    os.system('pystress')
    return 'CPU load finished'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
