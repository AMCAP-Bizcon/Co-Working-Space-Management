# -*- coding: utf-8 -*-
{
    'name': 'Manage Simple Billing',
    'version': '1.0',
    'summary': '',
    'sequence': 10,
    'description': """
    Module 7: simple_billing
📌 Purpose:

To generate simple draft invoices for bookings, memberships, or events—without integrating with Odoo's Accounting app.
✅ Functional Requirements:
1. Invoice Model

Fields:

    Invoice Number (auto-generated, e.g., INV0001)

    Customer (many2one to member_directory.member)

    Invoice Date (date)

    Total Amount (computed)

    Status (Selection: Draft, Confirmed, Cancelled)

    Notes (text)

SQL Constraints:

    Unique invoice number

    One draft invoice per customer per day (can be enforced by unique SQL constraint on customer + date + status = draft)

2. Invoice Line Model

Fields:

    Invoice (many2one to invoice)

    Description (char)

    Related Record (many2one to space_booking.booking or membership_plan.subscription) — optional

    Quantity (float)

    Unit Price (float)

    Subtotal (computed: qty × unit price)

SQL Constraints:

    Quantity and unit price must be ≥ 0

🔄 Behavior:

    @api.onchange:

        When customer is selected, allow pulling unbilled bookings/subscriptions

        When related record is picked, auto-fill line description and price

    @api.depends:

        Subtotal = Quantity × Unit Price

        Total = Sum of all line subtotals

📊 Views Required:

    Form View: Invoice form with embedded invoice lines

    List View:

        Invoice summary: customer, total, status

        Invoice lines (optional, useful for audit)

    Kanban View: Invoices grouped by status (optional)

🧭 Menu Structure:

Billing
 Invoices
 My Invoices (filtered by current user)
 Invoice Lines (optional submenu)


    """,
    'category': 'Co working space',
    'website': 'https://www.gtec.ac.in',
    'depends': ['base','member_directory'],
    'data': ['views/billing_invoice_views.xml','security/ir.model.access.csv'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
