import logging
import os
from typing import TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from aiohttp import web


@dataclass
class PostgreConfig:
    """Postgre config section."""
    dsn: str = field(init=False)

    def __init__(self, user: str, password: str, host: str, dbname: str):
        self.dsn = f'dbname={dbname} user={user} password={password} host={host}'


@dataclass
class ServerConfig:
    port: str
    debug: bool
    pg_cfg: PostgreConfig


def load_config(app: 'web.Application') -> 'ServerConfig':
    """Config init."""

    pg_cfg = {
        'user': os.getenv('POSTGRES_USER', 'dashboard'),
        'password': os.getenv('POSTGRES_PASSWORD', 'dashboard'),
        'dbname': os.getenv('POSTGRES_DB', 'dashboard'),
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
    }

    config = ServerConfig(
        port=os.getenv('SERVER_PORT', '8888'),
        debug=True if os.getenv('DEBUG', None) else False,
        pg_cfg=PostgreConfig(**pg_cfg),
    )

    app['config'] = config

    logging.getLogger().handlers = []  # drop all previous logger handlers
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if app['config'].debug else logging.INFO
    )
    return config
