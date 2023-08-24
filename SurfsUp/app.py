# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Start by listing all the available routes on the homepage
@app.route("/")
def homepage():
    """List all available API routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Retrieve the last 12 months of data and convery to a dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session link
    session = Session(engine) 

    # Query the measurement
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Create a Dicitonary 
    prcp_data = []
    for date, prcp in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)


    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create the session 
    session = Session(engine)

    # Retrieve all the stations
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    #End the session 
    session.close()

    # Create dictionary
    stations_data = []
    for station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations_data.append(station_dict)

    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create the sesison
    session = Session(engine)

    # Query the dates and temperature observation for most active station
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    active_observed = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()

    #Close session
    session.close()

    # Create dictionary
    most_active = []
    for date, temp in active_observed:
        most_dict = {}
        most_dict["date"] = date
        most_dict["temp"] = temp
        most_active.append(most_dict)
 
    return jsonify(most_active)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create Session
    session = Session(engine)

    # Calculate the min, avg, and mac for dates greater than start date.
    query_calculations = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    start_date = []
    for min, avg, max in query_calculations:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Average Temperature"] = avg
        start_dict["Maximum Temperature"] = max
        start_date.append(start_dict)
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def ranged(start, end):
    # Creae Session 
    session = Session(engine)

    query_calculations = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    start_date = []
    for min, avg, max in query_calculations:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Average Temperature"] = avg
        start_dict["Maximum Temperature"] = max
        start_date.append(start_dict)
    return jsonify(start_date)



if __name__ == '__main__':
    app.run(debug=True)