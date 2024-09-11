from core.celery import app

from .models import TelegramUserImport


@app.task
def convert_to_orm(import_id):
    import_obj = TelegramUserImport.objects.get(id=import_id)
    import_obj.convert_to_orm()
