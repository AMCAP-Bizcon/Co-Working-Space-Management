
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
https://github.com/AMCAP-Bizcon/Co-Working-Space-Management
    Form View: Complete member profile

    List View: Show member name, email, type, and status

    Kanban View: Display cards with photo, name, type, and status

🧭 Menu Structure:

Members
├── Members (list & form)
├── Companies (filtered where member_type = 'company')
└── Staff Directory (filtered where member_type = 'staff')

    """,
    'category': 'Co working space',
    'website': 'https://www.mkce.ac.in',
    'depends': ['base'],
    'data': [
        'views/member_view.xml',
        'security/ir.model.access.csv',
        ],
    'demo':[
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

