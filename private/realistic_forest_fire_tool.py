#!/usr/bin/env python3
"""
Realistic Forest Fire Emergency Database Tool
=============================================

Updated to work with the actual Sahana Eden database structure.
Uses existing tables like pr_person, gis_location, disease_case, etc.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class RealisticForestFireDatabaseTool:
    """
    Database tool for forest fire emergency response using actual Sahana Eden tables
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Get the absolute path to the databases directory
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "..", "databases", "storage.db")
            db_path = os.path.abspath(db_path)
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute SQL query and return results as list of dictionaries"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Query execution error: {e}")
            return []
    
    # =========================================================================
    # EMERGENCY OVERVIEW AND STATUS
    # =========================================================================
    
    def get_emergency_overview(self) -> Dict[str, Any]:
        """Get comprehensive emergency situation overview"""
        
        # Get person records (includes evacuees, staff, affected persons)
        persons_query = """
        SELECT 
            COUNT(*) as total_persons,
            SUM(CASE WHEN comments LIKE '%evacuee%' OR comments LIKE '%Shelter%' THEN 1 ELSE 0 END) as evacuees,
            SUM(CASE WHEN comments LIKE '%Fire Captain%' OR comments LIKE '%Emergency%' OR comments LIKE '%Role:%' THEN 1 ELSE 0 END) as response_staff
        FROM pr_person
        """
        
        person_stats = self.execute_query(persons_query)
        
        # Get location data (communities, shelters, fire stations)
        locations_query = """
        SELECT 
            COUNT(*) as total_locations,
            SUM(CASE WHEN name LIKE '%Township%' OR name LIKE '%Village%' OR name LIKE '%Estates%' THEN 1 ELSE 0 END) as communities,
            SUM(CASE WHEN name LIKE '%Shelter%' OR name LIKE '%School%' OR name LIKE '%Center%' THEN 1 ELSE 0 END) as shelters,
            SUM(CASE WHEN name LIKE '%Fire Station%' THEN 1 ELSE 0 END) as fire_stations
        FROM gis_location
        """
        
        location_stats = self.execute_query(locations_query)
        
        # Get disease case data (can represent incident victims/affected persons)
        disease_query = """
        SELECT 
            COUNT(*) as total_cases,
            SUM(CASE WHEN hospitalized = 'T' THEN 1 ELSE 0 END) as hospitalized,
            SUM(CASE WHEN illness_status = 'Recovered' THEN 1 ELSE 0 END) as recovered,
            SUM(CASE WHEN illness_status = 'Deceased' THEN 1 ELSE 0 END) as deceased
        FROM disease_case
        """
        
        disease_stats = self.execute_query(disease_query)
        
        # Get asset data (equipment, vehicles, resources)
        assets_query = """
        SELECT 
            COUNT(*) as total_assets
        FROM asset_asset
        """
        
        asset_stats = self.execute_query(assets_query)
        
        return {
            "emergency_status": "ACTIVE - Forest Fire Emergency",
            "alert_level": "EXTREME",
            "incident_name": "Pine Ridge Wildfire Crisis",
            "person_statistics": person_stats[0] if person_stats else {},
            "location_statistics": location_stats[0] if location_stats else {},
            "impact_statistics": disease_stats[0] if disease_stats else {},
            "asset_statistics": asset_stats[0] if asset_stats else {},
            "last_updated": datetime.now().isoformat()
        }
    
    def get_affected_persons(self) -> Dict[str, Any]:
        """Get information about affected persons and evacuees"""
        
        # Get all persons with details
        persons_query = """
        SELECT 
            id,
            first_name,
            last_name,
            gender,
            comments,
            date_of_birth,
            created_on,
            modified_on
        FROM pr_person
        ORDER BY modified_on DESC
        """
        
        all_persons = self.execute_query(persons_query)
        
        # Categorize persons based on comments and context
        evacuees = []
        response_staff = []
        affected_persons = []
        
        for person in all_persons:
            comments = person.get('comments', '').lower()
            
            if any(word in comments for word in ['evacuee', 'shelter', 'displaced', 'from:']):
                evacuees.append(person)
            elif any(word in comments for word in ['fire captain', 'emergency', 'role:', 'responder']):
                response_staff.append(person)
            else:
                affected_persons.append(person)
        
        return {
            "evacuees": evacuees,
            "response_staff": response_staff,
            "other_persons": affected_persons,
            "total_persons": len(all_persons),
            "evacuee_count": len(evacuees),
            "staff_count": len(response_staff)
        }
    
    def get_locations_and_facilities(self) -> Dict[str, Any]:
        """Get information about locations, communities, and facilities"""
        
        locations_query = """
        SELECT 
            id,
            name,
            level,
            lat,
            lon,
            addr_street,
            addr_postcode,
            population,
            comments,
            created_on
        FROM gis_location
        WHERE name IS NOT NULL
        ORDER BY name
        """
        
        all_locations = self.execute_query(locations_query)
        
        # Categorize locations
        communities = []
        shelters = []
        fire_stations = []
        other_locations = []
        
        for location in all_locations:
            name = location.get('name', '').lower()
            comments = location.get('comments', '').lower() if location.get('comments') else ''
            
            if any(word in name for word in ['township', 'village', 'estates', 'community']):
                communities.append(location)
            elif any(word in name for word in ['shelter', 'school', 'center', 'church']):
                shelters.append(location)
            elif 'fire station' in name:
                fire_stations.append(location) 
            else:
                other_locations.append(location)
        
        return {
            "communities": communities,
            "shelters": shelters,
            "fire_stations": fire_stations,
            "other_locations": other_locations,
            "total_locations": len(all_locations),
            "community_count": len(communities),
            "shelter_count": len(shelters),
            "fire_station_count": len(fire_stations)
        }
    
    def get_incident_impact_data(self) -> Dict[str, Any]:
        """Get incident impact data using disease case records as proxy"""
        
        # Get disease case data (representing incident victims/impacts)
        cases_query = """
        SELECT 
            id,
            case_number,
            person_id,
            disease_id,
            location_id,
            diagnosis_date,
            hospitalized,
            illness_status,
            comments,
            created_on,
            modified_on
        FROM disease_case
        ORDER BY diagnosis_date DESC
        """
        
        cases = self.execute_query(cases_query)
        
        # Get disease information
        diseases_query = """
        SELECT 
            id,
            name,
            code,
            comments
        FROM disease_disease
        """
        
        diseases = self.execute_query(diseases_query)
        
        # Get symptoms (can represent types of impacts)
        symptoms_query = """
        SELECT 
            id,
            name,
            assessment,
            comments
        FROM disease_symptom
        ORDER BY assessment, name
        """
        
        symptoms = self.execute_query(symptoms_query)
        
        # Calculate statistics
        total_cases = len(cases)
        hospitalized = len([c for c in cases if c.get('hospitalized') == 'T'])
        recovered = len([c for c in cases if c.get('illness_status') == 'Recovered'])
        deceased = len([c for c in cases if c.get('illness_status') == 'Deceased'])
        
        return {
            "impact_cases": cases,
            "diseases": diseases,
            "symptoms": symptoms,
            "statistics": {
                "total_cases": total_cases,
                "hospitalized": hospitalized,
                "recovered": recovered,
                "deceased": deceased,
                "hospitalization_rate": round(hospitalized/total_cases*100, 1) if total_cases > 0 else 0
            }
        }
    
    def get_resources_and_assets(self) -> Dict[str, Any]:
        """Get information about resources and assets"""
        
        # Get asset data
        assets_query = """
        SELECT 
            id,
            number,
            type,
            category,
            item_id,
            organisation_id,
            location_id,
            status,
            comments,
            created_on
        FROM asset_asset
        ORDER BY type, number
        """
        
        assets = self.execute_query(assets_query)
        
        # Get organisations
        orgs_query = """
        SELECT 
            id,
            name,
            acronym,
            organisation_type_id,
            website,
            comments
        FROM org_organisation
        WHERE name IS NOT NULL
        ORDER BY name
        """
        
        organisations = self.execute_query(orgs_query)
        
        return {
            "assets": assets,
            "organisations": organisations,
            "total_assets": len(assets),
            "total_organisations": len(organisations)
        }
    
    # =========================================================================
    # SEARCH AND QUERY FUNCTIONS
    # =========================================================================
    
    def search_emergency_data(self, search_term: str) -> Dict[str, List[Dict]]:
        """Search across all emergency-related data"""
        
        results = {
            "persons": [],
            "locations": [],
            "cases": [],
            "assets": [],
            "organisations": []
        }
        
        # Search persons
        persons_query = """
        SELECT first_name, last_name, gender, comments
        FROM pr_person
        WHERE first_name LIKE ? OR last_name LIKE ? OR comments LIKE ?
        ORDER BY last_name, first_name
        """
        results["persons"] = self.execute_query(persons_query, 
                                              (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        # Search locations
        locations_query = """
        SELECT name, lat, lon, comments, population
        FROM gis_location
        WHERE name LIKE ? OR comments LIKE ?
        ORDER BY name
        """
        results["locations"] = self.execute_query(locations_query, 
                                                (f"%{search_term}%", f"%{search_term}%"))
        
        # Search disease cases
        cases_query = """
        SELECT case_number, diagnosis_date, hospitalized, illness_status, comments
        FROM disease_case
        WHERE case_number LIKE ? OR comments LIKE ?
        ORDER BY diagnosis_date DESC
        """
        results["cases"] = self.execute_query(cases_query, 
                                            (f"%{search_term}%", f"%{search_term}%"))
        
        # Search assets
        assets_query = """
        SELECT number, type, category, status, comments
        FROM asset_asset
        WHERE number LIKE ? OR type LIKE ? OR comments LIKE ?
        ORDER BY type
        """
        results["assets"] = self.execute_query(assets_query, 
                                             (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        return results
    
    def get_situation_report(self) -> Dict[str, Any]:
        """Generate comprehensive situation report"""
        
        return {
            "overview": self.get_emergency_overview(),
            "persons": self.get_affected_persons(),
            "locations": self.get_locations_and_facilities(),
            "impact": self.get_incident_impact_data(),
            "resources": self.get_resources_and_assets(),
            "report_generated": datetime.now().isoformat()
        }
    
    def execute_custom_query(self, query: str) -> List[Dict]:
        """Execute a custom SQL query (read-only)"""
        
        # Safety check - only allow SELECT queries
        query_upper = query.upper().strip()
        if not query_upper.startswith('SELECT'):
            return [{"error": "Only SELECT queries are allowed for safety"}]
        
        return self.execute_query(query)

# =============================================================================
# TESTING AND DEMONSTRATION
# =============================================================================

def test_realistic_database():
    """Test the realistic forest fire database tool"""
    
    print("🌲🔥 REALISTIC FOREST FIRE EMERGENCY DATABASE")
    print("=" * 60)
    
    db_tool = RealisticForestFireDatabaseTool()
    
    if not db_tool.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Test 1: Emergency Overview
        print("\n🚨 EMERGENCY OVERVIEW:")
        overview = db_tool.get_emergency_overview()
        
        print(f"Status: {overview.get('emergency_status', 'Unknown')}")
        print(f"Alert Level: {overview.get('alert_level', 'Unknown')}")
        print(f"Incident: {overview.get('incident_name', 'Unknown')}")
        
        person_stats = overview.get('person_statistics', {})
        print(f"\n👥 PEOPLE:")
        print(f"   Total Persons: {person_stats.get('total_persons', 0)}")
        print(f"   Evacuees: {person_stats.get('evacuees', 0)}")
        print(f"   Response Staff: {person_stats.get('response_staff', 0)}")
        
        location_stats = overview.get('location_statistics', {})
        print(f"\n📍 LOCATIONS:")
        print(f"   Total Locations: {location_stats.get('total_locations', 0)}")
        print(f"   Communities: {location_stats.get('communities', 0)}")
        print(f"   Shelters: {location_stats.get('shelters', 0)}")
        print(f"   Fire Stations: {location_stats.get('fire_stations', 0)}")
        
        impact_stats = overview.get('impact_statistics', {})
        print(f"\n🏥 IMPACT:")
        print(f"   Total Cases: {impact_stats.get('total_cases', 0)}")
        print(f"   Hospitalized: {impact_stats.get('hospitalized', 0)}")
        print(f"   Recovered: {impact_stats.get('recovered', 0)}")
        print(f"   Deceased: {impact_stats.get('deceased', 0)}")
        
        # Test 2: Affected Persons
        print("\n👥 AFFECTED PERSONS:")
        persons = db_tool.get_affected_persons()
        print(f"   Total Persons: {persons.get('total_persons', 0)}")  
        print(f"   Evacuees: {persons.get('evacuee_count', 0)}")
        print(f"   Response Staff: {persons.get('staff_count', 0)}")
        
        # Show some evacuees
        evacuees = persons.get('evacuees', [])
        if evacuees:
            print("\n   🏠 Sample Evacuees:")
            for evacuee in evacuees[:3]:
                name = f"{evacuee.get('first_name', '')} {evacuee.get('last_name', '')}"
                print(f"      • {name}")
        
        # Test 3: Locations
        print("\n📍 LOCATIONS & FACILITIES:")
        locations = db_tool.get_locations_and_facilities()
        print(f"   Communities: {locations.get('community_count', 0)}")
        print(f"   Shelters: {locations.get('shelter_count', 0)}")
        print(f"   Fire Stations: {locations.get('fire_station_count', 0)}")
        
        # Show some communities
        communities = locations.get('communities', [])
        if communities:
            print("\n   🏘️ Communities:")
            for community in communities[:3]:
                name = community.get('name', 'Unknown')
                pop = community.get('population', 'Unknown')
                print(f"      • {name} (Pop: {pop})")
        
        # Test 4: Search functionality
        print("\n🔍 SEARCH TEST - 'COVID':")
        search_results = db_tool.search_emergency_data("COVID")
        total_results = sum(len(results) for results in search_results.values())
        print(f"   Total results: {total_results}")
        
        for category, results in search_results.items():
            if results:
                print(f"   • {category.capitalize()}: {len(results)} results")
        
        print("\n✅ Realistic database tool test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_tool.disconnect()

if __name__ == "__main__":
    test_realistic_database()
