# space_booking/models/booking.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class BookableResource(models.Model):
    _name = 'space_booking.resource'
    _description = 'Bookable Resource'

    name = fields.Char(required=True)
    resource_type = fields.Selection([
        ('desk', 'Desk'),
        ('room', 'Meeting Room'),
        ('booth', 'Booth')
    ], required=True)
    capacity = fields.Integer(required=True)
    location = fields.Char()
    hourly_rate = fields.Float(string='Hourly Rate', required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Resource name must be unique'),
        ('capacity_positive', 'CHECK(capacity > 0)', 'Capacity must be greater than 0'),
    ]


class ResourceBooking(models.Model):
    _name = 'space_booking.booking'
    _description = 'Booking'

    member_id = fields.Many2one('member_directory.member', string='Member', required=True)
    resource_id = fields.Many2one('space_booking.resource', string='Resource', required=True)
    start_datetime = fields.Datetime(required=True)
    end_datetime = fields.Datetime(required=True)
    purpose = fields.Char()
    duration_hours = fields.Float(compute='_compute_duration', store=True)
    amount_total = fields.Float(compute='_compute_total', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='draft')

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration_hours = delta.total_seconds() / 3600
            else:
                record.duration_hours = 0

    @api.depends('duration_hours', 'resource_id.hourly_rate')
    def _compute_total(self):
        for record in self:
            record.amount_total = record.duration_hours * record.resource_id.hourly_rate

    @api.constrains('start_datetime', 'end_datetime')
    def _check_valid_times(self):
        for rec in self:
            if rec.end_datetime <= rec.start_datetime:
                raise ValidationError("End time must be after start time.")

    @api.constrains('resource_id', 'start_datetime', 'end_datetime', 'status')
    def _check_overlapping(self):
        for rec in self:
            if rec.status == 'confirmed':
                overlaps = self.search([
                    ('id', '!=', rec.id),
                    ('resource_id', '=', rec.resource_id.id),
                    ('status', '=', 'confirmed'),
                    ('start_datetime', '<', rec.end_datetime),
                    ('end_datetime', '>', rec.start_datetime)
                ])
                if overlaps:
                    raise ValidationError("This booking overlaps with an existing booking.")