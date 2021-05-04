from typing import List

from redis import StrictRedis

from config import Config
from models import Fruit

REDIS: StrictRedis = StrictRedis.from_url(Config.REDIS_URL)


def init_cache():
    fruits: List[Fruit] = Fruit.query().all()
    for fruit in fruits:
        REDIS.set(fruit.name, f"{fruit.count}")
