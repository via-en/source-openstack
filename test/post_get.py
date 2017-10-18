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
                                                                    'search_q': ['Who are you, Joe Black'],
                                                                    'count': 1
                                                                    }
                                                                }
                                                            })
    result = r.json()
    logger.debug(result)

    if 'result' in result:

        r = requests.post('http://127.0.0.1:5000/social', json={"jsonrpc": "2.0", 'id': 123, 'method': 'status',
                                                                'params': {
                                                                    'ID': result['result']
                                                                }
                                                                })
        logger.debug(r.json())
        return r.json()


def get(ID):
    r = requests.post('http://127.0.0.1:5000/social', json={"jsonrpc": "2.0", 'id': 123, 'method': 'status',
                                                           'params': {
                                                               'ID': ID
                                                           }
                                                           })
    logger.debug(r.text)


if __name__ == '__main__':
    result = post_get()
    get(result['result']['ID'])
    #get('123')
