# -*- coding: utf-8 -*-
{
    'name': 'Manage membership plan',
    'version': '1.0',
    'summary': ' ',
    'sequence': 10,
    'description': """
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
 Constraints:

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
        'views/membership_views.xml',
        'security/ir.model.access.csv',
        ],
    'demo':[
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

