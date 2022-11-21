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
            found_city = Cities.query.filter_by(cities=city).first()
            if found_city:
                flash("city already added!")
            else:
                test_city = Weather.WeatherApp(city, "imperial")
                if test_city.status == 'City not found!':
                    flash("Not a valid city")
                    return render_template("search.html", city_list=Cities.query.all())
                citi = Cities(city)
                db.session.add(citi)
                db.session.commit()
                flash("City added!")
            return render_template("search.html", city_list=Cities.query.all())
        return redirect(url_for("get_weather", city=city, unit=unit, city_list=Cities.query.all()))
    else:
        return render_template("search.html", city_list=Cities.query.all())


@app.route('/<city>/<unit>', methods=["POST", "GET"])
def get_weather(city, unit):
    if request.method == "POST":
        city = request.form['city']
        unit = request.form['unit']
        return redirect(url_for("get_weather", city=city, unit=unit, city_list=Cities.query.all()))

    result = Weather.WeatherApp(city, unit)
    if result.status != 'City not found!':
        return render_template("results.html", city=city, unit=unit, temp=result.check_temp(), city_list=Cities.query.all())
    else:
        return render_template("404page.html", city=city, city_list=Cities.query.all())


@app.route('/addcity/', methods=["POST", "GET"])
def add_city():
    session.pop('_flashes', None)
    return render_template("addcity.html", city_list=Cities.query.all())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# print("File r __name__ is set to: {}".format(__name__))
