# -*- coding: utf-8 -*-
{
    'name': 'Manage maintenance tickets',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
    Module 5: maintenance_ticket
📌 Purpose:
To track facility-related issues like broken furniture, malfunctioning AC, or internet problems reported by members or staff.

✅ Functional Requirements:
1. Ticket Model
Fields:

Ticket Number (auto-generated, e.g., TCK0001)

Reported By (many2one to member_directory.member)

Reported On (date)

Issue Type (Selection: Electrical, Furniture, Internet, HVAC, Other)

Description (text)

Priority (Selection: Low, Medium, High)

SLA Deadline (computed: based on priority)

Assigned To (many2one to Staff – filtered from members with type = Staff)

Resolution Notes (text)

Resolved On (date)

Status (Selection: New, In Progress, Resolved, Closed)

🔄 Behavior:
@api.onchange:

When priority is set to “High”, set SLA Deadline = Reported On + 1 day

Medium → +3 days, Low → +7 days

@api.depends:

Compute SLA Deadline from priority and reported date

Compute resolution duration (Resolved On − Reported On) as a helper field (optional)

🔒 Constraints:
Only one unresolved ticket per asset (if you link this to a future asset model)

Resolved On cannot be before Reported On (SQL constraint)

📊 Views Required:
Form View: Create/edit maintenance tickets

List View: Ticket summary – issue, priority, status, deadline

Kanban View: Group tickets by status or priority

🧭 Menu Structure:
pgsql
Copy
Edit
Maintenance
├── Tickets
├── My Tickets (filtered by current user)
└── SLA Tracking (filtered: open & overdue)
    """,
    'category': 'Co working space',
    'website': 'https://www.mkce.ac.in',
    'depends': ['base'],
    'data': [
        ],
    'demo':[
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
