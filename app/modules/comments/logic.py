from flask import flash
from flask_babel import gettext
from flask_login import current_user
from app.models import Comment
from app import db


def get_comments(type, type_id):
    if type == 'task':
        result = Comment.query.filter(Comment._task_id == type_id)
        return result


def save_comment(data, task_id):
    new_comment = Comment(
        comment=data.comment.data,
        author_id=current_user.id,
        _task_id=task_id
    )
    db.session.add(new_comment)
    db.session.commit()
    result = new_comment.id
    flash(gettext('A new comment has been added'))
    return result
