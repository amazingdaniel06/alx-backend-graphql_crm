INSTALLED_APPS = [
    # Default Django apps...
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "graphene_django",

    # Local app
    "crm",
]

GRAPHENE = {
    "SCHEMA": "alx_backend_graphql_crm.schema.schema"  # points to schema.py
}
