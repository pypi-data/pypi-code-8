import os

RETRIES_LIMIT = 3

# Configuration TTL in secs
CFG_CACHE_TTL = 5

# Configuration envar name that contains settings path
CFG_FILE_PATH_ENV = "SALES_EPICENTER_CFG"
CFG_FILE_PATH = "/etc/openweather/settings.yaml"
CFG_FILE_PATH_EXAMPLE = "{}/contrib/settings.yaml".format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Log format
LOGGING_FORMATTER = "%(asctime)s[%(levelname)s][%(target)s]%(message)s"

WEATHER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

WEATHER_INFORMATION_SCHEMA = {
    "main": {"temp": float,
             "temp_min": float,
             "temp_max": float
             },
    "dt": int
}


FORECAST_WEATHER_INFORMATION_SCHEMA = {
    "list": [{
                 "main": {"temp": float,
                          "temp_min": float,
                          "temp_max": float
                          },
                 "dt_txt": str
             }]
}



