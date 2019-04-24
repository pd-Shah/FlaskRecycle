from flask_login import current_user
from app.models import (
    Conversation,
    Message,
    User
)
from app.account import get_user
from app import db

from sqlalchemy import or_


def get_conversation(id):
    result = Conversation.query.get(id)
    return result


def get_conversations(**kwargs):
    if 'offer_id' in kwargs:
        result = Conversation.query.filter_by(
                    _offer_id=kwargs.get('offer_id')).all()
    elif 'user_id' in kwargs:
        result = Conversation.query.filter_by(
                    author_id=kwargs.get('user_id')).all()
    elif 'recipient_id' in kwargs:
        result = Conversation.query.join(User.conversations).filter(User.id == kwargs.get('recipient_id')).all()
    else:
        result = 'Undefined user'
    return result


def get_messages(**kwargs):
    if 'conversation_id' in kwargs:
        result = Message.query.filter_by(conversation_id=kwargs.get('conversation_id'))\
                              .order_by(Message.created).all()
    elif 'send' in kwargs:
        user = User.query.get(kwargs.get('user_id'))
        result = user._messages.all()
    else:
        result = 'No results'
    return result


def get_conversations_all():
    result = Conversation.query.join(User.conversations)\
                               .filter(or_(Conversation.author_id == current_user.id,
                                           User.id == current_user.id))\
                               .order_by(Conversation.updated).all()
    return result


def create_conversation(data):
    # create conversation
    new_conversation = Conversation(
        subject=data.subject,
        _offer_id=data.offer,
        author_id=current_user.id
    )
    db.session.add(new_conversation)
    new_message = Message(
        message=data.message,
        author_id=current_user.id
    )
    db.session.add(new_message)
    db.session.flush()
    conversation = Conversation.query.get(new_conversation.id)
    message = Message.query.get(new_message.id)
    user = get_user(data.recipient)
    conversation._recipients.append(user)
    conversation._messages.append(message)
    db.session.commit()
    return new_conversation.id


def add_message(data):
    new_message = Message(
        message=data.message.data,
        author_id=current_user.id
    )
    db.session.add(new_message)
    db.session.flush()
    conversation = Conversation.query.get(data.conversation_id)
    message = Message.query.get(new_message.id)
    conversation._messages.append(message)
    db.session.commit()
    return 'Added new Message'
