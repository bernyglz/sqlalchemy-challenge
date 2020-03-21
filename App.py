# imports
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify 

# database set up
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Use FLASK to create your routes
app = Flask(__name__)

# ### Routes
# Home page.
#  List all routes that are available.
@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# `/api/v1.0/precipitation`
#
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session
    session = Session(engine)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >="2016-08-23").\
        order_by(Measurement.date).all()
    session.close()

    precip_dict = {date: prcp for date, prcp in precipitation}
    return jsonify(precip_dict)

# `/api/v1.0/stations`
@app.route("/api/v1.0/stations")
def stations():
    # create session
    session = Session(engine)

    stations = session.query(Station.station).all()
    session.close()
    
    return jsonify(stations)


# `/api/v1.0/tobs`

@app.route("/api/v1.0/tobs")
def tobs():
    # create session
    session = Session(engine)
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    station_temps = session.query(Station.station, Measurement.tobs).\
        filter(Measurement.date >= previous_year).\
        filter(Measurement.station == Station.station).all()

    session.close() 
    return jsonify(most_active_station_temps)


# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)

    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
    
    session.close()    
    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def startend(start_date, end_date):
    session = Session(engine)
    
    startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()

    session.close()
    return jsonify(startend)


if __name__ == "__main__":
    app.run()

    

