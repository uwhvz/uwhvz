import uuid
from datetime import datetime

from django.db import models
from enumfields import Enum, EnumField

from .game import Game

class RecipientGroup(Enum):
    HUMAN = 'H'
    ZOMBIE = 'Z'
    ALL = 'A'


class EmailManager(models.Manager):
    def create_email(self, name: str, data : str, group: RecipientGroup, game: Game, **extra_fields) -> 'Email':
        email = self.model(name=name, group=group, rule=rule, game=game, **extra_fields)
        email.save()
        return signup_location


class Email(models.Model):
    id: uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game: Game = models.ForeignKey(Game, on_delete=models.PROTECT)
    name: str = models.CharField(max_length=256)
    data: str = models.CharField(max_length=32768)
    group: Enum = EnumField(enum=RecipientGroup, max_length=1)
    player_made: bool = models.BooleanField(default=False)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    objects = EmailManager()

    def __str__(self):
        return self.name
