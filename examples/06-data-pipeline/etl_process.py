#!/usr/bin/env python3
"""
Example 6: Data Pipeline Optimization (Python → C++)
Original Python ETL (Extract, Transform, Load) pipeline with CSV processing
"""

import csv
import time
import sys
import math
import json
from datetime import datetime
from io import StringIO

# Simulated large dataset
def generate_sample_data(num_records=1000000):
    """Generate sample sales data for testing"""
    records = []

    for i in range(num_records):
        record = {
            'transaction_id': i + 1,
            'customer_id': (i % 10000) + 1,
            'product_id': (i % 500) + 1,
            'quantity': (i % 10) + 1,
            'unit_price': 10.0 + (i % 100),
            'discount_percent': (i % 20),
            'timestamp': f"2024-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00",
            'region': ['US', 'EU', 'APAC', 'LATAM'][i % 4],
            'category': ['Electronics', 'Clothing', 'Food', 'Books'][i % 4]
        }
        records.append(record)

    return records

def extract_data(records):
    """
    Extract: Read data from source
    In real world: CSV files, databases, APIs, etc.
    """
    print(f"  [EXTRACT] Processing {len(records):,} records...")
    return records

def transform_record(record):
    """
    Transform: Apply business logic to single record
    - Calculate total amount
    - Apply discount
    - Calculate tax
    - Categorize transaction
    - Compute metrics
    """
    quantity = record['quantity']
    unit_price = record['unit_price']
    discount_percent = record['discount_percent']

    # Calculate subtotal
    subtotal = quantity * unit_price

    # Apply discount
    discount_amount = subtotal * (discount_percent / 100.0)
    discounted_subtotal = subtotal - discount_amount

    # Calculate tax (8% rate)
    tax_amount = discounted_subtotal * 0.08

    # Total amount
    total_amount = discounted_subtotal + tax_amount

    # Categorize transaction size
    if total_amount < 50:
        size_category = 'small'
    elif total_amount < 200:
        size_category = 'medium'
    else:
        size_category = 'large'

    # Calculate profit margin (30% markup assumed)
    cost = unit_price * 0.7
    profit = total_amount - (cost * quantity)
    profit_margin = (profit / total_amount) * 100 if total_amount > 0 else 0

    # Calculate value score (business metric)
    value_score = math.log(total_amount + 1) * (1.0 + profit_margin / 100.0)

    # Return transformed record
    return {
        'transaction_id': record['transaction_id'],
        'customer_id': record['customer_id'],
        'product_id': record['product_id'],
        'region': record['region'],
        'category': record['category'],
        'timestamp': record['timestamp'],
        'quantity': quantity,
        'unit_price': unit_price,
        'subtotal': subtotal,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'discounted_subtotal': discounted_subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'size_category': size_category,
        'profit': profit,
        'profit_margin': profit_margin,
        'value_score': value_score
    }

def transform_data(records):
    """
    Transform: Apply business logic to all records
    Sequential processing (one record at a time)
    """
    print(f"  [TRANSFORM] Applying business logic...")

    transformed = []
    for i, record in enumerate(records):
        transformed_record = transform_record(record)
        transformed.append(transformed_record)

        # Progress reporting
        if (i + 1) % 100000 == 0:
            print(f"    Processed {i + 1:,} records...")

    return transformed

def aggregate_data(records):
    """
    Aggregate: Compute summary statistics
    - Total sales by region
    - Total sales by category
    - Average transaction value
    """
    print(f"  [AGGREGATE] Computing summary statistics...")

    region_totals = {}
    category_totals = {}
    size_counts = {'small': 0, 'medium': 0, 'large': 0}

    total_revenue = 0.0
    total_profit = 0.0

    for record in records:
        region = record['region']
        category = record['category']
        size = record['size_category']
        amount = record['total_amount']
        profit = record['profit']

        # Aggregate by region
        if region not in region_totals:
            region_totals[region] = 0.0
        region_totals[region] += amount

        # Aggregate by category
        if category not in category_totals:
            category_totals[category] = 0.0
        category_totals[category] += amount

        # Count by size
        size_counts[size] += 1

        # Totals
        total_revenue += amount
        total_profit += profit

    return {
        'total_records': len(records),
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'profit_margin_avg': (total_profit / total_revenue * 100) if total_revenue > 0 else 0,
        'avg_transaction_value': total_revenue / len(records) if len(records) > 0 else 0,
        'region_totals': region_totals,
        'category_totals': category_totals,
        'size_counts': size_counts
    }

def load_data(transformed_records, summary):
    """
    Load: Write data to destination
    In real world: Database, data warehouse, file system, etc.
    """
    print(f"  [LOAD] Writing {len(transformed_records):,} records...")

    # Simulate writing to output (in real world: database insert, file write, etc.)
    # For benchmark purposes, we just count the records

    return len(transformed_records)

def run_etl_pipeline(num_records=1000000):
    """
    Run full ETL pipeline:
    1. Extract data from source
    2. Transform data (apply business logic)
    3. Aggregate data (compute summaries)
    4. Load data to destination
    """
    print("╔══════════════════════════════════════════════╗")
    print("║     Python ETL Pipeline (Sequential)         ║")
    print("╚══════════════════════════════════════════════╝\n")

    total_start = time.time()

    # Step 1: Extract
    extract_start = time.time()
    raw_records = generate_sample_data(num_records)
    records = extract_data(raw_records)
    extract_time = time.time() - extract_start
    print(f"    Extract time: {extract_time:.2f}s\n")

    # Step 2: Transform
    transform_start = time.time()
    transformed = transform_data(records)
    transform_time = time.time() - transform_start
    print(f"    Transform time: {transform_time:.2f}s\n")

    # Step 3: Aggregate
    aggregate_start = time.time()
    summary = aggregate_data(transformed)
    aggregate_time = time.time() - aggregate_start
    print(f"    Aggregate time: {aggregate_time:.2f}s\n")

    # Step 4: Load
    load_start = time.time()
    loaded_count = load_data(transformed, summary)
    load_time = time.time() - load_start
    print(f"    Load time: {load_time:.2f}s\n")

    total_time = time.time() - total_start

    # Print summary
    print("="*60)
    print("PIPELINE SUMMARY")
    print("="*60)
    print(f"Total records: {len(records):,}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Throughput: {len(records) / total_time:.2f} records/sec")
    print(f"\nBreakdown:")
    print(f"  Extract:   {extract_time:.2f}s ({extract_time/total_time*100:.1f}%)")
    print(f"  Transform: {transform_time:.2f}s ({transform_time/total_time*100:.1f}%)")
    print(f"  Aggregate: {aggregate_time:.2f}s ({aggregate_time/total_time*100:.1f}%)")
    print(f"  Load:      {load_time:.2f}s ({load_time/total_time*100:.1f}%)")

    print(f"\nBusiness Metrics:")
    print(f"  Total revenue: ${summary['total_revenue']:,.2f}")
    print(f"  Total profit: ${summary['total_profit']:,.2f}")
    print(f"  Profit margin: {summary['profit_margin_avg']:.2f}%")
    print(f"  Avg transaction: ${summary['avg_transaction_value']:.2f}")

    print(f"\nBy Region:")
    for region, total in sorted(summary['region_totals'].items()):
        print(f"  {region}: ${total:,.2f}")

    print(f"\nBy Category:")
    for category, total in sorted(summary['category_totals'].items()):
        print(f"  {category}: ${total:,.2f}")

    print(f"\nBy Size:")
    for size, count in sorted(summary['size_counts'].items()):
        print(f"  {size}: {count:,} transactions")

    return {
        'total_time': total_time,
        'extract_time': extract_time,
        'transform_time': transform_time,
        'aggregate_time': aggregate_time,
        'load_time': load_time,
        'throughput': len(records) / total_time,
        'summary': summary
    }

if __name__ == "__main__":
    num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000

    result = run_etl_pipeline(num_records)

    # Save benchmark results
    if len(sys.argv) > 2 and sys.argv[2] == '--save':
        with open('python_benchmark.json', 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nBenchmark results saved to python_benchmark.json")
