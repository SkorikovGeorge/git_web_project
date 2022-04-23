from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return '<h1> First commit <h1>'


if __name__ == '__main__':
    app.run(debug=True)
