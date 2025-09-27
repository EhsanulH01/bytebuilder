"""
AI-powered PC compatibility analysis using Gemini
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import json

# Add the mcp-intro directory to path for environment loading
sys.path.append(str(Path(__file__).parent.parent / "mcp-intro"))

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    # Load environment variables from the mcp-intro directory
    env_path = Path(__file__).parent.parent / "mcp-intro" / ".env"
    load_dotenv(env_path)
    
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AICompatibilityAnalyzer:
    def __init__(self):
        self.model = None
        if GEMINI_AVAILABLE:
            self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini AI model"""
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key.strip():
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini AI initialized for compatibility analysis")
            else:
                print("⚠️ GOOGLE_API_KEY not found, using fallback compatibility logic")
        except Exception as e:
            print(f"⚠️ Failed to initialize Gemini: {e}")
            self.model = None
    
    async def analyze_compatibility(self, components: Dict) -> Dict:
        """
        Analyze PC component compatibility using AI
        
        Args:
            components: Dictionary of selected components
            
        Returns:
            Compatibility analysis report
        """
        if not self.model:
            return self._fallback_analysis(components)
        
        try:
            # Prepare component data for AI analysis
            component_specs = self._extract_component_specs(components)
            
            prompt = self._build_compatibility_prompt(component_specs)
            
            # Get AI analysis
            response = self.model.generate_content(prompt)
            
            # Parse AI response into structured format
            return self._parse_ai_response(response.text, components)
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_analysis(components)
    
    def _extract_component_specs(self, components: Dict) -> str:
        """Extract key specifications from components for AI analysis"""
        specs_text = "PC Build Components:\n"
        
        for category, component in components.items():
            if component:
                specs_text += f"\n{category.upper()}:\n"
                specs_text += f"  - Name: {component.get('name', 'Unknown')}\n"
                specs_text += f"  - Price: {component.get('price', 'Unknown')}\n"
                
                # Extract specs from snippet or other fields
                snippet = component.get('snippet', '')
                specs = component.get('specs', '')
                
                if snippet:
                    specs_text += f"  - Description: {snippet}\n"
                if specs:
                    specs_text += f"  - Specifications: {specs}\n"
        
        return specs_text
    
    def _build_compatibility_prompt(self, component_specs: str) -> str:
        """Build a detailed prompt for AI compatibility analysis"""
        return f"""
You are a PC building expert. Analyze the compatibility of these components and provide a detailed assessment.

{component_specs}

Please analyze:
1. CPU and Motherboard socket compatibility
2. RAM compatibility with motherboard and CPU
3. GPU power requirements and PSU capacity
4. Case size and component fitment
5. Cooling requirements
6. Power consumption vs PSU wattage
7. Any other potential compatibility issues

Provide your response in this JSON format:
{{
    "build_status": "compatible|warning|incompatible",
    "overall_score": 85,
    "compatibility_issues": [
        {{
            "severity": "error|warning|info",
            "component1": "CPU",
            "component2": "Motherboard", 
            "issue": "Socket mismatch",
            "suggestion": "Choose LGA1700 motherboard for Intel 13th gen CPU",
            "category": "socket_compatibility"
        }}
    ],
    "power_analysis": {{
        "estimated_consumption": 650,
        "recommended_psu_wattage": 750,
        "explanation": "System draws ~650W under load, 750W PSU provides good headroom"
    }},
    "summary": "✅ Build is compatible with minor recommendations",
    "recommendations": [
        "Consider upgrading to 850W PSU for future GPU upgrades",
        "Ensure case has adequate airflow for high-end components"
    ]
}}

Only return valid JSON, no additional text.
"""
    
    def _parse_ai_response(self, response_text: str, components: Dict) -> Dict:
        """Parse AI response and structure it properly"""
        try:
            # Try to extract JSON from the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                parsed = json.loads(json_text)
                
                # Ensure all required fields are present
                parsed.setdefault('build_status', 'unknown')
                parsed.setdefault('compatibility_issues', [])
                parsed.setdefault('power_analysis', {})
                parsed.setdefault('summary', 'AI analysis completed')
                parsed.setdefault('components_analyzed', len(components))
                
                return parsed
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            print(f"Failed to parse AI response: {e}")
            return self._fallback_analysis(components)
    
    def _fallback_analysis(self, components: Dict) -> Dict:
        """Fallback compatibility analysis when AI is not available"""
        issues = []
        total_power = 0
        
        # Basic compatibility checks
        if 'CPU' in components and 'Motherboard' in components:
            issues.append({
                "severity": "info",
                "component1": "CPU",
                "component2": "Motherboard",
                "issue": "Unable to verify socket compatibility",
                "suggestion": "Please verify CPU socket matches motherboard",
                "category": "socket_compatibility"
            })
        
        # Estimate power consumption
        for category, component in components.items():
            if category == 'CPU':
                total_power += 150  # Estimate
            elif category == 'GPU':
                total_power += 300  # Estimate
            elif category == 'RAM':
                total_power += 50   # Estimate
            else:
                total_power += 25   # Other components
        
        recommended_psu = max(total_power * 1.3, 650)  # 30% headroom
        
        return {
            "build_status": "warning" if issues else "compatible",
            "compatibility_issues": issues,
            "power_analysis": {
                "estimated_consumption": total_power,
                "recommended_psu_wattage": int(recommended_psu),
                "explanation": f"Estimated power draw: {total_power}W, recommended PSU: {int(recommended_psu)}W"
            },
            "summary": f"⚠️ Basic analysis complete - please verify compatibility manually",
            "components_analyzed": len(components)
        }

# Global instance
ai_analyzer = AICompatibilityAnalyzer()
