def test_weather_api(client):
    """
    This function test the /api/weather api
    """
    weather_data = client.get("/api/weather")
    
    expected_data = [{"station_id": "id_1", "date_": "2000-01-01T00:00:00", "max_temp": 100, "min_temp": -100, "amt_ppt": 100},
                     {"station_id": "id_2", "date_": "2000-01-02T00:00:00", "max_temp": 100, "min_temp": -100, "amt_ppt": 100},
                     {"station_id": "id_3", "date_": "2000-01-03T00:00:00", "max_temp": 100, "min_temp": -100, "amt_ppt": 100},
                     {"station_id": "id_4", "date_": "2000-01-04T00:00:00", "max_temp": 100, "min_temp": -100, "amt_ppt": 100},
                     {"station_id": "id_5", "date_": "2000-01-05T00:00:00", "max_temp": 100, "min_temp": -100, "amt_ppt": 100}
                    ]

    assert len(expected_data) == len(weather_data.json)
    
    for i in expected_data:
        if i in weather_data.json:
            assert True
        else:
            assert False

def test_yield_api(client):
    """
    This function test the /api/yield api
    """
    yield_data = client.get("/api/yield?year=1985")
    
    expected_data = [{"year_": 2000, "yield_": 1000},
                     {"year_": 2001, "yield_": 1000},
                     {"year_": 2002, "yield_": 1000},
                     {"year_": 2003, "yield_": 1000},
                     {"year_": 2004, "yield_": 1000}
                    ]

    assert len(expected_data) == len(yield_data.json)
    
    for i in expected_data:
        if i in yield_data.json:
            assert True
        else:
            assert False


def test_weather_stats_api(client):
    """
    This function test the /api/weather/stats api
    """
    weather_stats = client.get("/api/weather/stats")
    
    expected_data = [{"station_id": "id_1", "year_": 2000, "avg_max_temp": 100.0, "avg_min_temp": -100.0, "total_amt_ppt": 100}]

    assert len(expected_data) == len(weather_stats.json)
    
    for i in expected_data:
        if i in weather_stats.json:
            assert True
        else:
            assert False
