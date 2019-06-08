from datetime import datetime
from dotenv import load_dotenv
import logging
import os
import psycopg2
import psycopg2.extras
import pytz
import requests
import json

load_dotenv(dotenv_path = '.env')

def fetchWeather():
    url = 'http://api.openweathermap.org/data/2.5/weather?units=metric&id=1566319&appid=' + os.getenv('API_KEY')
    fetched = requests.get(url).json()
    data = {
        'location': fetched['name'],
        'weather': {
            'description': fetched['weather'][0]['description'],
            'humidity': str(fetched['main']['humidity']) + '%',
            'icon': 'https://openweathermap.org/img/w/' + fetched['weather'][0]['icon'] + '.png',
            'pressure': str(fetched['main']['pressure']) + 'hpa',
            'sunrise': toLocaleTime(fetched['sys']['sunrise']),
            'sunset': toLocaleTime(fetched['sys']['sunset']),
            'temp': str(fetched['main']['temp']) + '°C',
            'wind_speed': str(fetched['wind']['speed']) + 'm/s',
        },
        'get_time': toLocaleTime(fetched['dt'])
    }

    try:
        con = psycopg2.connect(database = os.getenv('DB_NAME'), user = os.getenv('DB_USER'), password = os.getenv('DB_PWD'))
    except:
        logging.exception('Unable to connect to db')
        return
    else:
        cursor = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute("""INSERT INTO station_weather (location, weather, get_time) VALUES (%s, %s, %s)""",
                        (data['location'], json.dumps(data['weather']), data['get_time'])
        )
        con.commit()
        cursor.close()

# @return str 'HH:mm:ss'
def toLocaleTime(time):
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return datetime.fromtimestamp(time, tz).strftime('%X')

fetchWeather()