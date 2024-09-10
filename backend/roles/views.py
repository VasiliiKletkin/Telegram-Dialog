# from django.shortcuts import render

# # Create your views here.
# class RoleAutocomplete(autocomplete.Select2QuerySetView):
#     queryset = Dialog.objects.all()
#     search_fields = ["name", "id"]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         is_active = self.forwarded.get("is_active")

#         if is_active is not None:
#             qs = qs.filter(is_active=is_active)

#         if telegram_group := self.forwarded.get("telegram_group"):
#             scenes = Scene.objects.filter(telegram_group=telegram_group)
#             qs = qs.exclude(scenes__in=scenes)
#         return qs
