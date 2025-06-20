from odoo import models, fields, api
from odoo.exceptions import ValidationError
class SupplyMovement(models.Model):
    _name = 'inventory.supplies.movement'
    _description = 'Supply Movement'

    item_id = fields.Many2one('inventory.supplies.item', string='Item', required=True)
    movement_type = fields.Selection([
        ('inward', 'Inward'),
        ('outward', 'Outward'),
    ], string='Movement Type', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    date = fields.Date(string='Date', required=True)
    note = fields.Char(string='Purpose / Note')

    @api.constrains('quantity')
    def _check_quantity_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("Quantity must be greater than 0.")

    @api.model
    def create(self, vals):
        item = self.env['inventory.supplies.item'].browse(vals.get('item_id'))
        movement_type = vals.get('movement_type')
        qty = vals.get('quantity', 0)

        if not item.exists():
            raise ValidationError("Invalid item selected.")

        if movement_type == 'inward':
            item.write({
                'total_purchased': item.total_purchased + qty
            })
        elif movement_type == 'outward':
            if qty > item.current_stock:
                raise ValidationError("Cannot consume more than available stock.")
            item.write({
                'total_consumed': item.total_consumed + qty
            })

        return super(SupplyMovement, self).create(vals)

    @api.onchange('item_id')
    def _onchange_item(self):
        if self.item_id:
            self.note = f"Category: {self.item_id.category}, UOM: {self.item_id.uom}"
