#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
    print("Google Generative AI loaded successfully")
except Exception as e:
    print(f"Google AI import error: {e}")
    GOOGLE_AI_AVAILABLE = False

try:
    from agno.agent import Agent
    from agno.models.google import Gemini
    AGNO_AVAILABLE = True
    print("Agno framework loaded successfully")
except Exception as e:
    print(f"Agno import error: {e}")
    AGNO_AVAILABLE = False

# Alternative AI using requests to Gemini API directly
try:
    import requests
    REQUESTS_AVAILABLE = True
    print("Requests library available for direct API calls")
except Exception as e:
    print(f"Requests import error: {e}")
    REQUESTS_AVAILABLE = False

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
        self.gemini_model = None
        self.conversation_history = []
        self.mode = "fallback"  # Track current operating mode
        
        # Try to initialize AI in order of preference
        self._initialize_ai()
    
    def _initialize_ai(self):
        """Initialize AI with fallback priority: Direct API > Google AI > Agno > Fallback"""
        
        # Try direct API first (most reliable)
        if REQUESTS_AVAILABLE and self.api_key:
            try:
                # Test the API connection
                test_response = self._test_gemini_direct_api()
                if test_response:
                    self.mode = "gemini_direct_api"
                    print("Direct Gemini API initialized successfully")
                    return
            except Exception as e:
                print(f"Direct API test failed: {e}")
        
        # Try Google AI library
        if GOOGLE_AI_AVAILABLE and self.api_key:
            try:
                self._initialize_google_ai()
                return
            except Exception as e:
                print(f"Google AI init failed: {e}")
        
        # Try Agno framework
        if AGNO_AVAILABLE and self.api_key:
            try:
                self._initialize_agent()
                return
            except Exception as e:
                print(f"Agno init failed: {e}")
        
        # Fallback mode
        self.mode = "fallback"
        print("Running in enhanced fallback mode")
    
    def _test_gemini_direct_api(self) -> bool:
        """Test if direct API access works"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "Test"}]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            return response.status_code == 200
        except:
            return False
    
    def _initialize_google_ai(self):
        """Initialize direct Google Generative AI"""
        try:
            import google.generativeai as genai_local
            genai_local.configure(api_key=self.api_key)
            self.gemini_model = genai_local.GenerativeModel('gemini-1.5-flash')
            self.mode = "google_ai"
            print("Google Generative AI initialized successfully")
        except Exception as e:
            print(f"Google AI initialization failed: {e}")
            raise
    
    def _initialize_agent(self):
        """Initialize the Agno AI agent"""
        try:
            model = Gemini(id="gemini-1.5-flash", api_key=self.api_key)
            
            self.agent = Agent(
                name="Forest Fire Emergency Response Coordinator",
                model=model,
                instructions=self._get_instructions(),
                show_tool_calls=True,
                markdown=True
            )
            self.mode = "agno"
            print("Agno AI agent initialized successfully")
        except Exception as e:
            print(f"Agent initialization failed: {e}")
            raise
    
    def get_mode(self) -> str:
        """Get current AI mode"""
        return self.mode
    
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
- Use proper Markdown formatting for all responses
- Use clear headers (##, ###) to organize information
- Use bullet lists (*) and numbered lists (1.) appropriately
- Use **bold** for critical information and *italic* for emphasis
- Include emojis for quick visual scanning
- Provide specific data and actionable information
- Prioritize life safety above all else
- Support emergency management decision-making

Always provide current, accurate information based on database queries.
"""
    
    def query(self, user_input: str) -> str:
        """Process user query"""
        if not user_input.strip():
            return "Please ask about the forest fire emergency situation."
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": None,
            "mode": self.mode
        })
        
        try:
            # Route to appropriate AI method based on mode
            if self.mode == "gemini_direct_api":
                agent_response = self._query_gemini_direct_api(user_input)
            elif self.mode == "google_ai" and self.gemini_model:
                agent_response = self._query_google_ai(user_input)
            elif self.mode == "agno" and self.agent:
                response = self.agent.run(user_input)
                agent_response = response.content if hasattr(response, 'content') else str(response)
            else:
                agent_response = self._fallback_response(user_input)
            
            self.conversation_history[-1]["agent"] = agent_response
            return agent_response
            
        except Exception as e:
            error_response = f"Error: {e}\n\n" + self._fallback_response(user_input)
            self.conversation_history[-1]["agent"] = error_response
            return error_response
    
    def _query_google_ai(self, user_input: str) -> str:
        """Query using Google's Generative AI directly"""
        try:
            # Get current fire data
            fire_overview = self.db.get_forest_fire_overview()
            
            # Create context-aware prompt
            context_prompt = f"""You are an AI Emergency Response Coordinator for the Pine Ridge National Forest Wildfire Crisis.

CURRENT SITUATION:
🔥 {fire_overview.get('incident_name', 'Major wildfire')}
📊 Alert Level: {fire_overview.get('alert_level', 'EXTREME')}
🔥 Status: {fire_overview.get('fire_status', 'ACTIVE')}
🏠 Structures Threatened: {fire_overview.get('fire_statistics', {}).get('structures_threatened', 0)}
👥 Total Affected: {fire_overview.get('casualties_and_impact', {}).get('total_affected_persons', 0)} people
👨‍🚒 Firefighters Deployed: {fire_overview.get('fire_statistics', {}).get('firefighters_deployed', 0)}

USER QUESTION: {user_input}

Provide a professional, urgent but calm response with proper Markdown formatting.

RESPONSE:"""
            
            response = self.gemini_model.generate_content(context_prompt)
            return response.text
            
        except Exception as e:
            return f"Gemini AI Error: {str(e)}\n\n" + self._fallback_response(user_input)
    
    def _query_gemini_direct_api(self, user_input: str) -> str:
        """Query Gemini using direct HTTP API"""
        try:
            # Get current fire data for context
            fire_overview = self.db.get_forest_fire_overview()
            
            # Create context-aware prompt
            context_prompt = f"""You are an AI Emergency Response Coordinator for the Pine Ridge National Forest Wildfire Crisis.

CURRENT SITUATION:
🔥 {fire_overview.get('incident_name', 'Major wildfire')}
📊 Alert Level: {fire_overview.get('alert_level', 'EXTREME')}
🔥 Status: {fire_overview.get('fire_status', 'ACTIVE')}
🏠 Structures Threatened: {fire_overview.get('fire_statistics', {}).get('structures_threatened', 0)}
👥 Total Affected: {fire_overview.get('casualties_and_impact', {}).get('total_affected_persons', 0)} people
👨‍🚒 Firefighters Deployed: {fire_overview.get('fire_statistics', {}).get('firefighters_deployed', 0)}

USER QUESTION: {user_input}

Provide a professional, urgent but calm response with proper Markdown formatting.

RESPONSE:"""
            
            # Gemini API endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": context_prompt}]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    if "content" in result["candidates"][0]:
                        if "parts" in result["candidates"][0]["content"]:
                            if len(result["candidates"][0]["content"]["parts"]) > 0:
                                gemini_text = result["candidates"][0]["content"]["parts"][0]["text"]
                                return f"## 🤖 **AI RESPONSE (Gemini Active)**\n\n{gemini_text}"
            
            # If API call failed, use enhanced fallback
            return f"**AI API temporarily unavailable. Using local emergency data:**\n\n" + self._fallback_response(user_input)
            
        except Exception as e:
            return f"**Direct API Error:** {str(e)}\n\n" + self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> str:
        """Enhanced fallback response using local data"""
        user_lower = user_input.lower()
        
        try:
            if any(word in user_lower for word in ['overview', 'status', 'situation']):
                overview = self.db.get_forest_fire_overview()
                impact = overview.get('casualties_and_impact', {})
                fire_stats = overview.get('fire_statistics', {})
                
                return f"""## 🌲🔥 **PINE RIDGE WILDFIRE - SITUATION OVERVIEW**

🚨 **Current Status**: {overview.get('fire_status', 'ACTIVE')}  
📊 **Alert Level**: {overview.get('alert_level', 'EXTREME')}  
🔥 **Fire Size**: {fire_stats.get('acres_burned', 0):,} acres burned  
🎯 **Containment**: {fire_stats.get('containment_percentage', 0)}% contained  

### 👥 **Human Impact**
• Total Affected: **{impact.get('total_affected_persons', 0)}** people  
• Severe Injuries: **{impact.get('severe_injuries', 0)}**  
• Evacuated Safely: **{impact.get('evacuated_safely', 0)}**  
• Casualties: **{impact.get('casualties', 0)}**  

### 🏠 **Structures**
• Threatened: **{fire_stats.get('structures_threatened', 0)}**  
• Destroyed: **{fire_stats.get('structures_destroyed', 0)}**  

### 👨‍🚒 **Response**
• Firefighters: **{fire_stats.get('firefighters_deployed', 0)}**  
• Aircraft: **{fire_stats.get('aircraft_deployed', 0)}**  

*Last Updated: {overview.get('last_updated', 'Unknown')}*"""
            
            elif any(word in user_lower for word in ['evacuee', 'evacuation', 'people', 'shelter']):
                evacuees_data = self.db.get_evacuees_and_affected_persons()
                stats = evacuees_data.get('statistics', {})
                
                response = f"""## 🏠 **EVACUATION & EVACUEE STATUS**

### 📊 **Statistics**
• Total Evacuees: **{stats.get('total_evacuees', 0)}**  
• Incident Impacts: **{stats.get('total_incidents', 0)}**  
• Hospitalized: **{stats.get('hospitalized', 0)}**  
• Success Rate: **{stats.get('evacuation_success_rate', '94%')}**  

### 👥 **Recent Evacuees**
"""
                
                for evacuee in evacuees_data.get('evacuees', [])[:5]:
                    response += f"• **{evacuee.get('name', 'Unknown')}** - {evacuee.get('status', 'Unknown')}\n"
                
                return response
            
            else:
                return f"""## ❓ **Forest Fire Emergency Information Available**

**Ask me about:**
• 🔥 Fire situation overview and status  
• 🏠 Evacuation and shelter information  
• 👥 Affected persons and evacuees  
• 🗺️ Fire zones and threatened communities  
• 👨‍🚒 Emergency resources and personnel  

**Try:** "What's the current fire situation?" or "Show me evacuation status"

*Current Mode: {self.mode.title()}*"""
                    
        except Exception as e:
            return f"Error retrieving information: {e}"

def get_gemini_response(query: str, api_key: str = None) -> str:
    """
    Standalone function to get Gemini response for web interface compatibility
    """
    try:
        agent = ForestFireAgent(api_key=api_key)
        response = agent.query(query)
        return str(response)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Forest Fire Emergency AI Agent")
    agent = ForestFireAgent()
    print(f"Agent initialized in {agent.get_mode()} mode")
