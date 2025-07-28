#!/usr/bin/env python3
"""
🌲🔥 FOREST FIRE EMERGENCY RESPONSE WEB INTERFACE
==================================================

Flask web application for the Forest Fire Emergency Response System.
Provides a user-friendly web interface for emergency coordinators to interact
with the AI agent and access real-time fire emergency data.

Features:
- Real-time fire status dashboard
- Natural language query interface with Gemini AI  
- Emergency metrics and visualizations
- Mobile-responsive design
- Professional emergency management styling

Updated: Fixed AI response formatting for clean output
"""

from flask import Flask, render_template, request, jsonify, session
import os
import sys
import json
from datetime import datetime
import sqlite3
import traceback

# Import our existing forest fire tools
sys.path.append(os.path.dirname(__file__))
try:
    from realistic_forest_fire_tool import RealisticForestFireDatabaseTool
    print("✅ Database tool imported successfully")
except ImportError as e:
    print(f"Warning: Could not import database tool: {e}")
    RealisticForestFireDatabaseTool = None

try:
    from final_forest_fire_agent import ForestFireAgent, get_gemini_response
    print("✅ AI agent imported successfully")
except ImportError as e:
    print(f"Warning: Could not import AI components: {e}")
    ForestFireAgent = None
    get_gemini_response = None

app = Flask(__name__)
app.secret_key = 'forest_fire_emergency_2025_secret_key'

# Global instances
db_tool = None
ai_agent = None

def initialize_components():
    """Initialize database and AI components"""
    global db_tool, ai_agent
    
    try:
        # Initialize database tool
        if RealisticForestFireDatabaseTool:
            db_tool = RealisticForestFireDatabaseTool()
            # Test the connection
            if db_tool.connect():
                print("✅ Database tool initialized and connected")
                db_tool.disconnect()
            else:
                print("⚠️ Database tool initialized but connection failed")
        else:
            db_tool = None
            print("⚠️ Database tool not available - using fallback mode")
        
        # Initialize AI agent if available
        if ForestFireAgent:
            # Use the API key from the agent
            ai_agent = ForestFireAgent(api_key="AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI")
            print("✅ AI agent initialized")
        else:
            ai_agent = None
            print("⚠️ AI agent not available - using fallback mode")
            
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        traceback.print_exc()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Get emergency overview data
        overview_data = get_emergency_overview()
        return render_template('dashboard.html', data=overview_data)
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        return render_template('dashboard.html', data={}, error=str(e))

@app.route('/chat')
def chat_interface():
    """Natural language chat interface"""
    return render_template('chat.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle natural language queries from the web interface"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Try AI agent first, then fallback to pattern matching
        response = None
        
        if ai_agent and get_gemini_response:
            try:
                response = ai_agent.query(query)
            except Exception as e:
                print(f"AI agent error: {e}")
                response = None
        
        # Fallback to pattern matching
        if not response:
            response = handle_query_fallback(query)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'query': query
        })
        
    except Exception as e:
        print(f"Query handling error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

def handle_query_fallback(query):
    """Fallback query handling using pattern matching"""
    query_lower = query.lower()
    
    try:
        if any(word in query_lower for word in ['fire', 'situation', 'status', 'current']):
            return get_fire_status_response()
        elif any(word in query_lower for word in ['evacuation', 'evacuees', 'displaced']):
            return get_evacuation_response()
        elif any(word in query_lower for word in ['casualties', 'injured', 'victims', 'affected']):
            return get_casualties_response()
        elif any(word in query_lower for word in ['resources', 'personnel', 'equipment']):
            return get_resources_response()
        elif any(word in query_lower for word in ['shelter', 'shelters', 'accommodation']):
            return get_shelters_response()
        elif any(word in query_lower for word in ['overview', 'summary', 'report']):
            return get_overview_response()
        else:
            return get_general_help_response()
    except Exception as e:
        return f"Error processing query: {str(e)}"

def get_fire_status_response():
    """Get fire status information"""
    if not db_tool:
        return "Database not available"
    
    overview = db_tool.get_emergency_overview()
    
    response = "🌲🔥 **PINE RIDGE WILDFIRE - CURRENT STATUS**\n\n"
    response += f"🚨 **Alert Level:** EXTREME\n"
    response += f"🔥 **Fire Size:** 15,750 acres burned\n"
    response += f"🎯 **Containment:** 25% contained\n"
    response += f"📅 **Date:** {overview.get('incident_date', 'July 28, 2025')}\n\n"
    response += f"📊 **Key Metrics:**\n"
    response += f"• Total Affected: {overview.get('total_affected', 25)} people\n"
    response += f"• Active Firefighters: 380\n"
    response += f"• Aircraft Deployed: 12\n"
    response += f"• Communities Threatened: 8\n\n"
    response += f"🌍 **Environmental Impact:**\n"
    response += f"• Air Quality: HAZARDOUS\n"
    response += f"• Wildlife Affected: 1,000+ animals\n"
    response += f"• Carbon Emissions: 50,000+ tons CO2"
    
    return response

def get_evacuation_response():
    """Get evacuation information"""
    if not db_tool:
        return "Database not available"
    
    people_data = db_tool.get_affected_persons()
    locations_data = db_tool.get_locations_and_facilities()
    
    people = people_data.get('affected_people', []) if people_data else []
    
    response = "🏠 **EVACUATION STATUS REPORT**\n\n"
    response += f"👥 **Evacuees:** {len(people)} registered evacuees\n"
    response += f"🏢 **Active Shelters:** 4 emergency shelters\n"
    response += f"🚨 **Evacuation Zones:**\n"
    response += f"• Zone A (Pine Ridge Township): MANDATORY\n"
    response += f"• Zone B (Cedar Valley Village): MANDATORY\n"
    response += f"• Zone C (Mountain View Estates): WARNING\n\n"
    
    if people:
        response += f"📋 **Recent Evacuees:**\n"
        for person in people[:5]:
            name = f"{person.get('first_name', '')} {person.get('last_name', '')}"
            response += f"• {name.strip()}\n"
    
    response += f"\n🏠 **Shelter Capacity:** 1,050 total beds\n"
    response += f"📊 **Current Occupancy:** 839 people (80% full)"
    
    return response

def get_casualties_response():
    """Get casualties and affected people information"""
    if not db_tool:
        return "Database not available"
    
    people_data = db_tool.get_affected_persons()
    people = people_data.get('affected_people', []) if people_data else []
    
    response = "🏥 **CASUALTIES & AFFECTED PERSONS**\n\n"
    response += f"👥 **Total Affected:** {len(people)} people\n"
    response += f"🚨 **Casualties Breakdown:**\n"
    response += f"• Severe Injuries: 7 hospitalized\n"
    response += f"• Minor Injuries: 12 treated and released\n"
    response += f"• Missing Persons: 2 (search ongoing)\n"
    response += f"• Fatalities: 4 confirmed\n\n"
    response += f"🏥 **Medical Response:**\n"
    response += f"• Field Medical Units: 3 active\n"
    response += f"• Ambulances: 8 on standby\n"
    response += f"• Medical Personnel: 25 deployed\n\n"
    
    if people:
        response += f"📋 **Affected Individuals:**\n"
        for person in people[:5]:
            name = f"{person.get('first_name', '')} {person.get('last_name', '')}"
            comments = person.get('comments', '')
            if 'Age:' in comments:
                age_info = comments.split('Age:')[1].split('|')[0].strip()
                response += f"• {name.strip()} (Age: {age_info})\n"
            else:
                response += f"• {name.strip()}\n"
    
    return response

def get_resources_response():
    """Get resource deployment information"""
    response = "👨‍🚒 **RESOURCE DEPLOYMENT STATUS**\n\n"
    response += f"🔥 **Firefighting Resources:**\n"
    response += f"• Firefighters: 380 personnel\n"
    response += f"• Fire Engines: 45 units\n"
    response += f"• Bulldozers: 15 units\n"
    response += f"• Hand Crews: 12 teams\n\n"
    response += f"🚁 **Aviation Resources:**\n"
    response += f"• Helicopters: 12 aircraft\n"
    response += f"• Air Tankers: 8 aircraft\n"
    response += f"• Water Drops: 150+ sorties\n\n"
    response += f"👮 **Support Personnel:**\n"
    response += f"• Law Enforcement: 50 officers\n"
    response += f"• Emergency Medical: 25 EMTs\n"
    response += f"• Public Works: 30 personnel\n"
    response += f"• Volunteers: 200+ active\n\n"
    response += f"📊 **Resource Status:**\n"
    response += f"• Deployment Rate: 85% of available resources\n"
    response += f"• Mutual Aid: 6 agencies responding\n"
    response += f"• National Guard: Requested, pending approval"
    
    return response

def get_shelters_response():
    """Get shelter information"""
    if not db_tool:
        return "Database not available"
    
    locations_data = db_tool.get_locations_and_facilities()
    
    response = "🏠 **EMERGENCY SHELTERS STATUS**\n\n"
    response += f"🏢 **Active Shelters:** 4 facilities\n\n"
    
    shelter_data = [
        {"name": "Cedar Valley Elementary School", "capacity": 300, "current": 245, "services": "Food, Medical, Pet Care"},
        {"name": "Mountain View Community Center", "capacity": 150, "current": 127, "services": "Food, Medical"},
        {"name": "Regional Sports Complex", "capacity": 500, "current": 378, "services": "Food, Medical, Childcare, Pet Care"},
        {"name": "Riverside Church Shelter", "capacity": 100, "current": 89, "services": "Food, Counseling"}
    ]
    
    for shelter in shelter_data:
        occupancy = int((shelter["current"] / shelter["capacity"]) * 100)
        response += f"📍 **{shelter['name']}**\n"
        response += f"• Capacity: {shelter['capacity']} people\n"
        response += f"• Current: {shelter['current']} people ({occupancy}% full)\n"
        response += f"• Services: {shelter['services']}\n\n"
    
    total_capacity = sum(s["capacity"] for s in shelter_data)
    total_current = sum(s["current"] for s in shelter_data)
    overall_occupancy = int((total_current / total_capacity) * 100)
    
    response += f"📊 **Overall Status:**\n"
    response += f"• Total Capacity: {total_capacity} people\n"
    response += f"• Current Occupancy: {total_current} people ({overall_occupancy}% full)\n"
    response += f"• Available Space: {total_capacity - total_current} people"
    
    return response

def get_overview_response():
    """Get comprehensive overview"""
    if not db_tool:
        return "Database not available"
    
    overview = db_tool.get_emergency_overview()
    
    response = "📊 **COMPREHENSIVE EMERGENCY OVERVIEW**\n\n"
    response += f"🌲🔥 **PINE RIDGE WILDFIRE CRISIS**\n"
    response += f"📅 Date: July 28, 2025\n"
    response += f"📍 Location: Pine Ridge National Forest, CA-NV Border\n\n"
    response += f"🔥 **Fire Status:**\n"
    response += f"• Size: 15,750 acres burned\n"
    response += f"• Containment: 25%\n"
    response += f"• Alert Level: EXTREME\n"
    response += f"• Growth Rate: 500 acres/hour\n\n"
    response += f"👥 **Human Impact:**\n"
    response += f"• Total Affected: {overview.get('total_affected', 25)} people\n"
    response += f"• Evacuees: 4,500 displaced\n"
    response += f"• Casualties: 15 injuries, 2 missing, 4 fatalities\n"
    response += f"• Sheltered: 839 people in 4 facilities\n\n"
    response += f"🏠 **Property Impact:**\n"
    response += f"• Homes Destroyed: 85\n"
    response += f"• Homes Threatened: 450\n"
    response += f"• Infrastructure: Highway 101 closed, power outages\n\n"
    response += f"👨‍🚒 **Response Resources:**\n"
    response += f"• Personnel: 380 firefighters, 200+ support\n"
    response += f"• Aircraft: 12 helicopters, 8 air tankers\n"
    response += f"• Ground Units: 45 engines, 15 bulldozers\n\n"
    response += f"🌍 **Environmental:**\n"
    response += f"• Air Quality: HAZARDOUS (AQI 300+)\n"
    response += f"• Wildlife: 1,000+ animals affected\n"
    response += f"• Emissions: 50,000+ tons CO2"
    
    return response

def get_general_help_response():
    """Get general help information"""
    response = "❓ **FOREST FIRE EMERGENCY SYSTEM HELP**\n\n"
    response += f"🔍 **Available Queries:**\n"
    response += f"• Fire status and containment information\n"
    response += f"• Evacuation zones and evacuee status\n"
    response += f"• Casualties and affected persons\n"
    response += f"• Resource deployment and personnel\n"
    response += f"• Emergency shelter information\n"
    response += f"• Comprehensive situation reports\n\n"
    response += f"💡 **Example Questions:**\n"
    response += f"• 'What's the current fire situation?'\n"
    response += f"• 'Show me evacuation status'\n"
    response += f"• 'How many people are affected?'\n"
    response += f"• 'What resources are deployed?'\n"
    response += f"• 'Give me a complete overview'\n\n"
    response += f"🆘 **Emergency Contacts:**\n"
    response += f"• Incident Command: (555) 123-4567\n"
    response += f"• Public Information: (555) 123-4568\n"
    response += f"• Evacuation Hotline: (555) 123-4569"
    
    return response

@app.route('/api/overview')
def api_overview():
    """API endpoint for emergency overview data"""
    try:
        overview_data = get_emergency_overview()
        return jsonify(overview_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_emergency_overview():
    """Get comprehensive emergency overview data"""
    try:
        if db_tool:
            overview = db_tool.get_emergency_overview()
            people_data = db_tool.get_affected_persons()
            people = people_data.get('affected_people', []) if people_data else []
            
            return {
                'incident_name': 'Pine Ridge Wildfire Crisis',
                'incident_date': 'July 28, 2025',
                'fire_size_acres': 15750,
                'containment_percent': 25,
                'alert_level': 'EXTREME',
                'total_affected': len(people) if people else 25,
                'total_evacuees': 4500,
                'total_shelters': 4,
                'firefighters': 380,
                'aircraft': 12,
                'homes_destroyed': 85,
                'homes_threatened': 450,
                'last_updated': datetime.now().isoformat()
            }
        else:
            # Fallback data
            return {
                'incident_name': 'Pine Ridge Wildfire Crisis',
                'incident_date': 'July 28, 2025',
                'fire_size_acres': 15750,
                'containment_percent': 25,
                'alert_level': 'EXTREME',
                'total_affected': 25,
                'total_evacuees': 4500,
                'total_shelters': 4,
                'firefighters': 380,
                'aircraft': 12,
                'homes_destroyed': 85,
                'homes_threatened': 450,
                'last_updated': datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Error getting overview: {e}")
        return {}

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    print("🌲🔥 FOREST FIRE EMERGENCY WEB INTERFACE")
    print("=" * 50)
    print("🚀 Initializing components...")
    
    initialize_components()
    
    print("🌐 Starting web server...")
    print("📱 Access the interface at: http://localhost:5000")
    print("💡 Dashboard: http://localhost:5000/")
    print("💬 Chat Interface: http://localhost:5000/chat")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
