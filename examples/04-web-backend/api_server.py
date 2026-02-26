#!/usr/bin/env python3
"""
Example 4: Web Backend Optimization (Python Flask → Go)
Original Flask API with database queries and business logic
"""

import sys
import time
import json
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler

# Simulated database
DATABASE = {
    f"user_{i}": {
        "id": i,
        "name": f"User {i}",
        "email": f"user{i}@example.com",
        "balance": i * 100.0
    }
    for i in range(1, 10001)
}

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path.startswith("/api/user/"):
            # Extract user ID
            user_id = self.path.split("/")[-1]
            self.handle_get_user(user_id)
        elif self.path == "/api/users":
            self.handle_list_users()
        elif self.path == "/api/health":
            self.handle_health()
        else:
            self.send_error(404, "Not Found")

    def handle_get_user(self, user_id):
        """Get single user by ID"""
        start = time.time()

        user_key = f"user_{user_id}"
        if user_key in DATABASE:
            user = DATABASE[user_key]

            # Simulate business logic processing
            processed_user = process_user_data(user)

            self.send_json_response(200, processed_user)
        else:
            self.send_error(404, "User not found")

        elapsed = (time.time() - start) * 1000
        print(f"GET /api/user/{user_id} - {elapsed:.2f}ms", file=sys.stderr)

    def handle_list_users(self):
        """List all users with filtering"""
        start = time.time()

        # Get query params (simplified)
        # In real app: parse query string for filters

        users = list(DATABASE.values())

        # Simulate filtering and sorting
        filtered = [u for u in users if u["balance"] > 500]
        sorted_users = sorted(filtered, key=lambda u: u["balance"], reverse=True)

        result = {
            "count": len(sorted_users),
            "users": sorted_users[:100]  # Limit to 100
        }

        self.send_json_response(200, result)

        elapsed = (time.time() - start) * 1000
        print(f"GET /api/users - {elapsed:.2f}ms", file=sys.stderr)

    def handle_health(self):
        """Health check endpoint"""
        self.send_json_response(200, {"status": "ok"})

    def send_json_response(self, status, data):
        """Send JSON response"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Suppress default request logging"""
        pass

def process_user_data(user):
    """
    Business logic: process user data
    - Calculate derived fields
    - Hash sensitive data
    - Add metadata
    """
    processed = user.copy()

    # Calculate account tier
    if user["balance"] > 10000:
        processed["tier"] = "premium"
    elif user["balance"] > 5000:
        processed["tier"] = "gold"
    else:
        processed["tier"] = "standard"

    # Hash email for privacy
    email_hash = hashlib.sha256(user["email"].encode()).hexdigest()[:16]
    processed["email_hash"] = email_hash

    # Add timestamp
    processed["processed_at"] = int(time.time())

    return processed

def run_server(port=8080):
    """Run HTTP server"""
    server = HTTPServer(("0.0.0.0", port), APIHandler)
    print(f"Server running on http://localhost:{port}")
    print(f"Endpoints:")
    print(f"  GET /api/user/<id>")
    print(f"  GET /api/users")
    print(f"  GET /api/health")
    print(f"\nPress Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
