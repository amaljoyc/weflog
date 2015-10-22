from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Welcome to Weflog!</h1>'


@app.route('/<name>')
def hello_user(name):
    welcome = index()
    return welcome + '<h2>Hello %s...!!</h2>' % name


if __name__ == '__main__':
    app.run(debug=True)
