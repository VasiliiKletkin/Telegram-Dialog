from .users import TelegramUser


class MemberUser(TelegramUser):

    class Meta:
        proxy = True
