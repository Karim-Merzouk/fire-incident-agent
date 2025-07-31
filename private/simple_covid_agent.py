"""
Simple COVID-19 Database Agent Demo
Ready-to-use agent with Gemini AI for natural language database queries
"""

import os
from covid_database_tool import COVID19DatabaseTool
import json

class SimpleCOVIDAgent:
    """Simple AI agent for COVID-19 database queries"""
    
    def __init__(self):
        self.db_tool = COVID19DatabaseTool()
        print("🤖 Simple COVID-19 Database Agent initialized!")
        print("💡 This demo uses text-based processing without AI for now.")
        print("   Add your API key to enable full AI capabilities.")
    
    def process_query(self, user_input: str) -> str:
        """Process user query and return appropriate response"""
        query = user_input.lower().strip()
        
        try:
            # Overview queries
            if any(word in query for word in ['overview', 'summary', 'stats', 'statistics']):
                data = self.db_tool.get_covid_overview()
                return self._format_overview(data)
            
            # Case queries
            elif any(word in query for word in ['cases', 'patients', 'recent']):
                if 'recent' in query or 'latest' in query:
                    limit = self._extract_number(query, default=10)
                    data = self.db_tool.get_recent_cases(limit)
                    return self._format_cases(data)
                else:
                    data = self.db_tool.get_recent_cases(10)
                    return self._format_cases(data)
            
            # Symptoms queries
            elif any(word in query for word in ['symptoms', 'symptom']):
                data = self.db_tool.get_symptoms_list()
                return self._format_symptoms(data)
            
            # Testing queries
            elif any(word in query for word in ['test', 'testing', 'devices']):
                if 'device' in query or 'equipment' in query:
                    data = self.db_tool.get_testing_devices()
                    return self._format_devices(data)
                else:
                    data = self.db_tool.get_testing_statistics(30)
                    return self._format_test_stats(data)
            
            # Hospitalization queries
            elif any(word in query for word in ['hospital', 'icu', 'admitted']):
                data = self.db_tool.get_hospitalization_trends()
                return self._format_hospitalization(data)
            
            # Status-based queries
            elif any(word in query for word in ['deceased', 'died', 'death', 'fatal']):
                data = self.db_tool.search_cases_by_status('Deceased')
                return self._format_cases(data, title="Deceased Cases")
            
            elif any(word in query for word in ['recovered', 'recovery']):
                data = self.db_tool.search_cases_by_status('Recovered')
                return self._format_cases(data, title="Recovered Cases")
            
            elif any(word in query for word in ['active', 'symptomatic']):
                data = self.db_tool.search_cases_by_status('Symptomatic')
                return self._format_cases(data, title="Active Symptomatic Cases")
            
            # Demographics
            elif any(word in query for word in ['demographics', 'demographic', 'population']):
                data = self.db_tool.get_demographics_data()
                return self._format_demographics(data)
            
            # Help
            elif any(word in query for word in ['help', 'commands', 'what can']):
                return self._get_help()
            
            else:
                return "🤔 I didn't understand that query. Try asking about:\n" + \
                       "• Overview or statistics\n• Recent cases\n• Symptoms\n• Testing data\n" + \
                       "• Hospitalizations\n• Demographics\n\nType 'help' for more options."
        
        except Exception as e:
            return f"❌ Error processing query: {str(e)}"
    
    def _extract_number(self, text: str, default: int = 10) -> int:
        """Extract number from text"""
        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else default
    
    def _format_overview(self, data: dict) -> str:
        """Format overview data"""
        if 'error' in data:
            return f"❌ Error: {data['error']}"
        
        result = "📊 **COVID-19 Database Overview**\n"
        result += "=" * 40 + "\n\n"
        
        if 'disease' in data:
            result += f"🦠 **Disease**: {data['disease']['name']}\n"
            result += f"📝 **Description**: {data['disease']['description']}\n\n"
        
        result += f"📈 **Total Cases**: {data.get('total_cases', 0)}\n"
        result += f"🏥 **Hospitalized**: {data.get('hospitalized_cases', 0)}\n"
        result += f"🚨 **ICU Cases**: {data.get('icu_cases', 0)}\n"
        result += f"🔬 **Testing Reports**: {data.get('testing_reports', 0)}\n"
        result += f"🧪 **Total Tests**: {data.get('total_tests', 0):,}\n"
        result += f"➕ **Positive Tests**: {data.get('positive_tests', 0):,}\n"
        result += f"📊 **Positivity Rate**: {data.get('positivity_rate', 0):.1f}%\n\n"
        
        if 'cases_by_status' in data:
            result += "📋 **Cases by Status**:\n"
            for status, count in data['cases_by_status'].items():
                result += f"  • {status}: {count} cases\n"
        
        return result
    
    def _format_cases(self, data: list, title: str = "Recent Cases") -> str:
        """Format cases data"""
        if not data:
            return "📭 No cases found."
        
        if 'error' in data[0]:
            return f"❌ Error: {data[0]['error']}"
        
        result = f"🏥 **{title}**\n"
        result += "=" * 40 + "\n\n"
        
        for i, case in enumerate(data[:15], 1):  # Limit to 15
            hosp_status = "🏥" if case.get('hospitalized') == 'T' else "🏠"
            icu_status = " (ICU)" if case.get('intensive_care') == 'T' else ""
            
            result += f"{i:2d}. **{case.get('case_number')}**\n"
            result += f"    Status: {case.get('illness_status')} | {case.get('diagnosis_status')}\n"
            result += f"    Date: {case.get('diagnosis_date')} | {hosp_status}{icu_status}\n"
            result += f"    Monitoring: {case.get('monitoring_level', 'N/A')}\n\n"
        
        if len(data) > 15:
            result += f"... and {len(data) - 15} more cases\n"
        
        return result
    
    def _format_symptoms(self, data: list) -> str:
        """Format symptoms data"""
        if not data or 'error' in data[0]:
            return "❌ No symptoms data available."
        
        result = "🤒 **COVID-19 Symptoms**\n"
        result += "=" * 40 + "\n\n"
        
        # Group by severity
        common = []
        serious = []
        less_common = []
        rare = []
        
        for symptom in data:
            assessment = symptom.get('assessment', 'Unknown')
            name = symptom.get('name')
            description = symptom.get('description', '')
            
            symptom_text = f"• **{name}**"
            if description:
                symptom_text += f": {description}"
            symptom_text += "\n"
            
            if assessment == 'Common':
                common.append(symptom_text)
            elif assessment == 'Serious':
                serious.append(symptom_text)
            elif assessment == 'Less common':
                less_common.append(symptom_text)
            elif assessment == 'Rare':
                rare.append(symptom_text)
        
        if common:
            result += "🔴 **Common Symptoms**:\n"
            result += "".join(common) + "\n"
        
        if serious:
            result += "🚨 **Serious Symptoms**:\n"
            result += "".join(serious) + "\n"
        
        if less_common:
            result += "🟡 **Less Common Symptoms**:\n"
            result += "".join(less_common) + "\n"
        
        if rare:
            result += "🔵 **Rare Symptoms**:\n"
            result += "".join(rare) + "\n"
        
        return result
    
    def _format_devices(self, data: list) -> str:
        """Format testing devices data"""
        if not data or 'error' in data[0]:
            return "❌ No testing devices data available."
        
        result = "🔬 **COVID-19 Testing Devices**\n"
        result += "=" * 40 + "\n\n"
        
        for device in data:
            status = "✅ Approved" if device.get('approved') == 'T' else "⏳ Pending"
            available = "📦 Available" if device.get('available') == 'T' else "❌ Unavailable"
            
            result += f"• **{device.get('name')}** ({device.get('code')})\n"
            result += f"  Class: {device.get('device_class')} | Source: {device.get('source')}\n"
            result += f"  Status: {status} | {available}\n"
            if device.get('comments'):
                result += f"  Info: {device.get('comments')}\n"
            result += "\n"
        
        return result
    
    def _format_test_stats(self, data: list) -> str:
        """Format testing statistics"""
        if not data or 'error' in data[0]:
            return "❌ No testing statistics available."
        
        result = "📈 **COVID-19 Testing Statistics**\n"
        result += "=" * 40 + "\n\n"
        
        total_tests = sum(stat.get('tests_total', 0) for stat in data)
        total_positive = sum(stat.get('tests_positive', 0) for stat in data)
        avg_positivity = (total_positive / total_tests * 100) if total_tests > 0 else 0
        
        result += f"📊 **Summary** ({len(data)} reports):\n"
        result += f"  Total Tests: {total_tests:,}\n"
        result += f"  Positive Tests: {total_positive:,}\n"
        result += f"  Average Positivity Rate: {avg_positivity:.1f}%\n\n"
        
        result += "📅 **Recent Reports**:\n"
        for stat in data[:10]:  # Show last 10
            date = stat.get('date')
            total = stat.get('tests_total', 0)
            positive = stat.get('tests_positive', 0)
            rate = stat.get('positivity_rate', 0)
            result += f"  {date}: {total:3d} tests, {positive:2d} positive ({rate:.1f}%)\n"
        
        return result
    
    def _format_hospitalization(self, data: dict) -> str:
        """Format hospitalization trends"""
        if 'error' in data:
            return f"❌ Error: {data['error']}"
        
        result = "🏥 **Hospitalization Trends**\n"
        result += "=" * 40 + "\n\n"
        
        if 'trends' in data:
            for trend in data['trends'][:12]:  # Show last 12 months
                month = trend.get('month')
                total = trend.get('total_cases', 0)
                hosp = trend.get('hospitalized', 0)
                icu = trend.get('icu', 0)
                hosp_rate = trend.get('hospitalization_rate', 0)
                icu_rate = trend.get('icu_rate', 0)
                
                result += f"📅 **{month}**:\n"
                result += f"  Total Cases: {total}\n"
                result += f"  Hospitalized: {hosp} ({hosp_rate:.1f}%)\n"
                result += f"  ICU: {icu} ({icu_rate:.1f}%)\n\n"
        
        return result
    
    def _format_demographics(self, data: list) -> str:
        """Format demographics data"""
        if not data or 'error' in data[0]:
            return "❌ No demographics data available."
        
        result = "👥 **Demographic Categories**\n"
        result += "=" * 40 + "\n\n"
        
        age_groups = []
        gender = []
        occupation = []
        other = []
        
        for demo in data:
            code = demo.get('code', '')
            name = demo.get('name', '')
            comments = demo.get('comments', '')
            
            demo_text = f"• **{name}** ({code})"
            if comments:
                demo_text += f": {comments}"
            demo_text += "\n"
            
            if 'AG' in code or 'Age' in name:
                age_groups.append(demo_text)
            elif code in ['MALE', 'FEMALE'] or 'gender' in comments.lower():
                gender.append(demo_text)
            elif 'Worker' in name or 'HCW' in code or 'ESW' in code:
                occupation.append(demo_text)
            else:
                other.append(demo_text)
        
        if age_groups:
            result += "🎂 **Age Groups**:\n"
            result += "".join(age_groups) + "\n"
        
        if gender:
            result += "👫 **Gender**:\n"  
            result += "".join(gender) + "\n"
        
        if occupation:
            result += "💼 **Occupational Categories**:\n"
            result += "".join(occupation) + "\n"
        
        if other:
            result += "🏷️ **Other Categories**:\n"
            result += "".join(other) + "\n"
        
        return result
    
    def _get_help(self) -> str:
        """Get help information"""
        return """
🤖 **COVID-19 Database Agent Help**
====================================

**Available Queries:**
• 'overview' or 'summary' - Get database overview and statistics
• 'cases' or 'recent cases' - View recent COVID-19 cases
• 'symptoms' - List all tracked COVID-19 symptoms
• 'testing' or 'devices' - View testing equipment and statistics
• 'hospital' or 'hospitalization' - Hospital and ICU trends
• 'deceased' or 'deaths' - Cases with fatal outcomes
• 'recovered' - Cases that have recovered
• 'demographics' - Population categories tracked

**Example Queries:**
• "Show me the latest 5 cases"
• "What are the COVID symptoms?"
• "Give me testing statistics"
• "How many people are hospitalized?"
• "Show me recovery trends"

**Tips:**
• Use natural language - the agent will understand context
• Add numbers for specific limits (e.g., "show 15 cases")
• Ask follow-up questions for more details
• Type 'quit' or 'exit' to end the session

**Data Source**: Sahana Eden COVID-19 Database
"""

def main():
    """Main interactive loop"""
    agent = SimpleCOVIDAgent()
    
    print("\n" + "="*60)
    print("🤖 COVID-19 Database Agent - Interactive Session")
    print("="*60)
    print("💡 Ask me anything about the COVID-19 database!")
    print("📝 Examples: 'overview', 'recent cases', 'symptoms', 'help'")
    print("🚪 Type 'quit' or 'exit' to end the session")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n❓ Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Thank you for using the COVID-19 Database Agent!")
                break
            
            if not user_input:
                print("💭 Please ask a question or type 'help' for assistance.")
                continue
            
            print("\n🔍 Processing your query...")
            response = agent.process_query(user_input)
            print("\n" + "="*60)
            print(response)
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Session ended by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("💡 Try rephrasing your question or type 'help'.")

if __name__ == "__main__":
    main()
