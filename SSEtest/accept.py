from flask import Flask, request

app = Flask(__name__)


@app.route('/accept', methods=["POST"])
def hello_world():
    print(request.json)
    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"))
