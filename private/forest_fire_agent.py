#!/usr/bin/env python3
"""
Forest Fire Emergency Response AI Agent
=======================================

An intelligent conversational agent for forest fire emergency response management.
Uses Gemini AI to provide natural language interaction with comprehensive forest
fire incident data including evacuations, resources, damages, and response coordination.

Features:
- Natural language queries about fire incidents
- Real-time evacuation and shelter status
- Resource deployment and personnel tracking  
- Damage assessment and impact analysis
- Multi-agency coordination support
- Emergency decision support
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agno import Agent
    from agno.models.gemini import Gemini
    from forest_fire_database_tool import ForestFireDatabaseTool
    AGNO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Agno import error: {e}")
    AGNO_AVAILABLE = False
    # Fallback imports
    import json
    import re

class ForestFireEmergencyAgent:
    """
    AI Agent for Forest Fire Emergency Response Management
    """
    
    def __init__(self, api_key: str = None, model_type: str = "gemini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_type = model_type
        self.db_tool = ForestFireDatabaseTool()
        self.agent = None
        self.conversation_history = []
        
        # Initialize the AI agent
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the AI agent with proper configuration"""
        
        if not AGNO_AVAILABLE:
            print("⚠️  Running in fallback mode without Agno framework")
            return
        
        if not self.api_key:
            print("⚠️  No API key found. Please set GEMINI_API_KEY environment variable")
            return
        
        try:
            # Configure the AI model
            if self.model_type == "gemini":
                model = Gemini(
                    id="gemini-1.5-flash",
                    api_key=self.api_key
                )
            else:
                raise ValueError(f"Unsupported model type: {self.model_type}")
            
            # Create the agent with forest fire tools
            self.agent = Agent(
                name="Forest Fire Emergency Response Agent",
                model=model,
                tools=[self._create_forest_fire_tools()],
                instructions=self._get_system_instructions(),
                show_tool_calls=True,
                markdown=True,
            )
            
            print("✅ AI Agent initialized successfully")
            
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            self.agent = None
    
    def _create_forest_fire_tools(self):
        """Create forest fire emergency management tools for the agent"""
        
        class ForestFireTools:
            def __init__(self, db_tool):
                self.db_tool = db_tool
            
            def get_situation_overview(self) -> str:
                """Get comprehensive forest fire situation overview and status"""
                try:
                    status = self.db_tool.get_situation_status()
                    return json.dumps(status, indent=2, default=str)
                except Exception as e:
                    return f"Error getting situation overview: {e}"
            
            def get_fire_incidents(self) -> str:
                """Get information about active forest fire incidents"""
                try:
                    incidents = self.db_tool.get_fire_incidents_overview()
                    return json.dumps(incidents, indent=2, default=str)
                except Exception as e:
                    return f"Error getting fire incidents: {e}"
            
            def get_fire_zones(self, zone_name: str = None) -> str:
                """Get detailed information about fire zones and affected areas"""
                try:
                    zones = self.db_tool.get_fire_zone_details(zone_name)
                    return json.dumps(zones, indent=2, default=str)
                except Exception as e:
                    return f"Error getting fire zones: {e}"
            
            def get_evacuation_status(self) -> str:
                """Get evacuation status, shelter information, and evacuee details"""
                try:
                    evacuation = self.db_tool.get_evacuation_status()
                    return json.dumps(evacuation, indent=2, default=str)
                except Exception as e:
                    return f"Error getting evacuation status: {e}"
            
            def get_shelter_details(self, shelter_name: str = None) -> str:
                """Get detailed information about emergency shelters"""
                try:
                    shelters = self.db_tool.get_shelter_details(shelter_name)
                    return json.dumps(shelters, indent=2, default=str)
                except Exception as e:
                    return f"Error getting shelter details: {e}"
            
            def get_response_personnel(self) -> str:
                """Get information about response personnel and volunteers"""
                try:
                    personnel = self.db_tool.get_response_personnel()
                    return json.dumps(personnel, indent=2, default=str)
                except Exception as e:
                    return f"Error getting personnel information: {e}"
            
            def get_resource_requests(self) -> str:
                """Get resource requests and deployment status"""
                try:
                    resources = self.db_tool.get_resource_requests()
                    return json.dumps(resources, indent=2, default=str)
                except Exception as e:
                    return f"Error getting resource requests: {e}"
            
            def get_damage_assessments(self) -> str:
                """Get damage assessments and impact analysis"""
                try:
                    damages = self.db_tool.get_damage_assessments()
                    return json.dumps(damages, indent=2, default=str)
                except Exception as e:
                    return f"Error getting damage assessments: {e}"
            
            def search_forest_fire_data(self, search_term: str) -> str:
                """Search across all forest fire emergency data"""
                try:
                    results = self.db_tool.search_forest_fire_data(search_term)
                    return json.dumps(results, indent=2, default=str)
                except Exception as e:
                    return f"Error searching data: {e}"
            
            def execute_custom_query(self, query: str) -> str:
                """Execute custom SQL query (SELECT only for safety)"""
                try:
                    results = self.db_tool.execute_custom_query(query)
                    return json.dumps(results, indent=2, default=str)
                except Exception as e:
                    return f"Error executing query: {e}"
        
        return ForestFireTools(self.db_tool)
    
    def _get_system_instructions(self) -> str:
        """Get comprehensive system instructions for the forest fire agent"""
        
        return """
You are an advanced AI agent specializing in forest fire emergency response management. 
You have access to a comprehensive forest fire emergency database containing real-time 
information about incidents, evacuations, resources, personnel, and damage assessments.

CURRENT SCENARIO: Pine Ridge Wildfire Crisis
- Major wildfire affecting 15,000+ acres
- Multiple communities evacuated
- Emergency shelters active
- Multi-agency response underway

YOUR CAPABILITIES:
🔥 Fire Incident Management
- Track active wildfires and fire zones
- Monitor fire progression and threat levels
- Analyze incident severity and resource needs

🏠 Evacuation & Shelter Coordination  
- Monitor evacuation zones and status
- Track shelter capacity and occupancy
- Manage evacuee information and needs

👨‍🚒 Personnel & Resource Management
- Track response personnel deployment
- Monitor resource requests and fulfillment
- Coordinate multi-agency response efforts

🏚️ Damage Assessment & Impact Analysis
- Document property and infrastructure damage
- Estimate economic and environmental impacts
- Support recovery planning efforts

🔍 Search & Analysis
- Search across all emergency data
- Provide situational awareness updates
- Generate reports and recommendations

RESPONSE GUIDELINES:
1. **Be Urgent but Calm**: Provide clear, actionable information for emergency situations
2. **Use Real Data**: Always use the database tools to get current, accurate information
3. **Prioritize Safety**: Focus on life safety, then property protection, then recovery
4. **Be Comprehensive**: Cover all aspects - people, resources, infrastructure, environment
5. **Support Decisions**: Provide data-driven insights for emergency managers
6. **Format Clearly**: Use emojis, sections, and clear structure for quick reading

COMMUNICATION STYLE:
- Use emergency management terminology appropriately
- Include relevant metrics and statistics
- Highlight critical information with emojis and formatting
- Provide actionable recommendations when appropriate
- Be concise but thorough in emergency situations

When users ask questions, use the appropriate database tools to get current information,
then provide comprehensive, well-formatted responses that support emergency decision-making.
"""
    
    def _fallback_response(self, user_input: str) -> str:
        """Provide fallback response when Agno is not available"""
        
        # Simple pattern matching for common queries
        user_lower = user_input.lower()
        
        try:
            if any(word in user_lower for word in ['overview', 'status', 'situation']):
                status = self.db_tool.get_situation_status()
                metrics = status.get("situation_overview", {})
                
                return f"""
🌲🔥 **FOREST FIRE EMERGENCY STATUS**

🚨 **Alert Level**: {metrics.get('alert_level', 'Unknown')}
📊 **Active Incidents**: {metrics.get('total_incidents', 0)}
🔥 **Fire Zones**: {metrics.get('active_fire_zones', 0)} active, {metrics.get('evacuation_zones', 0)} evacuation
👥 **Evacuees**: {metrics.get('total_evacuees', 0)} people displaced
🏠 **Shelters**: {metrics.get('shelter_occupancy', 0)}% occupancy
👨‍🚒 **Personnel**: {metrics.get('response_personnel', 0)} responders deployed
💰 **Estimated Damages**: {metrics.get('estimated_damages', '$0')}

*Data updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            elif any(word in user_lower for word in ['evacuation', 'shelter', 'evacuee']):
                evacuation = self.db_tool.get_evacuation_status()
                shelter_stats = evacuation.get("shelter_statistics", {})
                
                return f"""
🏠 **EVACUATION & SHELTER STATUS**

📊 **Shelter Statistics**:
- Total Capacity: {shelter_stats.get('total_capacity', 0)} people
- Currently Occupied: {shelter_stats.get('total_occupied', 0)} people  
- Available Space: {shelter_stats.get('available_space', 0)} people
- Occupancy Rate: {shelter_stats.get('occupancy_rate', 0)}%

🏘️ **Active Shelters**: {evacuation.get('evacuation_summary', {}).get('active_shelters', 0)}
👥 **Total Evacuees**: {evacuation.get('evacuation_summary', {}).get('total_evacuees', 0)}
🏘️ **Affected Communities**: {evacuation.get('evacuation_summary', {}).get('affected_communities', 0)}

*All shelters are operational and accepting evacuees*
"""
            
            elif any(word in user_lower for word in ['fire', 'zone', 'burning']):
                incidents = self.db_tool.get_fire_incidents_overview()
                
                response = "🔥 **FIRE INCIDENTS & ZONES**\n\n"
                
                if incidents.get("incidents"):
                    response += "📋 **Active Incidents**:\n"
                    for incident in incidents["incidents"][:3]:
                        response += f"• {incident.get('name', 'Unknown')}: {incident.get('status', 'Unknown')} ({incident.get('priority', 'N/A')} priority)\n"
                
                if incidents.get("fire_zones"):
                    response += f"\n🗺️ **Fire Zones**: {len(incidents['fire_zones'])} zones mapped\n"
                    for zone in incidents["fire_zones"][:5]:
                        response += f"• {zone.get('zone_name', 'Unknown')} ({zone.get('zone_type', 'Unknown')})\n"
                
                return response
            
            elif any(word in user_lower for word in ['damage', 'cost', 'destruction']):
                damages = self.db_tool.get_damage_assessments()
                
                response = f"""
🏚️ **DAMAGE ASSESSMENT**

💰 **Total Estimated Cost**: {damages.get('total_estimated_cost', '$0')}
📍 **Damage Areas**: {damages.get('total_damage_areas', 0)}

📊 **Damage by Severity**:
"""
                
                for severity, damage_list in damages.get("damages_by_severity", {}).items():
                    response += f"• {severity}: {len(damage_list)} areas\n"
                
                return response
            
            elif any(word in user_lower for word in ['personnel', 'staff', 'responder']):
                personnel = self.db_tool.get_response_personnel()
                
                response = f"""
👨‍🚒 **RESPONSE PERSONNEL**

👥 **Total Personnel**: {personnel.get('total_personnel', 0)}
🎯 **Roles Active**: {personnel.get('roles_count', 0)}

📋 **Personnel by Role**:
"""
                
                for role, people in personnel.get("personnel_by_role", {}).items():
                    response += f"• {role}: {len(people)} personnel\n"
                
                return response
            
            else:
                # General search
                search_results = self.db_tool.search_forest_fire_data(user_input)
                total_results = sum(len(results) for results in search_results.values())
                
                if total_results > 0:
                    response = f"🔍 **SEARCH RESULTS** for '{user_input}'\n\n"
                    for category, results in search_results.items():
                        if results:
                            response += f"📋 **{category.title()}**: {len(results)} results\n"
                    return response
                else:
                    return f"❓ No specific results found for '{user_input}'. Try asking about:\n• Fire situation overview\n• Evacuation status\n• Shelter information\n• Personnel deployment\n• Damage assessments"
        
        except Exception as e:
            return f"❌ Error processing request: {e}"
    
    def query(self, user_input: str) -> str:
        """Process user query and return response"""
        
        if not user_input.strip():
            return "❓ Please ask a question about the forest fire emergency situation."
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": None
        })
        
        try:
            if self.agent and AGNO_AVAILABLE:
                # Use Agno agent
                response = self.agent.run(user_input)
                agent_response = str(response)
            else:
                # Use fallback response
                agent_response = self._fallback_response(user_input)
            
            # Update conversation history
            self.conversation_history[-1]["agent"] = agent_response
            
            return agent_response
            
        except Exception as e:
            error_response = f"❌ Error processing query: {e}\n\nTrying fallback response...\n\n"
            error_response += self._fallback_response(user_input)
            
            self.conversation_history[-1]["agent"] = error_response
            return error_response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history.clear()

def main():
    """Main interactive loop for the forest fire emergency agent"""
    
    print("🌲🔥 FOREST FIRE EMERGENCY RESPONSE AI AGENT")
    print("=" * 60)
    print()
    print("🚨 CURRENT SCENARIO: Pine Ridge Wildfire Crisis")
    print("   Major wildfire affecting multiple communities")
    print("   Emergency shelters active, evacuations underway")
    print()
    print("💬 Ask me about:")
    print("   • Fire situation and zone status")
    print("   • Evacuation and shelter information") 
    print("   • Personnel and resource deployment")
    print("   • Damage assessments and impacts")
    print("   • Any aspect of the emergency response")
    print()
    print("Type 'quit' or 'exit' to end the session")
    print("Type 'clear' to clear conversation history")
    print("-" * 60)
    
    # Initialize the agent
    agent = ForestFireEmergencyAgent()
    
    # Interactive loop
    while True:
        try:
            print()
            user_input = input("🚨 Emergency Query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🚒 Forest Fire Emergency Agent session ended.")
                print("   Stay safe and coordinate well!")
                break
            
            if user_input.lower() == 'clear':
                agent.clear_conversation()
                print("🧹 Conversation history cleared.")
                continue
            
            print("\n🤖 Agent Response:")
            print("-" * 40)
            
            response = agent.query(user_input)
            print(response)
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n🚒 Emergency session interrupted. Stay safe!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try your query again.")

if __name__ == "__main__":
    main()
