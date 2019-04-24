from flask import (
    Blueprint,
    flash,
    request,
    jsonify
)
from flask_login import login_required
from app import db
from app.modules.tasks import get_task, relate_task, relate_task_remove, delete_task
from app.modules.offers import (
    delete_offer,
    change_offer_status
)

api = Blueprint('api', __name__,)


@api.route("/", methods=('GET', 'POST'))
@login_required
def api_tasks():
    # TODO: verify
    if request.method == 'POST':
        content = request.get_json()
        _id = content['id']
        data = content['data']
        if content['action'] == "updateStatus":
            task = get_task(_id)
            task.status = data
            db.session.commit()
            flash("Updated task status")
            return jsonify()
        elif content['action'] == "assignUser":
            result = relate_task(_id, 'user', data)
            return jsonify({'result': result})
        elif content['action'] == "assignUserRemove":
            result = relate_task_remove(_id, 'user', data)
            return jsonify({'result': result})
        elif content['action'] == "relatedContactRemove":
            result = relate_task_remove(_id, 'contact', data)
            return jsonify({'result': result})
        elif content['action'] == "deleteTask":
            result = delete_task(_id)
            return jsonify({'result': result, 'destination': '/account/tasks/'})
        else:
            flash("Error {}".format("this"))
            return "no action defined, nothing to do ..."
    else:
        return 400


@api.route("/offers", methods=('GET', 'POST'))
@login_required
def api_offers():
    if request.method == 'POST':
        content = request.get_json()
        _id = content['id']
        data = content['data']
        if content['action'] == "delete":
            result = delete_offer(_id)
            return jsonify({'result': result, 'destination': '/account/recycling/offers'})
        elif content['action'] == "updateStatus":
            result = change_offer_status(_id, data)
            return jsonify({'result': result, 'destination': '/account/recycling/offers/{}'.format(_id)})
