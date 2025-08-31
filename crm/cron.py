import datetime

def log_crm_heartbeat():
    ts = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{ts} CRM is alive\n")
