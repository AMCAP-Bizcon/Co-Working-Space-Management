from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FeedbackReview(models.Model):
    _name = 'feedback.review'
    _description = 'Feedback Review'
    _rec_name = 'member_id'

    member_id = fields.Many2one('member.directory', string="Member", required=True)
    feedback_type = fields.Selection([
        ('booking', 'Booking'),
        ('event', 'Event'),
        ('service', 'Service')
    ], string="Feedback Type", required=True)
    related_record_id = fields.Many2one('maintenance.ticket', string="Related Record")  # Use correct model later
    rating = fields.Integer(string="Rating", required=True)
    comment = fields.Text(string="Comment")
    submitted_on = fields.Datetime(string="Submitted On", default=fields.Datetime.now)
    staff_response = fields.Text(string="Staff Response")
    status = fields.Selection([
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('closed', 'Closed')
    ], string="Status", default='new')

    @api.constrains('rating')
    def _check_rating(self):
        for record in self:
            if not (1 <= record.rating <= 5):
                raise ValidationError("Rating must be between 1 and 5.")

    _sql_constraints = [
        ('unique_feedback', 'unique(member_id, related_record_id)',
         'Only one feedback per member per related record allowed.')
    ]

    @api.onchange('rating')
    def _onchange_rating(self):
        if self.rating and self.rating <= 2:
            if not self.comment:
                return {
                    'warning': {
                        'title': _('Low Rating'),
                        'message': _('Please provide a comment for low ratings.')
                    }
                }
            else:
                return None
        else:
            return None