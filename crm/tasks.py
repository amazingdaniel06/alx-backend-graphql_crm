from datetime import datetime
from celery import shared_task
import requests


@shared_task
def generate_crm_report():
    """Generate a weekly CRM report via GraphQL and log it to /tmp."""
    query = """
    query {
      customersCount
      ordersCount
      totalRevenue
    }
    """

    try:
        resp = requests.post("http://localhost:8000/graphql", json={"query": query})
        data = resp.json().get("data", {})
        customers = data.get("customersCount", 0)
        orders = data.get("ordersCount", 0)
        revenue = data.get("totalRevenue", 0)
    except Exception as e:
        customers, orders, revenue = 0, 0, f"Error: {e}"

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{ts} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
