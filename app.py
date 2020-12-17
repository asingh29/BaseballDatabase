from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/arod')
def arod():
    return render_template('arod.html')

@app.route('/altitude')
def altitude():
    return render_template('altitude.html')

@app.route('/peds')
def peds():
    return render_template('peds.html')

@app.route('/lookup')
def lookupPlayer():
    return render_template('lookup.html')