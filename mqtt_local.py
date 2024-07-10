import json
import time
import paho.mqtt.client as mqtt # type: ignore
from flask import render_template, redirect
from logger import logger


mqtt_client = mqtt.Client()


def on_publish(client, userdata, message):
    logger.info(message.payload.decode())

from Todo import methods as t_methods
from Employee import methods as e_methods

mqtt_subscribers = {
    'store_msg':on_publish,
    'flask/mqtt/create/todo': t_methods.create_data,
    'flask/mqtt/update/todo': t_methods.update_data,
    'flask/mqtt/delete/todo': t_methods.delete_data,
    'flask/mqtt/create/employee': e_methods.create_data,
    'flask/mqtt/update/employee': e_methods.update_data,
    'flask/mqtt/delete/employee': e_methods.delete_data
}

def init_mqtt():
    mqtt_client.connect("127.0.0.1", 1883)
    mqtt_client.on_connect = on_connect
    mqtt_client.loop_start()


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        logger.info("Connected to broker")
        for topic,func in mqtt_subscribers.items():
            mqtt_client.subscribe(topic)
            # print("before sub")
            print(f"sub to  topic -> {topic}")
            # print("after sub")
            mqtt_client.message_callback_add(topic,func)
            # time.sleep(0.1)
    else:
        logger.error("Connection failed with code %d", rc)

