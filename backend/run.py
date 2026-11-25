#!/usr/bin/env python3
"""
Run the OpenFunds Flask API server
"""
from app.main import app

if __name__ == '__main__':
    print("🚀 Starting OpenFunds API Server...")
    print("📍 Server running at: http://localhost:5000")
    print("📚 Health check: http://localhost:5000/api/v1/health")
    print("\n✨ Ready to accept requests!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
