import time
import datetime
import uuid
import json
import flask
import pika


app_port = 6001
app_uri = '/text'
app = flask.Flask(__name__)
output_exchange = 'model_speech'  # no need to interpret text with a model (yet)


def maragi_publish(message):
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('maragi-rabbit', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange=output_exchange, body=message, routing_key='')
    channel.close()
    connection.close()


@app.route(app_uri, methods=['POST'])
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
        maragi_publish(text)
        return json.dumps({'result': 'got it!'})


if __name__ == "__main__":
    app.run(port=app_port, host='0.0.0.0')
