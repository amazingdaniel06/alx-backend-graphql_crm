import re
import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import transaction
from graphql import GraphQLError
from django.utils import timezone
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter

class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerType, filterset_class=CustomerFilter)
    all_products = DjangoFilterConnectionField(ProductType, filterset_class=ProductFilter)
    all_orders = DjangoFilterConnectionField(OrderType, filterset_class=OrderFilter)


# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists")
        if phone and not re.match(r"^\+?\d[\d\-]+$", phone):
            raise GraphQLError("Invalid phone format")

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully!")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(graphene.JSONString)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, customers):
        created = []
        errors = []
        with transaction.atomic():
            for cust in customers:
                try:
                    if Customer.objects.filter(email=cust["email"]).exists():
                        raise ValueError("Email already exists")
                    c = Customer.objects.create(
                        name=cust["name"], email=cust["email"], phone=cust.get("phone", "")
                    )
                    created.append(c)
                except Exception as e:
                    errors.append(f"{cust.get('email')}: {str(e)}")
        return BulkCreateCustomers(customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False, default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise GraphQLError("Price must be positive")
        if stock < 0:
            raise GraphQLError("Stock cannot be negative")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime(required=False)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise GraphQLError("No valid product IDs provided")

        order = Order.objects.create(customer=customer, order_date=order_date or timezone.now())
        order.products.set(products)
        order.total_amount = sum(p.price for p in products)
        order.save()
        return CreateOrder(order=order)


# Query + Mutation Schema
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_orders(root, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

