"""
This module contains the required data models to support the application.
"""

# Import the modules
from config import db, ma

# Data Model for Weather Data
class WeatherData(db.Model):
    """
    This class represent the weather_data table in DB to store the weather data.
    """
    __tablename__ = 'weather_data' # TableName

    station_id = db.Column(db.String, primary_key=True)
    date_ = db.Column(db.DateTime, primary_key=True)
    max_temp = db.Column(db.Integer, nullable=True)
    min_temp = db.Column(db.Integer, nullable=True)
    amt_ppt = db.Column(db.Integer, nullable=True)


class WeatherDataSchema(ma.Schema):
    """
    This class defines how the attributes of WeatherData class will be converted into JSON-friendly formats.
    """
    class Meta:
        model = WeatherData
        load_instance = True
        fields = ("station_id", "date_", "max_temp", "min_temp", "amt_ppt")


# Data Model for Yield Data
class YieldData(db.Model):
    """
    This class represent the yield_data table in DB to store the yield data.
    """
    __tablename__ = 'yield_data' # TableName
    
    year_ = db.Column(db.Integer, primary_key=True)
    yield_ = db.Column(db.Integer)

class YieldDataSchema(ma.Schema):
    """
    This class defines how the attributes of YieldData class will be converted into JSON-friendly formats.
    """
    class Meta:
        model = YieldData
        load_instance = True
        fields = ("year_", "yield_")


# Data Model for Weather Stats Data
class WeatherStats(db.Model):
    """
    This class represent the weather_stats table in DB to store the weather stats data.
    """
    __tablename__ = 'weather_stats' # TableName
    
    station_id = db.Column(db.String, primary_key=True)
    year_ = db.Column(db.Integer, primary_key=True)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_amt_ppt = db.Column(db.Integer, nullable=True)


class WeatherStatsSchema(ma.Schema):
    """
    This class defines how the attributes of WeatherStats class will be converted into JSON-friendly formats.
    """
    class Meta:
        model = WeatherStats
        load_instance = True
        fields = ("station_id", "year_", "avg_max_temp", "avg_min_temp", "total_amt_ppt")


weatherdataschema = WeatherDataSchema(many=True)
yielddataschema = YieldDataSchema(many=True)
weatherstatsschema = WeatherStatsSchema(many=True)
