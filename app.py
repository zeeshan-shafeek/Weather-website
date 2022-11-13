from flask import Flask

app = Flask(__name__)


@app.route('/home')
def home():
    return 'hello! this is nice?'


if __name__ == "__main__":
    app.run()

# print("File r __name__ is set to: {}".format(__name__))
for _ in range(10):
    print("hehe")
