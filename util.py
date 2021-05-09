import os

from pykafka import KafkaClient
from dotenv import load_dotenv



load_dotenv()

def get_kafka_client():
    #TODO - wrap the kafka client around try-catch
    #do proper logging of errors if there is error
    return KafkaClient(os.environ.get("hosts"))


