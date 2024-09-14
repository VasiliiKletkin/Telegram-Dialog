from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from telegram_users.models.members import MemberUser
from telegram_users.models.users import TelegramUser
from .base import BaseGroupModel
from telegram_users.models import ActorUser, ListenerUser


class TelegramGroupSource(BaseGroupModel):
    listeners = models.ManyToManyField(
        ListenerUser,
        related_name="listener_sources",
        blank=True,
    )

    actors = models.ManyToManyField(
        ActorUser,
        related_name="actor_sources",
        blank=True,
        through="roles.TelegramGroupRole",
    )

    @property
    def is_ready(self):
        return (
            self.is_active
            and not self.errors
            and bool(self.last_check)
            and all(
                listener.is_ready and listener.is_member(self.get_id())
                for listener in self.user_listeners
            )
        )

    @property
    def user_actors(self) -> list[ActorUser]:
        return self.actors.all()

    @property
    def user_listeners(self) -> list[ListenerUser]:
        return self.listeners.all()

    def get_listener_user(self) -> ListenerUser:
        return self.listeners.first()

    @property
    def roles_count(self):
        return self.roles.count()

    def pre_check_obj(self):
        for listener in self.user_listeners:
            if not listener.is_member(self.get_id()):
                listener.join_chat(self.get_id())
                self.members.add(listener)

    def check_obj(self):
        try:
            if errors := self._check_users(self.listeners):
                raise Exception(errors)
        except Exception as e:
            self.errors = str(e)
        else:
            self.errors = None
        finally:
            self.last_check = now()
            self.save()

    def _check_users(self, users: list[ListenerUser]):
        errors = [
            f"{user} is not member of {self}"
            for user in users
            if not user.is_member(self.get_id())
        ]
        if errors:
            return errors
        for user in users:
            user.check_obj()
            user.refresh_from_db
        errors.extend(f"{user} is not active" for user in users if not user.is_active)
        if errors:
            return errors
        errors.extend(f"{user} has errors" for user in users if user.errors)
        if errors:
            return errors
        errors.extend(f"{user} is not ready" for user in users if not user.is_ready)
        if errors:
            return errors

    def get_messages(self, limit=1000):
        listener = self.get_listener_user()
        return listener.get_messages(chat_id=self.get_id(), limit=limit)

    def save_messages(self, limit=1000):
        def get_reply_to_msg(message):
            if message.reply_to and hasattr(message.reply_to, "reply_to_msg_id"):
                return self.messages.filter(
                    message_id=message.reply_to.reply_to_msg_id
                ).first()

        for message in self.get_messages(limit=limit):
            if not message.text or message.text == "":
                continue
            user = None
            if message.from_id and hasattr(message.from_id, "user_id"):
                user, created = TelegramUser.objects.get_or_create(
                    id=message.from_id.user_id,
                    defaults={
                        "username": getattr(message.from_id, "username", None),
                        "first_name": getattr(message.from_id, "first_name", None),
                        "last_name": getattr(message.from_id, "last_name", None),
                        "lang_code": getattr(message.from_id, "lang_code", None),
                        "phone": getattr(message.from_id, "phone", None),
                        "sex": getattr(message.from_id, "sex", None),
                    },
                )
                reply_to_msg = get_reply_to_msg(message)
                self.messages.get_or_create(
                    message_id=message.id,
                    defaults={
                        "text": message.text,
                        "date": message.date,
                        "user": user,
                        "reply_to_msg": reply_to_msg,
                    },
                )

    def get_members(self, limit=1000):
        listener = self.get_listener_user()
        return listener.get_participants(chat_id=self.get_id(), limit=limit)

    def save_members(self, limit=1000):
        for member in self.get_members(limit=limit):
            member, created = MemberUser.objects.get_or_create(
                id=member.id,
                defaults={
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "username": member.username,
                    "lang_code": member.lang_code,
                    "phone": member.phone,
                },
            )
            self.members.add(member)

    def create_random_roles(self):  # FIXME конкретный рефакторинг
        available_actors = ActorUser.active.exclude(actor_roles__in=self.roles.all())
        if self.members.count() < available_actors.count():
            raise ValidationError(
                f"Available actors{available_actors.count()} more than members{members.count()}"
            )
        for index, member in enumerate(self.members):
            self.roles.create(member=member, actor=available_actors[index])

    # def update_roles(self):
    #     self.create_roles_with_available_actors()
    #     roles = self.roles.all()
    #     end_date = now()
    #     start_date = end_date - timedelta(days=7)
    #     members = (
    #         self.members.annotate(
    #             messages_count=models.Count(
    #                 "messages",
    #                 filter=models.Q(messages__date__range=(start_date, end_date)),
    #             )
    #         )
    #         .order_by("messages_count")
    #         .filter(messages_count__gt=0)
    #     )

    #     members_without_roles = members.filter(member_roles__isnull=True)
    #     unusable_roles = roles.exclude(member__in=members).order_by("-modified")

    #     if members_without_roles.count() > unusable_roles.count():
    #         raise ValidationError(
    #             f"Active members{members_without_roles.count()} more than available roles{unusable_roles.count()}"
    #         )
    #     for index, member in enumerate(members_without_roles):
    #         unusable_roles[index].update(member=member)
