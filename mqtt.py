#!/usr/bin/env python
"""
This script writes test data to an MQTT broker
"""

from __future__ import print_function

import datetime
import random
import threading
import time

import paho.mqtt.client as mqtt


def send_mqtt(client, mqtt_broker, log_path):
    with open(log_path, "a") as lf:
        while True:
            lf.write("Posting data to " + mqtt_broker + " at " + str(time.time()) + "\n")

            # Make up some data
            # Syntax is important for str.split() in receiver.
            temperatureReading = random.randint(0, 100)
            humidityReading = random.randint(0, 100)
            tempAndHumid = "Temperature: " + str(temperatureReading) + " Humidity: " + str(humidityReading)
            print("Sending data " + "Temperature: " + str(temperatureReading) + " Humidity: " + str(humidityReading))

            windspeed = random.randint(0, 100)
            rainfall = random.randint(0, 50)
            wind_and_rain = "Windspeed: " + str(windspeed) + " Rainfall: " + str(rainfall)
            wind = "Windspeed: " + str(windspeed) + " Timestamp: " + str(datetime.datetime.now())
            print("Sending data " + "Windspeed: " + str(windspeed) + " Rainfall: " + str(rainfall))

            # Example publish setting
            client.publish("datadump/tempAndHumid", tempAndHumid)
            client.publish("datadump/windandrain", wind_and_rain)
            client.publish("datadump/wind", wind)

            time.sleep(5)


if __name__ == '__main__':
    mqtt_broker = "localhost"
    client_name = "PtyDash Test Client"
    log_path = "log.txt"

    client = mqtt.Client(client_name)
    client.connect(mqtt_broker, port=1883, keepalive=60, bind_address="")

    t_mqtt = threading.Thread(
        target=send_mqtt,
        args=(client,
              mqtt_broker,
              log_path)
    )
    t_mqtt.start()

