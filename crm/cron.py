import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"


def get_gql_client():
    """Return a gql client connected to the local GraphQL endpoint."""
    transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=False)
    return Client(transport=transport, fetch_schema_from_transport=True)


def log_crm_heartbeat():
    """Log heartbeat + test GraphQL hello query."""
    ts = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    client = get_gql_client()
    query = gql("{ hello }")   # expects your schema to have a `hello` field
    try:
        response = client.execute(query)
        status = response.get("hello", "No response")
    except Exception as e:
        status = f"Error: {e}"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{ts} CRM is alive - {status}\n")


def update_low_stock():
    """Run GraphQL mutation to restock low-stock products (< 10)."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    client = get_gql_client()
    mutation = gql("""
        mutation {
          updateLowStockProducts {
            success
            updated
          }
        }
    """)
    try:
        response = client.execute(mutation)["updateLowStockProducts"]
        success = response["success"]
        updated = ", ".join(response["updated"])
    except Exception as e:
        success = "Failed"
        updated = str(e)

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"{ts} - {success} - {updated}\n")
