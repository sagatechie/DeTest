"""
This the main module for this application. This is used to create/ register the REST APIS which are required to support this application.
"""

# Import the buult-in modules
import datetime

from flask import Flask, request
from flask_restful import Api, Resource

from config import app, db, ma
from models import WeatherData, YieldData, WeatherStats
from models import weatherdataschema, yielddataschema, weatherstatsschema

api = Api(app)

PER_PAGE_RESULT = 5

# REST APIs to fetch the Data from DB
class WeatherAPI(Resource):
    """
    This Class represent the Flask resource corresponding to GET /api/weather API.
    Retrieves the data from the weather_data table, filter based on query parameters and return the json formatted response.
    """
    def get(self):

        station_id = str(request.args['station_id']) if 'station_id' in request.args else None
        date_ = str(request.args['date_']) if 'date_' in request.args else None
        page = int(request.args['page']) if 'page' in request.args else 1

        if station_id is None and date_ is None:
            weather_data = WeatherData.query.paginate(page, PER_PAGE_RESULT, error_out=False)

        elif station_id is None:
            weather_data = WeatherData.query.filter(WeatherData.date_ == datetime.datetime.strptime(date_, '%Y%m%d')).\
                paginate(page, PER_PAGE_RESULT, error_out=False)

        elif date_ is None:
            weather_data = WeatherData.query.filter(WeatherData.station_id == station_id).paginate(page, PER_PAGE_RESULT, error_out=False)

        else:
            weather_data = WeatherData.query.\
                filter(db.and_(WeatherData.station_id == station_id,
                               WeatherData.date_ == datetime.datetime.strptime(date_, '%Y%m%d')))\
                .paginate(page, PER_PAGE_RESULT, error_out=False)

        return weatherdataschema.dump(weather_data.items)


class YieldAPI(Resource):
    """
    This Class represent the Flask resource corresponding to GET /api/yield API.
    Retrieves the data from the yield_data table, filter based on query parameters and return the json formatted response.
    """
    def get(self):

        year_ = int(request.args['year_']) if 'year_' in request.args else None
        page = int(request.args['page']) if 'page' in request.args else 1

        if year_ is None:
            yield_data = YieldData.query.paginate(page, PER_PAGE_RESULT, error_out=False)
        else:
            yield_data = YieldData.query.filter(YieldData.year_ == year_).paginate(page, PER_PAGE_RESULT, error_out=False)

        return yielddataschema.dump(yield_data.items)


class WeatherStatsAPI(Resource):
    """
    This Class represent the Flask resource corresponding to GET /api/weather/stats API.
    Retrieves the data from the weather_stats table, filter based on query parameters and return the json formatted response.
    """
    def get(self):

        station_id = str(request.args['station_id']) if 'station_id' in request.args else None
        year_ = int(request.args['year_']) if 'year_' in request.args else None
        page = int(request.args['page']) if 'page' in request.args else 1

        if station_id is None and year_ is None:
            weather_stats = WeatherStats.query.paginate(page, PER_PAGE_RESULT, error_out=False)

        elif station_id is None:
            weather_stats = WeatherStats.query.filter(WeatherStats.year_ == year_).paginate(page, PER_PAGE_RESULT, error_out=False)

        elif year_ is None:
            weather_stats = WeatherStats.query.filter(WeatherStats.station_id == station_id).paginate(page, PER_PAGE_RESULT, error_out=False)

        else:
            weather_stats = WeatherStats.query.filter(
                db.and_(WeatherStats.station_id == station_id, WeatherStats.year_ == year_)).paginate(page, PER_PAGE_RESULT, error_out=False)

        return weatherstatsschema.dump(weather_stats.items)


# GET API to get a JSON-formatted response the ingested Weather data in database.
# Supports query parameters (station_id, date, page) with pagination enabled
api.add_resource(WeatherAPI, '/api/weather')

# GET API to get a JSON-formatted response the ingested Yield data in database.
# Supports query parameters (year_, page) with pagination enabled
api.add_resource(YieldAPI, '/api/yield')

# GET API to get a JSON-formatted response the ingested Weather Stats data in database.
# Supports query parameters (station_id, year_, page) with pagination enabled
api.add_resource(WeatherStatsAPI, '/api/weather/stats')

if __name__ == '__main__':
    # starts the flask app
    app.run(debug=True)
