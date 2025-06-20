
from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class MemberDirectory(models.Model):
    _name = 'member.directory'
    _description = 'Member Directory'
    _rec_name = 'full_name'
    _order = 'id desc'

    full_name = fields.Char(string='Full Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    photo = fields.Image(string='Member Photo')
    joining_date = fields.Date(string='Joining Date')
    member_type = fields.Selection([
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('staff', 'Staff')
    ], string='Member Type', required=True)

    company_name = fields.Char(string='Company Name')
    gst_number = fields.Char(string='GST Number')
    contact_person_id = fields.Many2one('member.directory', string='Contact Person')

    membership_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('none', 'None')
    ], string='Membership Status', compute='_compute_membership_status', store=True)

    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    member_reference = fields.Char(string='Member Reference', readonly=True, copy=False, default=lambda self: _('New'))

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list):
            for val in vals:
                if val.get('member_reference', _('New')) == _('New'):
                    val['member_reference'] = self.env['ir.sequence'].next_by_code('member.directory') or _('New')
        else:
            if vals.get('member_reference', _('New')) == _('New'):
                vals['member_reference'] = self.env['ir.sequence'].next_by_code('member.directory') or _('New')

        return super(MemberDirectory, self).create(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year - (
                    (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0

    @api.depends('member_type')
    def _compute_membership_status(self):
        for rec in self:
            # This needs to be linked to a subscription model from membership_plan
            rec.membership_status = 'none'

    @api.onchange('member_type')
    def _onchange_member_type(self):
        if self.member_type != 'company':
            self.company_name = False
            self.gst_number = False
            self.contact_person_id = False

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self:
            if rec.email and self.search_count([('email', '=', rec.email), ('id', '!=', rec.id)]) > 0:
                raise ValidationError('Email must be unique.')

    @api.constrains('date_of_birth')
    def _check_dob_not_future(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > date.today():
                raise ValidationError('Date of Birth cannot be in the future.')
