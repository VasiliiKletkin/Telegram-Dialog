from .users import TelegramUser


class BaseClientUser(TelegramUser):
    class Meta:
        proxy = True

    def is_member(self, group_id):
        return super().is_member(group_id)

    def get_me(self):
        return self.client.get_me()

    def join_chat(self, chat_id):
        return self.client.join_chat(chat_id)
