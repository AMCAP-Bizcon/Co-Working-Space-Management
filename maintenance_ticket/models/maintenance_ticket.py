# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta

class MaintenanceTicket(models.Model):
    _name = 'maintenance.ticket'
    _description = 'Maintenance Ticket'

    ticket_number = fields.Char(string='Ticket Number', required=True, readonly=True, copy=False, default='New')
    description = fields.Text(string="Description")
    reported_on = fields.Date(string="Reported On", default=fields.Date.today)
    resolution_notes = fields.Text(string="Resolution Notes")
    resolved_on = fields.Date(string="Resolved On")

    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string='Status', default='new')

    issue_type = fields.Selection([
        ('electrical', 'Electrical'),
        ('furniture', 'Furniture'),
        ('internet', 'Internet'),
        ('hvac', 'HVAC'),
        ('other', 'Other'),
    ], string='Issue Type')

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')

    sla_deadline = fields.Date(string="SLA Deadline", compute="_compute_sla_deadline", store=True)

    @api.model
    def create(self, vals):
        if vals.get('ticket_number', 'New') == 'New':
            vals['ticket_number'] = self.env['ir.sequence'].next_by_code('maintenance.ticket') or 'New'
        return super(MaintenanceTicket, self).create(vals)

    @api.depends('reported_on', 'priority')
    def _compute_sla_deadline(self):
        for record in self:
            if record.reported_on and record.priority:
                if record.priority == 'low':
                    record.sla_deadline = record.reported_on + timedelta(days=5)
                elif record.priority == 'medium':
                    record.sla_deadline = record.reported_on + timedelta(days=3)
                elif record.priority == 'high':
                    record.sla_deadline = record.reported_on + timedelta(days=1)
            else:
                record.sla_deadline = False
