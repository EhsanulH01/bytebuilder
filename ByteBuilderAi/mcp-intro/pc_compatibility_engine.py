"""
PC Parts Compatibility Engine and Database
This module handles compatibility checking between PC components and maintains a database of parts.
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
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

class Socket(Enum):
    # Intel Sockets
    LGA1700 = "LGA1700"
    LGA1200 = "LGA1200"
    LGA2066 = "LGA2066"
    
    # AMD Sockets
    AM5 = "AM5"
    AM4 = "AM4"
    sTRX4 = "sTRX4"
    TRX40 = "TRX40"

class FormFactor(Enum):
    ATX = "ATX"
    MICRO_ATX = "mATX"
    MINI_ITX = "mITX"
    EXTENDED_ATX = "E-ATX"

class RAMType(Enum):
    DDR4 = "DDR4"
    DDR5 = "DDR5"

@dataclass
class CPUSpec:
    name: str
    brand: str  # Intel/AMD
    socket: Socket
    cores: int
    threads: int
    base_clock: float
    boost_clock: float
    tdp: int
    price_range: Tuple[int, int]  # (min, max) in USD
    integrated_graphics: bool = False

@dataclass
class MotherboardSpec:
    name: str
    brand: str
    socket: Socket
    chipset: str
    form_factor: FormFactor
    ram_type: RAMType
    ram_slots: int
    max_ram: int  # in GB
    pcie_slots: Dict[str, int]  # e.g., {"x16": 2, "x8": 1, "x1": 3}
    m2_slots: int
    sata_ports: int
    price_range: Tuple[int, int]
    wifi: bool = False
    bluetooth: bool = False

@dataclass
class RAMSpec:
    name: str
    brand: str
    type: RAMType
    capacity: int  # per stick in GB
    speed: int  # MHz
    cas_latency: int
    voltage: float
    kit_size: int  # number of sticks
    price_range: Tuple[int, int]

@dataclass
class GPUSpec:
    name: str
    brand: str
    chipset: str  # e.g., RTX 4080, RX 7800 XT
    vram: int  # in GB
    memory_type: str  # GDDR6, GDDR6X
    power_consumption: int  # TDP in watts
    length: int  # mm
    width: int  # slots (2, 2.5, 3)
    height: int  # mm
    connectors: List[str]  # e.g., ["8-pin", "8-pin"]
    price_range: Tuple[int, int]

@dataclass
class PSUSpec:
    name: str
    brand: str
    wattage: int
    efficiency: str  # 80+ Bronze, Gold, etc.
    modular: str  # Full, Semi, Non
    form_factor: str  # ATX, SFX
    connectors: Dict[str, int]  # e.g., {"PCIe 8-pin": 4, "CPU 8-pin": 2}
    price_range: Tuple[int, int]

@dataclass
class CaseSpec:
    name: str
    brand: str
    form_factor: List[FormFactor]  # Supported motherboard sizes
    max_gpu_length: int  # mm
    max_cpu_cooler_height: int  # mm
    drive_bays: Dict[str, int]  # e.g., {"2.5\"": 4, "3.5\"": 2}
    expansion_slots: int
    price_range: Tuple[int, int]

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
        self.load_sample_data()
    
    def init_database(self):
        """Initialize the SQLite database for PC parts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        tables = {
            'cpus': '''
                CREATE TABLE IF NOT EXISTS cpus (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    brand TEXT,
                    socket TEXT,
                    cores INTEGER,
                    threads INTEGER,
                    base_clock REAL,
                    boost_clock REAL,
                    tdp INTEGER,
                    min_price INTEGER,
                    max_price INTEGER,
                    integrated_graphics BOOLEAN
                )
            ''',
            'motherboards': '''
                CREATE TABLE IF NOT EXISTS motherboards (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    brand TEXT,
                    socket TEXT,
                    chipset TEXT,
                    form_factor TEXT,
                    ram_type TEXT,
                    ram_slots INTEGER,
                    max_ram INTEGER,
                    pcie_slots TEXT,
                    m2_slots INTEGER,
                    sata_ports INTEGER,
                    min_price INTEGER,
                    max_price INTEGER,
                    wifi BOOLEAN,
                    bluetooth BOOLEAN
                )
            ''',
            'ram': '''
                CREATE TABLE IF NOT EXISTS ram (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    brand TEXT,
                    type TEXT,
                    capacity INTEGER,
                    speed INTEGER,
                    cas_latency INTEGER,
                    voltage REAL,
                    kit_size INTEGER,
                    min_price INTEGER,
                    max_price INTEGER
                )
            ''',
            'gpus': '''
                CREATE TABLE IF NOT EXISTS gpus (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    brand TEXT,
                    chipset TEXT,
                    vram INTEGER,
                    memory_type TEXT,
                    power_consumption INTEGER,
                    length INTEGER,
                    width INTEGER,
                    height INTEGER,
                    connectors TEXT,
                    min_price INTEGER,
                    max_price INTEGER
                )
            '''
        }
        
        for table_sql in tables.values():
            cursor.execute(table_sql)
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """Load sample PC parts data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sample CPUs
        cpus = [
            CPUSpec("Intel Core i7-13700K", "Intel", Socket.LGA1700, 16, 24, 3.4, 5.4, 125, (400, 450)),
            CPUSpec("Intel Core i5-13600K", "Intel", Socket.LGA1700, 14, 20, 3.5, 5.1, 125, (320, 370)),
            CPUSpec("AMD Ryzen 7 7700X", "AMD", Socket.AM5, 8, 16, 4.5, 5.4, 105, (350, 400)),
            CPUSpec("AMD Ryzen 5 7600X", "AMD", Socket.AM5, 6, 12, 4.7, 5.3, 105, (280, 320)),
        ]
        
        for cpu in cpus:
            cursor.execute('''
                INSERT OR REPLACE INTO cpus 
                (name, brand, socket, cores, threads, base_clock, boost_clock, tdp, min_price, max_price, integrated_graphics)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cpu.name, cpu.brand, cpu.socket.value, cpu.cores, cpu.threads, 
                  cpu.base_clock, cpu.boost_clock, cpu.tdp, cpu.price_range[0], cpu.price_range[1], cpu.integrated_graphics))
        
        # Sample Motherboards
        motherboards = [
            MotherboardSpec("ASUS ROG STRIX Z790-E", "ASUS", Socket.LGA1700, "Z790", FormFactor.ATX, 
                          RAMType.DDR5, 4, 128, {"x16": 2, "x8": 1, "x1": 3}, 4, 6, (350, 400)),
            MotherboardSpec("MSI B650 TOMAHAWK", "MSI", Socket.AM5, "B650", FormFactor.ATX,
                          RAMType.DDR5, 4, 128, {"x16": 1, "x8": 1, "x1": 2}, 2, 6, (180, 220)),
        ]
        
        for mb in motherboards:
            cursor.execute('''
                INSERT OR REPLACE INTO motherboards
                (name, brand, socket, chipset, form_factor, ram_type, ram_slots, max_ram, pcie_slots, m2_slots, sata_ports, min_price, max_price, wifi, bluetooth)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (mb.name, mb.brand, mb.socket.value, mb.chipset, mb.form_factor.value,
                  mb.ram_type.value, mb.ram_slots, mb.max_ram, json.dumps(mb.pcie_slots),
                  mb.m2_slots, mb.sata_ports, mb.price_range[0], mb.price_range[1], mb.wifi, mb.bluetooth))
        
        # Sample RAM
        ram_kits = [
            RAMSpec("Corsair Vengeance DDR5-5600 32GB", "Corsair", RAMType.DDR5, 16, 5600, 36, 1.25, 2, (180, 220)),
            RAMSpec("G.SKILL Trident Z5 DDR5-6000 32GB", "G.SKILL", RAMType.DDR5, 16, 6000, 30, 1.35, 2, (250, 300)),
        ]
        
        for ram in ram_kits:
            cursor.execute('''
                INSERT OR REPLACE INTO ram
                (name, brand, type, capacity, speed, cas_latency, voltage, kit_size, min_price, max_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ram.name, ram.brand, ram.type.value, ram.capacity, ram.speed,
                  ram.cas_latency, ram.voltage, ram.kit_size, ram.price_range[0], ram.price_range[1]))
        
        # Sample GPUs
        gpus = [
            GPUSpec("RTX 4080", "NVIDIA", "RTX 4080", 16, "GDDR6X", 320, 310, 3, 137, ["8-pin", "8-pin"], (1100, 1300)),
            GPUSpec("RTX 4070", "NVIDIA", "RTX 4070", 12, "GDDR6X", 200, 260, 2, 112, ["8-pin"], (600, 700)),
            GPUSpec("RX 7800 XT", "AMD", "RX 7800 XT", 16, "GDDR6", 263, 267, 2, 110, ["8-pin", "6-pin"], (500, 600)),
        ]
        
        for gpu in gpus:
            cursor.execute('''
                INSERT OR REPLACE INTO gpus
                (name, brand, chipset, vram, memory_type, power_consumption, length, width, height, connectors, min_price, max_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (gpu.name, gpu.brand, gpu.chipset, gpu.vram, gpu.memory_type,
                  gpu.power_consumption, gpu.length, gpu.width, gpu.height,
                  json.dumps(gpu.connectors), gpu.price_range[0], gpu.price_range[1]))
        
        conn.commit()
        conn.close()
    
    def check_cpu_motherboard_compatibility(self, cpu_name: str, mb_name: str) -> List[CompatibilityIssue]:
        """Check CPU and motherboard compatibility"""
        issues = []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get CPU and motherboard details
        cpu = cursor.execute('SELECT * FROM cpus WHERE name = ?', (cpu_name,)).fetchone()
        mb = cursor.execute('SELECT * FROM motherboards WHERE name = ?', (mb_name,)).fetchone()
        
        if not cpu or not mb:
            issues.append(CompatibilityIssue("error", cpu_name, mb_name, 
                                            "Component not found in database", 
                                            "Please check component names"))
            return issues
        
        # Check socket compatibility
        cpu_socket = cpu[3]  # socket column
        mb_socket = mb[3]    # socket column
        
        if cpu_socket != mb_socket:
            issues.append(CompatibilityIssue("error", cpu_name, mb_name,
                                            f"Socket mismatch: CPU uses {cpu_socket}, motherboard uses {mb_socket}",
                                            f"Find a motherboard with {cpu_socket} socket or a CPU with {mb_socket} socket"))
        
        conn.close()
        return issues
    
    def check_ram_motherboard_compatibility(self, ram_name: str, mb_name: str) -> List[CompatibilityIssue]:
        """Check RAM and motherboard compatibility"""
        issues = []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        ram = cursor.execute('SELECT * FROM ram WHERE name = ?', (ram_name,)).fetchone()
        mb = cursor.execute('SELECT * FROM motherboards WHERE name = ?', (mb_name,)).fetchone()
        
        if not ram or not mb:
            issues.append(CompatibilityIssue("error", ram_name, mb_name,
                                            "Component not found in database",
                                            "Please check component names"))
            return issues
        
        # Check RAM type compatibility
        ram_type = ram[3]  # type column
        mb_ram_type = mb[6]  # ram_type column
        
        if ram_type != mb_ram_type:
            issues.append(CompatibilityIssue("error", ram_name, mb_name,
                                            f"RAM type mismatch: RAM is {ram_type}, motherboard supports {mb_ram_type}",
                                            f"Get {mb_ram_type} RAM or a motherboard that supports {ram_type}"))
        
        # Check capacity limits
        ram_capacity = ram[4] * ram[8]  # capacity * kit_size
        mb_max_ram = mb[8]  # max_ram column
        
        if ram_capacity > mb_max_ram:
            issues.append(CompatibilityIssue("warning", ram_name, mb_name,
                                            f"RAM capacity ({ram_capacity}GB) exceeds motherboard limit ({mb_max_ram}GB)",
                                            f"Consider RAM with total capacity ≤ {mb_max_ram}GB"))
        
        conn.close()
        return issues
    
    def estimate_power_requirements(self, components: Dict[str, str]) -> Dict[str, int]:
        """Estimate total power requirements for a build"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        power_breakdown = {
            'cpu': 0,
            'gpu': 0,
            'ram': 10,  # Estimate per stick
            'motherboard': 50,
            'storage': 20,  # Estimate
            'fans': 30,  # Estimate
            'total': 0
        }
        
        # Get CPU power consumption
        if 'cpu' in components:
            cpu = cursor.execute('SELECT tdp FROM cpus WHERE name = ?', (components['cpu'],)).fetchone()
            if cpu:
                power_breakdown['cpu'] = cpu[0]
        
        # Get GPU power consumption
        if 'gpu' in components:
            gpu = cursor.execute('SELECT power_consumption FROM gpus WHERE name = ?', (components['gpu'],)).fetchone()
            if gpu:
                power_breakdown['gpu'] = gpu[0]
        
        # Calculate total
        power_breakdown['total'] = sum(power_breakdown.values()) - power_breakdown['total']  # Remove the old total
        
        conn.close()
        return power_breakdown
    
    def recommend_psu_wattage(self, components: Dict[str, str]) -> Tuple[int, str]:
        """Recommend PSU wattage based on components"""
        power_req = self.estimate_power_requirements(components)
        total_power = power_req['total']
        
        # Add 20% headroom for efficiency and future upgrades
        recommended_wattage = int(total_power * 1.2)
        
        # Round up to common PSU wattages
        common_wattages = [450, 550, 650, 750, 850, 1000, 1200]
        for wattage in common_wattages:
            if wattage >= recommended_wattage:
                recommended_wattage = wattage
                break
        
        explanation = f"Total estimated power: {total_power}W. Recommended with 20% headroom: {recommended_wattage}W"
        
        return recommended_wattage, explanation
    
    def find_compatible_parts(self, base_component: str, component_name: str) -> List[str]:
        """Find parts compatible with a given component"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        compatible = []
        
        if base_component == "cpu":
            # Find compatible motherboards
            cpu = cursor.execute('SELECT socket FROM cpus WHERE name = ?', (component_name,)).fetchone()
            if cpu:
                motherboards = cursor.execute('SELECT name FROM motherboards WHERE socket = ?', (cpu[0],)).fetchall()
                compatible = [mb[0] for mb in motherboards]
        
        elif base_component == "motherboard":
            # Find compatible CPUs and RAM
            mb = cursor.execute('SELECT socket, ram_type FROM motherboards WHERE name = ?', (component_name,)).fetchone()
            if mb:
                cpus = cursor.execute('SELECT name FROM cpus WHERE socket = ?', (mb[0],)).fetchall()
                ram = cursor.execute('SELECT name FROM ram WHERE type = ?', (mb[1],)).fetchall()
                compatible = [cpu[0] for cpu in cpus] + [r[0] for r in ram]
        
        conn.close()
        return compatible
    
    def generate_build_report(self, components: Dict[str, str]) -> Dict:
        """Generate a comprehensive compatibility report for a build"""
        all_issues = []
        
        # Check CPU-Motherboard compatibility
        if 'cpu' in components and 'motherboard' in components:
            all_issues.extend(self.check_cpu_motherboard_compatibility(components['cpu'], components['motherboard']))
        
        # Check RAM-Motherboard compatibility
        if 'ram' in components and 'motherboard' in components:
            all_issues.extend(self.check_ram_motherboard_compatibility(components['ram'], components['motherboard']))
        
        # Get power requirements
        power_info = self.estimate_power_requirements(components)
        recommended_psu, psu_explanation = self.recommend_psu_wattage(components)
        
        # Calculate estimated total cost
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        total_cost_min = 0
        total_cost_max = 0
        cost_breakdown = {}
        
        for comp_type, comp_name in components.items():
            table_map = {
                'cpu': 'cpus',
                'motherboard': 'motherboards',
                'ram': 'ram',
                'gpu': 'gpus'
            }
            
            if comp_type in table_map:
                result = cursor.execute(f'SELECT min_price, max_price FROM {table_map[comp_type]} WHERE name = ?', (comp_name,)).fetchone()
                if result:
                    cost_breakdown[comp_type] = {'min': result[0], 'max': result[1]}
                    total_cost_min += result[0]
                    total_cost_max += result[1]
        
        conn.close()
        
        return {
            'components': components,
            'compatibility_issues': [asdict(issue) for issue in all_issues],
            'power_requirements': power_info,
            'recommended_psu_wattage': recommended_psu,
            'psu_explanation': psu_explanation,
            'estimated_cost': {
                'min': total_cost_min,
                'max': total_cost_max,
                'breakdown': cost_breakdown
            },
            'build_status': 'compatible' if not any(issue.severity == 'error' for issue in all_issues) else 'incompatible'
        }

# Example usage and test functions
def main():
    """Test the compatibility checker"""
    print("🔧 PC Parts Compatibility Checker")
    print("=" * 40)
    
    checker = PCCompatibilityChecker()
    
    # Test build configuration
    test_build = {
        'cpu': 'Intel Core i7-13700K',
        'motherboard': 'ASUS ROG STRIX Z790-E',
        'ram': 'Corsair Vengeance DDR5-5600 32GB',
        'gpu': 'RTX 4080'
    }
    
    print("\n🖥️  Testing Build Configuration:")
    for comp_type, comp_name in test_build.items():
        print(f"  {comp_type.upper()}: {comp_name}")
    
    # Generate compatibility report
    report = checker.generate_build_report(test_build)
    
    print(f"\n📊 Build Status: {report['build_status'].upper()}")
    
    if report['compatibility_issues']:
        print("\n⚠️  Compatibility Issues:")
        for issue in report['compatibility_issues']:
            icon = "❌" if issue['severity'] == 'error' else "⚠️" if issue['severity'] == 'warning' else "ℹ️"
            print(f"  {icon} {issue['issue']}")
            print(f"     💡 {issue['suggestion']}")
    else:
        print("\n✅ No compatibility issues found!")
    
    print(f"\n⚡ Power Requirements:")
    for component, watts in report['power_requirements'].items():
        if component != 'total':
            print(f"  {component.upper()}: {watts}W")
    print(f"  TOTAL: {report['power_requirements']['total']}W")
    print(f"  {report['psu_explanation']}")
    
    print(f"\n💰 Estimated Cost:")
    print(f"  Range: ${report['estimated_cost']['min']} - ${report['estimated_cost']['max']}")
    
    print("\n✅ Compatibility check complete!")

if __name__ == "__main__":
    main()