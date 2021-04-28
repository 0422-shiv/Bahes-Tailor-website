from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin

class ChatSystemAdmin(ModelAdmin):
    list_display = ["message_text","sender_id","receiver_id","send_datetime","read_status","read_datetime"]

admin.site.register(ChatSystem,ChatSystemAdmin)


admin.site.register(MuteChat)