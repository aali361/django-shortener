from django.contrib import admin

from . import models as app_models

@admin.register(app_models.Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'viewer', 'device', 'browser', 'created_at', )


@admin.register(app_models.URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'owner', 'created_at', )


@admin.register(app_models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'type', 'user_repetitive', 'created_at', )
