#!/bin/bash
# Script to clean inactive customers

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
deleted=$(python3 manage.py shell -c "
from crm.models import Customer
from django.utils.timezone import now
from datetime import timedelta
cutoff = now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")

echo "$timestamp - Deleted $deleted inactive customers" >> /tmp/customer_cleanup_log.txt
