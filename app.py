from db.db import db
from flask import Flask, render_template, make_response

app = Flask(__name__)
print("Hello")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/holidays", methods=["GET"])
def serve_holidays():
    holidays = db.get_holidays("*")

    return make_response(holidays, 200)


if __name__ == "__main__":
    app.run()