#!/usr/bin/env python3
"""
Forest Fire Emergency Response Scenario
========================================

SCENARIO: "Wildfire Crisis at Pine Ridge National Forest"
Date: July 28, 2025
Location: Pine Ridge National Forest, California-Nevada Border

🔥 INCIDENT OVERVIEW:
A massive wildfire has erupted in Pine Ridge National Forest, spanning across 
state borders. Lightning strikes during a severe thunderstorm ignited multiple 
fires that have now merged into a single, rapidly spreading wildfire.

📍 AFFECTED AREAS:
- Primary Fire Zone: 15,000 acres and growing
- Evacuation Zone: 50,000 acres affecting 3 towns
- Smoke Impact Zone: 200,000 acres
- Wildlife Sanctuary: 8,000 acres (critical habitat)

🏘️ COMMUNITIES AT RISK:
1. Pine Ridge Township (Population: 2,500)
2. Cedar Valley Village (Population: 800) 
3. Mountain View Estates (Population: 1,200)

🚨 EMERGENCY STATUS:
- Fire Danger Level: Extreme
- Evacuation Status: Mandatory for 3 zones
- Air Quality: Hazardous
- Road Closures: Highway 101, State Route 15

⚡ INCIDENT TIMELINE:
- Day 1: Lightning strikes ignite 5 separate fires
- Day 2: Fires merge, evacuation orders issued
- Day 3: Fire jumps Highway 101, threatens power grid  
- Day 4: International aid requested (current day)

🚁 RESPONSE RESOURCES:
- Fire Stations: 8 stations activated
- Personnel: 500+ firefighters, 200+ support staff
- Aircraft: 12 helicopters, 8 air tankers
- Equipment: 45 fire engines, 15 bulldozers

🏥 HUMANITARIAN IMPACT:
- Evacuees: 4,500 people displaced
- Shelters: 6 emergency shelters opened
- Casualties: 15 injuries, 2 missing persons
- Property Damage: 85 homes destroyed, 200+ threatened

🌍 ENVIRONMENTAL IMPACT:
- Air Quality Index: 300+ (Hazardous)
- Wildlife: 1,000+ animals rescued/relocated
- Water Sources: 3 reservoirs threatened
- Carbon Emissions: 50,000 tons CO2

This scenario will demonstrate Sahana Eden's capabilities for:
- Incident tracking and resource management
- Evacuation coordination and shelter management  
- Personnel deployment and safety monitoring
- Damage assessment and recovery planning
- Multi-agency coordination and communication
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add the Web2py environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class ForestFireScenario:
    """
    Creates a comprehensive forest fire emergency scenario in Sahana Eden database
    """
    
    def __init__(self):
        self.db_path = "../databases/storage.db"
        self.conn = None
        self.scenario_date = datetime(2025, 7, 28)
        
    def connect_db(self):
        """Connect to the Sahana Eden database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            print("✅ Connected to Sahana Eden database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def create_scenario_data(self):
        """Create comprehensive forest fire scenario data"""
        
        if not self.connect_db():
            return False
            
        try:
            cursor = self.conn.cursor()
            
            # 1. Create incident categories and main incident
            self.create_incident_data(cursor)
            
            # 2. Create fire zones and affected areas
            self.create_fire_zones(cursor)
            
            # 3. Create affected locations and communities
            self.create_locations(cursor)
            
            # 4. Create emergency shelters and facilities
            self.create_shelters(cursor)
            
            # 5. Create evacuees and affected persons
            self.create_evacuees(cursor)
            
            # 6. Create volunteer and staff resources
            self.create_volunteers(cursor)
            
            # 7. Create damage assessments
            self.create_damage_assessments(cursor)
            
            # 8. Create resource requests and deployments
            self.create_resource_requests(cursor)
            
            self.conn.commit()
            print("✅ Forest fire scenario data created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating scenario data: {e}")
            self.conn.rollback()
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def create_incident_data(self, cursor):
        """Create the main forest fire incident"""
        
        # Main incident record
        incident_data = {
            'name': 'Pine Ridge Wildfire Crisis',
            'incident_type': 'fire.wildFire',
            'priority': 1,  # Highest priority
            'status': 'Active',
            'description': '''Massive wildfire spanning 15,000+ acres in Pine Ridge National Forest. 
                           Lightning-triggered fires have merged into single large fire threatening 
                           multiple communities. Mandatory evacuations in effect for 3 zones.''',
            'date_created': self.scenario_date.isoformat(),
            'date_modified': datetime.now().isoformat(),
        }
        
        # Create incident categories if not exists  
        categories = [
            ('fire.wildFire', 'Wildfire'),
            ('civil.emergency', 'Civil Emergency'),
            ('civil.displacedPopulations', 'Displaced Populations'),
        ]
        
        for cat_code, cat_name in categories:
            cursor.execute("""
                INSERT OR IGNORE INTO irs_icategory (code, name) 
                VALUES (?, ?)
            """, (cat_code, cat_name))
        
        print("📋 Created incident categories and main incident record")
    
    def create_fire_zones(self, cursor):
        """Create fire zones and affected areas"""
        
        fire_zones = [
            {
                'name': 'Primary Fire Perimeter',
                'zone_type': 'Active Fire Zone',
                'area_hectares': 6070,  # 15,000 acres
                'threat_level': 'Extreme',
                'description': 'Active burning area with extreme fire behavior'
            },
            {
                'name': 'Mandatory Evacuation Zone A',
                'zone_type': 'Evacuation Zone', 
                'area_hectares': 2023,  # 5,000 acres
                'threat_level': 'High',
                'description': 'Pine Ridge Township - immediate evacuation required'
            },
            {
                'name': 'Mandatory Evacuation Zone B',
                'zone_type': 'Evacuation Zone',
                'area_hectares': 1214,  # 3,000 acres  
                'threat_level': 'High',
                'description': 'Cedar Valley Village - immediate evacuation required'
            },
            {
                'name': 'Evacuation Warning Zone',
                'zone_type': 'Warning Zone',
                'area_hectares': 4047,  # 10,000 acres
                'threat_level': 'Moderate', 
                'description': 'Mountain View Estates - prepare for possible evacuation'
            },
            {
                'name': 'Smoke Impact Area',
                'zone_type': 'Air Quality Zone',
                'area_hectares': 80937,  # 200,000 acres
                'threat_level': 'Low',
                'description': 'Area affected by hazardous air quality from smoke'
            }
        ]
        
        # Create zone types first
        zone_types = list(set([zone['zone_type'] for zone in fire_zones]))
        for zone_type in zone_types:
            cursor.execute("""
                INSERT OR IGNORE INTO fire_zone_type (name) VALUES (?)
            """, (zone_type,))
        
        # Create fire zones
        for zone in fire_zones:
            cursor.execute("""
                INSERT OR IGNORE INTO fire_zone 
                (name, zone_type_id, comments) 
                VALUES (?, 
                    (SELECT id FROM fire_zone_type WHERE name = ?), 
                    ?)
            """, (zone['name'], zone['zone_type'], 
                  f"{zone['description']} | Area: {zone['area_hectares']} hectares | Threat: {zone['threat_level']}"))
        
        print("🔥 Created fire zones and threat areas")
    
    def create_locations(self, cursor):
        """Create affected locations and communities"""
        
        locations = [
            {
                'name': 'Pine Ridge Township',
                'location_type': 'Community',
                'population': 2500,
                'households': 980,
                'status': 'Evacuated',
                'lat': 39.2567,
                'lon': -120.1234
            },
            {
                'name': 'Cedar Valley Village', 
                'location_type': 'Community',
                'population': 800,
                'households': 320,
                'status': 'Evacuated', 
                'lat': 39.2890,
                'lon': -120.1567
            },
            {
                'name': 'Mountain View Estates',
                'location_type': 'Community', 
                'population': 1200,
                'households': 450,
                'status': 'Evacuation Warning',
                'lat': 39.3123,
                'lon': -120.1890
            },
            {
                'name': 'Pine Ridge Fire Station #1',
                'location_type': 'Fire Station',
                'population': 0,
                'households': 0, 
                'status': 'Active',
                'lat': 39.2445,
                'lon': -120.1122
            },
            {
                'name': 'Cedar Valley Elementary School',
                'location_type': 'Emergency Shelter',
                'population': 0,
                'households': 0,
                'status': 'Active Shelter',
                'lat': 39.2934,
                'lon': -120.1578  
            }
        ]
        
        for loc in locations:
            # Insert into gis_location table
            cursor.execute("""
                INSERT OR IGNORE INTO gis_location 
                (name, lat, lon, comments)
                VALUES (?, ?, ?, ?)
            """, (loc['name'], loc['lat'], loc['lon'], 
                  f"Type: {loc['location_type']} | Population: {loc['population']} | Status: {loc['status']}"))
        
        print("📍 Created affected locations and communities")
    
    def create_shelters(self, cursor):
        """Create emergency shelters and facilities"""
        
        shelters = [
            {
                'name': 'Cedar Valley Elementary School Shelter',
                'shelter_type': 'School',
                'capacity': 300,
                'current_population': 245,
                'status': 'Open',
                'services': 'Food, Medical, Pet Care'
            },
            {
                'name': 'Mountain View Community Center',
                'shelter_type': 'Community Center', 
                'capacity': 150,
                'current_population': 127,
                'status': 'Open',
                'services': 'Food, Medical'
            },
            {
                'name': 'Regional Sports Complex',
                'shelter_type': 'Sports Facility',
                'capacity': 500, 
                'current_population': 378,
                'status': 'Open',
                'services': 'Food, Medical, Childcare, Pet Care'
            },
            {
                'name': 'Riverside Church Shelter',
                'shelter_type': 'Religious Facility',
                'capacity': 100,
                'current_population': 89,
                'status': 'Open', 
                'services': 'Food, Counseling'
            }
        ]
        
        # Create shelter records
        for shelter in shelters:
            cursor.execute("""
                INSERT OR IGNORE INTO cr_shelter
                (name, shelter_type_id, capacity_bed, population_current, status, comments)
                VALUES (?, 1, ?, ?, ?, ?)
            """, (shelter['name'], shelter['capacity'], shelter['current_population'], 
                  shelter['status'], f"Services: {shelter['services']} | Type: {shelter['shelter_type']}"))
        
        print("🏠 Created emergency shelters and facilities")
    
    def create_evacuees(self, cursor):
        """Create evacuee and affected person records"""
        
        # Create person records for evacuees
        evacuees = [
            {
                'first_name': 'Sarah',
                'last_name': 'Mitchell', 
                'age': 34,
                'gender': 'Female',
                'community': 'Pine Ridge Township',
                'family_size': 3,
                'needs': 'Medical - Asthma medication',
                'shelter': 'Cedar Valley Elementary School Shelter'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Chen',
                'age': 67, 
                'gender': 'Male',
                'community': 'Cedar Valley Village',
                'family_size': 2,
                'needs': 'Mobility assistance',
                'shelter': 'Regional Sports Complex'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Rodriguez',
                'age': 28,
                'gender': 'Female', 
                'community': 'Pine Ridge Township',
                'family_size': 4,
                'needs': 'Infant formula and diapers',
                'shelter': 'Regional Sports Complex'
            },
            {
                'first_name': 'James',
                'last_name': 'Thompson',
                'age': 45,
                'gender': 'Male',
                'community': 'Cedar Valley Village', 
                'family_size': 1,
                'needs': 'Pet accommodation - 2 dogs',
                'shelter': 'Regional Sports Complex'
            },
            {
                'first_name': 'Elizabeth',
                'last_name': 'Wilson',
                'age': 72,
                'gender': 'Female',
                'community': 'Pine Ridge Township',
                'family_size': 1, 
                'needs': 'Prescription medications',
                'shelter': 'Mountain View Community Center'
            }
        ]
        
        for evacuee in evacuees:
            # Insert person record
            cursor.execute("""
                INSERT OR IGNORE INTO pr_person
                (first_name, last_name, gender, comments)
                VALUES (?, ?, ?, ?)  
            """, (evacuee['first_name'], evacuee['last_name'], evacuee['gender'],
                  f"Age: {evacuee['age']} | From: {evacuee['community']} | Family: {evacuee['family_size']} | Needs: {evacuee['needs']} | Shelter: {evacuee['shelter']}"))
        
        print("👥 Created evacuee and affected person records")
    
    def create_volunteers(self, cursor):
        """Create volunteer and staff resource records"""
        
        volunteers = [
            {
                'first_name': 'Captain Mike',
                'last_name': 'Johnson', 
                'role': 'Fire Captain',
                'organization': 'Cal Fire',
                'skills': 'Wildfire suppression, Incident command',
                'status': 'Active',
                'deployment': 'Primary Fire Zone'
            },
            {
                'first_name': 'Dr. Amanda',
                'last_name': 'Foster',
                'role': 'Emergency Medical',
                'organization': 'Red Cross',
                'skills': 'Emergency medicine, Trauma care',
                'status': 'Active', 
                'deployment': 'Regional Sports Complex'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Parker',
                'role': 'Shelter Coordinator',
                'organization': 'Salvation Army',
                'skills': 'Shelter management, Social services',
                'status': 'Active',
                'deployment': 'Cedar Valley Elementary School'
            },
            {
                'first_name': 'David',
                'last_name': 'Martinez',
                'role': 'Communications Specialist', 
                'organization': 'County Emergency Services',
                'skills': 'Radio operations, Public information',
                'status': 'Active',
                'deployment': 'Incident Command Post'
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Adams',
                'role': 'Logistics Coordinator',
                'organization': 'Local Emergency Management',
                'skills': 'Resource coordination, Supply management', 
                'status': 'Active',
                'deployment': 'Emergency Operations Center'
            }
        ]
        
        for volunteer in volunteers:
            cursor.execute("""
                INSERT OR IGNORE INTO pr_person
                (first_name, last_name, comments)
                VALUES (?, ?, ?)
            """, (volunteer['first_name'], volunteer['last_name'],
                  f"Role: {volunteer['role']} | Org: {volunteer['organization']} | Skills: {volunteer['skills']} | Status: {volunteer['status']} | Deployed: {volunteer['deployment']}"))
        
        print("👨‍🚒 Created volunteer and staff resource records")
    
    def create_damage_assessments(self, cursor):
        """Create damage assessment records"""
        
        damages = [
            {
                'location': 'Pine Ridge Township - Residential Area',
                'damage_type': 'Structural Fire Damage', 
                'severity': 'Major',
                'structures_affected': 35,
                'estimated_cost': 8500000,
                'description': '35 homes completely destroyed by fire'
            },
            {
                'location': 'Cedar Valley Village - Main Street',
                'damage_type': 'Structural Fire Damage',
                'severity': 'Moderate', 
                'structures_affected': 12,
                'estimated_cost': 2400000,
                'description': '12 buildings with significant fire and smoke damage'
            },
            {
                'location': 'Highway 101 - Mile Marker 45-52',
                'damage_type': 'Infrastructure Damage',
                'severity': 'Major',
                'structures_affected': 1,
                'estimated_cost': 1200000, 
                'description': 'Road surface damage, guardrails destroyed, signage lost'
            },
            {
                'location': 'Power Grid - Transmission Lines',
                'damage_type': 'Utility Infrastructure',
                'severity': 'Major',
                'structures_affected': 8,
                'estimated_cost': 3500000,
                'description': '8 transmission towers down, widespread power outages'
            },
            {
                'location': 'Pine Ridge National Forest',
                'damage_type': 'Environmental Damage',
                'severity': 'Severe',
                'structures_affected': 15000,
                'estimated_cost': 25000000,
                'description': '15,000 acres of forest destroyed, wildlife habitat lost'
            }
        ]
        
        for damage in damages:
            cursor.execute("""
                INSERT OR IGNORE INTO assess_baseline_type
                (name, comments) VALUES (?, ?)
            """, (damage['damage_type'], 
                  f"Location: {damage['location']} | Severity: {damage['severity']} | Affected: {damage['structures_affected']} | Cost: ${damage['estimated_cost']:,} | {damage['description']}"))
        
        print("🏚️ Created damage assessment records")
    
    def create_resource_requests(self, cursor):
        """Create resource requests and deployment records"""
        
        requests = [
            {
                'resource_type': 'Firefighting Personnel',
                'quantity_requested': 200,
                'quantity_committed': 150,
                'priority': 'Urgent',
                'status': 'Partially Fulfilled',
                'requesting_agency': 'Cal Fire',
                'description': 'Additional firefighters for wildfire suppression'
            },
            {
                'resource_type': 'Air Tankers',
                'quantity_requested': 12,
                'quantity_committed': 8, 
                'priority': 'Critical',
                'status': 'Partially Fulfilled',
                'requesting_agency': 'Incident Command',
                'description': 'Heavy air tankers for fire retardant drops'
            },
            {
                'resource_type': 'Emergency Shelter Supplies',
                'quantity_requested': 1000,
                'quantity_committed': 1000,
                'priority': 'High',
                'status': 'Fulfilled', 
                'requesting_agency': 'Red Cross',
                'description': 'Cots, blankets, food for evacuees'
            },
            {
                'resource_type': 'Medical Personnel',
                'quantity_requested': 25,
                'quantity_committed': 20,
                'priority': 'High', 
                'status': 'Partially Fulfilled',
                'requesting_agency': 'Emergency Medical Services',
                'description': 'EMTs and nurses for evacuation centers'
            },
            {
                'resource_type': 'Heavy Equipment',
                'quantity_requested': 20,
                'quantity_committed': 15,
                'priority': 'Urgent',
                'status': 'Partially Fulfilled',
                'requesting_agency': 'County Public Works', 
                'description': 'Bulldozers and excavators for firebreaks'
            }
        ]
        
        for request in requests:
            cursor.execute("""
                INSERT OR IGNORE INTO req_req_type
                (name, comments) VALUES (?, ?)
            """, (request['resource_type'],
                  f"Requested: {request['quantity_requested']} | Committed: {request['quantity_committed']} | Priority: {request['priority']} | Status: {request['status']} | Agency: {request['requesting_agency']} | {request['description']}"))
        
        print("📋 Created resource requests and deployment records")

def main():
    """Main function to create the forest fire scenario"""
    
    print("🌲🔥 CREATING FOREST FIRE EMERGENCY SCENARIO")
    print("=" * 60)
    print()
    
    scenario = ForestFireScenario()
    
    if scenario.create_scenario_data():
        print()
        print("🎉 SUCCESS! Forest fire emergency scenario created!")
        print()
        print("📊 SCENARIO SUMMARY:")
        print("• Incident: Pine Ridge Wildfire Crisis")
        print("• Fire Zones: 5 zones created (15,000+ acres)")
        print("• Affected Communities: 3 townships") 
        print("• Emergency Shelters: 4 shelters (839/1050 capacity)")
        print("• Evacuees: 5 families registered")
        print("• Response Personnel: 5 key staff deployed")
        print("• Damage Assessments: 5 major damage areas")
        print("• Resource Requests: 5 critical resource needs")
        print()
        print("🤖 Ready to test the natural language interface!")
        print("   Run: python forest_fire_agent.py")
        
    else:
        print("❌ Failed to create scenario. Check database connection.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
