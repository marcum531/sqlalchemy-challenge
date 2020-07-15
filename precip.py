import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to my Precipitation API home page"
        f"Available Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-22").\
    filter(Measurement.date <= "2017-08-23").\
    order_by(Measurement.date)
    
    precip_data = []
    for r in results:
        precip_dict = {}
        precip_dict['date'] = r.date
        precip_dict['prcp'] = r.prcp
        precip_data.append(precip_dict)
    
    return jsonify(precip_data)

    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.name).all()
    
    session.close()
    
    station_names = list(np.ravel(results[1:9]))
    
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    
    results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    most_active = []
    for r in results:
        active_dict = {}
        active_dict = r.
        most_active.append(active_dict)
    
    temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active).\
    filter(Measurement.date >= "2016-08-22").\
    filter(Measurement.date <= "2017-08-23").\
    order_by(Measurement.date).all()
    
    session.close()
    
    most_active_temps = []
    for t in temps:
        most_active_temps_dict = {}
        most_active_temps_dict['date'] = t.date
        most_active_temps_dict['tobs'] = t.tobs
        most_active_temps.append(most_active_temps_dict)
    
    return jsonify(most_active_temps)
   

    

if __name__ == '__main__':
    app.run(debug=True)
