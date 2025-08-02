#!/usr/bin/env python3
"""
COVID-19 Database Initialization Script for Sahana Eden
This script populates the database with COVID-19 related data
"""

import os
import sys
import csv
import sqlite3
from datetime import datetime, date

def initialize_covid_database():
    """Initialize the COVID-19 database with sample data"""
    
    # Database path
    db_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db"
    
    if not os.path.exists(db_path):
        print("Database file not found. Please start Sahana Eden first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Initializing COVID-19 database...")
    
    try:
        # 1. Insert COVID-19 disease information
        print("Adding COVID-19 disease information...")
        cursor.execute("""
            INSERT OR REPLACE INTO disease_disease 
            (id, name, short_name, acronym, code, description, trace_period, watch_period, created_on)
            VALUES 
            (1, 'Coronavirus Disease', 'COVID-19', 'COVID-19', 'U07.1', 
             'Respiratory disease caused by the SARS-CoV-2 virus', 14, 16, ?)
        """, (datetime.now(),))
        
        # 2. Insert COVID-19 symptoms
        print("Adding COVID-19 symptoms...")
        symptoms = [
            ("Fever", "Fever (greater than 38.6°C or 101.5°F)", "Temperature measurement"),
            ("Dry Cough", "Unproductive (dry) cough, continuous", "Clinical observation"),
            ("Tiredness / Weakness", "Unexplained severe tiredness and/or sudden weakness", "Patient self-report"),
            ("Dyspnoea", "Shortness of breath, difficulty breathing", "Clinical assessment"),
            ("Myalgia / Arthralgia", "Muscle and/or joint pain", "Patient self-report"),
            ("Sore throat", "", "Clinical examination"),
            ("Rhinitis", "Nasal congestion, runny nose", "Clinical observation"),
            ("Diarrhea", "", "Patient self-report"),
            ("Loss of taste", "Ageusia - complete loss of taste", "Patient self-report"),
            ("Loss of smell", "Anosmia - complete loss of smell", "Patient self-report"),
            ("Headache", "Persistent headache", "Patient self-report"),
            ("Nausea", "Feeling sick to stomach", "Patient self-report"),
            ("Vomiting", "Throwing up", "Clinical observation"),
            ("Chills", "Feeling cold with shivering", "Patient self-report"),
            ("Conjunctivitis", "Pink eye inflammation", "Clinical examination"),
            ("Skin rash", "Rash on skin or discoloration of fingers/toes", "Clinical examination"),
            ("Night sweats", "Excessive sweating during sleep", "Patient self-report"),
            ("Brain fog", "Difficulty concentrating or thinking clearly", "Patient self-report"),
            ("Chest pain", "Pain or pressure in chest", "Patient self-report"),
            ("Fast heart rate", "Rapid heartbeat or palpitations", "Clinical measurement")
        ]
        
        for i, (name, description, assessment) in enumerate(symptoms, 1):
            cursor.execute("""
                INSERT OR REPLACE INTO disease_symptom 
                (id, disease_id, name, description, assessment, created_on)
                VALUES (?, 1, ?, ?, ?, ?)
            """, (i, name, description, assessment, datetime.now()))
        
        # 3. Insert testing devices
        print("Adding testing devices...")
        devices = [
            ("RT-PCR Test", "Real-time reverse transcription polymerase chain reaction"),
            ("Antigen Test", "Rapid antigen test"),
            ("Antibody Test", "Serology test for antibodies"),
            ("At-home Test Kit", "Self-administered test kit"),
            ("Lab PCR Test", "Laboratory PCR test"),
            ("Rapid Test", "Quick diagnostic test")
        ]
        
        for i, (name, description) in enumerate(devices, 1):
            cursor.execute("""
                INSERT OR REPLACE INTO disease_testing_device 
                (id, name, description, available, created_on)
                VALUES (?, ?, ?, 1, ?)
            """, (i, name, description, datetime.now()))
        
        # 4. Insert demographics
        print("Adding demographics...")
        demographics = [
            ("0-17 years", "Children and adolescents"),
            ("18-29 years", "Young adults"),
            ("30-49 years", "Adults"),
            ("50-64 years", "Middle-aged adults"),
            ("65-79 years", "Older adults"),
            ("80+ years", "Elderly"),
            ("Male", "Male gender"),
            ("Female", "Female gender"),
            ("Healthcare Workers", "Healthcare professionals"),
            ("Essential Workers", "Essential service workers"),
            ("Pregnant Women", "Pregnant individuals"),
            ("Immunocompromised", "People with weakened immune systems"),
            ("Chronic Conditions", "People with underlying health conditions"),
            ("Nursing Home Residents", "Residents of care facilities")
        ]
        
        for i, (name, comments) in enumerate(demographics, 1):
            cursor.execute("""
                INSERT OR REPLACE INTO disease_demographic 
                (id, name, comments, created_on)
                VALUES (?, ?, ?, ?)
            """, (i, name, comments, datetime.now()))
        
        # 5. Insert statistics parameters
        print("Adding statistics parameters...")
        parameters = [
            ("COVID-19 Cases", "Total confirmed COVID-19 cases"),
            ("COVID-19 Deaths", "Total COVID-19 related deaths"),
            ("COVID-19 Recovered", "Total recovered COVID-19 cases"),
            ("COVID-19 Hospitalized", "Total hospitalized COVID-19 cases"),
            ("COVID-19 ICU", "Total COVID-19 cases in ICU"),
            ("COVID-19 Tests Positive", "Total positive COVID-19 tests"),
            ("COVID-19 Tests Negative", "Total negative COVID-19 tests"),
            ("COVID-19 Tests Total", "Total COVID-19 tests performed"),
            ("COVID-19 Vaccinated First Dose", "People who received first vaccine dose"),
            ("COVID-19 Vaccinated Second Dose", "People who received second vaccine dose"),
            ("COVID-19 Vaccinated Booster", "People who received booster dose"),
            ("COVID-19 Contact Traced", "People contact traced"),
            ("COVID-19 Quarantined", "People in quarantine")
        ]
        
        for i, (name, comments) in enumerate(parameters, 1):
            cursor.execute("""
                INSERT OR REPLACE INTO stats_parameter 
                (id, name, comments, created_on)
                VALUES (?, ?, ?, ?)
            """, (i, name, comments, datetime.now()))
        
        # Commit all changes
        conn.commit()
        print("✅ COVID-19 database initialization completed successfully!")
        print("\nDatabase includes:")
        print("- COVID-19 disease definition with 14-day trace period")
        print("- 20 COVID-19 symptoms with assessment methods")
        print("- 6 testing device types")
        print("- 14 demographic categories")
        print("- 13 statistical parameters")
        print("\nYou can now:")
        print("1. Start Sahana Eden web server")
        print("2. Navigate to /disease/case to add COVID-19 cases")
        print("3. Use /disease/stats_data to add statistics")
        print("4. Access /disease/testing_report for testing data")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_covid_database()
