from database.db import Database
from flask import Flask, render_template, make_response, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/holidays", methods=["GET"])
def serve_holidays():
    location = request.args.get("location")

    if location is None:
        return make_response(None, 400)
    
    with Database() as db:
        holidays = db.get_holidays(location)

    return make_response(holidays, 200)


if __name__ == "__main__":
    app.run(debug=True)