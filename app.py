
from tkinter import N
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json
import numpy as np
import datetime as dt

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Homepage():
    print("Server received request for homepage")
    return """Homepage<br/> 
            /api/v1.0/precipitation<br/>
            /api/v1.0/stations<br/>
            /api/v1.0/tobs<br/>
            /api/v1.0/<start><br/>
            /api/v1.0/<start>/<end>"""


@app.route("/api/v1.0/precipitation")
def Precipitation():
    print("Server received request for precipitation data")
    measurement_precipitation = session.query(Measurement.date, Measurement.prcp). \
    filter(Measurement.date >= '2016-08-23').order_by(Measurement.date.asc()).all()
    measurement_precipitation_dict = dict(measurement_precipitation)

    return json.dumps(measurement_precipitation_dict, indent = 4)

    
@app.route("/api/v1.0/stations")
def Stations():
    print("Server received request for station data")
    stations = session.query(Station.station).all()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def Tobs():
    print("Server received request for temperature observation data")
    last_year_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23', \
                                Measurement.station=='USC00519281').all()
    last_year_data_list = list(np.ravel(last_year_data))
    return jsonify(last_year_data_list)


@app.route("/api/v1.0/start")
def Start():
    print("Server received request for the starting range data")
    lowest_temp_start = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').all()
    average_temp_start = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').all()
    highest_temp_start = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').all()
    return jsonify(lowest_temp_start, average_temp_start, highest_temp_start)



@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # start = dt.datetime.strptime(start, "%m/%d/%Y")
        # # calculate TMIN, TAVG, TMAX for dates greater than start
        # results = session.query(*sel).\
        #     filter(Measurement.date >= start).all()
        # # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)

        start = dt.datetime.strptime("8232016", "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime("8232016", "%m%d%Y")
    end = dt.datetime.strptime("8172017", "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__ == "__main__":
    app.run(debug=True)