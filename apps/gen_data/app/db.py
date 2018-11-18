from typing import TYPE_CHECKING

import aiopg

if TYPE_CHECKING:
    from aiohttp import web
    from app.views import RequestData

# Fixme
FORMULAS_QUERY = {
    't': 'SELECT 1',
    's': 'SELECT 2',
}


async def init_pg(app: 'web.Application'):
    """PostgreDB pool init with safe close."""
    pg_cfg = app['config'].pg_cfg
    app['pg_pool'] = await aiopg.create_pool(pg_cfg.dsn)
    yield
    app['pg_pool'].close()


async def gen_data_from_pg(app: 'web.Application', req_data: 'RequestData'):
    async with app['pg_pool'].acquire() as conn:
        async with conn.cursor() as cur:
            query = FORMULAS_QUERY[req_data.formula]
            await cur.execute(query)
            # Fixme
            ret = []
            async for row in cur:
                ret.append(row)
            return ret
