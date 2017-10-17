from flask_restful import Api, fields, marshal_with, reqparse, Resource
from flask import Blueprint, current_app, request, make_response, Response, g
import os, sys
import redis
from jsonrpcserver import methods
from social.config import Config
from social.sender import SenderSocial

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(CURRENT_DIR,'..', 'config')

social = Blueprint('social', __name__, url_prefix='/social')

rabbitmq_params = Config.setup_main_config(os.path.join(config_path, 'rabbitmq.yml'))
sc = SenderSocial(rabbitmq_params)

redis_params = Config.setup_main_config(os.path.join(config_path, 'redis.yml'))

if type(redis_params.password) is None:

    rd = redis.Redis(
            host=redis_params.host,
            port=redis_params.port)
else:
    rd = redis.Redis(
        host=redis_params.host,
        port=redis_params.port,
        password=redis_params.password
    )


@methods.add
def initialize(*args, **kwargs):

    current_app.logger.debug(kwargs)
    settings = kwargs['settings']

    tasks = current_app.mongo.db.tasks

    task_object_id = tasks.insert({'settings': settings})
    ID = tasks.find_one({'_id': task_object_id})

    task_result = {'ID': str(ID), 'mongoServerName': 'mongodb://localhost:27017',
                   'mongoDataBaseName': 'YandexData',
                   'mongoCollectionName': 'Snippets',
                   'redisHost': redis_params.host,
                   'redisPort': redis_params.port,
                   'redisPassword': redis_params.password
                   }
    task_result.update({'settings': settings})
    sc.send_and_close_channel(task_result)
    rd.set(str(task_result['ID']), 1)
    task_result['ID'] = str(task_result['ID'])
    return task_result


@methods.add
def status(*args, **kwargs):
    _id = kwargs['ID']
    #status = rd.set(_id, 1)
    status = rd.get(_id)
    current_app.logger.debug(status)

    return status.decode("utf-8")


class SocialItem(Resource):

    def post(self):
        req = request.get_data().decode()
        response = methods.dispatch(req)
        return Response(str(response), response.http_status,
                        mimetype='application/json')


api = Api(social)
api.add_resource(SocialItem, "")