"""
This module defines the pytest fixture to be utilized by all unit test cases.
pytest fixture allows us to mock differnt component of the application, 
which coudl be utlized at the time of testing different unit test cases without actually creating the resouce/ object.
"""

# importing built-in modules
import datetime
import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app, db
from app import api
from models import WeatherData, YieldData, WeatherStats
from models import weatherdataschema, yielddataschema, weatherstatsschema


@pytest.fixture(scope='module')
def client():

    app.config["TESTING_APP"] = True
    app.testing = True

    # Creates an in-memory sqlite db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    
    db.init_app(app)
    
    client = app.test_client()
    
    with app.app_context():
        db.create_all()
        
        # Create an dummy WeatherData type record and insert in DB
        weather_data = [WeatherData(station_id="id_1",
                                    date_=datetime.datetime.strptime('20000101', '%Y%m%d'),
                                    max_temp=100,
                                    min_temp=-100,
                                    amt_ppt=100),
                        WeatherData(station_id="id_2",
                                    date_=datetime.datetime.strptime('20000102', '%Y%m%d'),
                                    max_temp=100,
                                    min_temp=-100,
                                    amt_ppt=100),
                        WeatherData(station_id="id_3",
                                    date_=datetime.datetime.strptime('20000103', '%Y%m%d'),
                                    max_temp=100,
                                    min_temp=-100,
                                    amt_ppt=100),
                        WeatherData(station_id="id_4",
                                    date_=datetime.datetime.strptime('20000104', '%Y%m%d'),
                                    max_temp=100,
                                    min_temp=-100,
                                    amt_ppt=100),
                        WeatherData(station_id="id_5",
                                    date_=datetime.datetime.strptime('20000105', '%Y%m%d'),
                                    max_temp=100,
                                    min_temp=-100,
                                    amt_ppt=100)
                        ]
        

        # Create an dummy YieldData type record and insert in DB
        yield_data = [YieldData(year_=2000,
                                yield_=1000),
                      YieldData(year_=2001,
                                yield_=1000),
                      YieldData(year_=2002,
                                yield_=1000),
                      YieldData(year_=2003,
                                yield_=1000),
                      YieldData(year_=2004,
                                yield_=1000)
                      ]
        

        # Create an dummy WeatherStats type record and insert in DB
        weather_stats = [WeatherStats(station_id="id_1", 
                                      year_=2000, 
                                      avg_max_temp=100.0,
                                      avg_min_temp=-100.0, 
                                      total_amt_ppt=100)
                         ]

        db.session.add_all(weather_data)
        db.session.add_all(yield_data)
        db.session.add_all(weather_stats)        
        db.session.commit()
    
    yield client
