from app import db
from app.models import User, Bot, Botdetail, Chat, Chatdetail, Service
from app.api import bp
from app.email import send_email
import sys

def createchat(user, bot):
    newchat = Chat(user_id = user, bot_id = bot, botdetail_id = 1)
    db.session.add(newchat)
    db.session.commit()
    response = {}
    instruction = getbotmessage(bot, 1, user)
    response['instruction'] = instruction
    response['id'] = newchat.id
    return response
    
def insertchatdetail(chat, message, author):
    chatdetail = Chatdetail.query.filter_by(chat_id = chat).order_by(Chatdetail.order.desc()).first()
    if chatdetail:
        order = chatdetail.order + 1
    else:
        order = 1
    newchatdetail = Chatdetail(chat_id = chat, order = order, message = message, author = author)
    db.session.add(newchatdetail)
    db.session.commit()
    
def usermessage(chat, message):
    response = {}
    chatheader = Chat.query.get(chat)
    if chatheader.botdetail_id == 0:
        response['instruction'] = "Chat cerrado, favor de volver a acceder a la herramienta"
        return response
    user = User.query.get(chatheader.user_id)
    instruction = Botdetail.query.filter_by(bot_id = chatheader.bot_id, order = chatheader.botdetail_id).first()
    validator = instruction.vali
    validators = validator.split(';')
    siCumple = None
    action = "NOTHING"
    i = 0
    while i < len(validators):
        if siCumple:
            print(action, file=sys.stderr)
            if action == "NEXT":
                posts = instruction.post.split(';')
                k = 0
                while k < len(posts): 
                    if posts[k] == "SERVICE":
                        #send_service_email(user.email, posts[k+1], chatheader.vars)
                        newservice = Service(bot = posts[k+1], var = chatheader.vars, email = user.email, status = 0, chat_id = chatheader.id)
                        db.session.add(newservice)
                        db.session.commit
                        k +=1
                    elif posts[k] == "VAR":
                        if chatheader.vars:
                            chatheader.vars = chatheader.vars + message + ";"
                        else:
                            chatheader.vars = message + ";"
                        db.session.commit()
                    k +=1
                instructionnew = Botdetail.query.filter_by(bot_id = chatheader.bot_id, order = instruction.next).first()
                updatechatheader(chatheader.id, chatheader.bot_id, instructionnew.order)
                response['instruction'] = getbotmessage(chatheader.bot_id, instruction.next, chatheader.user_id)
            elif action == "REPEAT":
                response['instruction'] = "Lo siento, no entendi la respuesta que dio." + getbotmessage(chatheader.bot_id, chatheader.botdetail_id, chatheader.user_id)
            elif action == "EXIT":
                response['instruction'] = "Que tenga buen dia, si desea solicitar otro servicio favor de volver a acceder a la herramienta"
                updatechatheader(chatheader.id, chatheader.bot_id, 0)
            elif action == "CALLBOT":
                newbot = Bot.query.filter_by(botname = validators[i+1]).first()
                instructionnew = Botdetail.query.filter_by(bot_id = newbot.id, order = 1).first()
                updatechatheader(chatheader.id, newbot.id, 1)
                response['instruction'] = getbotmessage(newbot.id, 1, chatheader.user_id)
            i = len(validators)
        else:
            conditions = validators[i].split(':')
            j = 0
            print(conditions, file=sys.stderr)
        while j < len(conditions):
            print(conditions[j], file=sys.stderr)
            if conditions[j] == "NUMERIC":
                if is_number(message):
                    siCumple = True
                    action = validators[i+1]
                else:
                    siCumple = False
                    j = len(conditions)    
            elif conditions[j] == "LONG":
                if len(message) == int(conditions[j+1]):
                    siCumple = True
                    action = validators[i+1]
                    j+=1
                else:
                    siCumple = False
                    j = len(conditions)
            elif conditions[j] == message or conditions[j] == "OTHER":
                siCumple = True
                action = validators[i+1]
                j = len(conditions)
            j +=1
        i +=1
    insertchatdetail(chat, response['instruction'], "Bot")
    return response 
        
def updatechatheader(chat, bot, instruction):
    chatheader = Chat.query.get(chat)
    chatheader.bot_id = bot
    chatheader.botdetail_id = instruction
    db.session.commit()
    
def getbotmessage(bot_id, order_id, user_id):
    user = User.query.get(user_id)
    instruction = Botdetail.query.filter_by(bot_id = bot_id, order = order_id).first()
    instructiondet = instruction.mesg.split('#')
    instructiontemp = []
    for message in instructiondet:
        if message == 'USER':
            instructiontemp.append(user.username)
        elif message == 'EMAIL':
            instructiontemp.append(user.email)
        else:
            instructiontemp.append(message)
    return "".join(instructiontemp)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def send_service_email(recipient, subject, body):
    send_email(subject,
               recipients=recipient,
               text_body=body)