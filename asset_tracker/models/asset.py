from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Asset(models.Model):
    _name = 'asset_tracker.asset'
    _description = 'Physical Asset'

    name = fields.Char(string='Asset Name', required=True)
    asset_type = fields.Selection([
        ('chair', 'Chair'),
        ('desk', 'Desk'),
        ('monitor', 'Monitor'),
        ('router', 'Router'),
        ('other', 'Other'),
    ], string='Asset Type', required=True)
    serial_number = fields.Char(string='Serial Number', required=True, unique=True)
    purchase_date = fields.Date(string='Purchase Date', required=True)
    assigned_to = fields.Many2one('member.directory', string='Assigned To')
    assignment_date = fields.Date(string='Assignment Date')
    state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    ], string='State', default='available')
    usage_days = fields.Integer(string='Usage Days', compute='_compute_usage_days')
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('serial_number_unique', 'unique(serial_number)', 'Serial Number must be unique.'),
    ]

    @api.constrains('purchase_date')
    def _check_purchase_date(self):
        for record in self:
            if record.purchase_date > fields.Date.today():
                raise ValidationError("Purchase date cannot be in the future.")

    @api.onchange('assigned_to')
    def _onchange_assigned_to(self):
        for record in self:
            if record.assigned_to:
                record.state = 'in_use'
                record.assignment_date = fields.Date.today()
            else:
                record.state = 'available'

    @api.depends('assignment_date', 'state')
    def _compute_usage_days(self):
        for record in self:
            if record.assignment_date and record.state == 'in_use':
                delta = fields.Date.today() - record.assignment_date
                record.usage_days = delta.days
            else:
                record.usage_days = 0
