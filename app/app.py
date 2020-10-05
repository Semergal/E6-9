import os
from flask import Flask
from pymemcache.client.base import Client

app = Flask(__name__)
host = '0.0.0.0'
port = int(os.environ.get("PORT", 8081))

cache_server_host = 'cache'
cache_server_port = int(os.environ.get("PORT_CS", 11211))


class Cache():
    def __init__(self, hostname=cache_server_host, port=cache_server_port):
        self.server = Client((hostname, port))

    def set(self, key, value, expiry=0):
        self.server.set(str(key), value, expiry)

    def get(self, key):
        if self.server.get(str(key)):
            value = self.server.get(str(key)).decode("utf-8")
            return int(value)

    def delete(self, key):
        self.server.delete(str(key))


cache = Cache()


def fibonacci(n):
    value = cache.get(n)
    if value:
        return value
    elif n < 2:
        return n
    else:
        f = fibonacci(n - 1) + fibonacci(n - 2)
        cache.set(n, f)
        return f


@app.route("/<int:param_fi>/")
def get_fibo(param_fi):
    return str(fibonacci(param_fi))


@app.route("/cache/<int:param_fi>/")
def get_cache(param_fi):
    return str(cache.get(param_fi))


@app.route('/')
def index():
    return 'Введите число после 8081/ для расчета числа фибоначи, а так же сервис сохраняет число в кеше 8081/cache/' 


if __name__ == '__main__':
    app.run(debug=False, host=host, port=port)
