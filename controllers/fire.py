"""
    Fire Rescue - Controllers
"""

module = request.controller

if not settings.has_module(module):
    raise HTTP(404, body="Module disabled: %s" % module)

# -----------------------------------------------------------------------------
def index():
    """ Module Homepage """

    module_name = settings.modules[module].get("name_nice")
    response.title = module_name

    htable = s3db.fire_shift_staff
    stable = s3db.fire_station
    station_id = None
    station_name = None

    human_resource_id = auth.s3_logged_in_human_resource()
    query = htable.human_resource_id == human_resource_id

    left = htable.on(htable.station_id == stable.id)

    row = db(query).select(htable.station_id,
                           stable.name,
                           left = left,
                           limitby = (0, 1),
                           ).first()
    if row:
        station_id = row.fire_shift_staff.station_id
        station_name = row.fire_station.name

    # Note that this requires setting the Porto Incident Types in modules/s3db/irs.py
    incidents = DIV(A(DIV(T("Fire"),
                          _style="background-color:red;",
                          _class="question-container fleft"),
                      _href=URL(c="irs", f="ireport", args=["create"],
                                vars={"type":"fire"})),
                    A(DIV(T("Rescue"),
                          _style="background-color:green;",
                          _class="question-container fleft"),
                      _href=URL(c="irs", f="ireport", args=["create"],
                                vars={"type":"rescue"})),
                    A(DIV(T("Hazmat"),
                          _style="background-color:yellow;",
                          _class="question-container fleft"),
                      _href=URL(c="irs", f="ireport", args=["create"],
                                vars={"type":"hazmat"})))

    return dict(incidents = incidents,
                station_id = station_id,
                station_name = station_name,
                module_name = module_name,
                )

# -----------------------------------------------------------------------------
def zone():
    """ RESTful CRUD controller """

    return crud_controller()

# -----------------------------------------------------------------------------
def zone_type():
    """ RESTful CRUD controller """

    return crud_controller()

# -----------------------------------------------------------------------------
def station():
    """ Fire Station """

    # CSV column headers, so no T()
    csv_extra_fields = [
        dict(label="Country",
             field=s3db.gis_country_id()),
        dict(label="Organisation",
             field=s3db.org_organisation_id())
    ]

    # Pre-processor
    def prep(r):
        # Location Filter
        s3db.gis_location_filter(r)

        if r.interactive:
            if r.component:
                if r.component.name == "human_resource":
                    s3db.org_site_staff_config(r)
                elif r.component.name == "inv_item":
                    # remove CRUD generated buttons in the tabs
                    s3db.configure("inv_inv_item",
                                   create = False,
                                   deletable = False,
                                   editable = False,
                                   listadd = False,
                                   )
            elif r.method == "update":
                field = r.table.obsolete
                field.readable = field.writable = True
        return True
    s3.prep = prep

    return crud_controller(rheader = fire_rheader,
                           csv_extra_fields = csv_extra_fields,
                           )

# -----------------------------------------------------------------------------
def station_vehicle():
    """ Vehicles of Fire Stations """

    s3.prep = lambda r: r.method == "import"

    return crud_controller()

# -----------------------------------------------------------------------------
def water_source():
    """ Water Sources """

    return crud_controller()

# -----------------------------------------------------------------------------
def hazard_point():
    """ Hazard Points """

    return crud_controller()

# -----------------------------------------------------------------------------
def person():
    """ Person Controller for Ajax Requests """

    return crud_controller("pr", "person")

# -----------------------------------------------------------------------------
def ireport_vehicle():
    """ REST controller """

    return crud_controller("irs", "ireport_vehicle")

# -----------------------------------------------------------------------------
def ai_agent():
    """
    Forest Fire Emergency Response AI Agent
    Integrated AI assistant for fire emergency management
    """
    
    response.title = T("Forest Fire Emergency AI Agent")
    
    # Import the AI agent functionality
    import sys
    import os
    
    # Add the private directory to Python path for imports
    private_path = os.path.join(request.folder, "private")
    if private_path not in sys.path:
        sys.path.insert(0, private_path)
    
    try:
        # Import our AI agent
        from final_forest_fire_agent import ForestFireAgent
        from realistic_forest_fire_tool import RealisticForestFireDatabaseTool
        
        # Initialize the AI agent
        agent = ForestFireAgent()
        db_tool = RealisticForestFireDatabaseTool()
        
        # Handle AJAX requests for chat
        if request.extension == "json":
            if request.vars.action == "chat":
                user_message = request.vars.message
                if user_message:
                    try:
                        # Process the message through our AI agent
                        response_text = agent.query(user_message)
                        return {"status": "success", "response": response_text}
                    except Exception as e:
                        return {"status": "error", "message": str(e)}
            
            elif request.vars.action == "get_incidents":
                try:
                    # Get current fire incidents from database
                    incidents = db_tool.get_emergency_overview()
                    return {"status": "success", "incidents": incidents}
                except Exception as e:
                    return {"status": "error", "message": str(e)}
        
        # Render the AI agent interface
        return {"agent_initialized": True}
        
    except ImportError as e:
        # If AI agent modules are not available, show setup instructions
        error_msg = """
        Forest Fire AI Agent modules not found. 
        Please ensure the following files are in the private directory:
        - final_forest_fire_agent.py
        - realistic_forest_fire_tool.py
        - forest_fire_database_tool.py
        """
        return {"agent_initialized": False, "error": error_msg}

# -----------------------------------------------------------------------------
def chat():
    """
    AJAX endpoint for AI agent chat functionality with Gemini API
    """
    import json
    import sys
    import os
    from datetime import datetime
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    # Get user message
    user_message = request.vars.get('message', 'Hello')
    
    try:
        # Add the private directory to Python path for imports
        private_path = os.path.join(request.folder, "private")
        if private_path not in sys.path:
            sys.path.insert(0, private_path)
        
        # Force reload the module to get latest version
        import importlib
        if 'final_forest_fire_agent' in sys.modules:
            importlib.reload(sys.modules['final_forest_fire_agent'])
        
        # Import and initialize the working AI agent
        from final_forest_fire_agent import ForestFireAgent
        
        # Initialize the agent - it will automatically select the best available AI mode
        agent = ForestFireAgent()
        
        # Process the message through the AI agent
        ai_response = agent.query(user_message)
        
        # Get the current operating mode
        agent_mode = agent.get_mode()
        
        # Return proper JSON response
        return json.dumps({
            "status": "success", 
            "response": ai_response,
            "agent_mode": agent_mode,
            "timestamp": str(datetime.now())[:19]
        })
        
    except ImportError as e:
        # Import error - agent file not found or broken
        return json.dumps({
            "status": "error", 
            "message": f"AI Agent Import Error: {str(e)}",
            "agent_mode": "import_error"
        })
    except Exception as e:
        # General error
        return json.dumps({
            "status": "error", 
            "message": f"AI Agent Error: {str(e)}",
            "agent_mode": "error"
        })

# -----------------------------------------------------------------------------
def simple_test():
    """
    Ultra simple test function
    """
    return {"message": "Simple test works!"}

# -----------------------------------------------------------------------------
def test_agent():
    """
    Simple test endpoint to check AI agent functionality
    """
    try:
        # Test basic import
        import sys
        import os
        private_path = os.path.join(request.folder, "private")
        if private_path not in sys.path:
            sys.path.insert(0, private_path)
        
        # Test import step by step
        try:
            from final_forest_fire_agent import ForestFireAgent
            import_status = "✅ Import successful"
        except Exception as e:
            import_status = f"❌ Import failed: {str(e)}"
            return {"import": import_status}
        
        # Test initialization
        try:
            agent = ForestFireAgent()
            init_status = "✅ Agent initialized"
        except Exception as e:
            init_status = f"❌ Initialization failed: {str(e)}"
            return {"import": import_status, "init": init_status}
        
        # Test simple query
        try:
            response = agent.query("Hello")
            query_status = f"✅ Query successful: {response[:100]}..."
        except Exception as e:
            query_status = f"❌ Query failed: {str(e)}"
        
        return {
            "import": import_status,
            "init": init_status, 
            "query": query_status
        }
        
    except Exception as e:
        return {"error": f"General error: {str(e)}"}

# -----------------------------------------------------------------------------
def test_gemini():
    """
    Test Gemini API connectivity
    """
    import json
    import sys
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        # Add the private directory to Python path for imports
        private_path = os.path.join(request.folder, "private")
        if private_path not in sys.path:
            sys.path.insert(0, private_path)
        
        # Test agno import
        try:
            from agno.agent import Agent
            from agno.models.google import Gemini
            agno_status = "✅ Agno framework available"
        except Exception as e:
            agno_status = f"❌ Agno import failed: {str(e)}"
            return json.dumps({"agno": agno_status})
        
        # Test Gemini initialization
        try:
            api_key = "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
            model = Gemini(id="gemini-1.5-flash", api_key=api_key)
            gemini_status = "✅ Gemini model initialized"
        except Exception as e:
            gemini_status = f"❌ Gemini failed: {str(e)}"
            return json.dumps({"agno": agno_status, "gemini": gemini_status})
        
        # Test agent initialization
        try:
            agent = Agent(
                name="Test Agent",
                model=model,
                instructions="You are a test agent. Respond with exactly: 'Gemini is working correctly!'"
            )
            agent_status = "✅ Agent initialized"
        except Exception as e:
            agent_status = f"❌ Agent init failed: {str(e)}"
            return json.dumps({"agno": agno_status, "gemini": gemini_status, "agent": agent_status})
        
        # Test actual query
        try:
            response_obj = agent.run("Test message")
            if hasattr(response_obj, 'content'):
                test_response = response_obj.content
            else:
                test_response = str(response_obj)
            query_status = f"✅ Query successful: {test_response[:100]}"
        except Exception as e:
            query_status = f"❌ Query failed: {str(e)}"
        
        return json.dumps({
            "agno": agno_status,
            "gemini": gemini_status,
            "agent": agent_status,
            "query": query_status,
            "response": test_response if 'test_response' in locals() else "No response"
        })
        
    except Exception as e:
        return json.dumps({"error": f"General error: {str(e)}"})

# -----------------------------------------------------------------------------
def debug_ai():
    """
    Debug AI initialization status
    """
    import json
    import sys
    import os
    
    # Set proper response headers for JSON
    response.headers['Content-Type'] = 'application/json'
    
    try:
        # Add the private directory to Python path for imports
        private_path = os.path.join(request.folder, "private")
        if private_path not in sys.path:
            sys.path.insert(0, private_path)
        
        # Import and test the AI agent
        from final_forest_fire_agent import ForestFireAgent
        
        # Initialize agent and check flags
        agent = ForestFireAgent()
        
        # Check what's available
        debug_info = {
            "initialization": {
                "gemini_model": str(type(agent.gemini_model)) if agent.gemini_model else "None",
                "gemini_model_value": str(agent.gemini_model),
                "agent": str(type(agent.agent)) if agent.agent else "None", 
                "agent_value": str(agent.agent),
                "api_key_present": bool(agent.api_key),
                "api_key_length": len(agent.api_key) if agent.api_key else 0,
                "conversation_history": len(agent.conversation_history)
            }
        }
        
        # Check imports in the agent file
        try:
            from final_forest_fire_agent import GOOGLE_AI_AVAILABLE, AGNO_AVAILABLE, REQUESTS_AVAILABLE
            debug_info["imports"] = {
                "google_ai_available": GOOGLE_AI_AVAILABLE,
                "agno_available": AGNO_AVAILABLE, 
                "requests_available": REQUESTS_AVAILABLE
            }
        except Exception as e:
            debug_info["imports"] = {"error": str(e)}
        
        # Test requests import directly
        try:
            import requests
            debug_info["direct_requests"] = "Available"
        except Exception as e:
            debug_info["direct_requests"] = f"Error: {str(e)}"
        
        # Test a simple query
        test_response = agent.query("Test query")
        debug_info["test_query"] = test_response[:200] + "..." if len(test_response) > 200 else test_response
        
        return json.dumps(debug_info, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Debug error: {str(e)}"})

# -----------------------------------------------------------------------------
def fire_rheader(r, tabs=[]):
    """ Resource headers for component views """

    rheader = None
    if r.representation == "html":

        if r.name == "station":
            station = r.record
            if station:

                tabs = [
                    (T("Station Details"), None),
                    (T("Vehicles"), "vehicle"),
                    (T("Staff"), "human_resource"),
                    #(T("Shifts"), "shift"),
                    (T("Roster"), "shift_staff"),
                    (T("Vehicle Deployments"), "vehicle_report"),
                    (T("AI Agent"), "ai_agent"),  # Add AI Agent tab
                ]
                rheader_tabs = s3_rheader_tabs(r, tabs)

                rheader = DIV(rheader_tabs)

    return rheader

# END =========================================================================
