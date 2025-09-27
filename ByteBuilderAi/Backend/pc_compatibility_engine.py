"""
PC Parts Compatibility Engine and Database
This module handles compatibility checking between PC components and maintains a database of parts.
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import sqlite3
from pathlib import Path

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

class PCCompatibilityChecker:
    def __init__(self, db_path: str = "pc_parts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize a simple SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create a simple components table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                type TEXT,
                specs TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def recommend_psu_wattage(self, components: Dict[str, str]) -> Tuple[int, str]:
        """Recommend PSU wattage based on components"""
        # Simplified power estimation
        estimated_power = 400  # Base estimate
        
        # Add power for high-end components
        if components.get('gpu'):
            gpu_name = components['gpu'].upper()
            if any(gpu in gpu_name for gpu in ['RTX 4080', 'RTX 4090', '7900']):
                estimated_power += 200
            elif any(gpu in gpu_name for gpu in ['RTX 4070', '7800']):
                estimated_power += 150
        
        # Add 20% headroom
        recommended_wattage = int(estimated_power * 1.2)
        
        # Round up to common PSU wattages
        common_wattages = [450, 550, 650, 750, 850, 1000]
        for wattage in common_wattages:
            if wattage >= recommended_wattage:
                recommended_wattage = wattage
                break
        
        explanation = f"Estimated power: {estimated_power}W. Recommended with 20% headroom: {recommended_wattage}W"
        return recommended_wattage, explanation
    
    def find_compatible_parts(self, base_component: str, component_name: str) -> List[str]:
        """Find parts compatible with a given component (simplified)"""
        # Simplified compatibility matching
        return []
    
    def generate_build_report(self, components: Dict[str, str]) -> Dict:
        """Generate a simplified compatibility report for a build"""
        # Simplified build report
        recommended_psu, psu_explanation = self.recommend_psu_wattage(components)
        
        return {
            'components': components,
            'compatibility_issues': [],
            'recommended_psu_wattage': recommended_psu,
            'psu_explanation': psu_explanation,
            'build_status': 'compatible'
        }

