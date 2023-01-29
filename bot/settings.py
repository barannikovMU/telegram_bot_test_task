from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp_client_cache import CacheBackend
from environs import Env
from loguru import logger

env = Env()
env.read_env(override=True)

API_TOKEN = env.str('API_TOKEN')
CBR_URL = env.str('CBR_URL')

# Database
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


logger.add(
    'bot/logs/backend.log',
    format='{time:DD/MM/YYYY HH:mm:ss} | {name}:{function}:{line} | {level} | {message}',
    level='DEBUG',
    rotation='10 MB',
    serialize=True,
    compression='zip',
    backtrace=True,
    diagnose=True,
    encoding='utf-8',
)

CACHE_EXPIRE_AFTER = env.int('CACHE_EXPIRE_AFTER', default=60 * 60)
cache = CacheBackend(expire_after=CACHE_EXPIRE_AFTER)

storage = MemoryStorage()
