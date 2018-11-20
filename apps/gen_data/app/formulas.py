from typing import TYPE_CHECKING
from datetime import datetime, timedelta
if TYPE_CHECKING:
    from aiohttp import web
    from app.views import RequestData

FORMULAS = ('t', 's')


class Formula:
    def __init__(self, req_data):
        self.req_data = req_data
        self.formulas_query = {
            't': self._get_t_formula_sql,
            's': self._get_s_formula_sql
        }
        self.timestamps = None

    def get_timestamps(self):
        if self.timestamps is None:
            now = datetime.strptime(self.req_data.now, '%d.%m.%y %H:%M:%S.%f')
            time = now - timedelta(days=self.req_data.interval)
            timestamps = []
            while time <= now:
                timestamps.append(time.timestamp())
                time = time + timedelta(hours=self.req_data.dt)
            self.timestamps = timestamps
        return self.timestamps

    def _get_t_formula_sql(self):
        t_list_query = [f'{t} + 2.0/{t}' for t in self.get_timestamps()]
        return 'SELECT ' + ', '.join(t_list_query)

    def _get_s_formula_sql(self):
        t_list_query = [f'sin({t})' for t in self.get_timestamps()]
        return 'SELECT ' + ', '.join(t_list_query)

    def get_query(self):
        return self.formulas_query[self.req_data.formula]()


async def gen_data_from_pg(app: 'web.Application', req_data: 'RequestData'):
    formula = Formula(req_data)
    query = formula.get_query()
    async with app['pg_pool'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            data = await cur.fetchone()
            return {
                'categories': formula.get_timestamps(),
                'data': [float(item) for item in data]
            }
