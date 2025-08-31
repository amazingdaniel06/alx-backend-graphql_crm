INSTALLED_APPS += ["django_crontab"]

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
