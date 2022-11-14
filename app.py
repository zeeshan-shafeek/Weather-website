from flask import Flask
import Weather

app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <h1>hello!</h1>
    <h2>welcome to the this simple weather website</h2>
    <p> Please enter the city in at the end of the link </p>
    '''

@app.route('/<city>')
def get_weather(city):
    w = Weather.WeatherApp(city, 'metric')
    if w.status != 'City not found!':
        return f'temp: {w.check_temp()} °C'
    else:
        return f'<h1>{w.status}</h1>'



if __name__ == "__main__":
    app.run()

# print("File r __name__ is set to: {}".format(__name__))
