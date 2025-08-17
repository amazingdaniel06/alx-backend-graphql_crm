INSTALLED_APPS = [
    # Django default apps...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "graphene_django",
    "django_filters",

    # Local
    "crm",
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"
}

