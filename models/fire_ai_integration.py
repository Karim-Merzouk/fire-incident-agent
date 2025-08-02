"""
Forest Fire AI Agent Integration
Custom module for seamless AI agent integration in Sahana Eden
"""

def ai_agent_widget():
    """
    Create a widget for the AI agent that can be embedded in dashboards
    """
    
    widget_html = DIV(
        DIV(
            H4(ICON("robot"), " Forest Fire AI Agent", 
               _class="widget-title",
               _style="color: #d32f2f; margin-bottom: 15px;"),
            P("Intelligent emergency response assistant for forest fire incidents",
              _class="text-muted"),
            DIV(
                A(ICON("comments"), " Launch AI Assistant",
                  _href=URL(c="fire", f="ai_agent"),
                  _class="btn btn-primary btn-lg",
                  _style="background-color: #d32f2f; border-color: #d32f2f;"),
                _class="text-center"
            ),
            _class="panel-body"
        ),
        _class="panel panel-default ai-agent-widget",
        _style="border: 2px solid #d32f2f; margin: 20px 0;"
    )
    
    return widget_html

def add_ai_agent_to_homepage():
    """
    Add AI agent access to the main homepage
    """
    
    # Check if we're on the homepage
    if request.controller == "default" and request.function == "index":
        # Add JavaScript to inject the AI agent widget
        response.files.append(URL(r=request, c="static", f="scripts/ai_agent_integration.js"))

# Add to menu if in fire module
if request.controller == "fire":
    # Add AI Agent to response menu
    if hasattr(response, 'menu') and response.menu:
        ai_menu_item = (T("AI Agent"), False, URL(c="fire", f="ai_agent"), [])
        
        # Find fire menu and add AI agent
        for menu_item in response.menu:
            if menu_item[0] == T("Fire") or "fire" in str(menu_item[2]).lower():
                if len(menu_item) > 3 and isinstance(menu_item[3], list):
                    menu_item[3].append(ai_menu_item)
                break
