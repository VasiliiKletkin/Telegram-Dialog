from django.db import models
from django.utils.timezone import now
from model_utils.models import TimeStampedModel
from telegram_groups.models import TelegramGroupDrain
from .dialogs import Dialog
from telegram_users.models import ActorUser


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

    def _check_errors(self, actors: list[ActorUser]):
        errors = []
        for actor in actors:
            if not actor.is_active:
                errors.append(f"{actor} is not active")
            elif not actor.is_ready:
                errors.append(f"{actor} is not ready")
            elif actor.errors:
                errors.append(f"{actor} has errors")
            elif not actor.is_member(self.drain.get_id()):
                errors.append(f"{actor} is not member of group")
        return errors

    def start(self):
        if not self.is_ready:
            raise Exception("scene in not ready")
        for message in self.dialog.messages.order_by("start_time"):
            role = scene.roles.get(name=message.role_name)
            target_time = timezone.now() + timedelta(
                seconds=message.start_time.second,
                minutes=message.start_time.minute,
                hours=message.start_time.hour,
            )
            target_time_str = target_time.strftime("%d-%b-%Y:%H:%M:%S")
            clocked_schedule = ClockedSchedule.objects.create(clocked_time=target_time)
            PeriodicTask.objects.create(
                clocked=clocked_schedule,
                name=f"Send message id:{message.id}, start_time:{target_time_str}, user_id:{role.telegram_user.id}, group:@{scene.telegram_group.username},  message:{message.text[:15]}",
                one_off=True,
                task="telegram.tasks.send_message_from_scene",
                args=json.dumps(
                    [
                        message.id,
                        scene.id,
                    ]
                ),
            )


class SceneRole(TimeStampedModel):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=255)
    actor = models.ForeignKey(ActorUser, on_delete=models.CASCADE, related_name="scene_roles")

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
