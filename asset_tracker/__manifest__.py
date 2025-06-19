# -*- coding: utf-8 -*-
{
    'name': ' Assert Tracker',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """Module 10: asset_tracker
Purpose:

To track physical assets (chairs, monitors, routers, etc.) and their current assignments to members or areas.
 Functional Requirements:
1. Asset Model

Fields:

    Asset Name (char)

    Asset Type (Selection: Chair, Desk, Monitor, Router, Other)

    Serial Number (char)

    Purchase Date (date)

    Assigned To (many2one to member_directory.member)

    Assignment Date (date)

    State (Selection: Available, In Use, Maintenance, Retired)

    Usage Days (computed: days since last assignment)

    Notes (text)

SQL Constraints:

    Serial Number must be unique and not null

    Purchase Date cannot be in the future

 Behavior:

    @api.onchange:

        If Assigned To is selected, automatically set State = In Use and set Assignment Date = today

        If Assigned To is cleared, set State = Available

    @api.depends:

        Usage Days = today − Assignment Date (only if currently in use)


📊 Views Required:

    Form View: Create/edit asset record

    List View: Show asset name, type, state, assignee, usage days

    Kanban View: Group assets by state (In Use, Available, Maintenance, Retired)

 Menu Structure:

Assets
├── All Assets
├── Assigned Assets (filtered: In Use)
├── Available Assets
├── Maintenance Tracker
    
    """,
    'category': 'Co working space',
    'website': 'https://www.mkce.ac.in',
    'depends': ['base','member_directory'],
    'data': ['views/asset_view.xml',
        'security/ir.model.access.csv'
        ],
    'demo':[
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}