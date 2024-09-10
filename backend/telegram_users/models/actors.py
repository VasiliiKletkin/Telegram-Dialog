from .base import BaseClientUser


class ActorUser(BaseClientUser):
    class Meta:
        proxy = True

    def send_message(self, chat_id, text):
        return self.get_client().send_message(chat_id=chat_id, text=text)
