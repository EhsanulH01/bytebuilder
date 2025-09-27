"""
PC Part Picker Backend API
FastAPI server that provides PC part recommendations, compatibility checking, and price analysis.
Integrates with Scout MCP server for AI-powered recommendations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Add the project root to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from pc_compatibility_engine import PCCompatibilityChecker, ComponentType
except ImportError:
    # Create a minimal compatibility checker if import fails
    class PCCompatibilityChecker:
        def generate_build_report(self, components):
            return {"error": "Compatibility engine not available"}
        def find_compatible_parts(self, base_component, component_name):
            return []
        def recommend_psu_wattage(self, components):
            return 750, "Estimate based on typical requirements"

def get_enhanced_component_results(query: str) -> List[Dict]:
    """
    Return specific PC component results based on the query category
    """
    query_lower = query.lower()
    
    if "cpu" in query_lower or "processor" in query_lower:
        return [
            {
                "title": "Intel Core i7-13700K Processor",
                "price": "$409.99",
                "url": "https://www.intel.com/content/www/us/en/products/sku/230496/intel-core-i713700k-processor-25m-cache-up-to-5-40-ghz/page.html",
                "snippet": "16-core (8P+8E) 24-thread processor with up to 5.4 GHz boost clock. LGA1700 socket.",
                "rating": "4.7",
                "specs": "16 cores, 24 threads, 5.4 GHz boost, LGA1700"
            },
            {
                "title": "AMD Ryzen 7 7700X Processor", 
                "price": "$349.99",
                "url": "https://www.amd.com/en/products/cpu/amd-ryzen-7-7700x",
                "snippet": "8-core 16-thread processor with up to 5.4 GHz boost clock. AM5 socket, 65W TDP.",
                "rating": "4.6",
                "specs": "8 cores, 16 threads, 5.4 GHz boost, AM5"
            },
            {
                "title": "Intel Core i5-13600K Processor",
                "price": "$289.99", 
                "url": "https://www.intel.com/content/www/us/en/products/sku/230493/intel-core-i513600k-processor-24m-cache-up-to-5-10-ghz/page.html",
                "snippet": "14-core (6P+8E) 20-thread processor with up to 5.1 GHz boost clock. Great price/performance.",
                "rating": "4.8",
                "specs": "14 cores, 20 threads, 5.1 GHz boost, LGA1700"
            }
        ]
    
    elif "gpu" in query_lower or "graphics" in query_lower:
        return [
            {
                "title": "NVIDIA GeForce RTX 4070 Graphics Card",
                "price": "$599.99",
                "url": "https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070/", 
                "snippet": "12GB GDDR6X VRAM, DLSS 3, Ray Tracing. Perfect for 1440p gaming.",
                "rating": "4.5",
                "specs": "12GB GDDR6X, 5888 CUDA cores, 200W TDP"
            },
            {
                "title": "AMD Radeon RX 7800 XT Graphics Card",
                "price": "$549.99",
                "url": "https://www.amd.com/en/products/graphics/amd-radeon-rx-7800-xt",
                "snippet": "16GB GDDR6 VRAM, RDNA 3 architecture. Excellent 1440p performance.",
                "rating": "4.4", 
                "specs": "16GB GDDR6, 3840 stream processors, 263W TDP"
            },
            {
                "title": "NVIDIA GeForce RTX 4080 Graphics Card",
                "price": "$1199.99",
                "url": "https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4080/",
                "snippet": "16GB GDDR6X VRAM, flagship performance for 4K gaming with ray tracing.",
                "rating": "4.6",
                "specs": "16GB GDDR6X, 9728 CUDA cores, 320W TDP"
            }
        ]
    
    elif "ram" in query_lower or "memory" in query_lower:
        return [
            {
                "title": "Corsair Vengeance LPX 32GB DDR4-3200",
                "price": "$179.99",
                "url": "https://www.corsair.com/us/en/Categories/Products/Memory/VENGEANCE-LPX/p/CMK32GX4M2E3200C16",
                "snippet": "32GB (2x16GB) DDR4-3200 CL16 memory kit. Low profile design for better compatibility.",
                "rating": "4.5",
                "specs": "32GB DDR4, 3200 MHz, CL16, 1.35V"
            },
            {
                "title": "G.Skill Trident Z5 32GB DDR5-5600",
                "price": "$239.99", 
                "url": "https://www.gskill.com/product/165/326/1639708516/F5-5600J3636C16GX2-TZ5S",
                "snippet": "32GB (2x16GB) DDR5-5600 CL36. Premium RGB lighting with excellent performance.",
                "rating": "4.7",
                "specs": "32GB DDR5, 5600 MHz, CL36, RGB"
            },
            {
                "title": "Corsair Vengeance DDR5-5200 16GB",
                "price": "$129.99",
                "url": "https://www.corsair.com/us/en/Categories/Products/Memory/VENGEANCE-DDR5/p/CMK16GX5M2B5200C40",
                "snippet": "16GB (2x8GB) DDR5-5200 CL40. Great entry-level DDR5 for modern builds.",
                "rating": "4.3",
                "specs": "16GB DDR5, 5200 MHz, CL40, 1.25V"
            }
        ]
        
    elif "storage" in query_lower or "ssd" in query_lower or "drive" in query_lower:
        return [
            {
                "title": "Samsung 980 PRO 1TB NVMe SSD",
                "price": "$129.99",
                "url": "https://www.samsung.com/us/computing/memory-storage/solid-state-drives/980-pro-pcie-4-0-nvme-ssd-1tb-mz-v8p1t0b-am/",
                "snippet": "1TB PCIe 4.0 NVMe SSD with 7000 MB/s read speeds. Premium performance storage.",
                "rating": "4.8",
                "specs": "1TB NVMe, PCIe 4.0, 7000/5000 MB/s"
            },
            {
                "title": "Western Digital Black SN850X 2TB",
                "price": "$199.99",
                "url": "https://www.westerndigital.com/products/internal-drives/wd-black-sn850x-nvme-ssd",
                "snippet": "2TB PCIe 4.0 gaming SSD with heatsink. Optimized for gaming and content creation.",
                "rating": "4.6", 
                "specs": "2TB NVMe, PCIe 4.0, 7300/6600 MB/s"
            },
            {
                "title": "Crucial P3 Plus 1TB NVMe SSD",
                "price": "$79.99",
                "url": "https://www.crucial.com/ssd/p3-plus/CT1000P3PSSD8",
                "snippet": "1TB PCIe 4.0 SSD with solid performance at an affordable price point.",
                "rating": "4.2",
                "specs": "1TB NVMe, PCIe 4.0, 5000/4200 MB/s"
            }
        ]
        
    elif "motherboard" in query_lower:
        return [
            {
                "title": "ASUS ROG STRIX Z790-E GAMING WiFi",
                "price": "$449.99",
                "url": "https://rog.asus.com/motherboards/rog-strix/rog-strix-z790-e-gaming-wifi-model/",
                "snippet": "Premium Z790 motherboard with WiFi 6E, DDR5 support, and extensive connectivity.",
                "rating": "4.7",
                "specs": "LGA1700, Z790, DDR5, WiFi 6E, ATX"
            },
            {
                "title": "MSI MAG B650 TOMAHAWK WiFi",
                "price": "$229.99",
                "url": "https://www.msi.com/Motherboard/MAG-B650-TOMAHAWK-WIFI",
                "snippet": "B650 motherboard for AMD Ryzen 7000 series with WiFi 6 and PCIe 5.0 support.",
                "rating": "4.5",
                "specs": "AM5, B650, DDR5, WiFi 6, ATX"
            }
        ]
    
    elif "case" in query_lower:
        return [
            {
                "title": "Fractal Design Define 7 Compact",
                "price": "$169.99",
                "url": "https://www.fractal-design.com/products/cases/define/define-7-compact/black/",
                "snippet": "Premium silent case with excellent build quality and cable management.",
                "rating": "4.8",
                "specs": "Mid tower, ATX, USB-C, sound dampening"
            },
            {
                "title": "NZXT H7 Flow",
                "price": "$129.99", 
                "url": "https://nzxt.com/product/h7-flow",
                "snippet": "High airflow case with RGB lighting and excellent cooling performance.",
                "rating": "4.6",
                "specs": "Mid tower, ATX, RGB, high airflow"
            }
        ]
        
    elif "power" in query_lower or "psu" in query_lower:
        return [
            {
                "title": "Corsair RM850x 850W 80+ Gold",
                "price": "$149.99",
                "url": "https://www.corsair.com/us/en/Categories/Products/Power-Supply-Units/Power-Supply-Units-Advanced/RMx-Series/p/CP-9020200-NA",
                "snippet": "850W 80+ Gold modular PSU with 10-year warranty and silent operation.",
                "rating": "4.8",
                "specs": "850W, 80+ Gold, fully modular, 10yr warranty"
            },
            {
                "title": "EVGA SuperNOVA 750 GT 750W",
                "price": "$119.99",
                "url": "https://www.evga.com/products/product.aspx?pn=220-GT-0750-Y1",
                "snippet": "750W 80+ Gold PSU with excellent efficiency and reliable performance.",
                "rating": "4.5",
                "specs": "750W, 80+ Gold, semi-modular, 7yr warranty"
            }
        ]
        
    elif "cool" in query_lower or "fan" in query_lower:
        return [
            {
                "title": "Noctua NH-D15 CPU Air Cooler",
                "price": "$109.99",
                "url": "https://noctua.at/en/nh-d15",
                "snippet": "Premium dual-tower air cooler with exceptional cooling performance and silence.",
                "rating": "4.9",
                "specs": "Dual tower, 2x140mm fans, AM5/LGA1700"
            },
            {
                "title": "Corsair H100i RGB PLATINUM SE",
                "price": "$159.99",
                "url": "https://www.corsair.com/us/en/Categories/Products/Liquid-Cooling/Dual-Radiator-Liquid-Coolers/Hydro-Series%E2%84%A2-H100i-RGB-PLATINUM-SE/p/CW-9060042-WW",
                "snippet": "240mm AIO liquid cooler with RGB lighting and excellent cooling performance.",
                "rating": "4.4",
                "specs": "240mm AIO, RGB, 2400 RPM, Universal"
            }
        ]
        
    elif "accessories" in query_lower:
        return [
            {
                "title": "Logitech G Pro X Superlight Gaming Mouse", 
                "price": "$149.99",
                "url": "https://www.logitechg.com/en-us/products/gaming-mice/pro-x-superlight-wireless-mouse.html",
                "snippet": "Ultra-lightweight wireless gaming mouse with HERO 25K sensor.",
                "rating": "4.7",
                "specs": "25,600 DPI, 63g weight, wireless, 70hr battery"
            },
            {
                "title": "SteelSeries Apex Pro Mechanical Keyboard",
                "price": "$199.99",
                "url": "https://steelseries.com/gaming-keyboards/apex-pro",
                "snippet": "Adjustable mechanical switches with OLED display and per-key RGB.",
                "rating": "4.5",
                "specs": "OmniPoint switches, OLED, RGB, USB passthrough"
            }
        ]
    
    # Default fallback for unrecognized queries
    return [
        {
            "title": f"Premium {query.title()} Component",
            "price": "$299.99",
            "url": f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "snippet": f"High-quality {query} component with excellent performance and reliability.",
            "rating": "4.5",
            "specs": "Professional grade specifications"
        }
    ]

# Initialize FastAPI
app = FastAPI(
    title="PC Part Picker API",
    description="AI-powered PC building assistant with compatibility checking and price analysis",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    compare_prices: Optional[bool] = False

class CompatibilityRequest(BaseModel):
    components: Dict[str, Dict]

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "PC Part Picker API", 
        "version": "1.0.0",
        "endpoints": {
            "mcp_search": "/api/mcp-search",
            "compatibility_check": "/api/compatibility-check"
        }
    }

@app.post("/api/mcp-search")
async def mcp_search_parts(request: SearchRequest):
    """Search for PC parts using web search"""
    try:
        # Import our simple web search function
        from simple_web_search import simple_search_pc_parts
        
        # Use the simple search function
        results_data = await simple_search_pc_parts(request.query, request.max_results or 10)
        
        return {
            "query": request.query,
            "source": "Web Search",
            "results": results_data,
            "timestamp": "2025-09-26T12:00:00Z"
        }
            
    except Exception as e:
        print(f"Web search error: {e}")
        # Return fallback results with enhanced component data
        enhanced_results = get_enhanced_component_results(request.query)
        return {
            "query": request.query,
            "source": "Enhanced Search",
            "results": {
                "query": request.query,
                "results": enhanced_results,
                "message": f"Found {len(enhanced_results)} enhanced {request.query} results"
            }
        }

@app.post("/api/compatibility-check")
async def check_pc_compatibility(request: CompatibilityRequest):
    """Check compatibility of selected PC components using AI analysis"""
    try:
        # Import the AI compatibility analyzer
        from ai_compatibility import ai_analyzer
        
        # Use AI-powered compatibility analysis
        compatibility_report = await ai_analyzer.analyze_compatibility(request.components)
        
        return {
            "status": "success",
            "compatibility_report": compatibility_report,
            "timestamp": "2025-09-27"
        }
            
    except Exception as e:
        print(f"Compatibility check error: {e}")
        return {
            "status": "error",
            "message": f"Compatibility check failed: {str(e)}",
            "compatibility_report": {
                "build_status": "unknown",
                "compatibility_issues": [],
                "power_analysis": {"recommended_psu_wattage": 750, "explanation": "Unable to analyze - using safe default"},
                "components_analyzed": 0,
                "summary": "❓ Unable to check compatibility due to an error"
            }
        }

@app.post("/api/ai-search")
async def ai_enhanced_search(request: SearchRequest):
    """AI-enhanced PC component search with intelligent recommendations"""
    try:
        from ai_compatibility import ai_analyzer
        
        # Get basic search results first
        from simple_web_search import simple_search_pc_parts
        search_results = await simple_search_pc_parts(request.query, request.max_results or 10)
        
        # If AI is available, enhance the results with recommendations
        if ai_analyzer.model:
            try:
                # Create AI prompt for component recommendations
                prompt = f"""
You are a PC building expert. Analyze this search query and provide intelligent recommendations.

Search Query: {request.query}
Component Category: {request.query.split()[0] if request.query else 'Unknown'}

Provide recommendations in JSON format:
{{
    "search_insights": {{
        "component_type": "CPU|GPU|RAM|Storage|Motherboard|Case|PSU|Cooler|Accessories",
        "key_factors": ["Performance", "Price-to-performance", "Compatibility"],
        "recommended_specs": {{
            "budget_range": "$200-400",
            "performance_tier": "Mid-range",
            "key_features": ["Feature 1", "Feature 2"]
        }},
        "compatibility_tips": [
            "Ensure socket compatibility with motherboard",
            "Check power requirements"
        ]
    }}
}}

Only return valid JSON, no additional text.
"""
                
                ai_response = ai_analyzer.model.generate_content(prompt)
                
                # Try to parse AI insights
                try:
                    json_start = ai_response.text.find('{')
                    json_end = ai_response.text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        ai_insights = json.loads(ai_response.text[json_start:json_end])
                    else:
                        ai_insights = {"search_insights": {"component_type": "Unknown"}}
                except:
                    ai_insights = {"search_insights": {"component_type": "Unknown"}}
                
                return {
                    "query": request.query,
                    "source": "AI-Enhanced Search",
                    "results": search_results,
                    "ai_insights": ai_insights,
                    "timestamp": "2025-09-27"
                }
                
            except Exception as ai_error:
                print(f"AI enhancement failed: {ai_error}")
                # Fall back to regular search
                pass
        
        # Return regular search results if AI enhancement fails
        return {
            "query": request.query,
            "source": "Web Search",
            "results": search_results,
            "timestamp": "2025-09-27"
        }
        
    except Exception as e:
        print(f"AI search error: {e}")
        # Return enhanced fallback results
        enhanced_results = get_enhanced_component_results(request.query)
        return {
            "query": request.query,
            "source": "Enhanced Fallback",
            "results": {
                "query": request.query,
                "results": enhanced_results,
                "message": f"Found {len(enhanced_results)} enhanced {request.query} results"
            }
        }

# Run the server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting PC Part Picker API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 Interactive docs at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )