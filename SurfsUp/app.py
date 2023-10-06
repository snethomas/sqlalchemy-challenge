# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
    """Welcome to Honolulu's Climate API!"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_yr=session.query(measurement.date,measurement.prcp).filter(measurement.date>='2016-08-23').all()
    session.close()
    prcp_yr_list = [{p[0]: p[1]} for p in prcp_yr]
    return jsonify(prcp_yr_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations=session.query(station.station,station.name,station.latitude,station.longitude,station.elevation).all()
    session.close()
    stations_list = [{"station": s[0], "name": s[1],"latitude": s[2], "longitude": s[3], "elevation": s[4]} for s in stations]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_temp=session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281')\
        .filter(measurement.date>='2016-08-18').all()
    session.close()
    most_active_temp_list = [{t[0]:t[1]} for t in most_active_temp]
    return jsonify(most_active_temp_list)

@app.route("/api/v1.0/<start>")
def start(start_date):
    session = Session(engine)
    temp_range=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
    .filter(measurement.date>=start_date).all()
    session.close()
    temp_range_list = [{"TMIN": t[0],"TMAX": t[1],"TAVG": t[2]} for t in temp_range]
    return jsonify(temp_range_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date,end_date):
    session = Session(engine)
    temp_range=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
    .filter(measurement.date>=start_date,measurement.date<=end_date ).all()
    session.close()
    temp_range_list = [{"TMIN": t[0],"TMAX": t[1],"TAVG": t[2]} for t in temp_range]
    return jsonify(temp_range_list)

if __name__ == '__main__':
    app.run(debug=True)
