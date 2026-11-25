"""
Simple test script to verify Flask API works
"""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

def test_app():
    """Test basic Flask app creation and routes"""
    print("Testing OpenFunds Backend API...")
    print("-" * 50)
    
    # Create app
    print("\n[1] Creating Flask app...")
    app = create_app()
    print("[OK] Flask app created successfully!")
    
    # Create test client
    client = app.test_client()
    
    # Test root endpoint
    print("\n[2] Testing root endpoint (/)...")
    response = client.get('/')
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.get_json()}")
    assert response.status_code == 200, "Root endpoint failed!"
    print("[OK] Root endpoint works!")
    
    # Test health check
    print("\n[3] Testing health check endpoint (/api/v1/health)...")
    response = client.get('/api/v1/health')
    print(f"   Status Code: {response.status_code}")
    data = response.get_json()
    print(f"   Response: {data}")
    assert response.status_code == 200, "Health check failed!"
    assert data['status'] == 'healthy', "Health status not healthy!"
    print("[OK] Health check works!")
    
    # Test ping
    print("\n[4] Testing ping endpoint (/api/v1/ping)...")
    response = client.get('/api/v1/ping')
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.get_json()}")
    assert response.status_code == 200, "Ping failed!"
    print("[OK] Ping works!")
    
    # Test user registration
    print("\n[5] Testing user registration (/api/v1/auth/register)...")
    response = client.post('/api/v1/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.get_json()}")
    assert response.status_code == 201, "Registration failed!"
    print("[OK] User registration works!")
    
    # Test user login
    print("\n[6] Testing user login (/api/v1/auth/login)...")
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"   Status Code: {response.status_code}")
    data = response.get_json()
    print(f"   Response: {data}")
    assert response.status_code == 200, "Login failed!"
    assert 'access_token' in data, "No access token returned!"
    token = data['access_token']
    print("[OK] User login works!")
    
    # Test authenticated endpoint
    print("\n[7] Testing authenticated endpoint (/api/v1/auth/me)...")
    response = client.get('/api/v1/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.get_json()}")
    assert response.status_code == 200, "Auth verification failed!"
    print("[OK] Authentication works!")
    
    # Test campaign creation
    print("\n[8] Testing campaign creation (/api/v1/campaigns)...")
    response = client.post('/api/v1/campaigns', 
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Campaign',
            'description': 'This is a test campaign for the OpenFunds platform',
            'btc_address': '2N8hwP1WmJrFF5QWABn38y63uYLhnJYJYTF',
            'target_amount': 1.5
        }
    )
    print(f"   Status Code: {response.status_code}")
    data = response.get_json()
    print(f"   Response: {data}")
    assert response.status_code == 201, "Campaign creation failed!"
    campaign_id = data['campaign']['id']
    print("[OK] Campaign creation works!")
    
    # Test get all campaigns
    print("\n[9] Testing get all campaigns (/api/v1/campaigns)...")
    response = client.get('/api/v1/campaigns')
    print(f"   Status Code: {response.status_code}")
    data = response.get_json()
    print(f"   Found {data['count']} campaign(s)")
    assert response.status_code == 200, "Get campaigns failed!"
    print("[OK] Get campaigns works!")
    
    # Test get single campaign
    print("\n[10] Testing get single campaign (/api/v1/campaigns/{id})...")
    response = client.get(f'/api/v1/campaigns/{campaign_id}')
    print(f"   Status Code: {response.status_code}")
    print(f"   Campaign: {response.get_json()['campaign']['title']}")
    assert response.status_code == 200, "Get campaign failed!"
    print("[OK] Get single campaign works!")
    
    # Test donation
    print("\n[11] Testing donation (/api/v1/campaigns/{id}/donate)...")
    response = client.post(f'/api/v1/campaigns/{campaign_id}/donate', json={
        'amount': 0.5
    })
    print(f"   Status Code: {response.status_code}")
    data = response.get_json()
    print(f"   Current amount: {data['campaign']['current_amount']} BTC")
    assert response.status_code == 200, "Donation failed!"
    print("[OK] Donation works!")
    
    # Test statistics
    print("\n[12] Testing statistics (/api/v1/campaigns/stats)...")
    response = client.get('/api/v1/campaigns/stats')
    print(f"   Status Code: {response.status_code}")
    stats = response.get_json()['statistics']
    print(f"   Total Campaigns: {stats['total_campaigns']}")
    print(f"   Total Raised: {stats['total_raised']} BTC")
    assert response.status_code == 200, "Stats failed!"
    print("[OK] Statistics work!")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] ALL BACKEND TESTS PASSED!")
    print("=" * 50)
    print("\nBackend is working perfectly!")
    print("Ready for production deployment!")

if __name__ == '__main__':
    try:
        test_app()
    except AssertionError as e:
        print(f"\n[FAILED] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
