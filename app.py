from database.db import Database
from flask import Flask, render_template, make_response, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/bookings/new", methods=["POST"])
def add_new_booking():

    print("We managed to get pyscript to send a POST request")

    new_booking = request.json

    print(new_booking)

    # make models out of the data that was received


    # invalid data
        # return ERROR status code 400

    # valid data
        # run a database function

    return make_response({"status" : "Booking succesful."}, 200)


@app.route("/api/holidays", methods=["GET"])
def serve_holidays():
    location = request.args.get("location")

    if location is None:
        return make_response(None, 400)
    
    with Database() as db:
        holidays = db.get_holidays_by_location(location)

    return make_response(holidays, 200)


if __name__ == "__main__":
    app.run(debug=True)