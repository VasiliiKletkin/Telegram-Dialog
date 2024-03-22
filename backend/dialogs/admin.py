from django.contrib import admin, messages
from .models import Dialog, Message, Scene, Role
from .tasks import start_scene, check_scene
from .forms import RoleInlineAdminForm, MessageInlineAdminForm, SceneAdminForm


class MessageInlineAdmin(admin.TabularInline):
    form = MessageInlineAdminForm
    model = Message
    extra = 1


class DialogAdmin(admin.ModelAdmin):
    inlines = [MessageInlineAdmin]


class RoleInlineAdmin(admin.TabularInline):
    form = RoleInlineAdminForm
    model = Role
    extra = 1


class SceneAdmin(admin.ModelAdmin):
    list_display = ("dialog", "telegram_group", "is_active")
    inlines = [RoleInlineAdmin]
    actions = ["start", "check_obj"]
    form = SceneAdminForm

    def start(self, request, queryset):
        messages.add_message(request, messages.INFO, "Scenes starting...")
        for obj in queryset:
            start_scene(obj.id)

    start.short_description = "Start scene"

    def check_obj(self, request, queryset):
        messages.add_message(request, messages.INFO, "Scenes checking...")
        for obj in queryset:
            check_scene(obj.id)

    check_obj.short_description = "Check scene"


admin.site.register(Scene, SceneAdmin)
admin.site.register(Dialog, DialogAdmin)
