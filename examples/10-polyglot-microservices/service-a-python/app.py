#!/usr/bin/env python3
"""
Service A: API Gateway (Python/Flask)

Role: Orchestrate requests across microservices
- Handles HTTP API requests from clients
- Calls Rust pricing service for calculations
- Calls Go inventory service for stock queries
- Aggregates results and returns to client

Why Python?
- Fast development for business logic
- Easy API routing with Flask
- Delegates heavy lifting to compiled services
"""

from flask import Flask, jsonify, request
import requests
import os
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service URLs from environment
RUST_SERVICE_URL = os.getenv('RUST_SERVICE_URL', 'http://localhost:8001')
GO_SERVICE_URL = os.getenv('GO_SERVICE_URL', 'http://localhost:8002')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'service': 'api-gateway',
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get product information with pricing and inventory

    Workflow:
    1. Call Go service for inventory status
    2. Call Rust service for dynamic pricing
    3. Aggregate results
    4. Return to client
    """
    start_time = time.time()

    try:
        # Step 1: Get inventory from Go service
        logger.info(f"Fetching inventory for product {product_id}")
        inventory_response = requests.get(
            f"{GO_SERVICE_URL}/api/inventory/{product_id}",
            timeout=2.0
        )
        inventory_data = inventory_response.json()

        # Step 2: Calculate pricing from Rust service
        logger.info(f"Calculating pricing for product {product_id}")
        pricing_response = requests.post(
            f"{RUST_SERVICE_URL}/api/calculate_price",
            json={
                'product_id': product_id,
                'base_price': inventory_data.get('base_price', 100.0),
                'quantity_available': inventory_data.get('quantity', 0),
                'demand_factor': 1.2
            },
            timeout=2.0
        )
        pricing_data = pricing_response.json()

        # Step 3: Aggregate results
        result = {
            'product_id': product_id,
            'inventory': {
                'available': inventory_data.get('quantity', 0),
                'warehouse': inventory_data.get('warehouse', 'unknown'),
                'last_updated': inventory_data.get('last_updated')
            },
            'pricing': {
                'base_price': pricing_data.get('base_price'),
                'final_price': pricing_data.get('final_price'),
                'discount_percent': pricing_data.get('discount_percent', 0),
                'price_tier': pricing_data.get('price_tier')
            },
            'processing_time_ms': (time.time() - start_time) * 1000
        }

        logger.info(f"Product {product_id} request completed in {result['processing_time_ms']:.2f}ms")

        return jsonify(result)

    except requests.Timeout as e:
        logger.error(f"Timeout calling downstream service: {e}")
        return jsonify({'error': 'Service timeout'}), 504
    except requests.RequestException as e:
        logger.error(f"Error calling downstream service: {e}")
        return jsonify({'error': 'Service unavailable'}), 503
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/order', methods=['POST'])
def create_order():
    """
    Create a new order

    Workflow:
    1. Validate product availability (Go service)
    2. Calculate final pricing (Rust service)
    3. Reserve inventory (Go service)
    4. Return order confirmation
    """
    start_time = time.time()
    order_data = request.json

    try:
        product_id = order_data['product_id']
        quantity = order_data['quantity']

        # Step 1: Check inventory
        inventory_response = requests.get(
            f"{GO_SERVICE_URL}/api/inventory/{product_id}",
            timeout=2.0
        )
        inventory = inventory_response.json()

        if inventory.get('quantity', 0) < quantity:
            return jsonify({'error': 'Insufficient inventory'}), 400

        # Step 2: Calculate pricing
        pricing_response = requests.post(
            f"{RUST_SERVICE_URL}/api/calculate_price",
            json={
                'product_id': product_id,
                'base_price': inventory.get('base_price', 100.0),
                'quantity_available': inventory.get('quantity', 0),
                'demand_factor': 1.2
            },
            timeout=2.0
        )
        pricing = pricing_response.json()

        # Step 3: Reserve inventory
        reserve_response = requests.post(
            f"{GO_SERVICE_URL}/api/inventory/reserve",
            json={
                'product_id': product_id,
                'quantity': quantity
            },
            timeout=2.0
        )
        reservation = reserve_response.json()

        # Step 4: Create order
        order_result = {
            'order_id': int(time.time() * 1000),
            'product_id': product_id,
            'quantity': quantity,
            'unit_price': pricing.get('final_price'),
            'total_price': pricing.get('final_price') * quantity,
            'reservation_id': reservation.get('reservation_id'),
            'status': 'confirmed',
            'processing_time_ms': (time.time() - start_time) * 1000
        }

        logger.info(f"Order created: {order_result['order_id']}")

        return jsonify(order_result), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except requests.Timeout:
        return jsonify({'error': 'Service timeout'}), 504
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get aggregated statistics from all services
    """
    try:
        # Query all services for their stats
        rust_stats = requests.get(f"{RUST_SERVICE_URL}/api/stats", timeout=1.0).json()
        go_stats = requests.get(f"{GO_SERVICE_URL}/api/stats", timeout=1.0).json()

        return jsonify({
            'api_gateway': {
                'service': 'Python/Flask',
                'uptime': time.time()
            },
            'pricing_service': rust_stats,
            'inventory_service': go_stats
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': 'Unable to fetch stats'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
