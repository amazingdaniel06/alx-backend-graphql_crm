import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

log_file = "/tmp/order_reminders_log.txt"
url = "http://localhost:8000/graphql"

transport = RequestsHTTPTransport(url=url, verify=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
query {
  orders(last7days: true) {
    id
    customer {
      email
    }
  }
}
""")

orders = client.execute(query)["orders"]

with open(log_file, "a") as f:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for order in orders:
        f.write(f"{ts} - Reminder for Order {order['id']} to {order['customer']['email']}\n")

print("Order reminders processed!")
