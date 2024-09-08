from dialogs.models import Message


def get_answer_from_message(group_messages, ask_message):
    answer_messages = group_messages.filter(reply_to_msg_id=ask_message.message_id)
    dialogs_dict = {}
    for msg in answer_messages:
        # ищем сообщения которые являются ответами на текущее сообщение
        dialogs_dict[msg] = get_answer_from_message(group_messages, msg)

        context_messages = group_messages.filter(
            message_id__in=range(msg.message_id + 1, msg.message_id + 3),
            user_id=msg.user_id,
            reply_to_msg_id__isnull=True,  # ищем сообщения которые не являются ответами в контексте
        )
        for m in context_messages:
            # проверям есть ли ответы на сообщения из контекста
            dialogs_dict[m] = get_answer_from_message(group_messages, m)
    return dialogs_dict


def get_dialog_messages_from_dict(dialog, delta, messages_dict, reply_to_msg=None):
    dialog_messages = []
    if isinstance(messages_dict, dict) and messages_dict == {}:
        return dialog_messages
    for message, reply_messages_dict in messages_dict.items():
        msg, created = Message.objects.get_or_create(
            dialog=dialog,
            text=message.text,
            defaults={
                "role_name": message.user_id or "Smbd",
                "start_time": message.date - delta,
                "reply_to_msg": reply_to_msg,
            },
        )
        dialog_messages.append(msg.id)
        dialog_messages.extend(
            get_dialog_messages_from_dict(
                dialog,
                delta,
                reply_messages_dict,
                reply_to_msg=msg,
            )
        )
    return dialog_messages
