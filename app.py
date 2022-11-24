from flask import Flask, redirect, url_for, render_template, request, flash, session
import Weather
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countries = db.Column(db.String(50))
    cities = db.relationship('Cities', backref='countries')


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cities = db.Column(db.String(50))
    temp = db.Column(db.Float)
    countries_id = db.Column(db.Integer, db.ForeignKey('countries.id'))

    # def __init__(self, city):
    #     self.cities = city


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form['city']
        try:
            unit = request.form['unit']
        except KeyError:
            result = Weather.WeatherApp(city, "metric")
            if result.status == 'City not found!':
                flash("Not a valid city")
                return render_template("search.html", city_list=Countries.query.all())
            db_city = result.city
            db_country = result.country
            db_temp = result.temp

            found_city = Cities.query.filter_by(cities=db_city).first()
            if found_city:
                flash("city already added!")
            else:
                countri = Countries.query.filter_by(countries=db_country).first()
                if countri:
                    pass
                else:
                    countri = Countries(countries=db_country)
                    db.session.add(countri)
                    db.session.commit()
                citi = Cities(cities=db_city, countries=countri, temp=db_temp)
                db.session.add(citi)
                db.session.commit()
                flash("City added!")
            return render_template("search.html", city_list=Countries.query.all())
        return redirect(url_for("get_weather", city=city, unit=unit, city_list=Countries.query.all()))
    else:
        return render_template("search.html", city_list=Countries.query.all())


@app.route('/<city>/<unit>', methods=["POST", "GET"])
def get_weather(city, unit):
    if request.method == "POST":
        city = request.form['city']
        unit = request.form['unit']
        return redirect(url_for("get_weather", city=city, unit=unit, city_list=Countries.query.all()))

    result = Weather.WeatherApp(city, unit)
    if result.status != 'City not found!':
        cities = Cities.query.filter_by(cities=city).first()
        country = Countries.query.filter_by(countries=cities.countries.countries).first()
        all_city = country.cities
        country_temp = 0.0
        for c in all_city:
            country_temp += c.temp
        country_temp = country_temp/len(all_city)
        print(country_temp)
        return render_template("results.html", city=city, unit=unit, country=cities.countries.countries,
                               temp=result.check_temp(),
                               country_temp=country_temp,
                               city_list=Countries.query.all())
    else:
        return render_template("404page.html", city=city, city_list=Countries.query.all())


@app.route('/add-city/', methods=["POST", "GET"])
def add_city():
    session.pop('_flashes', None)
    return render_template("add-city.html", city_list=Countries.query.all())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# print("File r __name__ is set to: {}".format(__name__))
