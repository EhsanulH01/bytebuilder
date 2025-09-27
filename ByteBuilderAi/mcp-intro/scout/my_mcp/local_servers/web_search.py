"""
Web Search and Scraping MCP Server for PC Parts
This server provides tools to search Google for PC parts and scrape product information from web pages.
"""

import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional
import urllib.parse
import json
from dataclasses import dataclass
import time
import random

# Initialize FastMCP server
mcp = FastMCP("web-search")

@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    price: Optional[str] = None
    rating: Optional[str] = None
    availability: Optional[str] = None

class WebSearchSession:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def get_session(self) -> aiohttp.ClientSession:
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

    def extract_price(self, text: str) -> Optional[str]:
        """Extract price from text using regex patterns"""
        price_patterns = [
            r'\$[\d,]+\.?\d*',  # $199.99, $1,299
            r'USD\s*[\d,]+\.?\d*',  # USD 299.99
            r'[\d,]+\.?\d*\s*USD',  # 299.99 USD
            r'Price:\s*\$?[\d,]+\.?\d*',  # Price: $299.99
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def extract_rating(self, text: str) -> Optional[str]:
        """Extract rating from text"""
        rating_patterns = [
            r'(\d+\.?\d*)\s*(?:out of|/)\s*5\s*stars?',
            r'Rating:\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*★',
            r'(\d+\.?\d*)\s*stars?'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) + "/5"
        return None

    async def search_google(self, query: str, num_results: int = 10) -> List[SearchResult]:
        """Search Google for PC parts and return results"""
        try:
            session = await self.get_session()
            
            # Encode the search query
            encoded_query = urllib.parse.quote_plus(f"{query} pc computer hardware price buy")
            search_url = f"https://www.google.com/search?q={encoded_query}&num={num_results}&gl=us&hl=en"
            
            # Add random delay to avoid being blocked
            await asyncio.sleep(random.uniform(1, 3))
            
            async with session.get(search_url) as response:
                if response.status != 200:
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                
                # Extract search results
                for result in soup.find_all('div', class_='g')[:num_results]:
                    try:
                        # Get title and URL
                        title_elem = result.find('h3')
                        url_elem = result.find('a')
                        snippet_elem = result.find('span', {'data-ved': True}) or result.find('div', class_='VwiC3b')
                        
                        if title_elem and url_elem:
                            title = title_elem.get_text().strip()
                            url = url_elem.get('href', '')
                            snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                            
                            # Clean up the URL
                            if url.startswith('/url?q='):
                                url = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['q'][0]
                            
                            # Extract price and rating from snippet
                            price = self.extract_price(snippet + " " + title)
                            rating = self.extract_rating(snippet + " " + title)
                            
                            results.append(SearchResult(
                                title=title,
                                url=url,
                                snippet=snippet,
                                price=price,
                                rating=rating
                            ))
                    except Exception as e:
                        continue
                
                return results
                
        except Exception as e:
            return []

    async def scrape_product_page(self, url: str) -> Dict[str, str]:
        """Scrape detailed product information from a web page"""
        try:
            session = await self.get_session()
            
            # Add delay to be respectful
            await asyncio.sleep(random.uniform(2, 5))
            
            async with session.get(url) as response:
                if response.status != 200:
                    return {"error": f"Failed to fetch page: {response.status}"}
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract various product information
                product_info = {
                    "url": url,
                    "title": "",
                    "price": "",
                    "description": "",
                    "specifications": "",
                    "availability": "",
                    "rating": "",
                    "reviews_count": ""
                }
                
                # Extract title
                title_selectors = ['h1', 'title', '.product-title', '.item-title', '[data-testid="product-title"]']
                for selector in title_selectors:
                    elem = soup.select_one(selector)
                    if elem:
                        product_info["title"] = elem.get_text().strip()
                        break
                
                # Extract price
                price_selectors = [
                    '.price', '.current-price', '.sale-price', '.product-price',
                    '[data-testid*="price"]', '.price-current', '.notranslate'
                ]
                for selector in price_selectors:
                    elem = soup.select_one(selector)
                    if elem:
                        price_text = elem.get_text().strip()
                        extracted_price = self.extract_price(price_text)
                        if extracted_price:
                            product_info["price"] = extracted_price
                            break
                
                # Extract description
                desc_selectors = [
                    '.product-description', '.item-description', '.description',
                    '.product-details', '.overview', '[data-testid*="description"]'
                ]
                for selector in desc_selectors:
                    elem = soup.select_one(selector)
                    if elem:
                        product_info["description"] = elem.get_text().strip()[:500] + "..."
                        break
                
                # Extract specifications
                spec_selectors = [
                    '.specifications', '.specs', '.product-specs', '.technical-details',
                    '.features', '[data-testid*="spec"]'
                ]
                for selector in spec_selectors:
                    elem = soup.select_one(selector)
                    if elem:
                        product_info["specifications"] = elem.get_text().strip()[:1000] + "..."
                        break
                
                # Extract availability
                availability_selectors = [
                    '.availability', '.stock-status', '.in-stock', '.out-of-stock',
                    '[data-testid*="stock"]', '.inventory-status'
                ]
                for selector in availability_selectors:
                    elem = soup.select_one(selector)
                    if elem:
                        product_info["availability"] = elem.get_text().strip()
                        break
                
                # Extract rating
                full_text = soup.get_text()
                rating = self.extract_rating(full_text)
                if rating:
                    product_info["rating"] = rating
                
                return product_info
                
        except Exception as e:
            return {"error": f"Failed to scrape page: {str(e)}"}

# Initialize the session
web_session = WebSearchSession()

@mcp.tool()
async def search_pc_parts(query: str, num_results: int = 10) -> str:
    """
    Search Google for PC parts and return structured results with prices and ratings.
    
    Args:
        query: The PC part to search for (e.g., "RTX 4080", "Intel i7-13700K", "32GB DDR5 RAM")
        num_results: Number of search results to return (default: 10, max: 20)
    
    Returns:
        JSON string containing search results with titles, URLs, snippets, prices, and ratings
    """
    try:
        # Limit num_results to reasonable range
        num_results = min(max(num_results, 1), 20)
        
        results = await web_session.search_google(query, num_results)
        
        if not results:
            return json.dumps({
                "query": query,
                "results": [],
                "message": "No results found or search failed"
            }, indent=2)
        
        # Convert results to dict format
        results_data = []
        for result in results:
            results_data.append({
                "title": result.title,
                "url": result.url,
                "snippet": result.snippet,
                "price": result.price,
                "rating": result.rating,
                "availability": result.availability
            })
        
        return json.dumps({
            "query": query,
            "results_count": len(results_data),
            "results": results_data
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "query": query,
            "error": f"Search failed: {str(e)}",
            "results": []
        }, indent=2)

@mcp.tool()
async def scrape_product_details(url: str) -> str:
    """
    Scrape detailed product information from a specific web page.
    
    Args:
        url: The URL of the product page to scrape
    
    Returns:
        JSON string containing detailed product information including title, price, description, specifications, availability, and rating
    """
    try:
        if not url.startswith(('http://', 'https://')):
            return json.dumps({
                "error": "Invalid URL format. URL must start with http:// or https://",
                "url": url
            }, indent=2)
        
        product_info = await web_session.scrape_product_page(url)
        return json.dumps(product_info, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Scraping failed: {str(e)}",
            "url": url
        }, indent=2)

@mcp.tool()
async def search_and_compare_prices(part_name: str, max_sites: int = 5) -> str:
    """
    Search for a PC part and scrape detailed information from multiple retailer sites for price comparison.
    
    Args:
        part_name: The PC part to search for and compare prices
        max_sites: Maximum number of sites to scrape for detailed information (default: 5)
    
    Returns:
        JSON string containing search results and detailed scraped information from multiple sites
    """
    try:
        # First, search for the part
        search_results = await web_session.search_google(part_name, max_sites * 2)
        
        if not search_results:
            return json.dumps({
                "part_name": part_name,
                "error": "No search results found",
                "comparison": []
            }, indent=2)
        
        # Filter for retail sites and scrape detailed info
        retail_keywords = ['amazon', 'newegg', 'bestbuy', 'microcenter', 'bhphoto', 'tigerdirect', 'fry', 'walmart']
        detailed_results = []
        
        scraped_count = 0
        for result in search_results[:max_sites * 2]:  # Try more sites in case some fail
            if scraped_count >= max_sites:
                break
            
            # Prioritize retail sites
            is_retail = any(keyword in result.url.lower() for keyword in retail_keywords)
            
            if is_retail or scraped_count < max_sites // 2:  # Always scrape some retail sites
                try:
                    product_details = await web_session.scrape_product_page(result.url)
                    
                    if "error" not in product_details:
                        detailed_results.append({
                            "search_result": {
                                "title": result.title,
                                "url": result.url,
                                "snippet": result.snippet,
                                "search_price": result.price,
                                "search_rating": result.rating
                            },
                            "scraped_details": product_details
                        })
                        scraped_count += 1
                        
                        # Add delay between scraping requests
                        await asyncio.sleep(random.uniform(3, 7))
                        
                except Exception as e:
                    continue
        
        return json.dumps({
            "part_name": part_name,
            "total_search_results": len(search_results),
            "scraped_sites": len(detailed_results),
            "comparison": detailed_results
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "part_name": part_name,
            "error": f"Price comparison failed: {str(e)}",
            "comparison": []
        }, indent=2)

# Cleanup function
async def cleanup():
    await web_session.close_session()

if __name__ == "__main__":
    import atexit
    atexit.register(lambda: asyncio.run(cleanup()))
    mcp.run()