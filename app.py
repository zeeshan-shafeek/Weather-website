from flask import Flask, redirect, url_for, render_template, request
import Weather

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        city = request.form['city']
        unit = request.form['unit']
        return redirect(url_for("get_weather", city=city, unit=unit))
    else:
        return render_template("search.html")

    # return '''
    # <h1>hello!</h1>
    # <h2>welcome to the this simple weather website</h2>
    # <p> Please enter the city in at the end of the link </p>
    # '''


@app.route('/<city>/<unit>')
def get_weather(city, unit):
    result = Weather.WeatherApp(city, unit)
    if result.status != 'City not found!':
        return render_template("results.html", city=city, unit=unit, temp=result.check_temp())
    else:
        return render_template("404page.html", city=city)


if __name__ == "__main__":
    app.run(debug=True)

# print("File r __name__ is set to: {}".format(__name__))
