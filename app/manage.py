import os
from aiohttp import web
import aiohttp_jinja2
import jinja2
from app.constant import APP_ROOT, UPLOAD_FOLDER, DATA_FOLDER
from app.common.utils import load_config, get_logger
from app.config import CONFIG


def create_app():
    app = web.Application(client_max_size=1024 * 1024 * 5)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(APP_ROOT + '/templates'))
    app['static_root_url'] = '/static'
    app.router.add_static(app['static_root_url'], 'app/static/')
    config_name = os.getenv('ENVIRONMENT', 'Development')

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)

    app.config = load_config(CONFIG[config_name])
    logger = get_logger()
    logger.info(f'Starting server for: [{app.config.ENVIRONMENT}]')
    return app, logger