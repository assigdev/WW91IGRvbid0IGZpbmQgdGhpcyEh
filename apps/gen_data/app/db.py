from typing import TYPE_CHECKING

import aiopg

if TYPE_CHECKING:
    from aiohttp import web


async def init_pg(app: 'web.Application'):
    """PostgreDB pool init with safe close."""
    pg_cfg = app['config'].pg_cfg
    app['pg_pool'] = await aiopg.create_pool(pg_cfg.dsn)
    yield
    app['pg_pool'].close()
