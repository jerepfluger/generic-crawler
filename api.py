from threading import Thread

from flask import Flask, request

from api import routes
from config.config import settings

app = Flask(__name__)
app.register_blueprint(routes)


class Api(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._config = settings
        self.name = settings.api.name
        self._port = settings.api.port

    def run(self):
        app.run(host='127.0.0.1', port=self._port)

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @staticmethod
    @app.route('/health-check')
    def index():
        return 'ok!'

    @staticmethod
    @app.route('/shutdown')
    def shutdown():
        Api.shutdown_server()
        return 'Server shutting down...'


if __name__ == '__main__':
    thread = Api()
    thread.run()
