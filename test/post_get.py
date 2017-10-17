import os, sys
import requests
import logging.config
sys.path.append(os.getcwd())
from config import Config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR, 'config')
logging.config.fileConfig(os.path.join(config_path, 'logging.conf'))
logger = logging.getLogger(__name__)


def post_get():

    r = requests.post('http://127.0.0.1:5000/social', json={"jsonrpc": "2.0", 'id': 123, 'method': 'initialize',
                                                            'params': {
                                                                'settings': {
                                                                    'searcher': 'https://yandex.ru',
                                                                    'search_q': ['пластиковые окна'],
                                                                    'count': 1
                                                                    }
                                                                }
                                                            })
    result = r.json()
    logger.debug(result)

    if 'result' in result:

        r = requests.post('http://127.0.0.1:5000/social', json={"jsonrpc": "2.0", 'id': 123, 'method': 'status',
                                                                'params': {
                                                                    'ID': result['result']['ID']
                                                                }
                                                                })
        logger.debug(r.json())


def get(ID='59e489a4266e0d4bfa18a246'):
    r = requests.post('http://127.0.0.1:5000/social', json={"jsonrpc": "2.0", 'id': 123, 'method': 'status',
                                                           'params': {
                                                               'ID': ID
                                                           }
                                                           })
    logger.debug(r.json())


if __name__ == '__main__':
    post_get()
    #get('59e489a4266e0d4bfa18a246')