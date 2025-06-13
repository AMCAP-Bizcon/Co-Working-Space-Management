from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SimpleBillingInvoice(models.Model):
    _name = 'simple.billing.invoice'
    _description = 'Simple Billing Invoice'
    _order = 'id desc'

    name = fields.Char(string='Invoice Number', readonly=True, copy=False, default='New')
    customer_id = fields.Many2one('member_directory.member', string='Customer', required=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today)
    invoice_line_ids = fields.One2many('simple.billing.line', 'invoice_id', string='Invoice Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string='Status')
    note = fields.Text(string='Note')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('simple.billing.invoice') or 'INV0001'
        return super().create(vals)

    @api.depends('invoice_line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.subtotal for line in rec.invoice_line_ids)

    _sql_constraints = [
        ('unique_invoice_name', 'UNIQUE(name)', 'Invoice Number must be unique.'),
    ]


class SimpleBillingLine(models.Model):
    _name = 'simple.billing.line'
    _description = 'Simple Invoice Line'

    invoice_id = fields.Many2one('simple.billing.invoice', string='Invoice', required=True, ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    related_record_id = fields.Many2one('space_booking.booking', string='Related Booking')  # optional

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.unit_price

    @api.constrains('quantity', 'unit_price')
    def _check_positive_values(self):
        for rec in self:
            if rec.quantity < 0 or rec.unit_price < 0:
                raise ValidationError('Quantity and Unit Price must be non-negative.')