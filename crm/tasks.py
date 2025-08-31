import datetime
from celery import shared_task
import requests

@shared_task
def generate_crm_report():
    query = """
    query {
      customersCount
      ordersCount
      totalRevenue
    }
    """
    resp = requests.post("http://localhost:8000/graphql", json={"query": query})
    data = resp.json()["data"]
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{ts} - Report: {data['customersCount']} customers, "
                f"{data['ordersCount']} orders, {data['totalRevenue']} revenue\n")
