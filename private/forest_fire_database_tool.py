#!/usr/bin/env python3
"""
Forest Fire Emergency Database Tool
===================================

A comprehensive database interface for forest fire emergency response management.
Provides structured access to all forest fire related data including incidents,
evacuations, resources, damages, and response coordination.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class ForestFireDatabaseTool:
    """
    Database tool for forest fire emergency response management
    """
    
    def __init__(self, db_path: str = "../databases/storage.db"):
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
    # FOREST FIRE INCIDENT MANAGEMENT
    # =========================================================================
    
    def get_fire_incidents_overview(self) -> Dict[str, Any]:
        """Get comprehensive overview of all fire incidents"""
        
        # Main incident details
        incidents_query = """
        SELECT 
            name,
            incident_type,
            priority,
            status, 
            description,
            date_created,
            date_modified
        FROM incident 
        WHERE incident_type LIKE '%fire%' OR incident_type LIKE '%Fire%'
        ORDER BY priority, date_created DESC
        """
        
        incidents = self.execute_query(incidents_query)
        
        # Fire zones summary
        zones_query = """
        SELECT 
            fz.name as zone_name,
            fzt.name as zone_type,
            fz.comments
        FROM fire_zone fz
        LEFT JOIN fire_zone_type fzt ON fz.zone_type_id = fzt.id
        ORDER BY fzt.name, fz.name
        """
        
        zones = self.execute_query(zones_query)
        
        # Affected locations
        locations_query = """
        SELECT 
            name,
            lat,
            lon,
            comments
        FROM gis_location 
        WHERE comments LIKE '%Community%' OR comments LIKE '%Fire Station%' OR comments LIKE '%Shelter%'
        ORDER BY name
        """
        
        locations = self.execute_query(locations_query)
        
        return {
            "incidents": incidents,
            "fire_zones": zones,
            "affected_locations": locations,
            "total_incidents": len(incidents),
            "total_zones": len(zones),
            "total_locations": len(locations),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_fire_zone_details(self, zone_name: Optional[str] = None) -> List[Dict]:
        """Get detailed information about fire zones"""
        
        if zone_name:
            query = """
            SELECT 
                fz.name as zone_name,
                fzt.name as zone_type,
                fz.comments,
                fz.id as zone_id
            FROM fire_zone fz
            LEFT JOIN fire_zone_type fzt ON fz.zone_type_id = fzt.id
            WHERE fz.name LIKE ?
            ORDER BY fz.name
            """
            params = (f"%{zone_name}%",)
        else:
            query = """
            SELECT 
                fz.name as zone_name,
                fzt.name as zone_type,
                fz.comments,
                fz.id as zone_id
            FROM fire_zone fz
            LEFT JOIN fire_zone_type fzt ON fz.zone_type_id = fzt.id
            ORDER BY fzt.name, fz.name
            """
            params = ()
        
        return self.execute_query(query, params)
    
    # =========================================================================
    # EVACUATION AND SHELTER MANAGEMENT  
    # =========================================================================
    
    def get_evacuation_status(self) -> Dict[str, Any]:
        """Get comprehensive evacuation status and shelter information"""
        
        # Shelter information
        shelters_query = """
        SELECT 
            name,
            capacity_bed as capacity,
            population_current,
            status,
            comments
        FROM cr_shelter
        WHERE status = 'Open' OR population_current > 0
        ORDER BY population_current DESC
        """
        
        shelters = self.execute_query(shelters_query)
        
        # Calculate shelter statistics
        total_capacity = sum(s.get('capacity', 0) or 0 for s in shelters)
        total_occupied = sum(s.get('population_current', 0) or 0 for s in shelters)
        occupancy_rate = (total_occupied / total_capacity * 100) if total_capacity > 0 else 0
        
        # Evacuee locations from person records  
        evacuees_query = """
        SELECT 
            first_name,
            last_name,
            gender,
            comments
        FROM pr_person
        WHERE comments LIKE '%Shelter%' OR comments LIKE '%evacuee%' OR comments LIKE '%From:%'
        ORDER BY last_name, first_name
        """
        
        evacuees = self.execute_query(evacuees_query)
        
        # Affected communities
        communities_query = """
        SELECT 
            name,
            comments,
            lat,
            lon
        FROM gis_location
        WHERE comments LIKE '%Community%' AND (comments LIKE '%Evacuated%' OR comments LIKE '%Warning%')
        ORDER BY name
        """
        
        communities = self.execute_query(communities_query)
        
        return {
            "shelters": shelters,
            "evacuees": evacuees,
            "affected_communities": communities,
            "shelter_statistics": {
                "total_capacity": total_capacity,
                "total_occupied": total_occupied,
                "available_space": total_capacity - total_occupied,
                "occupancy_rate": round(occupancy_rate, 1)
            },
            "evacuation_summary": {
                "total_evacuees": len(evacuees),
                "active_shelters": len([s for s in shelters if s.get('status') == 'Open']),
                "affected_communities": len(communities)
            }
        }
    
    def get_shelter_details(self, shelter_name: Optional[str] = None) -> List[Dict]:
        """Get detailed shelter information"""
        
        if shelter_name:
            query = """
            SELECT 
                name,
                capacity_bed as capacity,
                population_current,
                status,
                comments
            FROM cr_shelter
            WHERE name LIKE ?
            ORDER BY name
            """
            params = (f"%{shelter_name}%",)
        else:
            query = """
            SELECT 
                name,
                capacity_bed as capacity,
                population_current,
                status,
                comments
            FROM cr_shelter
            ORDER BY population_current DESC
            """
            params = ()
        
        return self.execute_query(query, params)
    
    # =========================================================================
    # PERSONNEL AND RESOURCE MANAGEMENT
    # =========================================================================
    
    def get_response_personnel(self) -> Dict[str, Any]:
        """Get information about response personnel and volunteers"""
        
        personnel_query = """
        SELECT 
            first_name,
            last_name,
            comments
        FROM pr_person
        WHERE comments LIKE '%Role:%' OR comments LIKE '%Fire Captain%' OR comments LIKE '%Emergency%'
        ORDER BY last_name, first_name
        """
        
        personnel = self.execute_query(personnel_query)
        
        # Parse roles from comments
        personnel_by_role = {}
        for person in personnel:
            comments = person.get('comments', '')
            if 'Role:' in comments:
                try:
                    role = comments.split('Role:')[1].split('|')[0].strip()
                    if role not in personnel_by_role:
                        personnel_by_role[role] = []
                    personnel_by_role[role].append(person)
                except:
                    pass
        
        return {
            "all_personnel": personnel,
            "personnel_by_role": personnel_by_role,
            "total_personnel": len(personnel),
            "roles_count": len(personnel_by_role)
        }
    
    def get_resource_requests(self) -> Dict[str, Any]:
        """Get resource requests and deployment status"""
        
        resources_query = """
        SELECT 
            name as resource_type,
            comments
        FROM req_req_type
        ORDER BY name
        """
        
        resources = self.execute_query(resources_query)
        
        # Parse resource details from comments
        parsed_resources = []
        for resource in resources:
            comments = resource.get('comments', '')
            parsed = {'resource_type': resource.get('resource_type', '')}
            
            # Extract details from comments
            try:
                if 'Requested:' in comments:
                    parsed['requested'] = comments.split('Requested:')[1].split('|')[0].strip()
                if 'Committed:' in comments:
                    parsed['committed'] = comments.split('Committed:')[1].split('|')[0].strip()
                if 'Priority:' in comments:
                    parsed['priority'] = comments.split('Priority:')[1].split('|')[0].strip()
                if 'Status:' in comments:
                    parsed['status'] = comments.split('Status:')[1].split('|')[0].strip()
                if 'Agency:' in comments:
                    parsed['agency'] = comments.split('Agency:')[1].split('|')[0].strip()
                
                parsed['description'] = comments.split('|')[-1].strip()
            except:
                parsed['description'] = comments
            
            parsed_resources.append(parsed)
        
        return {
            "resource_requests": parsed_resources,
            "total_requests": len(resources)
        }
    
    # =========================================================================
    # DAMAGE ASSESSMENT AND IMPACT ANALYSIS
    # =========================================================================
    
    def get_damage_assessments(self) -> Dict[str, Any]:
        """Get comprehensive damage assessment information"""
        
        damage_query = """
        SELECT 
            name as damage_type,
            comments
        FROM assess_baseline_type
        ORDER BY name
        """
        
        damages = self.execute_query(damage_query)
        
        # Parse damage details
        parsed_damages = []
        total_estimated_cost = 0
        
        for damage in damages:
            comments = damage.get('comments', '')
            parsed = {'damage_type': damage.get('damage_type', '')}
            
            try:
                if 'Location:' in comments:
                    parsed['location'] = comments.split('Location:')[1].split('|')[0].strip()
                if 'Severity:' in comments:
                    parsed['severity'] = comments.split('Severity:')[1].split('|')[0].strip()
                if 'Affected:' in comments:
                    parsed['affected'] = comments.split('Affected:')[1].split('|')[0].strip()
                if 'Cost:' in comments:
                    cost_str = comments.split('Cost:')[1].split('|')[0].strip()
                    # Extract numeric value from cost string
                    cost_num = ''.join(filter(str.isdigit, cost_str))
                    if cost_num:
                        total_estimated_cost += int(cost_num)
                        parsed['estimated_cost'] = cost_str
                
                parsed['description'] = comments.split('|')[-1].strip()
            except:
                parsed['description'] = comments
            
            parsed_damages.append(parsed)
        
        # Categorize by severity
        damages_by_severity = {}
        for damage in parsed_damages:
            severity = damage.get('severity', 'Unknown')
            if severity not in damages_by_severity:
                damages_by_severity[severity] = []
            damages_by_severity[severity].append(damage)
        
        return {
            "damage_assessments": parsed_damages,
            "damages_by_severity": damages_by_severity,
            "total_estimated_cost": f"${total_estimated_cost:,}",
            "total_damage_areas": len(damages)
        }
    
    # =========================================================================
    # SITUATION STATUS AND ANALYTICS
    # =========================================================================
    
    def get_situation_status(self) -> Dict[str, Any]:
        """Get comprehensive situation status and key metrics"""
        
        # Get all key information
        incidents = self.get_fire_incidents_overview()
        evacuation = self.get_evacuation_status()
        personnel = self.get_response_personnel()
        resources = self.get_resource_requests()
        damages = self.get_damage_assessments()
        
        # Calculate key metrics
        situation_metrics = {
            "alert_level": "EXTREME",
            "total_incidents": incidents.get("total_incidents", 0),
            "active_fire_zones": len([z for z in incidents.get("fire_zones", []) 
                                    if "Active Fire" in z.get("zone_type", "")]),
            "evacuation_zones": len([z for z in incidents.get("fire_zones", []) 
                                   if "Evacuation" in z.get("zone_type", "")]),
            "total_evacuees": evacuation.get("evacuation_summary", {}).get("total_evacuees", 0),
            "shelter_occupancy": evacuation.get("shelter_statistics", {}).get("occupancy_rate", 0),
            "response_personnel": personnel.get("total_personnel", 0),
            "resource_requests": resources.get("total_requests", 0),
            "damage_areas": damages.get("total_damage_areas", 0),
            "estimated_damages": damages.get("total_estimated_cost", "$0")
        }
        
        return {
            "situation_overview": situation_metrics,
            "incidents": incidents,
            "evacuation": evacuation,
            "personnel": personnel,
            "resources": resources,
            "damages": damages,
            "last_updated": datetime.now().isoformat()
        }
    
    def search_forest_fire_data(self, search_term: str) -> Dict[str, List[Dict]]:
        """Search across all forest fire related data"""
        
        results = {
            "incidents": [],
            "zones": [],
            "locations": [],
            "shelters": [],
            "personnel": [],
            "resources": [],
            "damages": []
        }
        
        # Search incidents
        incidents_query = """
        SELECT name, incident_type, status, description
        FROM incident 
        WHERE name LIKE ? OR description LIKE ? OR incident_type LIKE ?
        """
        results["incidents"] = self.execute_query(incidents_query, 
                                                 (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        # Search fire zones
        zones_query = """
        SELECT fz.name, fzt.name as type, fz.comments
        FROM fire_zone fz
        LEFT JOIN fire_zone_type fzt ON fz.zone_type_id = fzt.id
        WHERE fz.name LIKE ? OR fz.comments LIKE ? OR fzt.name LIKE ?
        """
        results["zones"] = self.execute_query(zones_query, 
                                            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        # Search locations
        locations_query = """
        SELECT name, comments, lat, lon
        FROM gis_location
        WHERE name LIKE ? OR comments LIKE ?
        """
        results["locations"] = self.execute_query(locations_query, 
                                                (f"%{search_term}%", f"%{search_term}%"))
        
        # Search shelters
        shelters_query = """
        SELECT name, status, comments
        FROM cr_shelter
        WHERE name LIKE ? OR comments LIKE ?
        """
        results["shelters"] = self.execute_query(shelters_query, 
                                               (f"%{search_term}%", f"%{search_term}%"))
        
        # Search personnel
        personnel_query = """
        SELECT first_name, last_name, comments
        FROM pr_person
        WHERE first_name LIKE ? OR last_name LIKE ? OR comments LIKE ?
        """
        results["personnel"] = self.execute_query(personnel_query, 
                                                (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        return results
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """Get information about a specific table structure"""
        
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def list_all_tables(self) -> List[str]:
        """List all tables in the database"""
        
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        result = self.execute_query(query)
        return [row['name'] for row in result]
    
    def execute_custom_query(self, query: str) -> List[Dict]:
        """Execute a custom SQL query (read-only)"""
        
        # Safety check - only allow SELECT queries
        query_upper = query.upper().strip()
        if not query_upper.startswith('SELECT'):
            return [{"error": "Only SELECT queries are allowed for safety"}]
        
        return self.execute_query(query)

# =============================================================================
# USAGE EXAMPLES AND TESTING
# =============================================================================

def test_forest_fire_database():
    """Test the forest fire database tool"""
    
    print("🌲🔥 TESTING FOREST FIRE DATABASE TOOL")
    print("=" * 50)
    
    db_tool = ForestFireDatabaseTool()
    
    if not db_tool.connect():
        print("❌ Failed to connect to database")
        return
    
    try:
        # Test 1: Get situation overview
        print("\n📊 SITUATION OVERVIEW:")
        status = db_tool.get_situation_status()
        metrics = status.get("situation_overview", {})
        
        print(f"Alert Level: {metrics.get('alert_level', 'Unknown')}")
        print(f"Active Incidents: {metrics.get('total_incidents', 0)}")
        print(f"Fire Zones: {metrics.get('active_fire_zones', 0)} active, {metrics.get('evacuation_zones', 0)} evacuation")
        print(f"Evacuees: {metrics.get('total_evacuees', 0)} people")
        print(f"Shelter Occupancy: {metrics.get('shelter_occupancy', 0)}%")
        print(f"Response Personnel: {metrics.get('response_personnel', 0)}")
        print(f"Estimated Damages: {metrics.get('estimated_damages', '$0')}")
        
        # Test 2: Get fire zones
        print("\n🔥 FIRE ZONES:")
        zones = db_tool.get_fire_zone_details()
        for zone in zones[:3]:  # Show first 3
            print(f"• {zone.get('zone_name', 'Unknown')} ({zone.get('zone_type', 'Unknown')})")
        
        # Test 3: Get evacuation status
        print("\n🏠 EVACUATION STATUS:")
        evacuation = db_tool.get_evacuation_status()
        shelter_stats = evacuation.get("shelter_statistics", {})
        print(f"Shelter Capacity: {shelter_stats.get('total_occupied', 0)}/{shelter_stats.get('total_capacity', 0)} ({shelter_stats.get('occupancy_rate', 0)}%)")
        print(f"Active Shelters: {evacuation.get('evacuation_summary', {}).get('active_shelters', 0)}")
        
        # Test 4: Search functionality
        print("\n🔍 SEARCH TEST - 'Pine Ridge':")
        search_results = db_tool.search_forest_fire_data("Pine Ridge")
        for category, results in search_results.items():
            if results:
                print(f"• {category.capitalize()}: {len(results)} results")
        
        print("\n✅ Database tool test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        db_tool.disconnect()

if __name__ == "__main__":
    test_forest_fire_database()
