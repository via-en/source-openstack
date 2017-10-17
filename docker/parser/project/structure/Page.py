from mongoengine import *
import datetime


class Page(Document):
    title = StringField(max_length=200, required=True)
    date_modified = DateTimeField(default=datetime.datetime.now)
    date_create = DateTimeField(default=datetime.datetime.now)
    task_id = StringField(max_length=256, required=True)
    snippet = StringField(max_length=200, required=True)
    text = StringField(max_length=200, required=True)
    url = StringField(max_length=200, required=True)
    search_query = StringField(max_length=200, required=True)
    snippet_number = IntField(required=True)
