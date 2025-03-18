from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    status = fields.TextField()
    balance = fields.IntField()

    class Meta:
        table = "users"

    def __str__(self):
        return self.name


class Blackjack(Model):
    id = fields.IntField(primary_key=True)
    cards = fields.TextField()
    bet = fields.IntField()

    class Meta:
        table = "blackjack"

    def __str__(self):
        return self.name


class HorseRace(Model):
    id = fields.IntField(primary_key=True)
    horse_number = fields.IntField()
    bet = fields.IntField()

    class Meta:
        table = "horse_race"

    def __str__(self):
        return self.name