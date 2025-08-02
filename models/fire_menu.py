"""
Fire Module Menu Configuration
Adds Fire module with AI Agent to the main navigation menu
"""

# Add Fire module to the main menu after import
if hasattr(response, 'menu') and response.menu:
    # Fire module menu item
    fire_menu = (T("Fire Stations"), False, URL(c="fire", f="index"), [
        (T("Fire Stations"), False, URL(c="fire", f="station")),
        (T("Vehicles"), False, URL(c="fire", f="vehicle")),
        (T("Personnel"), False, URL(c="fire", f="human_resource")),
        (T("AI Emergency Agent"), False, URL(c="fire", f="ai_agent")),
    ])
    
    # Insert Fire menu into the main menu
    # Find a good position (after Organizations, before Disease Tracking)
    menu_inserted = False
    for i, menu_item in enumerate(response.menu):
        if "disease" in str(menu_item[2]).lower() or "Disease" in str(menu_item[0]):
            response.menu.insert(i, fire_menu)
            menu_inserted = True
            break
    
    # If no good position found, add at the end
    if not menu_inserted:
        response.menu.append(fire_menu)

# Also add a direct emergency access button if we're on any page
if request.controller != "fire":
    # Add emergency AI agent quick access
    if hasattr(response, 'view'):
        emergency_ai_script = """
        <style>
        .emergency-ai-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: #d32f2f;
            color: white;
            border: none;
            border-radius: 50px;
            padding: 15px 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            font-weight: bold;
        }
        .emergency-ai-btn:hover {
            background: #b71c1c;
            color: white;
            text-decoration: none;
        }
        </style>
        <a href="%s" class="emergency-ai-btn">
            <i class="fa fa-fire"></i> Emergency AI
        </a>
        """ % URL(c="fire", f="ai_agent")
        
        # Add to the page if possible
        try:
            response.files.append(('js', emergency_ai_script))
        except:
            pass
