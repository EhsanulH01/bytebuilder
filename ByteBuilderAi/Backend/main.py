"""
PC Part Picker Backend API
FastAPI server that provides PC part recommendations, compatibility checking, and price analysis.
Integrates with Scout MCP server for AI-powered recommendations.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import sys
import os
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

# Initialize the compatibility checker
try:
    compatibility_checker = PCCompatibilityChecker()
except Exception as e:
    print(f"Warning: Could not initialize compatibility checker: {e}")
    compatibility_checker = None

# Pydantic models for request/response
class ComponentRequest(BaseModel):
    component_type: str
    requirements: Optional[Dict[str, Any]] = {}
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None

class BuildRequest(BaseModel):
    components: Dict[str, str]
    use_case: Optional[str] = "gaming"  # gaming, productivity, content_creation
    budget: Optional[int] = None

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    compare_prices: Optional[bool] = False

class RecommendationRequest(BaseModel):
    use_case: str  # gaming, productivity, content_creation, budget
    budget: int
    preferences: Optional[Dict[str, Any]] = {}

# Sample PC parts database (in production, this would be a real database)
SAMPLE_PARTS = {
    "cpu": [
        {"name": "Intel Core i7-13700K", "price": 425, "performance": 95, "socket": "LGA1700"},
        {"name": "AMD Ryzen 7 7700X", "price": 375, "performance": 90, "socket": "AM5"},
        {"name": "Intel Core i5-13600K", "price": 345, "performance": 85, "socket": "LGA1700"},
        {"name": "AMD Ryzen 5 7600X", "price": 300, "performance": 80, "socket": "AM5"},
    ],
    "gpu": [
        {"name": "RTX 4080", "price": 1200, "performance": 95, "vram": 16},
        {"name": "RTX 4070", "price": 650, "performance": 85, "vram": 12},
        {"name": "RX 7800 XT", "price": 550, "performance": 80, "vram": 16},
        {"name": "RTX 4060", "price": 400, "performance": 70, "vram": 8},
    ],
    "motherboard": [
        {"name": "ASUS ROG STRIX Z790-E", "price": 375, "socket": "LGA1700", "ram_type": "DDR5"},
        {"name": "MSI B650 TOMAHAWK", "price": 200, "socket": "AM5", "ram_type": "DDR5"},
    ]
}

class PCPartPickerAPI:
    def __init__(self):
        self.active_builds = {}  # Store user builds in memory (use database in production)
    
    async def call_scout_mcp(self, query: str) -> Dict[str, Any]:
        """
        Call Scout MCP server for AI recommendations
        In production, this would connect to the actual MCP server
        """
        # Simulated MCP response for now
        return {
            "response": f"AI recommendation for: {query}",
            "suggestions": [
                "Consider compatibility between components",
                "Check power supply requirements", 
                "Look for current pricing and availability"
            ],
            "confidence": 0.85
        }
    
    def filter_parts_by_budget(self, parts: List[Dict], budget_min: int = None, budget_max: int = None) -> List[Dict]:
        """Filter parts by budget range"""
        if not budget_min and not budget_max:
            return parts
        
        filtered = []
        for part in parts:
            price = part.get("price", 0)
            if budget_min and price < budget_min:
                continue
            if budget_max and price > budget_max:
                continue
            filtered.append(part)
        
        return filtered
    
    def recommend_parts_for_use_case(self, use_case: str, budget: int) -> Dict[str, Any]:
        """Recommend parts based on use case and budget"""
        recommendations = {
            "use_case": use_case,
            "budget": budget,
            "components": {},
            "explanation": ""
        }
        
        if use_case == "gaming":
            # Gaming builds prioritize GPU, then CPU
            gpu_budget = budget * 0.4  # 40% for GPU
            cpu_budget = budget * 0.2  # 20% for CPU
            
            # Find best GPU within budget
            gpus = [gpu for gpu in SAMPLE_PARTS["gpu"] if gpu["price"] <= gpu_budget]
            if gpus:
                recommendations["components"]["gpu"] = max(gpus, key=lambda x: x["performance"])
            
            # Find compatible CPU
            cpus = [cpu for cpu in SAMPLE_PARTS["cpu"] if cpu["price"] <= cpu_budget]
            if cpus:
                recommendations["components"]["cpu"] = max(cpus, key=lambda x: x["performance"])
                
            recommendations["explanation"] = "Gaming build focused on high GPU performance"
            
        elif use_case == "productivity":
            # Productivity builds prioritize CPU, then RAM
            cpu_budget = budget * 0.3  # 30% for CPU
            
            cpus = [cpu for cpu in SAMPLE_PARTS["cpu"] if cpu["price"] <= cpu_budget]
            if cpus:
                recommendations["components"]["cpu"] = max(cpus, key=lambda x: x["performance"])
                
            recommendations["explanation"] = "Productivity build focused on CPU performance"
            
        elif use_case == "budget":
            # Budget builds focus on value
            total_remaining = budget
            
            # Start with most affordable options
            for component_type in ["cpu", "gpu"]:
                if component_type in SAMPLE_PARTS:
                    affordable_parts = [part for part in SAMPLE_PARTS[component_type] 
                                      if part["price"] <= total_remaining * 0.4]
                    if affordable_parts:
                        best_value = max(affordable_parts, key=lambda x: x["performance"] / x["price"])
                        recommendations["components"][component_type] = best_value
                        total_remaining -= best_value["price"]
            
            recommendations["explanation"] = "Budget build focused on best price-to-performance ratio"
        
        return recommendations

# Initialize the API helper
api_helper = PCPartPickerAPI()

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "PC Part Picker API", 
        "version": "1.0.0",
        "endpoints": {
            "recommendations": "/recommend",
            "compatibility": "/compatibility/check",
            "search": "/search",
            "parts": "/parts/{component_type}"
        }
    }

@app.get("/parts/{component_type}")
async def get_parts(component_type: str, budget_min: int = None, budget_max: int = None):
    """Get available parts for a specific component type"""
    if component_type not in SAMPLE_PARTS:
        raise HTTPException(status_code=404, detail=f"Component type '{component_type}' not found")
    
    parts = SAMPLE_PARTS[component_type]
    filtered_parts = api_helper.filter_parts_by_budget(parts, budget_min, budget_max)
    
    return {
        "component_type": component_type,
        "count": len(filtered_parts),
        "parts": filtered_parts
    }

@app.post("/search")
async def search_parts(request: SearchRequest):
    """Search for PC parts using AI-powered web search"""
    try:
        # In production, this would call the web search MCP server
        # For now, simulate search results
        simulated_results = []
        query_lower = request.query.lower()
        
        for component_type, parts in SAMPLE_PARTS.items():
            for part in parts:
                if any(word in part["name"].lower() for word in query_lower.split()):
                    simulated_results.append({
                        "component_type": component_type,
                        "name": part["name"],
                        "price": part["price"],
                        "relevance_score": 0.8
                    })
        
        return {
            "query": request.query,
            "results_count": len(simulated_results),
            "results": simulated_results[:request.max_results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/mcp-search")
async def mcp_search_parts(request: SearchRequest):
    """Search for PC parts using MCP web search server"""
    try:
        # Try to import MCP search functions with multiple possible paths
        mcp_available = False
        search_pc_parts = None
        search_and_compare_prices = None
        
        # Add potential MCP paths to Python path
        potential_paths = [
            str(Path(__file__).parent.parent / "mcp-intro"),
            str(Path(__file__).parent / "mcp-intro"),
            str(Path(__file__).parent.parent.parent / "mcp-intro")
        ]
        
        for path in potential_paths:
            if path not in sys.path:
                sys.path.append(path)
        
        try:
            # Try different import paths
            try:
                from scout.my_mcp.local_servers.web_search import search_pc_parts, search_and_compare_prices
                mcp_available = True
            except ImportError:
                try:
                    from my_mcp.local_servers.web_search import search_pc_parts, search_and_compare_prices
                    mcp_available = True
                except ImportError:
                    try:
                        from local_servers.web_search import search_pc_parts, search_and_compare_prices
                        mcp_available = True
                    except ImportError:
                        mcp_available = False
            
            if mcp_available:
                # Use MCP search for real web results
                if hasattr(request, 'compare_prices') and request.compare_prices:
                    results_json = await search_and_compare_prices(request.query, request.max_results or 5)
                else:
                    results_json = await search_pc_parts(request.query, request.max_results or 10)
                
                import json
                results_data = json.loads(results_json)
                
                return {
                    "query": request.query,
                    "source": "MCP Web Search",
                    "results": results_data,
                    "timestamp": "2025-09-26T12:00:00Z"
                }
            else:
                raise ImportError("MCP modules not found")
                
        except ImportError as e:
            # Fallback to simulated results if MCP is not available
            print(f"MCP import failed: {e}")
            return {
                "query": request.query,
                "source": "Fallback - MCP unavailable",
                "error": f"MCP server not available: {str(e)}",
                "results": {
                    "query": request.query,
                    "results": [],
                    "message": "MCP web search server is not available. Please check if the MCP server is installed and running."
                }
            }
            
    except Exception as e:
        print(f"MCP search error: {e}")
        raise HTTPException(status_code=500, detail=f"MCP search failed: {str(e)}")

@app.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    """Get AI-powered PC build recommendations"""
    try:
        # Get base recommendations
        recommendations = api_helper.recommend_parts_for_use_case(request.use_case, request.budget)
        
        # Get AI insights from Scout MCP (simulated for now)
        ai_response = await api_helper.call_scout_mcp(
            f"Recommend PC build for {request.use_case} with ${request.budget} budget"
        )
        
        return {
            "recommendations": recommendations,
            "ai_insights": ai_response,
            "timestamp": "2025-09-26T12:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

@app.post("/compatibility/check")
async def check_compatibility(request: BuildRequest):
    """Check compatibility between selected components"""
    try:
        if not compatibility_checker:
            return {"error": "Compatibility checker not available"}
        
        # Generate compatibility report
        report = compatibility_checker.generate_build_report(request.components)
        
        return {
            "build": request.components,
            "compatibility_report": report,
            "use_case": request.use_case,
            "timestamp": "2025-09-26T12:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compatibility check failed: {str(e)}")

@app.get("/compatibility/suggestions/{component_type}/{component_name}")
async def get_compatible_parts(component_type: str, component_name: str):
    """Get parts compatible with a specific component"""
    try:
        if not compatibility_checker:
            return {"error": "Compatibility checker not available"}
        
        compatible_parts = compatibility_checker.find_compatible_parts(component_type, component_name)
        
        return {
            "base_component": {
                "type": component_type,
                "name": component_name
            },
            "compatible_parts": compatible_parts,
            "count": len(compatible_parts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find compatible parts: {str(e)}")

@app.post("/builds/save")
async def save_build(request: BuildRequest):
    """Save a PC build configuration"""
    try:
        build_id = f"build_{len(api_helper.active_builds) + 1}"
        
        build_data = {
            "id": build_id,
            "components": request.components,
            "use_case": request.use_case,
            "budget": request.budget,
            "created_at": "2025-09-26T12:00:00Z"
        }
        
        api_helper.active_builds[build_id] = build_data
        
        return {
            "build_id": build_id,
            "message": "Build saved successfully",
            "build": build_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save build: {str(e)}")

@app.get("/builds/{build_id}")
async def get_build(build_id: str):
    """Retrieve a saved build"""
    if build_id not in api_helper.active_builds:
        raise HTTPException(status_code=404, detail="Build not found")
    
    return api_helper.active_builds[build_id]

@app.get("/builds")
async def list_builds():
    """List all saved builds"""
    return {
        "builds": list(api_helper.active_builds.values()),
        "count": len(api_helper.active_builds)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "compatibility_checker": "available" if compatibility_checker else "unavailable",
        "timestamp": "2025-09-26T12:00:00Z"
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