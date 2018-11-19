import json
import logging
from dataclasses import dataclass

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest

from app.formulas import gen_data_from_pg, FORMULAS

logger = logging.getLogger(__name__)


class RequestDataException(HTTPBadRequest):
    """Exception class for RequestData"""


def get_bad_request_kwargs(error_text):
    return {
        'body': json.dumps({
            'error': error_text
        }),
        'content_type': 'application/json'
    }


@dataclass(frozen=True)
class RequestData:
    formula: str
    interval: int
    dt: int
    now: str

    def __post_init__(self):
        """Validate request data."""
        if not self.formula:
            raise RequestDataException(**get_bad_request_kwargs('Empty formula.'))
        if self.formula not in FORMULAS:
            raise RequestDataException(**get_bad_request_kwargs('invalid formula.'))
        if not self.interval:
            raise RequestDataException(**get_bad_request_kwargs('Empty interval.'))
        if not self.dt:
            raise RequestDataException(**get_bad_request_kwargs('Empty dt.'))
        if not self.now:
            raise RequestDataException(**get_bad_request_kwargs('Empty now.'))


class GenerateData(web.View):
    async def post(self) -> 'web.Response':
        """Generate data endpoint."""
        body = {'error': ''}
        try:
            data = await self.request.json()
            req_data = RequestData(**data)
            body['result'] = await gen_data_from_pg(self.request.app, req_data)
        except (TypeError, json.decoder.JSONDecodeError) as err:
            logger.info(err)
            raise HTTPBadRequest(**get_bad_request_kwargs("Bad request data"))
        else:
            logger.debug('Response: %s', body)
            return web.Response(body=json.dumps(body), content_type='application/json')
