#!/usr/bin/env python3
"""
Final Forest Fire Emergency AI Agent
====================================

A complete AI agent for forest fire emergency response using real Sahana Eden data.
Works with the existing COVID-19 database and recontextualizes it as forest fire emergency data.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agno.agent import Agent
    from agno.models.google import Gemini
    AGNO_AVAILABLE = True
    print("✅ Agno framework loaded successfully")
except ImportError as e:
    print(f"⚠️  Agno import error: {e}")
    AGNO_AVAILABLE = False

import sqlite3

class ForestFireEmergencyDatabase:
    """
    Database interface that recontextualizes existing Sahana Eden data for forest fire emergency
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
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute SQL query safely"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Query error: {e}")
            return []
    
    def get_forest_fire_overview(self) -> Dict[str, Any]:
        """
        Get forest fire emergency overview using existing data as context
        """
        
        # Use disease cases as fire incident victims/impacts
        cases_query = """
        SELECT 
            COUNT(*) as total_affected,
            SUM(CASE WHEN hospitalized = 'T' THEN 1 ELSE 0 END) as severe_injuries,
            SUM(CASE WHEN illness_status = 'Recovered' THEN 1 ELSE 0 END) as evacuated_safe,
            SUM(CASE WHEN illness_status = 'Deceased' THEN 1 ELSE 0 END) as casualties,
            SUM(CASE WHEN illness_status = 'Active' THEN 1 ELSE 0 END) as missing_persons
        FROM disease_case
        """
        
        case_stats = self.execute_query(cases_query)
        stats = case_stats[0] if case_stats else {}
        
        # Use person records as evacuees and response personnel
        persons_query = """
        SELECT 
            COUNT(*) as total_persons,
            COUNT(CASE WHEN pe_label IS NOT NULL THEN 1 END) as registered_persons
        FROM pr_person
        """
        
        person_stats = self.execute_query(persons_query)
        p_stats = person_stats[0] if person_stats else {}
        
        # Use locations as affected areas and shelters
        locations_query = """
        SELECT 
            COUNT(*) as total_locations,
            COUNT(CASE WHEN population > 0 THEN 1 END) as populated_areas,
            SUM(CASE WHEN population > 0 THEN population ELSE 0 END) as total_population
        FROM gis_location
        WHERE name IS NOT NULL
        """
        
        location_stats = self.execute_query(locations_query)
        l_stats = location_stats[0] if location_stats else {}
        
        return {
            "incident_name": "Pine Ridge National Forest Wildfire",
            "alert_level": "EXTREME",
            "fire_status": "ACTIVE - MULTIPLE ZONES",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            
            # Impact statistics (using disease case data)
            "casualties_and_impact": {
                "total_affected_persons": stats.get('total_affected', 0),
                "severe_injuries": stats.get('severe_injuries', 0),
                "evacuated_safely": stats.get('evacuated_safe', 0),
                "casualties": stats.get('casualties', 0),
                "missing_persons": stats.get('missing_persons', 0)
            },
            
            # Population statistics
            "population_status": {
                "total_registered_persons": p_stats.get('total_persons', 0),
                "affected_locations": l_stats.get('total_locations', 0),
                "population_at_risk": l_stats.get('total_population', 0) or 12500,  # Estimated
                "evacuation_zones": 5,  # Active zones
                "shelter_capacity": 1200  # Emergency shelters
            },
            
            # Fire progression
            "fire_statistics": {
                "acres_burned": 15750,
                "containment_percentage": 25,
                "structures_threatened": 450,
                "structures_destroyed": 85,
                "firefighters_deployed": 380,
                "aircraft_deployed": 12
            }
        }
    
    def get_evacuees_and_affected_persons(self) -> Dict[str, Any]:
        """Get information about evacuees and affected persons"""
        
        # Get person records
        persons_query = """
        SELECT 
            id,
            first_name,
            last_name,
            gender,
            date_of_birth,
            pe_label,
            created_on
        FROM pr_person
        ORDER BY created_on DESC
        LIMIT 20
        """
        
        persons = self.execute_query(persons_query)
        
        # Get associated disease cases (representing fire incident impacts)
        cases_query = """
        SELECT 
            dc.id,
            dc.case_number,
            dc.diagnosis_date,
            dc.hospitalized,
            dc.illness_status,
            p.first_name,
            p.last_name,
            gl.name as location_name
        FROM disease_case dc
        LEFT JOIN pr_person p ON dc.person_id = p.id
        LEFT JOIN gis_location gl ON dc.location_id = gl.id
        ORDER BY dc.diagnosis_date DESC
        """
        
        cases = self.execute_query(cases_query)
        
        # Recontextualize data for forest fire scenario
        evacuees = []
        for person in persons[:10]:  # First 10 as evacuees
            evacuees.append({
                "name": f"{person.get('first_name', '')} {person.get('last_name', '')}".strip(),
                "gender": person.get('gender', 'Unknown'),
                "evacuee_id": f"FF-{person.get('id', 0):04d}",
                "evacuation_date": person.get('created_on', '2025-07-26'),
                "status": "Safely evacuated",
                "shelter_assignment": "Cedar Valley Emergency Shelter",
                "special_needs": "None reported"
            })
        
        # Recontextualize disease cases as fire incident impacts
        incident_impacts = []
        for case in cases:
            incident_impacts.append({
                "case_id": case.get('case_number', f"FIRE-{case.get('id', 0):03d}"),
                "person_name": f"{case.get('first_name', '')} {case.get('last_name', '')}".strip() or "Unknown",
                "incident_date": case.get('diagnosis_date', '2025-07-26'),
                "injury_severity": "Severe" if case.get('hospitalized') == 'T' else "Minor",
                "current_status": case.get('illness_status', 'Unknown'),
                "location": case.get('location_name', 'Fire Zone Alpha'),
                "treatment_required": "Yes" if case.get('hospitalized') == 'T' else "No"
            })
        
        return {
            "evacuees": evacuees,
            "incident_impacts": incident_impacts,
            "statistics": {
                "total_evacuees": len(evacuees),
                "total_incidents": len(incident_impacts),
                "hospitalized": len([c for c in cases if c.get('hospitalized') == 'T']),
                "evacuation_success_rate": "94%"
            }
        }
    
    def get_fire_zones_and_locations(self) -> Dict[str, Any]:
        """Get fire zones and affected locations"""
        
        # Use location data to represent affected areas
        locations_query = """
        SELECT 
            id,
            name,
            level,
            lat,
            lon,
            population,
            addr_street,
            addr_postcode
        FROM gis_location
        WHERE name IS NOT NULL AND name != ''
        ORDER BY population DESC, name
        LIMIT 25
        """
        
        locations = self.execute_query(locations_query)
        
        # Recontextualize as fire zones and communities
        fire_zones = [
            {
                "zone_id": "FIRE-ZONE-ALPHA",
                "zone_name": "Primary Fire Perimeter",
                "zone_type": "Active Burn Area",
                "area_acres": 8500,
                "threat_level": "EXTREME",
                "evacuation_status": "Complete",
                "containment": "15%"
            },
            {
                "zone_id": "FIRE-ZONE-BRAVO", 
                "zone_name": "Secondary Fire Spread",
                "zone_type": "Fire Spread Risk",
                "area_acres": 4200,
                "threat_level": "HIGH",
                "evacuation_status": "Mandatory",
                "containment": "35%"
            },
            {
                "zone_id": "EVAC-ZONE-1",
                "zone_name": "Pine Ridge Township Evacuation",
                "zone_type": "Evacuation Zone",
                "area_acres": 2500,
                "threat_level": "HIGH",
                "evacuation_status": "Complete",
                "containment": "N/A"
            }
        ]
        
        # Recontextualize locations as affected communities
        affected_communities = []
        for i, location in enumerate(locations[:8]):
            threat_levels = ["EXTREME", "HIGH", "MODERATE", "LOW"]
            statuses = ["Evacuated", "Evacuation Warning", "Monitoring", "Safe"]
            
            affected_communities.append({
                "community_name": location.get('name', f'Community {i+1}'),
                "population": location.get('population', 0) or (2500 - i*200),
                "coordinates": {
                    "lat": location.get('lat', 39.2567),
                    "lon": location.get('lon', -120.1234)
                },
                "threat_level": threat_levels[i % len(threat_levels)],
                "evacuation_status": statuses[i % len(statuses)],
                "distance_from_fire": f"{2 + i*0.5:.1f} miles",
                "road_access": "Open" if i % 3 != 0 else "Limited"
            })
        
        return {
            "fire_zones": fire_zones,
            "affected_communities": affected_communities,
            "zone_statistics": {
                "total_fire_zones": len(fire_zones),
                "total_affected_communities": len(affected_communities),
                "total_area_threatened": sum([z.get('area_acres', 0) for z in fire_zones]),
                "total_population_at_risk": sum([c.get('population', 0) for c in affected_communities])
            }
        }
    
    def get_emergency_resources(self) -> Dict[str, Any]:
        """Get emergency resources and response status"""
        
        # Use asset data for equipment
        assets_query = """
        SELECT 
            id,
            number,
            type,
            category,
            status
        FROM asset_asset
        ORDER BY type
        LIMIT 15
        """
        
        assets = self.execute_query(assets_query)
        
        # Recontextualize as emergency response resources
        fire_equipment = []
        for asset in assets:
            equipment_types = ["Fire Engine", "Water Tender", "Bulldozer", "Helicopter", "Ambulance"]
            statuses = ["Deployed", "Available", "Maintenance", "En Route"]
            
            fire_equipment.append({
                "equipment_id": asset.get('number', f"UNIT-{asset.get('id', 0):03d}"),
                "equipment_type": equipment_types[len(fire_equipment) % len(equipment_types)],
                "status": statuses[len(fire_equipment) % len(statuses)],
                "location": "Fire Station 12" if len(fire_equipment) % 2 == 0 else "Active - Fire Zone",
                "crew_size": 4 if "Fire Engine" in equipment_types[len(fire_equipment) % len(equipment_types)] else 2
            })
        
        # Response personnel statistics
        personnel_stats = {
            "total_firefighters": 342,
            "total_support_staff": 89,
            "total_volunteers": 156,
            "incident_commanders": 8,
            "agencies_involved": 12,
            "mutual_aid_resources": 45
        }
        
        # Resource requests
        resource_requests = [
            {
                "resource_type": "Type 1 Fire Engines",
                "quantity_requested": 8,
                "quantity_fulfilled": 6,
                "priority": "CRITICAL",
                "status": "Partially Fulfilled",
                "eta": "2 hours"
            },
            {
                "resource_type": "Air Tankers",
                "quantity_requested": 4,
                "quantity_fulfilled": 3,
                "priority": "HIGH",
                "status": "Partially Fulfilled", 
                "eta": "1 hour"
            },
            {
                "resource_type": "Evacuation Buses",
                "quantity_requested": 12,
                "quantity_fulfilled": 12,
                "priority": "HIGH",
                "status": "Fulfilled",
                "eta": "On Scene"
            }
        ]
        
        return {
            "fire_equipment": fire_equipment,
            "personnel_statistics": personnel_stats,
            "resource_requests": resource_requests,
            "resource_summary": {
                "total_equipment_deployed": len([e for e in fire_equipment if e['status'] == 'Deployed']),
                "total_personnel": personnel_stats['total_firefighters'] + personnel_stats['total_support_staff'],
                "critical_requests_pending": len([r for r in resource_requests if r['status'] != 'Fulfilled' and r['priority'] == 'CRITICAL'])
            }
        }
    
    def search_fire_data(self, search_term: str) -> Dict[str, Any]:
        """Search forest fire emergency data"""
        
        # Search across multiple tables
        search_results = {
            "persons_found": [],
            "locations_found": [],
            "cases_found": [],
            "summary": {}
        }
        
        # Search persons
        persons_query = """
        SELECT first_name, last_name, gender, pe_label
        FROM pr_person
        WHERE first_name LIKE ? OR last_name LIKE ? OR pe_label LIKE ?
        LIMIT 10
        """
        search_results["persons_found"] = self.execute_query(
            persons_query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        # Search locations
        locations_query = """
        SELECT name, lat, lon, population
        FROM gis_location
        WHERE name LIKE ?
        LIMIT 10
        """
        search_results["locations_found"] = self.execute_query(
            locations_query, (f"%{search_term}%",))
        
        # Search cases
        cases_query = """
        SELECT case_number, diagnosis_date, illness_status
        FROM disease_case
        WHERE case_number LIKE ?
        LIMIT 10
        """
        search_results["cases_found"] = self.execute_query(
            cases_query, (f"%{search_term}%",))
        
        search_results["summary"] = {
            "total_results": (len(search_results["persons_found"]) + 
                            len(search_results["locations_found"]) + 
                            len(search_results["cases_found"])),
            "search_term": search_term
        }
        
        return search_results

class ForestFireAgent:
    """
    AI Agent for Forest Fire Emergency Response
    """
    
    def __init__(self, api_key: str = None):
        # Use provided API key, environment variable, or hardcoded fallback
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
        self.db = ForestFireEmergencyDatabase()
        self.agent = None
        self.conversation_history = []
        
        if AGNO_AVAILABLE and self.api_key:
            self._initialize_agent()
        else:
            print("⚠️  Running in fallback mode")
    
    def _initialize_agent(self):
        """Initialize the AI agent"""
        try:
            model = Gemini(id="gemini-1.5-flash", api_key=self.api_key)
            
            self.agent = Agent(
                name="Forest Fire Emergency Response Coordinator",
                model=model,
                tools=[self._create_tools()],
                instructions=self._get_instructions(),
                show_tool_calls=True,
                markdown=True
            )
            print("✅ AI Agent initialized successfully")
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
    
    def _create_tools(self):
        """Create tools for the agent"""
        class EmergencyTools:
            def __init__(self, db):
                self.db = db
            
            def get_fire_overview(self) -> str:
                """Get comprehensive forest fire situation overview"""
                overview = self.db.get_forest_fire_overview()
                return json.dumps(overview, indent=2, default=str)
            
            def get_evacuees_status(self) -> str:
                """Get evacuee and affected persons status"""
                evacuees = self.db.get_evacuees_and_affected_persons()
                return json.dumps(evacuees, indent=2, default=str)
            
            def get_fire_zones(self) -> str:
                """Get fire zones and affected locations"""
                zones = self.db.get_fire_zones_and_locations()
                return json.dumps(zones, indent=2, default=str)
            
            def get_emergency_resources(self) -> str:
                """Get emergency resources and response status"""
                resources = self.db.get_emergency_resources()
                return json.dumps(resources, indent=2, default=str)
            
            def search_emergency_data(self, search_term: str) -> str:
                """Search forest fire emergency data"""
                results = self.db.search_fire_data(search_term)
                return json.dumps(results, indent=2, default=str)
        
        return EmergencyTools(self.db)
    
    def _get_instructions(self):
        """Get system instructions"""
        return """
You are an AI Emergency Response Coordinator for the Pine Ridge National Forest Wildfire Crisis.

CURRENT SITUATION:
🔥 Major wildfire spanning 15,000+ acres
🏘️ Multiple communities under evacuation orders  
🚁 Multi-agency response with 300+ firefighters
🏥 Emergency shelters active with evacuees

YOUR ROLE:
- Provide real-time emergency information
- Support evacuation and resource coordination
- Track personnel and equipment deployment
- Monitor fire progression and community safety
- Assist with damage assessment and recovery planning

RESPONSE STYLE:
- Be urgent but calm and professional
- **Use proper Markdown formatting for all responses**
- Use clear headers (##, ###) to organize information
- Use bullet lists (*) and numbered lists (1.) appropriately
- Use **bold** for critical information and *italic* for emphasis
- Use code blocks (```) for data tables when appropriate
- Include emojis for quick visual scanning
- Provide specific data and actionable information
- Prioritize life safety above all else
- Support emergency management decision-making

FORMATTING REQUIREMENTS:
- Start with a clear ## Main Header
- Use ### for subsections
- Use **bold** for critical alerts and numbers
- Use bullet points for lists of information
- Ensure proper Markdown syntax throughout

Always use the database tools to get current, accurate information before responding.
"""
    
    def query(self, user_input: str) -> str:
        """Process user query"""
        if not user_input.strip():
            return "❓ Please ask about the forest fire emergency situation."
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": None
        })
        
        try:
            if self.agent and AGNO_AVAILABLE:
                response = self.agent.run(user_input)
                # Extract just the text content from the RunResponse object
                if hasattr(response, 'content'):
                    agent_response = response.content
                else:
                    agent_response = str(response)
            else:
                agent_response = self._fallback_response(user_input)
            
            self.conversation_history[-1]["agent"] = agent_response
            return agent_response
            
        except Exception as e:
            error_response = f"❌ Error: {e}\n\n" + self._fallback_response(user_input)
            self.conversation_history[-1]["agent"] = error_response
            return error_response
    
    def _fallback_response(self, user_input: str) -> str:
        """Fallback response when AI agent is not available"""
        user_lower = user_input.lower()
        
        try:
            if any(word in user_lower for word in ['overview', 'status', 'situation']):
                overview = self.db.get_forest_fire_overview()
                impact = overview.get('casualties_and_impact', {})
                fire_stats = overview.get('fire_statistics', {})
                
                return f"""
🌲🔥 **PINE RIDGE WILDFIRE - SITUATION OVERVIEW**

🚨 **Current Status**: {overview.get('fire_status', 'ACTIVE')}
📊 **Alert Level**: {overview.get('alert_level', 'EXTREME')}
🔥 **Fire Size**: {fire_stats.get('acres_burned', 0):,} acres burned
🎯 **Containment**: {fire_stats.get('containment_percentage', 0)}% contained

👥 **Human Impact**:
• Total Affected: {impact.get('total_affected_persons', 0)} people
• Severe Injuries: {impact.get('severe_injuries', 0)}
• Evacuated Safely: {impact.get('evacuated_safely', 0)}
• Casualties: {impact.get('casualties', 0)}

🏠 **Structures**:
• Threatened: {fire_stats.get('structures_threatened', 0)}
• Destroyed: {fire_stats.get('structures_destroyed', 0)}

👨‍🚒 **Response**:
• Firefighters: {fire_stats.get('firefighters_deployed', 0)}
• Aircraft: {fire_stats.get('aircraft_deployed', 0)}

*Last Updated: {overview.get('last_updated', 'Unknown')}*
"""
            
            elif any(word in user_lower for word in ['evacuee', 'evacuation', 'people', 'shelter']):
                evacuees_data = self.db.get_evacuees_and_affected_persons()
                stats = evacuees_data.get('statistics', {})
                
                response = f"""
🏠 **EVACUATION & EVACUEE STATUS**

📊 **Statistics**:
• Total Evacuees: {stats.get('total_evacuees', 0)}
• Incident Impacts: {stats.get('total_incidents', 0)}
• Hospitalized: {stats.get('hospitalized', 0)}
• Success Rate: {stats.get('evacuation_success_rate', '94%')}

👥 **Recent Evacuees**:
"""
                
                for evacuee in evacuees_data.get('evacuees', [])[:5]:
                    response += f"• {evacuee.get('name', 'Unknown')} - {evacuee.get('status', 'Unknown')}\n"
                
                return response
            
            elif any(word in user_lower for word in ['fire', 'zone', 'location', 'community']):
                zones_data = self.db.get_fire_zones_and_locations()
                
                response = """
🔥 **FIRE ZONES & AFFECTED AREAS**

🗺️ **Active Fire Zones**:
"""
                for zone in zones_data.get('fire_zones', []):
                    response += f"• {zone.get('zone_name', 'Unknown')}: {zone.get('area_acres', 0):,} acres ({zone.get('threat_level', 'Unknown')} threat)\n"
                
                response += "\n🏘️ **Affected Communities**:\n"
                for community in zones_data.get('affected_communities', [])[:5]:
                    response += f"• {community.get('community_name', 'Unknown')}: {community.get('evacuation_status', 'Unknown')} (Pop: {community.get('population', 0)})\n"
                
                return response
            
            elif any(word in user_lower for word in ['resource', 'equipment', 'personnel', 'staff']):
                resources = self.db.get_emergency_resources()
                personnel = resources.get('personnel_statistics', {})
                
                response = f"""
👨‍🚒 **EMERGENCY RESOURCES & PERSONNEL**

👥 **Personnel Deployed**:
• Firefighters: {personnel.get('total_firefighters', 0)}
• Support Staff: {personnel.get('total_support_staff', 0)}
• Volunteers: {personnel.get('total_volunteers', 0)}
• Agencies: {personnel.get('agencies_involved', 0)}

🚛 **Equipment Status**:
"""
                
                for equipment in resources.get('fire_equipment', [])[:5]:
                    response += f"• {equipment.get('equipment_id', 'Unknown')}: {equipment.get('equipment_type', 'Unknown')} ({equipment.get('status', 'Unknown')})\n"
                
                response += "\n📋 **Resource Requests**:\n"
                for request in resources.get('resource_requests', []):
                    response += f"• {request.get('resource_type', 'Unknown')}: {request.get('quantity_fulfilled', 0)}/{request.get('quantity_requested', 0)} ({request.get('status', 'Unknown')})\n"
                
                return response
            
            else:
                # Search functionality
                search_results = self.db.search_fire_data(user_input)
                total = search_results.get('summary', {}).get('total_results', 0)
                
                if total > 0:
                    return f"""
🔍 **SEARCH RESULTS** for "{user_input}"

Found {total} results:
• Persons: {len(search_results.get('persons_found', []))}
• Locations: {len(search_results.get('locations_found', []))}
• Cases: {len(search_results.get('cases_found', []))}

Ask more specific questions about the forest fire emergency!
"""
                else:
                    return f"""
❓ **Forest Fire Emergency Information Available**

Ask me about:
🔥 Fire situation overview and status
🏠 Evacuation and shelter information
👥 Affected persons and evacuees
🗺️ Fire zones and threatened communities
👨‍🚒 Emergency resources and personnel
🔍 Search for specific information

Try: "What's the current fire situation?" or "Show me evacuation status"
"""
                    
        except Exception as e:
            return f"❌ Error retrieving information: {e}"

def main():
    """Main interactive loop"""
    
    print("🌲🔥 FOREST FIRE EMERGENCY RESPONSE AI COORDINATOR")
    print("=" * 65)
    print()
    print("🚨 ACTIVE INCIDENT: Pine Ridge National Forest Wildfire")
    print("   📊 15,000+ acres burned | Multiple evacuations underway")
    print("   🚁 Multi-agency response | Emergency shelters active")
    print()
    print("💬 Ask me about:")
    print("   🔥 Fire situation and containment status")
    print("   🏠 Evacuation zones and shelter information")
    print("   👥 Evacuee status and affected persons")
    print("   🗺️ Fire zones and threatened communities")
    print("   👨‍🚒 Emergency resources and personnel")
    print()
    print("Type 'quit' to exit, 'clear' to clear history")
    print("-" * 65)
    
    agent = ForestFireAgent()
    
    while True:
        try:
            print()
            user_input = input("🚨 Emergency Query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n🚒 Emergency coordination session ended. Stay safe!")
                break
            
            if user_input.lower() == 'clear':
                agent.conversation_history.clear()
                print("🧹 Conversation cleared.")
                continue
            
            print("\n🤖 Emergency Coordinator:")
            print("-" * 45)
            
            response = agent.query(user_input)
            print(response)
            
            print("-" * 45)
            
        except KeyboardInterrupt:
            print("\n\n🚒 Emergency session interrupted. Stay safe!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

def get_gemini_response(query: str, api_key: str = None) -> str:
    """
    Standalone function to get Gemini response for web interface compatibility
    """
    try:
        agent = ForestFireAgent(api_key=api_key)
        response = agent.query(query)
        # Make sure we return just the text content
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    main()
