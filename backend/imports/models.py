from django.db import models


class TelegramUserImport(models.Model):
    json_field = models.FileField(upload_to='telegram_json')
    session_file = models.FileField(upload_to='telegram_session')

    def __str__(self):
        return f'{self.id}'
