from flask import Flask, render_template
from main import start
from param import katespade, nordstrom, evisu

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('main_page.html')

@app.route('/nordstrom/')
def call_nordstrom():
  return start(nordstrom)

@app.route('/katespade/')
def call_katespade():
  return  start(katespade)

@app.route('/evisu/')
def call_evisu():
  return  start(evisu)


if __name__ == '__main__':
  app.run(debug=True)