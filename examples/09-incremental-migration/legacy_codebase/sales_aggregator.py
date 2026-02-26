#!/usr/bin/env python3
"""
Legacy: Sales Aggregation Engine (Performance Bottleneck)

This module handles daily sales aggregation for the ERP system.
Currently responsible for 23.4% of total CPU time.

Migration Target: Go (for concurrency + simplicity)
Expected Speedup: 12x
Priority: HIGH (Phase 1, #1 candidate)
"""

import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SalesRecord:
    """Single sales transaction record"""
    def __init__(self, order_id, customer_id, product_id, quantity, unit_price, discount, timestamp):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount = discount
        self.timestamp = timestamp

class DailyAggregate:
    """Daily aggregated sales metrics"""
    def __init__(self, date, total_revenue, total_orders, unique_customers, top_products):
        self.date = date
        self.total_revenue = total_revenue
        self.total_orders = total_orders
        self.unique_customers = unique_customers
        self.top_products = top_products

def aggregate_daily_sales(sales_records: List[SalesRecord], target_date: datetime) -> DailyAggregate:
    """
    Aggregate sales data for a specific date

    BOTTLENECK: This function processes 2.4M records/day
    - Runtime: 18.5 minutes (sequential processing)
    - CPU: 23.4% of total application time
    - Memory: 2.1 GB peak usage

    Args:
        sales_records: List of all sales records
        target_date: Date to aggregate

    Returns:
        DailyAggregate with computed metrics
    """
    start_time = time.time()

    # Filter records for target date (SLOW - full scan)
    date_filtered = []
    for record in sales_records:
        if record.timestamp.date() == target_date.date():
            date_filtered.append(record)

    logger.info(f"Filtered {len(date_filtered)} records for {target_date.date()}")

    # Calculate total revenue (SLOW - sequential loop)
    total_revenue = 0.0
    for record in date_filtered:
        subtotal = record.quantity * record.unit_price
        discounted = subtotal * (1.0 - record.discount / 100.0)
        total_revenue += discounted

    # Count unique customers (SLOW - set operations)
    unique_customers = set()
    for record in date_filtered:
        unique_customers.add(record.customer_id)

    # Find top 10 products by revenue (SLOW - manual sorting)
    product_revenue = {}
    for record in date_filtered:
        subtotal = record.quantity * record.unit_price
        discounted = subtotal * (1.0 - record.discount / 100.0)

        if record.product_id in product_revenue:
            product_revenue[record.product_id] += discounted
        else:
            product_revenue[record.product_id] = discounted

    # Sort products by revenue (SLOW - Python sort)
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    top_products = sorted_products[:10]

    elapsed = time.time() - start_time
    logger.info(f"Aggregation completed in {elapsed:.2f}s")

    return DailyAggregate(
        date=target_date,
        total_revenue=total_revenue,
        total_orders=len(date_filtered),
        unique_customers=len(unique_customers),
        top_products=top_products
    )

def aggregate_date_range(sales_records: List[SalesRecord], start_date: datetime, end_date: datetime) -> List[DailyAggregate]:
    """
    Aggregate sales for a date range

    BOTTLENECK: Called nightly for 30-day reports
    - Runtime: 9.5 hours (sequential, 30 iterations × 18.5 min)
    - Blocks other batch jobs

    MIGRATION OPPORTUNITY:
    - Go goroutines can parallelize 30 date aggregations
    - Expected: 9.5 hours → 47 minutes (12x speedup)
    """
    results = []
    current_date = start_date

    while current_date <= end_date:
        logger.info(f"Aggregating sales for {current_date.date()}...")
        aggregate = aggregate_daily_sales(sales_records, current_date)
        results.append(aggregate)
        current_date += timedelta(days=1)

    return results

# MIGRATION NOTES:
#
# 1. Go implementation can use:
#    - Goroutines for parallel date processing (30x parallelism)
#    - Maps for O(1) lookup instead of O(n) loops
#    - Channels for thread-safe aggregation
#    - sync.Pool for object reuse
#
# 2. Integration approach:
#    - Build Go shared library (.so)
#    - Use ctypes to call from Python
#    - Minimal changes to calling code
#
# 3. Validation:
#    - Run both implementations in parallel
#    - Compare results with 0.01% tolerance
#    - Canary deployment: 1% → 10% → 50% → 100%
#
# 4. Expected gains:
#    - 12x speedup (9.5 hours → 47 minutes)
#    - 60% less memory (2.1 GB → 850 MB)
#    - $12,000/year cloud cost savings
