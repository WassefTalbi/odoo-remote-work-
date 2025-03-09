from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    break_ids = fields.One2many("hr.break", "attendance_id", string="Breaks")
    total_break_time = fields.Float(string="Total Break Time (minutes)", compute="_compute_total_break_time", store=True)
    is_under_8_hours = fields.Boolean(string="is_under_8_hours ",compute="_compute_is_under_8_hours", store=False)

    @api.depends('break_ids.break_duration')
    def _compute_total_break_time(self):
        """ Compute the total break time for an attendance """
        for record in self:
            record.total_break_time = sum(record.break_ids.mapped('break_duration'))

    @api.depends('check_in', 'check_out', 'total_break_time')
    def _compute_worked_hours(self):
        """ Compute the worked hours, subtracting the total break time """
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                total_seconds = delta.total_seconds()
                # Convert total_break_time from minutes to seconds
                total_break_seconds = attendance.total_break_time * 60
                # Subtract break time from total worked time
                worked_seconds = total_seconds - total_break_seconds
                # Convert worked_seconds to hours
                attendance.worked_hours = worked_seconds / 3600
            else:
                attendance.worked_hours = 0

    def action_view_attendance_details(self):
        """ Open the attendance details wizard """
        return {
            'name': 'Attendance Details',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.break.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_attendance_id': self.id},
        }

    @api.depends('worked_hours')
    def _compute_is_under_8_hours(self):
        """ Check if the worked hours are less than 8 hours """
        for attendance in self:

            if attendance.worked_hours < 8:
                attendance.is_under_8_hours = True
            else:
                attendance.is_under_8_hours = False

    @api.depends('worked_hours')
    def _compute_overtime_hours(self):
        """ Calculate over time if worked hours exceed 8 hours """
        for attendance in self:
            if attendance.worked_hours > 8:
                attendance.overtime_hours = attendance.worked_hours - 8
            else:
                attendance.overtime_hours = 0