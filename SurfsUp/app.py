# Import the dependencies.
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>\<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    #session = Session(engine)

    # Query results form precipitation analysis

    # Calculate the most recent date and the date one year from the most recent date in data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()

    session.close()

    # Create a dictionary using date as the key and prcp as the value.
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset.
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations  = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the most recent date and the date one year from the most recent date in data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    most_active_station = 'USC00519281'

    # Query the dates and temperature observations for the previous year of data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station, Measurement.date >= last_year).\
        order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    most_active_tobs = list(np.ravel(results))

    return jsonify(most_active_tobs)


@app.route("/api/v1.0/<start>")
def single_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create start date format
    try:
        start_date = dt.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Incorrect date format. Please use YYYY-MM-DD."}), 400

     # Get the oldest and most recent dates in datetime format for setting date range later.
    oldest_date = session.query(func.min(Measurement.date)).scalar()
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    session.close()

    if isinstance(oldest_date, str):
        oldest_date = dt.strptime(oldest_date, '%Y-%m-%d')
    if isinstance(most_recent_date, str):
        most_recent_date = dt.strptime(most_recent_date, '%Y-%m-%d')

    # Check if any results are found and return error message or dictionary of results.
    if start_date < oldest_date or start_date > most_recent_date:
        return jsonify({"error": "No data found for the specified date range."}), 404

    session = Session(engine)

    # Query  the minimum temperature, the average temperature, 
    # and the maximum temperature for the specified start date.
    results = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    session.close()

    # Convert the result into a dictionary
    single_start_dict = {
        "Start Date": start,
        "TMIN": results[0][0],
        "TMAX": results[0][1],
        "TAVG": results[0][2]
    }

    return jsonify(single_start_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Create start date and end date format with error message for incorrect format.
    try:
        start_date = dt.strptime(start, '%Y-%m-%d')
        end_date = dt.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Date format must be YYYY-MM-DD/YYYY-MM-DD."}), 400

    # Get the oldest and most recent dates in datetime format for setting date range later
    oldest_date = session.query(func.min(Measurement.date)).scalar()
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    session.close()

    if isinstance(oldest_date, str):
        oldest_date = dt.strptime(oldest_date, '%Y-%m-%d')
    if isinstance(most_recent_date, str):
        most_recent_date = dt.strptime(most_recent_date, '%Y-%m-%d')

    # Check if any results are found and return error message or dictionary of results.
    if start_date < oldest_date or end_date > most_recent_date:
        return jsonify({"error": "No data found for the specified date range."}), 404
    if start_date > end_date:
        return jsonify({"error": "Start date must be before or equal to end date."}), 400

    session = Session(engine)

    # Query  the minimum temperature, the average temperature, 
    # and the maximum temperature for the specified start date.
    results = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    if results[0][0] is None:
        return jsonify({"error": "No data found for the specified date range."}), 404

    start_and_end_dict = {
        "Start Date": start,
        "End Date": end,
        "Temperature MIN": results[0][0],
        "Temperature MAX": results[0][1],
        "Temperature AVG": results[0][2]
    }

    return jsonify(start_and_end_dict)

if __name__ == '__main__':
    app.run(debug=True)