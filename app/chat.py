from flask import jsonify
from app import app
import json
import requests
import sys

def begin_chat(user_id, bot_id, token):
    payload = {'user': user_id, 'bot': bot_id, 'id':0, 'message':"" }
    headers={'Authorization':'Bearer {}'.format(token)}
    r = requests.post('http://localhost:5000/api/chats', headers=headers, json=payload)
    if r.status_code != 200:
        if r.status_code == 401:
            return ('Reiniciar sesion')
        return ('Dif a 200')
    message = json.loads(r.content)
    print(message, file=sys.stderr)
    return json.dumps(message)
    
def respond_chat(chat_id, message, token):
    payload = {'chat': chat_id, 'message': message }
    headers={'Authorization':'Bearer {}'.format(token)}
    r = requests.get('http://localhost:5000/api/chats', headers=headers, json=payload)
    if r.status_code != 200:
        if r.status_code == 401:
            return ('Reiniciar sesion')
        return ('Dif a 200')
    message = json.loads(r.content)
    print(message, file=sys.stderr)
    return json.dumps(message)
    
def loginUser(user, password):
    r = requests.post('http://localhost:5000/api/tokens', auth=(user,password))
    if r.status_code !=200:
       print('Error en la API de generar tokens', file=sys.stderr)
    print(r.content.decode('utf-8-sig'), file=sys.stderr)
    
def logoutUser(token):
    headers={'Authorization':'Bearer {}'.format(token)}
    r = requests.delete('http://localhost:5000/api/tokens', headers = headers)
    if r.status_code !=204:
        print('Error en la API de borrar tokens', file=sys.stderr)
        print(r.status_code, file=sys.stderr)