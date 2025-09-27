"""
Test script for the PC Parts Web Search MCP Server
This script demonstrates how to use the web search tools to find PC parts.
"""

import asyncio

from scout.my_mcp.local_servers.web_search import web_session, search_pc_parts, scrape_product_details, search_and_compare_prices

async def test_search_functionality():
    """Test the web search functionality"""
    print("🔍 Testing PC Parts Web Search Functionality\n")
    
    # Test 1: Basic search
    print("1. Testing basic search for RTX 4080...")
    try:
        results = await search_pc_parts("RTX 4080", 5)
        print("✅ Search completed successfully")
        print("Results preview:", results[:200] + "..." if len(results) > 200 else results)
        print()
    except Exception as e:
        print(f"❌ Search failed: {e}\n")
    
    # Test 2: Search for CPU
    print("2. Testing search for Intel CPU...")
    try:
        results = await search_pc_parts("Intel i7-13700K processor", 3)
        print("✅ CPU search completed")
        print("Results preview:", results[:200] + "..." if len(results) > 200 else results)
        print()
    except Exception as e:
        print(f"❌ CPU search failed: {e}\n")
    
    # Test 3: Price comparison
    print("3. Testing price comparison for RAM...")
    try:
        results = await search_and_compare_prices("32GB DDR5 RAM", 2)
        print("✅ Price comparison completed")
        print("Results preview:", results[:300] + "..." if len(results) > 300 else results)
        print()
    except Exception as e:
        print(f"❌ Price comparison failed: {e}\n")
    
    # Cleanup
    await web_session.close_session()
    print("🧹 Cleaned up web session")

if __name__ == "__main__":
    print("🚀 Starting PC Parts Search Test\n")
    asyncio.run(test_search_functionality())
    print("\n✅ Test completed!")