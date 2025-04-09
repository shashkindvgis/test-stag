from flask import Flask, jsonify
import redis
import time

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

def count():
    retries = 5
    while True:
        try:
            return cache.incr('visits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})



@app.route("/count")
def list_count():
	visits = count()
	return jsonify({"count": visits})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
