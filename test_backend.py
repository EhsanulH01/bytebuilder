"""
Test script to demonstrate the PC Part Picker backend is working
"""
import requests
import json

def test_backend():
    print("🚀 Testing PC Part Picker Backend...")
    print("=" * 50)
    
    # Test root endpoint (health check)
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            health = response.json()
            print("✅ Health Check: PASSED")
            print(f"   Message: {health['message']}")
            print(f"   Version: {health['version']}")
            print(f"   Available Endpoints: {health['endpoints']}")
        else:
            print("❌ Health Check: FAILED")
            return False
    except Exception as e:
        print(f"❌ Health Check: FAILED - {e}")
        return False
    
    print()
    
    # Test search endpoint
    try:
        search_data = {
            "query": "RTX 4080 graphics card",
            "max_results": 5,
            "compare_prices": True
        }
        
        print("🔍 Testing Search Functionality...")
        print(f"   Query: {search_data['query']}")
        
        response = requests.post(
            "http://localhost:8000/api/mcp-search",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            search_results = response.json()
            print("✅ Search Test: PASSED")
            print(f"   Source: {search_results['source']}")
            print(f"   Query: {search_results['query']}")
            
            results = search_results.get('results', {})
            if isinstance(results, dict) and 'results' in results:
                items = results['results']
                print(f"   Found {len(items)} results:")
                
                for i, item in enumerate(items[:3], 1):  # Show first 3 results
                    print(f"      {i}. {item.get('title', 'Unknown')}")
                    print(f"         Price: {item.get('price', 'N/A')}")
                    print(f"         Rating: {item.get('rating', 'N/A')}")
                    print()
            
        else:
            print(f"❌ Search Test: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Search Test: FAILED - {e}")
        return False
    
    print("🎉 All Tests Passed! Your PC Part Picker backend is working!")
    print("\n📡 Backend is running at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    test_backend()