from django.contrib import admin, messages
from .models import Dialog, Message, Scene, Role
from .tasks import start_dialogs


class MessageInlineAdmin(admin.TabularInline):
    model = Message
    extra = 1


class DialogAdmin(admin.ModelAdmin):
    inlines = [MessageInlineAdmin]


class RoleInlineAdmin(admin.TabularInline):
    model = Role
    extra = 1


class SceneAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'group')
    inlines = [RoleInlineAdmin]
    actions = ['start_scene']

    def start_scene(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes started')
        for obj in queryset:
            start_dialogs.delay(obj.id)

    start_scene.short_description = "Start scene"


admin.site.register(Scene, SceneAdmin)
admin.site.register(Dialog, DialogAdmin)
