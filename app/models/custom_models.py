from models.models import Model
from fields import fields

class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField()

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField()
    sex = fields.CharField()
    birthday = fields.DateTimeField()
    room = fields.ForeignKey(Room, 'id')
