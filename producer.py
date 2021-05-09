import os
import json
from datetime import datetime
import time

import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from loguru import logger
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

from util import get_kafka_client

#get environment variables
load_dotenv()


#url
api_key = os.environ.get('api_key')
url = f'http://api.openweathermap.org/data/2.5/box/city?bbox=3.200614,6.311608,5.804373,8.142567,8&appid={api_key}'

#get data from api
def get_weather_data():
    weather_data = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            weather_data['data'] = response_json
            weather_data['timestamp'] = str(datetime.utcnow())
            weather_message = json.dumps(weather_data)
            print(weather_message) 
            logger.info('Request successful')
            return weather_message
        else:
            logger.info('Request unsuccessful')      
    except Exception as err:
        logger.exception(f'Http error occured: {err}') 


#get topic
def get_topic():
    client = get_kafka_client()
    return client.topics[os.environ.get("topic")]
      
    
#get kafka producer
def get_producer():
    topic = get_topic()

    return topic.get_sync_producer()


#send data to kafka
def send_weather_data():       
    producer = get_producer()
    with producer as producer:
        while True:
            message = get_weather_data()
                        
            try:
                producer.produce(message.encode('ascii'))
                logger.info('Message produced to kafka')
            except (SocketDisconnectedError, LeaderNotAvailable) as err:
                producer = get_producer()
                producer.stop()
                producer.start()
                producer.produce(message.encode('ascii'))
                logger.exception(f'Error occured:{err}')
            except Exception as err:
                logger.exception(f'Error occured:{err}')
                
            time.sleep(1)

send_weather_data()
        

