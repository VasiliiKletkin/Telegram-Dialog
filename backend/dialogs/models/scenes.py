from datetime import timedelta
import json
from typing import List
from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel
from telegram_messages.models import TelegramGroupMessage
from telegram_groups.models import TelegramGroupDrain
from .dialogs import Dialog, DialogMessage
from telegram_users.models import ActorUser
from django_celery_beat.models import ClockedSchedule, PeriodicTask


class Scene(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)

    start_date = models.DateTimeField(default=now)
    drain = models.ForeignKey(TelegramGroupDrain, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="scenes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dialog", "drain"],
                name="dialog_drain_unique",
            )
        ]

    def __str__(self):
        return f"{self.id}-{self.drain.get_groupname()}-{self.dialog.name[:50]}"

    @property
    def is_ready(self):
        return (
            self.is_active
            and not self.errors
            and self.roles_count == self.dialog.roles_count
            and bool(self.last_check)
            and all(
                actor.is_ready and actor.is_member(self.drain.get_id())
                for actor in self.get_actors()
            )
        )

    def get_actors(self):
        return ActorUser.objects.filter(scene_roles__in=self.roles.all()).distinct()

    @property
    def roles_count(self):
        return self.roles.count()

    def pre_check_obj(self):
        for actor in self.get_actors():
            if not actor.is_member(self.drain.get_id()):
                actor.join_chat(self.drain.get_id())
                self.drain.members.add(actor)

    def check_obj(self):
        actors = self.get_actors()
        try:
            if self.roles_count != self.dialog.roles_count:
                raise Exception(
                    "Count of roles of Dialog are not equal count of roles of scene"
                )
            errors = self._check_errors(actors)
            if errors:
                raise Exception(errors)
        except Exception as error:
            self.error = str(error)
        else:
            self.error = None
        finally:
            self.last_check = now()
            self.save()

    def _check_users(self, users: list[ActorUser]):
        errors = []
        for user in users:
            if not user.is_active:
                errors.append(f"{user} is not active")
        if errors:
            return errors
        for user in users:
            if not user.is_ready:
                errors.append(f"{user} is not ready")
        if errors:
            return errors
        for user in users:
            if user.errors:
                errors.append(f"{user} has errors")
        if errors:
            return errors
        for user in users:
            if not user.is_member(self.drain.get_id()):
                errors.append(f"{user} is not member of group")
        if errors:
            return errors

    def get_role(self, role_name):
        return self.roles.get(name=role_name)

    def start(self):
        if not self.is_ready:
            raise Exception("scene in not ready")
        messages: List[DialogMessage] = self.dialog.messages.order_by("delay")
        for message in messages:
            role: SceneRole = self.get_role(message.role_name)
            target_time = now() + timedelta(
                seconds=message.delay.hour * 3600
                + message.delay.minute * 60
                + message.delay.second
            )
            target_time_str = target_time.strftime("%d-%b-%Y:%H:%M:%S")
            clocked_schedule = ClockedSchedule.objects.create(clocked_time=target_time)
            PeriodicTask.objects.create(
                clocked=clocked_schedule,
                name=f"Send message, id:{message.id}, time:{target_time_str}, user:{role.actor.get_id()}, group:{self.drain.get_id()},  message:{message.text[:10]}",
                one_off=True,
                task="dialogs.tasks.scenes.send_message_from_scene",
                args=json.dumps(
                    [
                        self.id,
                        message.id,
                    ]
                ),
            )

    def get_role(self, role_name):
        return self.roles.get(name=role_name)

    def get_reply_to_msg(self, message: DialogMessage) -> TelegramGroupMessage:
        if asked_message := message.reply_to_msg:
            asked_role: SceneRole = self.get_role(asked_message.role_name)
            return (
                self.drain.messages.filter(
                    user=asked_role.actor,
                    text=asked_message.text.replace("\r\n", " \n"),
                )
                .order_by("-date")
                .first()
            )

    def send_message(self, message_id):
        message: DialogMessage = self.dialog.messages.get(id=message_id)
        role: SceneRole = self.get_role(message.role_name)
        reply_to_msg: TelegramGroupMessage = self.get_reply_to_msg(message)

        sent_message = role.actor.send_message(
            chat_id=self.drain.get_id(),
            text=message.text,
            reply_to_msg_id=reply_to_msg.message_id if reply_to_msg else None,
        )
        self.drain.messages.create(
            message_id=sent_message.id,
            text=sent_message.message,
            date=sent_message.date,
            user_id=sent_message.from_id.user_id,
            reply_to_msg=reply_to_msg,
        )


class SceneRole(TimeStampedModel):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=255)
    actor = models.ForeignKey(
        ActorUser, on_delete=models.CASCADE, related_name="scene_roles"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["scene", "name", "actor"],
                name="scene_name_actor_unique",
            )
        ]
        indexes = [
            # models.Index(fields=["name"], name="name_idx"),
        ]

    def __str__(self):
        return f"role:{self.name}, actor:{self.actor}"
