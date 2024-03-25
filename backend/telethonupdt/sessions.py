from django_telethon.models import UpdateState
from django_telethon.sessions import DjangoSession
from .models import UpdateStateClient
from telethon.tl import types


class CustomDjangoSession(DjangoSession):

    def get_update_state(self, entity_id):
        try:
            pass
            state = UpdateStateClient.objects.get(
                entity=entity_id, client_session=self.client_session
            ).state
            return types.updates.State(
                state.pts, state.qts, state.date, state.seq, unread_count=0
            )
        except UpdateState.DoesNotExist:
            return None

    def set_update_state(self, entity_id, state):
        qs_ids = UpdateStateClient.objects.filter(
            client_session=self.client_session,
            entity_id=entity_id,
        ).values_list("state_id", flat=True)

        if qs_ids.exists():
            UpdateState.objects.filter(id__in=qs_ids).update(
                pts=state.pts,
                qts=state.qts,
                date=state.date,
                seq=state.seq,
            )
        else:
            current_state = UpdateState.objects.create(
                client_session=self.client_session,
                pts=state.pts,
                qts=state.qts,
                date=state.date,
                seq=state.seq,
            )

            UpdateStateClient.objects.create(
                client_session=self.client_session,
                entity_id=entity_id,
                state=current_state,
            )
