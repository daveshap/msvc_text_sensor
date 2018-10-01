import json
import flask
import pika


app_port = 6001
app_uri = '/text'
app = flask.Flask(__name__)


def amqp_connect():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('MaragiRabbit', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return connection, channel


@app.route(app_uri, methods=['POST'])
def default():
    request = flask.request
    payload = json.loads(request.data)
    print(payload)
    if request.method == 'POST':
        con, chan = amqp_connect()
        chan.basic_publish(exchange='sensor_text_chat', body=payload, routing_key='')
        chan.close()
        con.close()
        return json.dump({'result': 'got it!'})


if __name__ == "__main__":
    app.run(port=app_port)
