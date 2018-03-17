import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import arrow
import acp_times
# import config

import logging

app = Flask(__name__)

client = MongoClient('db', 27017)

#getting a databse
db = client.tododb
db.tododb.delete_many({})
# db.tododb.drop()
#
# CONFIG = config.configuration()
# app.secret_key = CONFIG.SECRET_KEY

#clear the data already in the databse



@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.route('/todo')
def todo():
#getting a collection:a group of documents stored in Mongodb

    # app.logger.debug("1")
    _items = db.tododb.find()
    # # app.logger.debug(_items);
    items = [item for item in _items]
    #app.logger.debug(items)
    return render_template('todo.html', items = items)


@app.route('/new', methods = ['post'])

def new():
    app.logger.debug(request.form)
    mi = request.form['mi']
    km = request.form['km']
    open_time = request.form['open']
    begin_time = request.form['time']
    begin_date = request.form['date']
    close_time = request.form['close']




    #documents
    item_doc = {
        'mi': mi,
        'km': km,
        'open_time':open_time,
        'begin_date':begin_date,
        'begin_time':begin_time,
        'close_time':close_time
    }
    db.tododb.insert_one(item_doc)

    return "something"

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times


    distance = request.args.get("distance", type=int)
    begin_time = request.args.get("begin_time", 999, type=str)
    begin_date = request.args.get("begin_date", type=str)

    #in order to have format
    #tring to add am/pm here, but how?
    brevet_start_time = arrow.get(begin_date + " " + begin_time, "YYYY-MM-DD HH:mm")
    #change the time zone
    brevet_start_time = brevet_start_time.shift(hours =+ 8)

    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, distance, brevet_start_time)
    close_time = acp_times.close_time(km, distance, brevet_start_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/favicon.ico")
def favicon():
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    # flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
