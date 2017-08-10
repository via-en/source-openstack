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

if not redis_params.password:

    rd = redis.Redis(
            host=redis_params.host,
            port=redis_params.port)
else:
    rd = redis.Redis(
        host=redis_params.host,
        port=redis_params.port,
        password=redis_params.password)


@methods.add
def initialize(*args, **kwargs):

    current_app.logger.debug(kwargs)
    settings = kwargs['settings']

    tasks = current_app.mongo.db.tasks
    task_object_id = tasks.insert({'settings': settings})
    task_result = tasks.find_one({'_id': task_object_id})
    sc.send_and_close_channel(str(task_result['_id']))
    task_result['_id'] = str(task_result['_id'])
    return task_result


@methods.add
def status(*args, **kwargs):
    current_app.logger.debug(kwargs)
    _id = kwargs['_id']
    status = rd.get(_id)
    return status.decode("utf-8")


class SocialItem(Resource):

    def post(self):
        req = request.get_data().decode()
        response = methods.dispatch(req)
        return Response(str(response), response.http_status,
                        mimetype='application/json')


api = Api(social)
api.add_resource(SocialItem, "")