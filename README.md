# Real-time Weather Data Ingestion

Real time weather data Ingestion from [OpenWeather API](https://openweathermap.org/api). Sign up to get an api key.


### Broker Setup Using Docker

  * Prerequisite
    - Install Docker
    - Install Docker-compose

  * Run Kakfa and Zookeeper Container. You can check a docker-compose template [here](https://github.com/conduktor/kafka-stack-docker-compose)
  * Create a kafka topic for the weather data
    - Use `docker ps` to get the name of the Kafka container
    - Use the command `docker exec -it <container name> /bin/bash` to get a bash shell in the container
  
    
  ``` 
  # Run this command to create a topic
  Kafka-topics --zookeeper <zookeeper-container-name:port> --topic <topic name> --create --partitions <number> --replication-factor <number> 
  ```
  
### Update the .env file 
  ```
  host=<hostaddress:port>
  topic=<topic-name>
  api_key=<openweather-api-key>
  ```
  
### Install Dependencies
  ```
  pip install -r requirements.txt
  ```
  
### Start Producer
  ```
  python producer.py
  ```
