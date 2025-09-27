"""
Simple Web Search Demo for PC Parts
This demonstrates basic web scraping for PC part information.
"""

import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
import urllib.parse
import json
import random
import time

class PCPartSearcher:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    async def get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers=self.headers
            )
        return self.session
    
    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    def extract_price(self, text):
        """Extract price from text"""
        price_patterns = [
            r'\$[\d,]+\.?\d*',
            r'USD\s*[\d,]+\.?\d*',
            r'Price:\s*\$?[\d,]+\.?\d*',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None

    async def search_google_for_parts(self, query, num_results=5):
        """Search Google for PC parts"""
        try:
            session = await self.get_session()
            
            # Encode query
            encoded_query = urllib.parse.quote_plus(f"{query} pc hardware price buy")
            search_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
            
            print(f"🔍 Searching for: {query}")
            print(f"📡 URL: {search_url}")
            
            # Add delay
            await asyncio.sleep(random.uniform(1, 3))
            
            async with session.get(search_url) as response:
                if response.status != 200:
                    print(f"❌ Search failed with status: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                
                # Look for search results
                for i, result in enumerate(soup.find_all('div', class_='g')[:num_results]):
                    try:
                        # Get title
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text().strip()
                        
                        # Get URL
                        url_elem = result.find('a')
                        if not url_elem:
                            continue
                            
                        url = url_elem.get('href', '')
                        if url.startswith('/url?q='):
                            url = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['q'][0]
                        
                        # Get snippet
                        snippet_elem = result.find('span', {'data-ved': True}) or result.find('div', class_='VwiC3b')
                        snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                        
                        # Extract price
                        price = self.extract_price(snippet + " " + title)
                        
                        result_data = {
                            "rank": i + 1,
                            "title": title,
                            "url": url,
                            "snippet": snippet[:200] + "..." if len(snippet) > 200 else snippet,
                            "price": price
                        }
                        
                        results.append(result_data)
                        print(f"✅ Found result {i+1}: {title}")
                        if price:
                            print(f"   💰 Price: {price}")
                        
                    except Exception as e:
                        print(f"⚠️  Error processing result {i+1}: {e}")
                        continue
                
                return results
                
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

    async def demo_search(self):
        """Demo the search functionality"""
        print("🚀 PC Parts Search Demo Starting...\n")
        
        # Test searches
        test_queries = [
            "RTX 4080 graphics card",
            "Intel i7-13700K processor", 
            "32GB DDR5 RAM memory"
        ]
        
        all_results = {}
        
        for query in test_queries:
            print(f"\n{'='*50}")
            results = await self.search_google_for_parts(query, 3)
            all_results[query] = results
            
            print(f"\n📊 Results for '{query}': {len(results)} found")
            for result in results:
                print(f"\n{result['rank']}. {result['title']}")
                if result['price']:
                    print(f"   💰 {result['price']}")
                print(f"   🔗 {result['url'][:60]}...")
                print(f"   📝 {result['snippet'][:100]}...")
            
            # Wait between searches
            await asyncio.sleep(3)
        
        # Save results to file
        with open('search_results.json', 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Demo complete! Results saved to 'search_results.json'")
        print(f"📁 Found {sum(len(results) for results in all_results.values())} total results")
        
        await self.close_session()

async def main():
    searcher = PCPartSearcher()
    await searcher.demo_search()

if __name__ == "__main__":
    print("🛠️  PC Parts Web Search Tool")
    print("=" * 40)
    asyncio.run(main())