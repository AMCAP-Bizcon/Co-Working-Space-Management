from odoo import models, fields, api
class SupplyItem(models.Model):
    _name = 'inventory.supplies.item'  # MUST match exactly
    _description = 'Supply Item'

    name = fields.Char(string="Item Name", required=True)
    category = fields.Selection([
        ('beverage', 'Beverage'),
        ('stationery', 'Stationery'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other'),
    ], string="Category", required=True)
    uom = fields.Selection([
        ('units', 'Units'),
        ('kg', 'Kg'),
        ('liters', 'Liters'),
        ('packets', 'Packets'),
    ], string="Unit of Measure", required=True)
    opening_stock = fields.Integer(string="Opening Stock", default=0)
    total_purchased = fields.Integer(string="Total Purchased", default=0)
    total_consumed = fields.Integer(string="Total Consumed", default=0)
    current_stock = fields.Integer(string="Current Stock", compute='_compute_current_stock', store=True)
    reorder_qty = fields.Integer(string="Reorder Quantity", default=5)
    reorder_needed = fields.Boolean(string="Reorder Needed", compute='_compute_reorder_needed')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_item_name', 'unique(name)', 'Item name must be unique.'),
        ('reorder_qty_positive', 'CHECK(reorder_qty >= 0)', 'Reorder quantity must be non-negative.')
    ]

    @api.depends('opening_stock', 'total_purchased', 'total_consumed')
    def _compute_current_stock(self):
        for rec in self:
            rec.current_stock = rec.opening_stock + rec.total_purchased - rec.total_consumed

    @api.depends('current_stock', 'reorder_qty')
    def _compute_reorder_needed(self):
        for rec in self:
            rec.reorder_needed = rec.current_stock <= rec.reorder_qty

