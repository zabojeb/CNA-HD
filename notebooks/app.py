from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = ['Content-Type', 'Access-Control-Allow-Origin']


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
