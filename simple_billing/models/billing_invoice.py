from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SimpleInvoice(models.Model):
    _name = 'simple.billing.invoice'
    _description = 'Simple Invoice'
    _order = 'invoice_date desc'

    name = fields.Char(string='Invoice Number', required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('member.directory', string='Customer', required=True)
    invoice_date = fields.Date(string='Invoice Date', required=True, default=fields.Date.today)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                              default='draft', required=True)
    notes = fields.Text(string='Notes')
    line_ids = fields.One2many('simple.billing.invoice.line', 'invoice_id', string='Invoice Lines')

    _sql_constraints = [
        ('unique_invoice_number', 'unique(name)', 'Invoice Number must be unique.'),
        ('unique_draft_per_day_customer',
         'unique(customer_id, invoice_date, status)',
         'Only one draft invoice per customer per day is allowed.')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('simple.billing.invoice') or 'INV0001'
        return super().create(vals)

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.line_ids)


class SimpleInvoiceLine(models.Model):
    _name = 'simple.billing.invoice.line'
    _description = 'Invoice Line'

    invoice_id = fields.Many2one('simple.billing.invoice', string='Invoice', required=True, ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    related_record_id = fields.Reference(
        selection=[
            ('space_booking.booking', 'Booking'),
            ('membership_plan.subscription', 'Subscription')
        ],
        string='Related Record',
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('related_record_id')
    def _onchange_related_record(self):
        if self.related_record_id:
            self.description = self.related_record_id.display_name
            if hasattr(self.related_record_id, 'amount'):
                self.unit_price = self.related_record_id.amount

    @api.constrains('quantity', 'unit_price')
    def _check_non_negative(self):
        for line in self:
            if line.quantity < 0 or line.unit_price < 0:
                raise ValidationError("Quantity and Unit Price must be non-negative.")
