from django.contrib import admin
# from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.
# @admin.register(Announcement)
# class AnnouncementAdmin(ModelAdmin):
#     list_display = ('user','content')
#     list_display_links = ('user',)
#     readonly_fields = ('name',)

admin.site.register(Announcement)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Suggestion)
admin.site.register(Routine)
admin.site.register(Batch)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(VerifyPin)
admin.site.register(Event)
