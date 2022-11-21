from flask import Flask, redirect, url_for, render_template, request, flash, session
import Weather
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Cities(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    cities = db.Column(db.String(50))

    def __init__(self, city):
        self.cities = city


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form['city']
        try:
            unit = request.form['unit']
        except KeyError:
            flash("City added!")
            return render_template("search.html")
        return redirect(url_for("get_weather", city=city, unit=unit))
    else:
        return render_template("search.html")

    # return '''
    # <h1>hello!</h1>
    # <h2>welcome to the this simple weather website</h2>
    # <p> Please enter the city in at the end of the link </p>
    # '''


@app.route('/<city>/<unit>', methods=["POST", "GET"])
def get_weather(city, unit):
    if request.method == "POST":
        city = request.form['city']
        unit = request.form['unit']
        return redirect(url_for("get_weather", city=city, unit=unit))

    result = Weather.WeatherApp(city, unit)
    if result.status != 'City not found!':
        return render_template("results.html", city=city, unit=unit, temp=result.check_temp())
    else:
        return render_template("404page.html", city=city)


@app.route('/addcity/', methods=["POST", "GET"])
def add_city():
    session.pop('_flashes', None)
    return render_template("addcity.html")


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()

# print("File r __name__ is set to: {}".format(__name__))
