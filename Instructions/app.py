from flask import Flask, jsonify
import pandas as pd

import numpy as np

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#create engine
engine = create_engine("sqlite:///Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base= automap_base()

# # reflect the tables
Base.prepare(engine, reflect=True)

# # We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement= Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

inspector=inspect(engine)

inspector.get_columns("measurement")

#variables needed
end_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
e=dt.datetime.strptime(*end_date, "%Y-%m-%d")
start_date=e-dt.timedelta(days=365)

station=session.query(Measurement.station).\
                              group_by(Measurement.station).\
                                  order_by((Measurement.station).desc()).all()
list_1= np.ravel(station)
highestNumberTemp_stations=list_1[0]
results_2=session.query(Measurement.date).\
                        filter(Measurement.date>=start_date).\
                        order_by(Measurement.date).all()

r=np.ravel(results_2)


#start flask app
app= Flask(__name__)

@app.route("/")
def home():
     return "welcome to my page"

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results=session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date>=start_date).\
                filter(Measurement.prcp.isnot(None)).\
                order_by(Measurement.date).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    station=session.query(Measurement.station).\
                              group_by(Measurement.station).\
                                  order_by((Measurement.station).desc()).all()
    session.close()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)
    station=session.query(Measurement.station).\
                              group_by(Measurement.station).\
                                  order_by((Measurement.station).desc()).all()
    list_1= np.ravel(station)
    highestNumberTemp_stations=list_1[0]
    results_2=session.query(Measurement.date, Measurement.tobs).\
                        filter(Measurement.date>=start_date).\
                        filter(Measurement.station==highestNumberTemp_stations).\
                        order_by(Measurement.date).all()
    session.close()
    return jsonify(results_2)

@app.route("/api/v1.0/<start>")
def date(start):
    session=Session(engine)
    search_term=session.query(Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    session.close()
    start_list= list(np.ravel(search_term))
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")

def dates(start, end):
    session=Session(engine)
    search_term=session.query(Measurement.date, func.max(Measurement.tobs), func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date>=start, Measurement.date<=end).all()
    session.close()
    end_list=list(np.ravel(search_term))
    return jsonify(end_list)

app.run()