# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect,text

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station= Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

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
        f"Honolulu, Hawaii climate app:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# API Static Routes 

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    session=Session(engine)
    # Design a query to retrieve the last 12 months of precipitation data 
    # Starting from the most recent data point in the database. 
    recent_date= session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # for recent in session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1):
    #     print(recent)
    # recent_date=recent[0]
    # recent_date
    
   # Calculate the date one year from the last date in data set.
    last_yr_date = dt.datetime.strptime(recent_date,"%Y-%m-%d")- dt.timedelta(days=365)
    query_date = last_yr_date.strftime("%Y-%m-%d")

    # Perform a query to retrieve the data and precipitation scores

    prcp_data = session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date >= query_date).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of precipitation
    precipitation = []
    for date, prcp in prcp_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    session=Session(engine)
    
    # Query all station data
    station_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of stations
    station_list = []
    for station, name, latitude, longitude, elevation in station_data:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        
        station_list.append(station_dict)
#     station_list = list(np.ravel(station_data))

    return jsonify(station_list)


# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations of the most active stations"""
    session=Session(engine)
    
 
    # Find the most recent date in the data set.
    recent_date= session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
   
    
      # Calculate the date one year from the last date in data set.
    last_yr_date = dt.datetime.strptime(recent_date,"%Y-%m-%d")- dt.timedelta(days=365)
    query_date = last_yr_date.strftime("%Y-%m-%d")
   
    # Active station - station id that has the greatest number of observations
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
                  group_by(Measurement.station).\
                  order_by(func.count(Measurement.station).desc()).all()
    
    top_station_id=active_stations[0].station

    
     # Query the dates and temperature observations of the most-active station for the previous year of data.
    station_date_temp = session.query(Measurement.tobs).\
                        filter(Measurement.station == top_station_id).\
                        filter(Measurement.date > query_date).all()

    
    session.close()
    
    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(station_date_temp))

    return jsonify(tobs_data)


# API Dynamic Route 

# start route
@app.route("/api/v1.0/<start>")
def startd(start):
    """Returns the min, max, and average temperatures"""
    session=Session(engine)
    
    start_date = dt.datetime.strptime(start,"%Y-%m-%d")
    temp = session.query(func.min(Measurement.tobs),
                         func.max(Measurement.tobs), 
                         func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
    session.close()
    result=list(np.ravel(temp))
    return jsonify(result)

        
# start/end route 
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Returns the min, max, and average temperatures from the given start date to the given end date """
    session=Session(engine)
    
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date = dt.datetime.strptime(end,"%Y-%m-%d")
    
    temp = session.query(func.min(Measurement.tobs),
                         func.max(Measurement.tobs), 
                         func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).all()
    session.close()
    result=list(np.ravel(temp))
    return jsonify(result)



        
if __name__ == '__main__':
    app.run()


