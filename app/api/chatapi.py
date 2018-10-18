from flask import jsonify, url_for, request, flash
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.botmind import createchat, insertchatdetail, usermessage
from app.api.auth import token_auth
import sys

@bp.route('/chats', methods=['GET'])
def respond_chat():
    data = request.get_json() or {}
    if 'chat' not in data or 'message' not in data:
	    return bad_request('Debe incluir chat y mensaje')
    insertchatdetail(data['chat'],data['message'],"User")
    resp = usermessage(data['chat'], data['message'])
    data['message'] = ""
    data['message'] = resp['instruction']
    response = jsonify(data)
    response.statuscode = 200
    return response

@bp.route('/chats', methods=['POST'])
@token_auth.login_required
def create_chat():
    data = request.get_json() or {}
    if 'user' not in data or 'bot' not in data:
	    return bad_request('Debe incluir user y bot')
    resp = createchat(data['user'],data['bot'])
    data['message'] = resp['instruction']
    data['id'] = resp['id']
    insertchatdetail(data['id'],data['message'],"Bot")
    response = jsonify(data)
    response.statuscode = 201
    response.headers['Location'] = url_for('main.index')
    return response