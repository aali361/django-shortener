import datetime
from django.db.models import Count
from django.shortcuts import get_object_or_404
from celery.decorators import periodic_task, task
from celery.task.schedules import crontab

from . import models as app_models

ONE_DAY = 1
ONE_WEEK = 6
ONE_MONTH = 30

def get_related_records(url, time_type):
    accesses =  app_models.Access.objects.filter(url=url)
    yesterday = datetime.date.today() - datetime.timedelta(days=ONE_DAY)
    if time_type == app_models.Report.DAY:
        accesses = accesses.filter(created_at__date__gte=yesterday).filter(created_at__date__lte=yesterday)
    elif time_type == app_models.Report.WEEK:
        lastweek = yesterday - datetime.timedelta(days=ONE_WEEK)
        accesses = accesses.filter(created_at__date__gte=lastweek).filter(created_at__date__lte=yesterday)
    elif time_type == app_models.Report.MONTH:
        lastmonth = yesterday - datetime.timedelta(days=ONE_MONTH)
        accesses = accesses.filter(created_at__date__gte=lastmonth).filter(created_at__date__lte=yesterday)
    return accesses

def to_json(queryset):
    result = {}
    for item in queryset:
        result[list(item.values())[0]] = list(item.values())[1]
    return result

def get_statics(url=None, time_type=None, distinct=False, data=None):
    if data is None:
        records = get_related_records(url, time_type)
    else:
        records = data
    if distinct:
        records = records.values('url', 'viewer').distinct()
    view = records.count()
    device = records.values('device').annotate(count=Count('device', distinct=distinct))
    device = to_json(device)
    browser = records.values('browser').annotate(count=Count('browser', distinct=distinct))
    browser = to_json(browser)
    return view, device, browser

@periodic_task(run_every=(crontab(minute=0, hour=0)), name="daily_report")
def daily_report():
    urls = app_models.URL.objects.all()
    for url in urls:
        view, device, browser = get_statics(url, app_models.Report.DAY)
        R1 = app_models.Report(url=url, type=app_models.Report.DAY, view=view, device=device, browser=browser)
        view, device, browser = get_statics(url, app_models.Report.DAY, True)
        R2 = app_models.Report(url=url, type=app_models.Report.DAY, view=view, device=device, browser=browser, user_repetitive=True)
        view, device, browser = get_statics(url, app_models.Report.WEEK)
        R3 = app_models.Report(url=url, type=app_models.Report.WEEK, view=view, device=device, browser=browser)
        view, device, browser = get_statics(url, app_models.Report.WEEK, True)
        R4 = app_models.Report(url=url, type=app_models.Report.WEEK, view=view, device=device, browser=browser, user_repetitive=True)
        view, device, browser = get_statics(url, app_models.Report.MONTH)
        R5 = app_models.Report(url=url, type=app_models.Report.MONTH, view=view, device=device, browser=browser)
        view, device, browser = get_statics(url, app_models.Report.MONTH, True)
        R6 = app_models.Report(url=url, type=app_models.Report.MONTH, view=view, device=device, browser=browser, user_repetitive=True)
        app_models.Report.objects.bulk_create([R1,R2,R3,R4,R5,R6])

@task(name="register_access")
def register_access(short, user_id, is_mobile, is_pc, browser_family):
    url = get_object_or_404(app_models.URL, short=short)
    device = 'NA'
    if is_mobile:
        device = app_models.Access.MOBILE
    elif is_pc:
        device = app_models.Access.DESKTOP
    app_models.Access.objects.create(url=url, viewer_id=user_id, device=device, browser=browser_family)

