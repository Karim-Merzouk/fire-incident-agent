"""
COVID-19 Database Agent using Agno Framework
Supports both LLAMA and Gemini models for natural language interaction with the database
"""

import os
from typing import List, Dict, Any
from agno import Agent
from agno.models.gemini import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.python_tools import PythonTools
from covid_database_tool import COVID19DatabaseTool
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class COVID19DatabaseAgent:
    """AI Agent for interacting with COVID-19 database using natural language"""
    
    def __init__(self, model_type: str = "gemini", api_key: str = None):
        """
        Initialize the agent
        
        Args:
            model_type: "gemini" or "openai" (for LLAMA via OpenAI-compatible API)
            api_key: API key for the chosen model
        """
        self.model_type = model_type
        self.db_tool = COVID19DatabaseTool()
        
        # Initialize the AI model
        if model_type == "gemini":
            if not api_key:
                api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
            
            self.model = Gemini(
                id="gemini-1.5-flash",
                api_key=api_key
            )
            
        elif model_type == "openai":
            if not api_key:
                api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
            
            self.model = OpenAIChat(
                id="gpt-4",
                api_key=api_key
            )
        else:
            raise ValueError("model_type must be 'gemini' or 'openai'")
        
        # Create the agent with database tools
        self.agent = Agent(
            model=self.model,
            tools=[
                self._create_database_overview_tool(),
                self._create_cases_query_tool(),
                self._create_symptoms_tool(),
                self._create_testing_tool(),
                self._create_statistics_tool(),
                self._create_custom_query_tool(),
                PythonTools()
            ],
            instructions=self._get_agent_instructions(),
            show_tool_calls=True,
            markdown=True
        )
    
    def _get_agent_instructions(self) -> str:
        """Get comprehensive instructions for the agent"""
        return """
You are a COVID-19 Database Assistant for the Sahana Eden humanitarian management system.
You have access to a comprehensive COVID-19 database containing:

- Disease information and definitions
- Case records with patient status, hospitalization, and ICU data
- Symptoms tracking and assessment
- Testing devices and their specifications
- Testing reports with positivity rates
- Demographic categories
- Geographic location data

CAPABILITIES:
1. **Database Overview**: Get general statistics and summaries
2. **Case Analysis**: Query cases by date, status, or specific criteria
3. **Symptom Information**: List and describe COVID-19 symptoms
4. **Testing Data**: Access testing device info and test results
5. **Statistics**: Calculate trends, rates, and comparative analysis
6. **Custom Queries**: Execute specific database queries

GUIDELINES:
- Always provide clear, accurate information based on the database
- Include relevant statistics and context in your responses
- Format responses clearly with headers, bullet points, and tables when appropriate
- If asked about trends, provide both numbers and percentages
- When discussing cases, respect privacy by using case numbers, not personal details
- Suggest follow-up queries that might be useful
- If data seems incomplete or unusual, mention it

RESPONSE FORMAT:
- Use markdown formatting for clarity
- Include relevant emoji icons (🦠 📊 🏥 🔬 etc.)
- Provide actionable insights when possible
- Always cite the data source as "Sahana Eden COVID-19 Database"

Remember: You're helping public health officials, humanitarian workers, and medical professionals make informed decisions.
"""
    
    def _create_database_overview_tool(self):
        """Create tool for database overview"""
        def get_covid_overview():
            """Get comprehensive overview of COVID-19 database including case counts, testing data, and statistics"""
            return self.db_tool.get_covid_overview()
        
        return get_covid_overview
    
    def _create_cases_query_tool(self):
        """Create tool for querying cases"""
        def query_covid_cases(query_type: str = "recent", **kwargs):
            """
            Query COVID-19 cases from database
            
            Args:
                query_type: Type of query - "recent", "by_date", "by_status"
                **kwargs: Additional parameters like limit, start_date, end_date, status
            """
            if query_type == "recent":
                limit = kwargs.get("limit", 10)
                return self.db_tool.get_recent_cases(limit)
            
            elif query_type == "by_date":
                start_date = kwargs.get("start_date")
                end_date = kwargs.get("end_date")
                if not start_date or not end_date:
                    return [{"error": "start_date and end_date are required for date range queries"}]
                return self.db_tool.get_cases_by_date_range(start_date, end_date)
            
            elif query_type == "by_status":
                status = kwargs.get("status")
                if not status:
                    return [{"error": "status parameter is required"}]
                return self.db_tool.search_cases_by_status(status)
            
            else:
                return [{"error": f"Unknown query_type: {query_type}"}]
        
        return query_covid_cases
    
    def _create_symptoms_tool(self):
        """Create tool for symptoms information"""
        def get_covid_symptoms():
            """Get list of all COVID-19 symptoms with descriptions and severity assessments"""
            return self.db_tool.get_symptoms_list()
        
        return get_covid_symptoms
    
    def _create_testing_tool(self):
        """Create tool for testing information"""
        def get_testing_info(info_type: str = "devices"):
            """
            Get COVID-19 testing information
            
            Args:
                info_type: "devices" for testing devices, "statistics" for test results data
            """
            if info_type == "devices":
                return self.db_tool.get_testing_devices()
            elif info_type == "statistics":
                return self.db_tool.get_testing_statistics()
            else:
                return [{"error": f"Unknown info_type: {info_type}"}]
        
        return get_testing_info
    
    def _create_statistics_tool(self):
        """Create tool for statistical analysis"""
        def get_covid_statistics(stat_type: str = "hospitalization"):
            """
            Get COVID-19 statistical analysis
            
            Args:
                stat_type: "hospitalization" for hospital trends, "demographics" for demographic data
            """
            if stat_type == "hospitalization":
                return self.db_tool.get_hospitalization_trends()
            elif stat_type == "demographics":
                return self.db_tool.get_demographics_data()
            else:
                return [{"error": f"Unknown stat_type: {stat_type}"}]
        
        return get_covid_statistics
    
    def _create_custom_query_tool(self):
        """Create tool for custom database queries"""
        def execute_custom_query(sql_query: str):
            """
            Execute custom SQL query on the COVID-19 database (SELECT queries only)
            
            Args:
                sql_query: SQL SELECT query to execute
            """
            return self.db_tool.custom_query(sql_query)
        
        return execute_custom_query
    
    def chat(self, message: str) -> str:
        """
        Chat with the agent
        
        Args:
            message: User's question or request
            
        Returns:
            Agent's response
        """
        try:
            response = self.agent.run(message)
            return response.content
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def get_quick_stats(self) -> Dict[str, Any]:
        """Get quick statistics for dashboard display"""
        return self.db_tool.get_covid_overview()

# Example usage and testing
if __name__ == "__main__":
    print("🤖 COVID-19 Database Agent Setup")
    print("=" * 50)
    
    # You can set your API key here or in environment variables
    # For Gemini: set GEMINI_API_KEY
    # For OpenAI: set OPENAI_API_KEY
    
    try:
        # Initialize agent (change to "openai" for LLAMA/GPT models)
        agent = COVID19DatabaseAgent(
            model_type="gemini",  # or "openai"
            # api_key="your-api-key-here"  # Optional if set in environment
        )
        
        print("✅ Agent initialized successfully!")
        print("\n🔍 Quick Database Stats:")
        stats = agent.get_quick_stats()
        print(json.dumps(stats, indent=2))
        
        print("\n💬 Starting interactive session...")
        print("Ask questions about the COVID-19 database (type 'quit' to exit):")
        
        while True:
            user_input = input("\n📝 Your question: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            print("\n🤖 Agent response:")
            response = agent.chat(user_input)
            print(response)
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        print("\n💡 Tips:")
        print("1. Set your API key in environment variables:")
        print("   - For Gemini: set GEMINI_API_KEY=your-key")
        print("   - For OpenAI: set OPENAI_API_KEY=your-key")
        print("2. Make sure all packages are installed: pip install -r requirements_agent.txt")
        print("3. Ensure the COVID-19 database is properly set up")
