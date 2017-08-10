import redis
import os, sys
import logging.config
import time
sys.path.append(os.getcwd())
from config import Config


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)
params = Config.setup_main_config(os.path.join(config_path, 'main.yml'))
logger.debug(params.__dict__)
r = redis.Redis(
    host=params.host,
    port=params.port,
    #password=params.password
)

r.set('598af840266e0d7435ea7a5e', 1)
for i in range(0, 99):
    time.sleep(5)
    logger.debug(i)
    r.incr('598af840266e0d7435ea7a5e')
