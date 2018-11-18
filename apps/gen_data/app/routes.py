import logging
from typing import TYPE_CHECKING

from app.views import GenerateData

if TYPE_CHECKING:
    from aiohttp import web

logger = logging.getLogger(__name__)


def setup_routes(app: 'web.Application'):
    """App routes."""
    logger.debug('Setup routes.')
    app.router.add_route(method='POST', path='/get_data/',
                         handler=GenerateData)
