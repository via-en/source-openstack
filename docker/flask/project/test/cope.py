# current_app.logger.debug(request.form)
#         data = {'success': True}
#         status_code = 201
#
#         try:
#             args = post_parser.parse_args()
#             sc = SenderSocial(params=rabbitmq_params)
#             sc.send_and_close_connection(text=json.dumps(args))
#         except Exception as err:
#             data = {'success': False, 'error': str(err)}
#             status_code = 400
#
#         return make_response(json.dumps(data), status_code)

# post_parser = reqparse.RequestParser()
# post_parser.add_argument(
#     'socialType', location='form', required=True,
#     help='Social type',
# )
# post_parser.add_argument(
#     'socialId', location='form', required=True,
#     help='Social id',
# )
# post_parser.add_argument(
#     'params', location='form', required=True,
#     help='Params',
# )
#
# fields = {
#     'id': fields.Integer,
#     'socialType': fields.String,
#     'socialId': fields.String,
#     'params': fields.String
# }
#
# #{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}
