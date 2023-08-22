from django.db import models
from mongoengine import *


class Blob(EmbeddedDocument):
    id = IntField(primary_key=True)
    vitality = IntField()
    charisma = IntField()
    life = IntField()
    speed = IntField()
    freeze = IntField()
    location = ListField()


class Snapshot(Document):
    step = IntField(primary_key=True)
    blobs = DictField(EmbeddedDocumentField(Blob))
    field = DictField()
    blobs_on_field = DictField()


class Configuration(Document):
    field_size = IntField()
    exp = IntField()
    sd = IntField()
    field_fertility = IntField()
    vitality = IntField()
    charisma = IntField()
    life_decrease = IntField()
    life_increase = IntField()
    prob_decrease = FloatField()


class Simulation(Document):
    simulation_id = StringField(primary_key=True)
    configuration = ReferenceField(Configuration)
    snapshots = ListField(ReferenceField(Snapshot), default=[])
