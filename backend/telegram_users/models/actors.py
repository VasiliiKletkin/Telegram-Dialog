from .base import BaseClientUser, BaseClientUserManager


class ActorUserManager(BaseClientUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(client__is_listener=False)


class ActiveActorUserManager(ActorUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(client__is_listener=False)


class ActorUser(BaseClientUser):
    objects = ActorUserManager()
    active = ActiveActorUserManager()

    class Meta:
        proxy = True

    def send_message(self, chat_id, text, reply_to_msg_id=None):
        return self.get_client().send_message(
            chat_id=chat_id, text=text, reply_to_msg_id=reply_to_msg_id
        )
