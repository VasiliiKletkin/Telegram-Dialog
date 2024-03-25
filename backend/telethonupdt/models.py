from django.db import models
from django_telethon.models import UpdateState, ClientSession


class UpdateStateClient(models.Model):
    entity_id = models.BigIntegerField()
    client_session = models.ForeignKey(ClientSession, on_delete=models.CASCADE)
    state = models.OneToOneField(UpdateState, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("entity_id", "client_session")
