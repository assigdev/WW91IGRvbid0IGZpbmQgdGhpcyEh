import logging

from aiohttp import web

from app.db import init_pg
from app.routes import setup_routes
from app.settings import load_config

try:
    import uvloop
except ImportError:
    logging.warning('Uvloop is not installed. Default event loop will be used.')
else:
    import asyncio

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def create_app(debug: bool = False) -> web.Application:
    """Init application"""
    app = web.Application(debug=debug)

    load_config(app)
    setup_routes(app)

    app.cleanup_ctx.append(init_pg)
    return app


def main():
    """Entrypoint."""
    app = create_app()
    return web.run_app(app, port=app['config'].port)


if __name__ == '__main__':
    main()
