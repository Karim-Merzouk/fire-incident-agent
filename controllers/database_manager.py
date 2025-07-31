def database_manager():
    """
    Database connection management interface for AI Agent
    """
    return dict(
        title="Database Connection Manager",
        subtitle="Connect and manage databases for the Forest Fire AI Agent"
    )

# -----------------------------------------------------------------------------
def test_database_connection():
    """
    AJAX endpoint to test database connection
    """
    import json
    import sys
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        # Get database parameters from request
        db_type = request.vars.get('db_type', 'sqlite')
        db_path = request.vars.get('db_path', '')
        db_host = request.vars.get('db_host', '')
        db_port = request.vars.get('db_port', '')
        db_name = request.vars.get('db_name', '')
        db_user = request.vars.get('db_user', '')
        db_password = request.vars.get('db_password', '')
        
        # Add private directory to path
        private_path = os.path.join(request.folder, "private")
        if private_path not in sys.path:
            sys.path.insert(0, private_path)
        
        # Test connection based on database type
        if db_type == 'sqlite':
            if not db_path:
                return json.dumps({
                    "status": "error",
                    "message": "SQLite database path is required"
                })
            
            # Test SQLite connection
            import sqlite3
            try:
                # Check if file exists
                if not os.path.exists(db_path):
                    return json.dumps({
                        "status": "error",
                        "message": f"Database file not found: {db_path}"
                    })
                
                # Test connection
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Get table list
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
                # Test some basic queries
                test_results = {}
                for table in tables[:5]:  # Test first 5 tables
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        test_results[table] = count
                    except Exception as e:
                        test_results[table] = f"Error: {str(e)}"
                
                conn.close()
                
                return json.dumps({
                    "status": "success",
                    "message": "SQLite connection successful",
                    "database_info": {
                        "type": "SQLite",
                        "path": db_path,
                        "tables_found": len(tables),
                        "table_list": tables,
                        "sample_counts": test_results
                    }
                })
                
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"SQLite connection failed: {str(e)}"
                })
        
        elif db_type == 'mysql':
            try:
                import mysql.connector
                
                config = {
                    'host': db_host,
                    'port': int(db_port) if db_port else 3306,
                    'database': db_name,
                    'user': db_user,
                    'password': db_password
                }
                
                conn = mysql.connector.connect(**config)
                cursor = conn.cursor()
                
                # Get table list
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                
                conn.close()
                
                return json.dumps({
                    "status": "success",
                    "message": "MySQL connection successful",
                    "database_info": {
                        "type": "MySQL",
                        "host": db_host,
                        "database": db_name,
                        "tables_found": len(tables),
                        "table_list": tables
                    }
                })
                
            except ImportError:
                return json.dumps({
                    "status": "error",
                    "message": "MySQL connector not installed. Run: pip install mysql-connector-python"
                })
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"MySQL connection failed: {str(e)}"
                })
        
        elif db_type == 'postgresql':
            try:
                import psycopg2
                
                conn = psycopg2.connect(
                    host=db_host,
                    port=db_port or 5432,
                    database=db_name,
                    user=db_user,
                    password=db_password
                )
                cursor = conn.cursor()
                
                # Get table list
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                tables = [row[0] for row in cursor.fetchall()]
                
                conn.close()
                
                return json.dumps({
                    "status": "success",
                    "message": "PostgreSQL connection successful",
                    "database_info": {
                        "type": "PostgreSQL",
                        "host": db_host,
                        "database": db_name,
                        "tables_found": len(tables),
                        "table_list": tables
                    }
                })
                
            except ImportError:
                return json.dumps({
                    "status": "error",
                    "message": "PostgreSQL connector not installed. Run: pip install psycopg2"
                })
            except Exception as e:
                return json.dumps({
                    "status": "error",
                    "message": f"PostgreSQL connection failed: {str(e)}"
                })
        
        else:
            return json.dumps({
                "status": "error",
                "message": f"Unsupported database type: {db_type}"
            })
            
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Connection test failed: {str(e)}"
        })

# -----------------------------------------------------------------------------
def save_database_config():
    """
    Save database configuration for AI Agent
    """
    import json
    import sys
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        # Get configuration from request
        config = {
            "db_type": request.vars.get('db_type', 'sqlite'),
            "db_path": request.vars.get('db_path', ''),
            "db_host": request.vars.get('db_host', ''),
            "db_port": request.vars.get('db_port', ''),
            "db_name": request.vars.get('db_name', ''),
            "db_user": request.vars.get('db_user', ''),
            "db_password": request.vars.get('db_password', ''),
            "config_name": request.vars.get('config_name', 'default'),
            "description": request.vars.get('description', '')
        }
        
        # Save configuration to file
        private_path = os.path.join(request.folder, "private")
        config_file = os.path.join(private_path, "database_configs.json")
        
        # Load existing configurations
        try:
            with open(config_file, 'r') as f:
                configs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            configs = {}
        
        # Add new configuration
        configs[config["config_name"]] = config
        
        # Save configurations
        with open(config_file, 'w') as f:
            json.dump(configs, f, indent=2)
        
        return json.dumps({
            "status": "success",
            "message": f"Database configuration '{config['config_name']}' saved successfully"
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to save configuration: {str(e)}"
        })

# -----------------------------------------------------------------------------
def load_database_configs():
    """
    Load saved database configurations
    """
    import json
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        private_path = os.path.join(request.folder, "private")
        config_file = os.path.join(private_path, "database_configs.json")
        
        try:
            with open(config_file, 'r') as f:
                configs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            configs = {}
        
        return json.dumps({
            "status": "success",
            "configs": configs
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to load configurations: {str(e)}"
        })

# -----------------------------------------------------------------------------
def apply_database_config():
    """
    Apply a database configuration to the AI Agent
    """
    import json
    import sys
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        config_name = request.vars.get('config_name', '')
        
        if not config_name:
            return json.dumps({
                "status": "error",
                "message": "Configuration name is required"
            })
        
        # Load configuration
        private_path = os.path.join(request.folder, "private")
        config_file = os.path.join(private_path, "database_configs.json")
        
        with open(config_file, 'r') as f:
            configs = json.load(f)
        
        if config_name not in configs:
            return json.dumps({
                "status": "error",
                "message": f"Configuration '{config_name}' not found"
            })
        
        config = configs[config_name]
        
        # Create custom database adapter for the AI Agent
        adapter_code = f'''
# Custom Database Adapter - Generated by Database Manager
import sqlite3
import os
from typing import Dict, List, Any

class CustomDatabaseAdapter:
    def __init__(self):
        self.db_type = "{config.get('db_type', 'sqlite')}"
        self.db_path = r"{config.get('db_path', '')}"
        self.db_host = "{config.get('db_host', '')}"
        self.db_port = "{config.get('db_port', '')}"
        self.db_name = "{config.get('db_name', '')}"
        self.db_user = "{config.get('db_user', '')}"
        self.db_password = "{config.get('db_password', '')}"
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            if self.db_type == 'sqlite':
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row
            elif self.db_type == 'mysql':
                import mysql.connector
                self.connection = mysql.connector.connect(
                    host=self.db_host,
                    port=int(self.db_port) if self.db_port else 3306,
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password
                )
            elif self.db_type == 'postgresql':
                import psycopg2
                self.connection = psycopg2.connect(
                    host=self.db_host,
                    port=self.db_port or 5432,
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password
                )
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
            
            if self.db_type == 'sqlite':
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            else:
                # For MySQL/PostgreSQL
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            print(f"Query error: {e}")
            return []

# Replace the original database in ForestFireEmergencyDatabase
original_init = ForestFireEmergencyDatabase.__init__

def new_init(self, db_path=None):
    self.adapter = CustomDatabaseAdapter()
    self.db_path = self.adapter.db_path
    self.connection = None

def new_connect(self):
    return self.adapter.connect()

def new_execute_query(self, query, params=()):
    return self.adapter.execute_query(query, params)

ForestFireEmergencyDatabase.__init__ = new_init
ForestFireEmergencyDatabase.connect = new_connect
ForestFireEmergencyDatabase.execute_query = new_execute_query

        print(f"Applied database configuration: {config_name}")
        print(f"Database type: {config.get('db_type', 'sqlite')}")
        if config.get('db_type') == 'sqlite':
            print(f"Database path: {config.get('db_path', 'Unknown')}")
        else:
            print(f"Database host: {config.get('db_host', 'Unknown')}")
        '''        # Save the adapter code
        adapter_file = os.path.join(private_path, "custom_database_adapter.py")
        with open(adapter_file, 'w') as f:
            f.write(adapter_code)
        
        return json.dumps({
            "status": "success",
            "message": f"Database configuration '{config_name}' applied successfully",
            "config": config
        })
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to apply configuration: {str(e)}"
        })

# -----------------------------------------------------------------------------
