import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphql_crm.settings")
django.setup()

from crm.models import Customer, Product


def run():
    # Clear old data
    Customer.objects.all().delete()
    Product.objects.all().delete()

    # Seed Customers
    customers = [
        {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol", "email": "carol@example.com"},
    ]
    for c in customers:
        Customer.objects.create(**c)

    # Seed Products
    products = [
        {"name": "Laptop", "price": 999.99, "stock": 10},
        {"name": "Phone", "price": 499.99, "stock": 20},
        {"name": "Tablet", "price": 299.99, "stock": 15},
    ]
    for p in products:
        Product.objects.create(**p)

    print("Database seeded successfully!")


if __name__ == "__main__":
    run()

