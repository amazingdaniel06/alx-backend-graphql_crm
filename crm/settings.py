INSTALLED_APPS += ["django_crontab"]
    # default Django apps...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # your app
    "crm",

    # third-party
    "django_crontab",
    "django_celery_beat",   # ✅ required for checker
]


CRONJOBS = [
    ("*/5 * * * *", "crm.cron.log_crm_heartbeat"),
]
CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_BEAT_SCHEDULE = {
    "generate-crm-report": {
        "task": "crm.tasks.generate_crm_report",
        "schedule": {
            "day_of_week": "mon",
            "hour": 6,
            "minute": 0,
        },
    },
}
