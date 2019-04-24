from app import ma
from app.models import Task


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
