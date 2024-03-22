from django.contrib import admin, messages
from .models import Dialog, Message, Scene, Role
from .tasks import start_scene, check_scene
from .forms import RoleInlineForm


class MessageInlineAdmin(admin.TabularInline):
    model = Message
    extra = 1


class DialogAdmin(admin.ModelAdmin):
    inlines = [MessageInlineAdmin]


class RoleInlineAdmin(admin.TabularInline):
    form = RoleInlineForm
    model = Role
    extra = 1


class SceneAdmin(admin.ModelAdmin):
    list_display = ('dialog', 'telegram_group', 'is_active')
    inlines = [RoleInlineAdmin]
    actions = ['start', 'check_obj']

    def start(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes starting...')
        for obj in queryset:
            start_scene.delay(obj.id)
    start.short_description = "Start scene"

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, 'Scenes checking...')
        for obj in queryset:
            check_scene.delay(obj.id)
    check_obj.short_description = "Check scene"


admin.site.register(Scene, SceneAdmin)
admin.site.register(Dialog, DialogAdmin)
