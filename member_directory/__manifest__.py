# -*- coding: utf-8 -*-
{
    'name': 'Manage member directory',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
    Module 1: member_directory
📌 Purpose:

To maintain a centralized directory of all individuals who interact with the co-working space—members, staff, or visitors.
✅ Functional Requirements:

    Member Types

        A member can be of type: Individual, Company, or Staff.

    Basic Information

        Full Name

        Email (must be unique)

        Phone

        Date of Birth

        Gender

        Member Photo

        Joining Date

        Member Type (selection field)

    Company Fields (Only for Company type)

        Company Name

        GST Number

        Contact Person (many2one to another member record)

    Membership Status (computed)

        Active if linked to an ongoing subscription (from membership_plan module)

        Expired if subscription is expired

        None if not subscribed

    Age (computed)

        Calculated from DOB

    Member Reference (auto)

        A unique auto-generated member code like MBR0001, MBR0002, etc.

🔄 Behavior:

    @api.onchange:

        If Member Type = Company, show company fields

        If Member Type ≠ Company, hide company fields and clear values

    @api.depends:

        Compute age from DOB

        Compute membership_status from related subscription

🔒 Constraints:

    Email must be unique (SQL constraint)

    DOB cannot be in the future (SQL constraint)

📊 Views Required:

    Form View: Complete member profile

    List View: Show member name, email, type, and status

    Kanban View: Display cards with photo, name, type, and status

🧭 Menu Structure:

Members
├── Members (list & form)
├── Companies (filtered where member_type = 'company')
└── Staff Directory (filtered where member_type = 'staff')

Shall I proceed with Module 2: membership_plan?
You said:
yes
ChatGPT said:

Great! Here's the spec for the second module:
Module 2: membership_plan
📌 Purpose:

To manage available membership plans (daily, weekly, monthly, etc.) and track active subscriptions purchased by members.
✅ Functional Requirements:
1. Membership Plan Model

Fields:

    Plan Name (e.g., “Daily Pass”, “Monthly Pro”)

    Duration in days (integer) — e.g., 1, 30

    Price (float)

    Description (text)

    Active (boolean)

SQL Constraints:

    Price must be ≥ 0

    Duration must be > 0

    Unique plan name

2. Member Subscription Model

Each subscription is linked to a member and a plan.

Fields:

    Member (many2one to member_directory.member)

    Plan (many2one to membership_plan.plan)

    Start Date (date)

    End Date (computed: start_date + plan.duration)

    Price (related or copied from plan)

    Status (computed): Upcoming, Active, Expired

🔄 Behavior:

    @api.onchange:

        When plan is selected, auto-set price and compute end date

    @api.depends:

        End Date (depends on start_date, plan.duration)

        Status (based on today’s date vs. start/end)

🔒 Constraints:

    A member cannot have overlapping active subscriptions (SQL constraint)

    One active subscription per member at a time

📊 Views Required:

    Form View: Plan creation/editing, subscription entry

    List View:

        Plan list: show name, duration, price, active

        Subscription list: show member, plan, start/end, status

    Kanban View (optional): For visualizing active/inactive plans

🧭 Menu Structure:

Membership
├── Plans
├── Member Subscriptions
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
