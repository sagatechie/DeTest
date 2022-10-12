"""
This module contains the required data models to support the application.
"""
# Import the modules
import datetime
import fileinput as fi
from glob import glob
from sqlalchemy import func

from config import db
from models import WeatherData, YieldData, WeatherStats
from models import weatherdataschema, yielddataschema, weatherstatsschema


# Data Paths
# Path of the weather data from where to load and ingest into DB
WEATHER_DATA_PATH = r"data\wx_data\*"

# Path of the yield data from where to load and ingest into DB
YIELD_DATA_PATH = r"data\yld_data\*"

# Batch Size to issue commit to DB
COMMIT_BATCH_SIZE = 100000

def ingest_weather_data():
    """
    This function load the data from WEATHER_DATA_PATH and insert only record in weather_data table which are already not ingested
    PS: For checking whether record exist in table or not, only station id is compared.
    """

    print('----------------------------------------')
    print('Weather Data Ingestion Started at: {}'.format(str(datetime.datetime.now())))

    # find out the existing station_id for which data is already present in table
    existing_station_id = weatherdataschema.dump(WeatherData.query.with_entities(WeatherData.station_id).all())

    print('Existing Weather Data Records: {}'.format(len(existing_station_id)))

    existing_station_id = {item['station_id'] for item in existing_station_id}
    
    
    # initialize a list to ingest the records in table    
    records_to_ingest = []

    # iterate over each file in WEATHER_DATA_PATH
    with fi.input(files=glob(WEATHER_DATA_PATH)) as fo:
        for date_line in fo:
            fields_ = [field.strip('\n').strip() for field in date_line.split('\t')]
            station_id = fo.filename().split('\\')[-1].strip('.txt')

            if station_id not in existing_station_id:
                records_to_ingest\
                    .append(WeatherData(station_id=station_id,
                                        date_=datetime.datetime.strptime(fields_[0], '%Y%m%d'),
                                        max_temp=int(fields_[1]) if fields_[1] != '-9999' else None,
                                        min_temp=int(fields_[2]) if fields_[2] != '-9999' else None,
                                        amt_ppt=int(fields_[3]) if fields_[3] != '-9999' else None))
    
    for index in range(0, len(records_to_ingest), COMMIT_BATCH_SIZE):
        db.session.add_all(records_to_ingest[index: index + COMMIT_BATCH_SIZE])
        db.session.commit()
        print('{}/{} records ingested for Weather Data'.format(index + COMMIT_BATCH_SIZE, len(records_to_ingest)))

    print('{} records ingested in Weather Data table'.format(len(records_to_ingest)))
    print('Weather Data Ingestion Completed at: {}'.format(str(datetime.datetime.now())))


def ingest_yield_data():
    """
    This function load the data from YIELD_DATA_PATH and insert only record in yield_data table which are already not ingested
    """

    print('----------------------------------------')
    print('Yield Data Ingestion Started at: {}'.format(str(datetime.datetime.now())))

    # find out the existing yield data for which data is already present in table
    existing_yield_records = yielddataschema.dump(YieldData.query.all())

    print('Existing Yield Data Records: {}'.format(len(existing_yield_records)))
    
    # initialize a list to ingest the records in table    
    records_to_ingest = []

    # iterate over each file in YIELD_DATA_PATH
    with fi.input(files=glob(YIELD_DATA_PATH)) as fo:
        for date_line in fo:

            fields_ = [field.strip('\n').strip() for field in date_line.split('\t')]
            
            temp_yield_data = {}
            temp_yield_data['year_'] = int(fields_[0])
            temp_yield_data['yield_'] = int(fields_[1])

            if temp_yield_data not in existing_yield_records:
                records_to_ingest\
                    .append(YieldData(year_=temp_yield_data['year_'],
                                      yield_=temp_yield_data['yield_']))


    
    for index in range(0, len(records_to_ingest), COMMIT_BATCH_SIZE):
        db.session.add_all(records_to_ingest[index: index + COMMIT_BATCH_SIZE])
        db.session.commit()
        print('{}/{} records ingested for Weather Data'.format(index + COMMIT_BATCH_SIZE, len(records_to_ingest)))

    print('{} records ingested in Yield Data table'.format(len(records_to_ingest)))
    print('Yield Data Ingestion Completed at: {}'.format(str(datetime.datetime.now())))


def ingest_weather_stats_data():
    """
    This function load the data from Weather table, computes the stats and ingest in weather_stats table
    """

    print('----------------------------------------')
    print('Weather Stats Data Ingestion Started at: {}'.format(str(datetime.datetime.now())))

    # Delete the existing stats from table
    WeatherStats.query.delete()

    new_weather_stats = \
        db.session \
            .query(WeatherData.station_id.label('station_id'),
                   func.strftime('%Y', WeatherData.date_).label('year_'),
                   func.avg(WeatherData.max_temp).label('avg_max_temp'),
                   func.avg(WeatherData.min_temp).label('avg_min_temp'),
                   func.sum(WeatherData.amt_ppt).label('total_amt_ppt')) \
            .group_by(WeatherData.station_id, func.strftime('%Y', WeatherData.date_))

    records_to_ingest = [WeatherStats(station_id=stat['station_id'], 
                                      year_=stat['year_'], 
                                      avg_max_temp=stat['avg_max_temp'],
                                      avg_min_temp=stat['avg_min_temp'], 
                                      total_amt_ppt=stat['total_amt_ppt']) for stat in weatherstatsschema.dump(new_weather_stats)]


    for index in range(0, len(records_to_ingest), COMMIT_BATCH_SIZE):
        db.session.add_all(records_to_ingest[index: index + COMMIT_BATCH_SIZE])
        db.session.commit()
        print('{}/{} records ingested for Weather Data'.format(index + COMMIT_BATCH_SIZE, len(records_to_ingest)))

    print('{} records ingested in Weather Stats Data table'.format(len(records_to_ingest)))
    print('Weather Stats Data Ingestion Completed at: {}'.format(str(datetime.datetime.now())))


def main():
    
    db.create_all()
    
    # call func ingest_weather_data to ingest the weather data
    ingest_weather_data()

    # call func ingest_yield_data to ingest the weather data
    ingest_yield_data()

    # call func ingest_weather_stats_data to ingest the weather data
    ingest_weather_stats_data()


if __name__ == '__main__':
    main()