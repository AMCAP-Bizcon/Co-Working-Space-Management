# -*- coding: utf-8 -*-

{
    'name': 'Space Booking Management',
    'version': '1.0',
    'summary': 'Manage reservations for desks, meeting rooms, and booths.',
    'sequence': 10,
    'description': """
Module 3: space_booking

Purpose:
To manage reservations for desks, meeting rooms, and booths in the co-working space.

Functional Requirements:

Bookable Resource Model
- Name (e.g., "Meeting Room A", "Booth 3")
- Resource Type (Selection: Desk, Meeting Room, Booth)
- Capacity (integer)
- Location (char)
- Active (boolean)

Booking Model
- Member (many2one to member_directory.member)
- Resource (many2one to Bookable Resource)
- Start Datetime
- End Datetime
- Purpose (char)
- Booking Duration (computed in hours)
- Subtotal (computed: hourly rate × duration)
- Status (Selection: Draft, Confirmed, Cancelled)
- Hourly rate can be hardcoded or stored in the resource model as an additional field if needed.

Behavior:
- Onchange: Filter available resources when selecting date/time to avoid overlap. Autofill hourly rate when resource selected.
- Depends: Compute booking duration and subtotal.

Constraints:
- Prevent overlapping confirmed bookings for same resource.
- End datetime must be after start datetime.

Views Required:
- Form View
- List View
- Kanban View (optional)

Menu Structure:
Bookings > Resources > All Bookings > My Bookings.
    """,
    'category': 'Co working space',
    'website': 'https://www.gtec.ac.in/',
    'depends': ['base', 'member_directory'],
    'data': ['views/booking_views.xml', 'security/ir.model.access.csv'],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}