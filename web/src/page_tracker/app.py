import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

ERR_MESSAGE = "Sorry, something went wrong \N{thinking face}"
REDIS_PORT = 3679


app = Flask(__name__)


@app.get("/")
def index():
    try:
        page_views = redis(port=REDIS_PORT).incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return ERR_MESSAGE, 500
    else:
        return f"This page has been seen {page_views} times."


@cache
def redis(*, port=None):
    if port:
        try:
            port = int(port)
        except ValueError:
            print(f"You've specified an invalid port value: {port}")
            print("Please try again.")
            raise
    else:
        port = 6379
    return Redis.from_url(os.getenv("REDIS_URL", f"redis://localhost:{port}"))
