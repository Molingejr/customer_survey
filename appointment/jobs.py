from django.core.exceptions import AppRegistryNotReady

"""Configuration for our job scheduler"""

try:
    import time

    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    register_events(scheduler)

except AppRegistryNotReady as exp:
    print(exp)