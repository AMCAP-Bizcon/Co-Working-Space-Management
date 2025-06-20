from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, date


class MembershipPlan(models.Model):
    _name = 'membership.plan'
    _description = 'Membership Plan'
    _rec_name = 'name'
    _sql_constraints = [
        ('price_non_negative', 'CHECK(price >= 0)', 'Price must be non-negative.'),
        ('duration_positive', 'CHECK(duration > 0)', 'Duration must be greater than 0.'),
        ('name_unique', 'UNIQUE(name)', 'Plan name must be unique.'),
    ]

    name = fields.Char(string="Plan Name", required=True)
    duration = fields.Integer(string="Duration (days)", required=True)
    price = fields.Float(string="Price", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)


class MemberSubscription(models.Model):
    _name = 'member.subscription'
    _description = 'Member Subscription'
    _rec_name = 'member_id'

    member_id = fields.Many2one('member.directory', string='Member', required=True)
    plan_id = fields.Many2one('membership.plan', string='Plan', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', compute='_compute_end_date', store=True)
    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], string='Status', compute='_compute_status', store=True)

    @api.onchange('plan_id', 'start_date')
    def _onchange_plan(self):
        if self.plan_id:
            self.price = self.plan_id.price
            if self.start_date:
                self.end_date = self.start_date + timedelta(days=self.plan_id.duration)

    @api.depends('start_date', 'plan_id.duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.plan_id:
                rec.end_date = rec.start_date + timedelta(days=rec.plan_id.duration)
            else:
                rec.end_date = False

    @api.depends('start_date', 'end_date')
    def _compute_status(self):
        today = date.today()
        for rec in self:
            if not rec.start_date or not rec.end_date:
                rec.status = 'upcoming'
            elif today < rec.start_date:
                rec.status = 'upcoming'
            elif rec.start_date <= today <= rec.end_date:
                rec.status = 'active'
            else:
                rec.status = 'expired'

    @api.constrains('member_id', 'start_date', 'end_date')
    def _check_overlapping_subscriptions(self):
        for rec in self:
            overlapping = self.search([
                ('id', '!=', rec.id),
                ('member_id', '=', rec.member_id.id),
                ('start_date', '<=', rec.end_date),
                ('end_date', '>=', rec.start_date),
            ])
            if overlapping:
                raise ValidationError('A member cannot have overlapping active subscriptions.')

