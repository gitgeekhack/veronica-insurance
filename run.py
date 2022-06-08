from app import app
from aiohttp import web

if __name__ == "__main__":
    web.run_app(app, port=8081, host='127.0.0.1')
