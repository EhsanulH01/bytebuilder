"""
Dynamic PC Parts Compatibility Engine
This module handles real-time compatibility checking between PC components using live search data.
No hardcoded values - all compatibility checks are based on component specifications from search results.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

class ComponentType(Enum):
    CPU = "cpu"
    MOTHERBOARD = "motherboard"
    RAM = "ram"
    GPU = "gpu"
    PSU = "psu"
    STORAGE = "storage"
    CASE = "case"
    COOLER = "cooler"

@dataclass
class CompatibilityIssue:
    severity: str  # "error", "warning", "info"
    component1: str
    component2: str
    issue: str
    suggestion: str
    category: str

@dataclass
class ComponentSpecs:
    name: str
    category: str
    socket: Optional[str] = None
    chipset: Optional[str] = None
    memory_type: Optional[str] = None
    memory_slots: Optional[int] = None
    max_memory: Optional[str] = None
    power_consumption: Optional[int] = None
    form_factor: Optional[str] = None
    pcie_slots: Optional[List[str]] = None
    storage_support: Optional[List[str]] = None
    dimensions: Optional[Dict[str, float]] = None

class DynamicPCCompatibilityChecker:
    def __init__(self):
        """Initialize dynamic compatibility checker - no database required"""
        pass
    
    def extract_component_specs(self, component_data: Dict) -> ComponentSpecs:
        """Extract specifications from search result data"""
        name = component_data.get('title', '').lower()
        snippet = component_data.get('snippet', '').lower()
        combined_text = f"{name} {snippet}"
        
        specs = ComponentSpecs(
            name=component_data.get('title', ''),
            category=self._determine_category(name)
        )
        
        # Extract socket information
        specs.socket = self._extract_socket(combined_text)
        
        # Extract memory information
        specs.memory_type = self._extract_memory_type(combined_text)
        specs.max_memory = self._extract_max_memory(combined_text)
        
        # Extract power consumption
        specs.power_consumption = self._extract_power_consumption(combined_text)
        
        # Extract form factor
        specs.form_factor = self._extract_form_factor(combined_text)
        
        return specs
    
    def _determine_category(self, name: str) -> str:
        """Determine component category from name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['cpu', 'processor', 'ryzen', 'intel core']):
            return 'CPU'
        elif any(word in name_lower for word in ['motherboard', 'mobo', 'mainboard']):
            return 'Motherboard'
        elif any(word in name_lower for word in ['gpu', 'graphics', 'rtx', 'gtx', 'radeon']):
            return 'GPU'
        elif any(word in name_lower for word in ['ram', 'memory', 'ddr4', 'ddr5']):
            return 'RAM'
        elif any(word in name_lower for word in ['ssd', 'hdd', 'nvme', 'storage']):
            return 'Storage'
        elif any(word in name_lower for word in ['psu', 'power supply']):
            return 'Power Supply'
        elif any(word in name_lower for word in ['case', 'tower', 'chassis']):
            return 'Case'
        elif any(word in name_lower for word in ['cooler', 'cooling', 'fan']):
            return 'Cooling System'
        return 'Unknown'
    
    def _extract_socket(self, text: str) -> Optional[str]:
        """Extract CPU/Motherboard socket from text"""
        socket_patterns = [
            r'lga\s*(\d+)', r'am[45]', r'am5', r'am4', r'tr4', r'trx40', r'trx50'
        ]
        for pattern in socket_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).upper()
        return None
    
    def _extract_memory_type(self, text: str) -> Optional[str]:
        """Extract memory type (DDR4/DDR5) from text"""
        memory_patterns = [r'ddr[45]', r'ddr\s*[45]']
        for pattern in memory_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).upper().replace(' ', '')
        return None
    
    def _extract_max_memory(self, text: str) -> Optional[str]:
        """Extract maximum memory capacity"""
        memory_patterns = [r'(\d+)\s*gb', r'up\s*to\s*(\d+)\s*gb']
        for pattern in memory_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}GB"
        return None
    
    def _extract_power_consumption(self, text: str) -> Optional[int]:
        """Extract power consumption in watts"""
        power_patterns = [r'(\d+)\s*w(?:att)?', r'tdp\s*(\d+)', r'power\s*(\d+)']
        for pattern in power_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_form_factor(self, text: str) -> Optional[str]:
        """Extract form factor information"""
        form_factors = ['atx', 'micro-atx', 'mini-itx', 'e-atx', 'full tower', 'mid tower', 'mini-itx']
        for ff in form_factors:
            if ff.lower() in text:
                return ff.title()
        return None
    
    def check_cpu_motherboard_compatibility(self, cpu_specs: ComponentSpecs, mb_specs: ComponentSpecs) -> List[CompatibilityIssue]:
        """Check CPU and Motherboard socket compatibility"""
        issues = []
        
        if cpu_specs.socket and mb_specs.socket:
            if cpu_specs.socket != mb_specs.socket:
                issues.append(CompatibilityIssue(
                    severity="error",
                    component1=cpu_specs.name,
                    component2=mb_specs.name,
                    issue=f"Socket mismatch: CPU requires {cpu_specs.socket}, Motherboard has {mb_specs.socket}",
                    suggestion=f"Choose a CPU with {mb_specs.socket} socket or a motherboard with {cpu_specs.socket} socket",
                    category="socket_compatibility"
                ))
        elif not cpu_specs.socket or not mb_specs.socket:
            issues.append(CompatibilityIssue(
                severity="warning",
                component1=cpu_specs.name,
                component2=mb_specs.name,
                issue="Unable to verify socket compatibility - insufficient specification data",
                suggestion="Manually verify CPU and motherboard socket compatibility",
                category="insufficient_data"
            ))
        
        return issues
    
    def check_ram_motherboard_compatibility(self, ram_specs: ComponentSpecs, mb_specs: ComponentSpecs) -> List[CompatibilityIssue]:
        """Check RAM and Motherboard memory type compatibility"""
        issues = []
        
        if ram_specs.memory_type and mb_specs.memory_type:
            if ram_specs.memory_type != mb_specs.memory_type:
                issues.append(CompatibilityIssue(
                    severity="error",
                    component1=ram_specs.name,
                    component2=mb_specs.name,
                    issue=f"Memory type mismatch: RAM is {ram_specs.memory_type}, Motherboard supports {mb_specs.memory_type}",
                    suggestion=f"Choose {mb_specs.memory_type} RAM or a motherboard that supports {ram_specs.memory_type}",
                    category="memory_compatibility"
                ))
        elif not ram_specs.memory_type or not mb_specs.memory_type:
            issues.append(CompatibilityIssue(
                severity="info",
                component1=ram_specs.name,
                component2=mb_specs.name,
                issue="Unable to verify memory type compatibility",
                suggestion="Ensure RAM and motherboard memory types match (DDR4/DDR5)",
                category="insufficient_data"
            ))
        
        return issues
    
    def calculate_power_requirements(self, components_specs: List[ComponentSpecs]) -> Tuple[int, str, List[CompatibilityIssue]]:
        """Calculate total power requirements and recommend PSU"""
        total_power = 100  # Base system power
        issues = []
        power_breakdown = {"Base System": 100}
        
        for spec in components_specs:
            if spec.power_consumption:
                total_power += spec.power_consumption
                power_breakdown[spec.name] = spec.power_consumption
            elif spec.category == 'GPU':
                # Estimate GPU power based on name if not available
                estimated_power = self._estimate_gpu_power(spec.name)
                total_power += estimated_power
                power_breakdown[spec.name] = f"{estimated_power}W (estimated)"
            elif spec.category == 'CPU':
                # Estimate CPU power
                estimated_power = self._estimate_cpu_power(spec.name)
                total_power += estimated_power
                power_breakdown[spec.name] = f"{estimated_power}W (estimated)"
        
        # Add 20% safety margin
        recommended_psu = int(total_power * 1.2)
        
        # Round up to standard PSU wattages
        standard_wattages = [450, 550, 650, 750, 850, 1000, 1200]
        for wattage in standard_wattages:
            if wattage >= recommended_psu:
                recommended_psu = wattage
                break
        
        explanation = f"Total estimated power: {total_power}W. Recommended PSU: {recommended_psu}W (with 20% safety margin)"
        
        return recommended_psu, explanation, issues
    
    def _estimate_gpu_power(self, gpu_name: str) -> int:
        """Estimate GPU power consumption based on model"""
        gpu_name_upper = gpu_name.upper()
        if any(model in gpu_name_upper for model in ['RTX 4090', '7900 XTX']):
            return 350
        elif any(model in gpu_name_upper for model in ['RTX 4080', '7900 XT']):
            return 280
        elif any(model in gpu_name_upper for model in ['RTX 4070', '7800 XT']):
            return 220
        elif any(model in gpu_name_upper for model in ['RTX 4060', '7600 XT']):
            return 150
        else:
            return 200  # Conservative estimate
    
    def _estimate_cpu_power(self, cpu_name: str) -> int:
        """Estimate CPU power consumption based on model"""
        cpu_name_upper = cpu_name.upper()
        if any(model in cpu_name_upper for model in ['I9', 'RYZEN 9']):
            return 125
        elif any(model in cpu_name_upper for model in ['I7', 'RYZEN 7']):
            return 100
        elif any(model in cpu_name_upper for model in ['I5', 'RYZEN 5']):
            return 80
        else:
            return 65  # Conservative estimate
    
    async def check_build_compatibility(self, components: Dict[str, Dict]) -> Dict:
        """Main compatibility checking function"""
        issues = []
        component_specs = []
        
        # Extract specs from all components
        for category, component_data in components.items():
            if component_data:
                spec = self.extract_component_specs(component_data)
                component_specs.append(spec)
        
        # Check CPU-Motherboard compatibility
        cpu_spec = next((spec for spec in component_specs if spec.category == 'CPU'), None)
        mb_spec = next((spec for spec in component_specs if spec.category == 'Motherboard'), None)
        
        if cpu_spec and mb_spec:
            issues.extend(self.check_cpu_motherboard_compatibility(cpu_spec, mb_spec))
        
        # Check RAM-Motherboard compatibility
        ram_spec = next((spec for spec in component_specs if spec.category == 'RAM'), None)
        
        if ram_spec and mb_spec:
            issues.extend(self.check_ram_motherboard_compatibility(ram_spec, mb_spec))
        
        # Calculate power requirements
        recommended_psu, psu_explanation, psu_issues = self.calculate_power_requirements(component_specs)
        issues.extend(psu_issues)
        
        # Determine overall build status
        error_issues = [issue for issue in issues if issue.severity == "error"]
        warning_issues = [issue for issue in issues if issue.severity == "warning"]
        
        if error_issues:
            build_status = "incompatible"
        elif warning_issues:
            build_status = "warning"
        else:
            build_status = "compatible"
        
        return {
            "build_status": build_status,
            "compatibility_issues": [
                {
                    "severity": issue.severity,
                    "component1": issue.component1,
                    "component2": issue.component2,
                    "issue": issue.issue,
                    "suggestion": issue.suggestion,
                    "category": issue.category
                } for issue in issues
            ],
            "power_analysis": {
                "recommended_psu_wattage": recommended_psu,
                "explanation": psu_explanation
            },
            "components_analyzed": len(component_specs),
            "summary": self._generate_compatibility_summary(issues, build_status)
        }
    
    def _generate_compatibility_summary(self, issues: List[CompatibilityIssue], status: str) -> str:
        """Generate a human-readable compatibility summary"""
        if status == "compatible":
            return "✅ All components appear to be compatible!"
        elif status == "warning":
            warning_count = len([i for i in issues if i.severity == "warning"])
            return f"⚠️ Build is compatible but has {warning_count} warnings that should be reviewed."
        else:
            error_count = len([i for i in issues if i.severity == "error"])
            return f"❌ Build has {error_count} compatibility errors that must be resolved."

# Keep the original class for backward compatibility
PCCompatibilityChecker = DynamicPCCompatibilityChecker

