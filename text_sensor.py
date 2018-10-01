"""
SUMMARY:
    allows maragi to receive chat messages

INPUT:
    text message via REST API (flask)

OUTPUT:
    standard sensor message

OUTPUT EXAMPLE:
    {data: <sentence>,
    uuid: <uuid>,
    time: <unix>,
    date: <datetime>,
    sensor_name: text_chat,
    sensor_type: API,
    sensor_data: string}
"""

import time
import datetime
import uuid
import json
import flask
import pika


app_port = 6001
app = flask.Flask(__name__)


def amqp_connect():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('MaragiRabbit', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return connection, channel


def publish_amqp(message):
    con, chan = amqp_connect()
    chan.basic_publish(exchange='sensor_text_api', body=message, routing_key='')
    chan.close()
    con.close()


@app.route('/text', methods=['POST'])
def default():
    request = flask.request
    payload = json.loads(request.data)
    print(payload)
    if request.method == 'POST':
        message = {'data': payload['message'],
                   'time': str(time.time()),
                   'uuid': str(uuid.uuid4()),
                   'datetime': str(datetime.datetime.now()),
                   'sensor_name': 'text_sensor',
                   'sensor_type': 'API',
                   'sensor_data': 'string'}
        text = json.dumps(message)
        publish_amqp(text)
        return text


if __name__ == "__main__":
    app.run(port=app_port)
