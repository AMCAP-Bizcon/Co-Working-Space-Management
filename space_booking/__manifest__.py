# -*- coding: utf-8 -*-
{
    'name': 'Space Booking Management',
    'version': '1.0',
    'summary': '',
    'sequence': 10,
    'description': """
    Module 3: space_booking
📌 Purpose:

To manage reservations for desks, meeting rooms, and booths in the co-working space.
✅ Functional Requirements:
1. Bookable Resource Model

Fields:

    Name (e.g., "Meeting Room A", "Booth 3")

    Resource Type (Selection: Desk, Meeting Room, Booth)

    Capacity (integer)

    Location (char)

    Active (boolean)

SQL Constraints:

    Capacity must be > 0

    Unique name

2. Booking Model

Fields:

    Member (many2one to member_directory.member)

    Resource (many2one to Bookable Resource)

    Start Datetime

    End Datetime

    Purpose (char)

    Booking Duration (computed in hours)

    Subtotal (computed: hourly rate × duration)

    Status (Selection: Draft, Confirmed, Cancelled)

    Hourly rate can be hardcoded or stored in the resource model as an additional field if needed.

🔄 Behavior:

    @api.onchange:

        When a date/time is chosen, filter available resources (to avoid overlapping)

        When resource is selected, autofill hourly rate (optional)

    @api.depends:

        Compute booking_duration in hours

        Compute subtotal

🔒 Constraints:

    Prevent overlapping confirmed bookings for the same resource (SQL-level check on datetime overlap)

    End datetime must be after start datetime (SQL constraint)

📊 Views Required:

    Form View: Create or modify a booking

    List View: Show bookings with member, resource, start, end, status

    Kanban View: Optional – show bookings by status or resource

🧭 Menu Structure:

Bookings
 Resources
 All Bookings
 My Bookings (filtered by current user if applicable)

    """,
    'category': 'Co working space',
    'website': 'https://www.gtec.ac.in/',
    'depends': ['base'],
    'data': [
            ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
