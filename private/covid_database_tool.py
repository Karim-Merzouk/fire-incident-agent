"""
COVID-19 Database Query Tool for Agno Framework
This tool allows AI agents to query the Sahana Eden COVID-19 database
"""

import sqlite3
import os
import pandas as pd
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class COVID19DatabaseTool:
    """Tool for querying COVID-19 database in Sahana Eden"""
    
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
        self.description = "Query COVID-19 database for cases, symptoms, testing data, and statistics"
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute SQL query and return results as list of dictionaries"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Fetch all results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            return results
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_covid_overview(self) -> Dict[str, Any]:
        """Get overview of COVID-19 data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            overview = {}
            
            # Disease info
            cursor.execute("SELECT name, description FROM disease_disease WHERE id = 1")
            disease = cursor.fetchone()
            if disease:
                overview["disease"] = {"name": disease[0], "description": disease[1]}
            
            # Case counts
            cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1")
            overview["total_cases"] = cursor.fetchone()[0]
            
            # Cases by status
            cursor.execute("""
                SELECT illness_status, COUNT(*) 
                FROM disease_case 
                WHERE disease_id = 1 
                GROUP BY illness_status
            """)
            overview["cases_by_status"] = dict(cursor.fetchall())
            
            # Hospitalization stats
            cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1 AND hospitalized = 'T'")
            overview["hospitalized_cases"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1 AND intensive_care = 'T'")
            overview["icu_cases"] = cursor.fetchone()[0]
            
            # Testing data
            cursor.execute("SELECT COUNT(*) FROM disease_testing_report WHERE disease_id = 1")
            overview["testing_reports"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(tests_total), SUM(tests_positive) FROM disease_testing_report WHERE disease_id = 1")
            test_data = cursor.fetchone()
            if test_data[0]:
                overview["total_tests"] = test_data[0]
                overview["positive_tests"] = test_data[1]
                overview["positivity_rate"] = round((test_data[1] / test_data[0]) * 100, 2)
            
            # Symptoms count
            cursor.execute("SELECT COUNT(*) FROM disease_symptom WHERE disease_id = 1")
            overview["symptoms_tracked"] = cursor.fetchone()[0]
            
            conn.close()
            return overview
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_cases_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get cases within date range"""
        query = """
            SELECT case_number, illness_status, diagnosis_status, diagnosis_date,
                   hospitalized, intensive_care, monitoring_level
            FROM disease_case 
            WHERE disease_id = 1 
            AND diagnosis_date BETWEEN ? AND ?
            ORDER BY diagnosis_date DESC
        """
        return self.execute_query(query, (start_date, end_date))
    
    def get_symptoms_list(self) -> List[Dict]:
        """Get all COVID-19 symptoms"""
        query = """
            SELECT name, description, assessment
            FROM disease_symptom 
            WHERE disease_id = 1
            ORDER BY name
        """
        return self.execute_query(query)
    
    def get_testing_devices(self) -> List[Dict]:
        """Get testing devices information"""
        query = """
            SELECT name, code, device_class, approved, available, source, comments
            FROM disease_testing_device 
            WHERE disease_id = 1
        """
        return self.execute_query(query)
    
    def get_recent_cases(self, limit: int = 10) -> List[Dict]:
        """Get most recent COVID-19 cases"""
        query = """
            SELECT case_number, illness_status, diagnosis_status, diagnosis_date,
                   hospitalized, intensive_care, monitoring_level
            FROM disease_case 
            WHERE disease_id = 1
            ORDER BY diagnosis_date DESC
            LIMIT ?
        """
        return self.execute_query(query, (limit,))
    
    def get_testing_statistics(self, days: int = 30) -> List[Dict]:
        """Get testing statistics for recent days"""
        query = """
            SELECT date, tests_total, tests_positive,
                   ROUND((CAST(tests_positive AS FLOAT) / tests_total) * 100, 2) as positivity_rate
            FROM disease_testing_report 
            WHERE disease_id = 1
            AND date >= date('now', '-{} days')
            ORDER BY date DESC
        """.format(days)
        return self.execute_query(query)
    
    def search_cases_by_status(self, status: str) -> List[Dict]:
        """Search cases by illness or diagnosis status"""
        query = """
            SELECT case_number, illness_status, diagnosis_status, diagnosis_date,
                   hospitalized, intensive_care, monitoring_level
            FROM disease_case 
            WHERE disease_id = 1
            AND (illness_status LIKE ? OR diagnosis_status LIKE ?)
            ORDER BY diagnosis_date DESC
        """
        status_pattern = f"%{status}%"
        return self.execute_query(query, (status_pattern, status_pattern))
    
    def get_demographics_data(self) -> List[Dict]:
        """Get demographic categories"""
        query = """
            SELECT code, name, comments
            FROM disease_demographic
            ORDER BY code
        """
        return self.execute_query(query)
    
    def get_hospitalization_trends(self) -> Dict[str, Any]:
        """Get hospitalization and ICU trends"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Monthly hospitalization data
            cursor.execute("""
                SELECT 
                    strftime('%Y-%m', diagnosis_date) as month,
                    COUNT(*) as total_cases,
                    SUM(CASE WHEN hospitalized = 'T' THEN 1 ELSE 0 END) as hospitalized,
                    SUM(CASE WHEN intensive_care = 'T' THEN 1 ELSE 0 END) as icu
                FROM disease_case 
                WHERE disease_id = 1
                GROUP BY strftime('%Y-%m', diagnosis_date)
                ORDER BY month DESC
            """)
            
            trends = []
            for row in cursor.fetchall():
                month, total, hosp, icu = row
                trends.append({
                    "month": month,
                    "total_cases": total,
                    "hospitalized": hosp,
                    "icu": icu,
                    "hospitalization_rate": round((hosp / total) * 100, 2) if total > 0 else 0,
                    "icu_rate": round((icu / total) * 100, 2) if total > 0 else 0
                })
            
            conn.close()
            return {"trends": trends}
            
        except Exception as e:
            return {"error": str(e)}
    
    def custom_query(self, query: str) -> List[Dict]:
        """Execute custom SQL query (use with caution)"""
        # Basic safety check - only allow SELECT queries
        if not query.strip().upper().startswith('SELECT'):
            return [{"error": "Only SELECT queries are allowed"}]
        
        return self.execute_query(query)

# Test the tool
if __name__ == "__main__":
    tool = COVID19DatabaseTool()
    
    print("🔍 Testing COVID-19 Database Tool")
    print("=" * 50)
    
    # Test overview
    overview = tool.get_covid_overview()
    print("📊 Overview:")
    print(json.dumps(overview, indent=2))
    
    print("\n🤒 Recent Cases:")
    recent_cases = tool.get_recent_cases(5)
    for case in recent_cases:
        print(f"  • {case['case_number']}: {case['illness_status']} - {case['diagnosis_date']}")
    
    print("\n🔬 Testing Devices:")
    devices = tool.get_testing_devices()
    for device in devices:
        print(f"  • {device['name']} ({device['code']}): {device['device_class']}")
