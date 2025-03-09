import subprocess
import json
import os
import signal
from odoo import models, fields, api

class CheckinCheckoutWizard(models.TransientModel):
    _name = 'checkin.checkout.wizard'
    _description = 'Wizard for Employee Check-In/Check-Out'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    check_in = fields.Datetime(string="Check In Time", readonly=True)
    check_out = fields.Datetime(string="Check Out Time", readonly=True)
    disabled_check_in = fields.Boolean(compute="_compute_disabled_check_in", store=False)
    disabled_check_out = fields.Boolean(compute="_compute_disabled_check_out", store=False)
    process = None
    SCRIPT_PATH = os.path.expanduser("~/PycharmProjects/ScriptDev/TrackUserSystemApplications.py")
    VENV_PATH = os.path.expanduser("~/PycharmProjects/ScriptDev/.venv/bin/activate")


    def run_script(self):
        try:
            if not os.path.exists(self.SCRIPT_PATH):

                return {"error": f"Script not found: {self.SCRIPT_PATH}"}

            if not os.path.exists(self.VENV_PATH):

                return {"error": f"Virtual environment not found: {self.VENV_PATH}"}

            print("start run the script ..")
            command = f"source {self.VENV_PATH} && python {self.SCRIPT_PATH}"
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                executable="/bin/bash"
            )
            print(" script running ...")
        except Exception as e:
            print(f"Error running script: {str(e)}")
            return {"error": str(e)}
    def stop_script(self):
        """
        Stop the running script by terminating the process using its PID.
        """

        try:

            command = f"ps aux | grep {self.SCRIPT_PATH.split('/')[-1]} | grep -v grep"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            if out:

                pid = int(out.split()[1])
                os.kill(pid, signal.SIGTERM)


        except Exception as e:
            print(f"Error stopping script: {str(e)}")
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        employee = self.env['hr.employee'].search([], limit=1)
        if employee:
            res.update({
                'employee_id': self.env.user.employee_id.id,
                'check_in': fields.Datetime.now(),
            })

        return res
    @api.depends('employee_id')
    def _compute_disabled_check_in(self):
        for record in self:
            record.disabled_check_in = bool(record._get_attendance_status())
    @api.depends('employee_id')
    def _compute_disabled_check_out(self):
        for record in self:
            attendance = record._get_attendance_status()
            record.disabled_check_out = not (attendance and not attendance.check_out)
    def _get_attendance_status(self):
        """ Returns the attendance record if the employee has checked in but not checked out. """
        return self.env['hr.attendance'].search([
            ('employee_id', '=', self.env.user.employee_id.id),
            ('check_out', '=', False)
        ], limit=1)
    def toggle_checkin(self):
        self.run_script()
        attendance = self.env['hr.attendance'].create({
            'employee_id': self.env.user.employee_id.id ,
            'check_in': fields.Datetime.now(),
        })

        return  {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.attendance',
            'view_mode': 'tree',
            'target': 'current',
            'views': [(self.env.ref('hr_attendance.view_attendance_tree').id, 'tree')],
            'context': {
                'default_employee_id': self.env.user.employee_id.id,
                'search_default_filter': 1,

            }
        }

    def toggle_checkout(self):


        self.stop_script()
        attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', self.env.user.employee_id.id ),
            ('check_out', '=', False)
        ], limit=1)
        if attendance:
            attendance.write({'check_out': fields.Datetime.now()})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.attendance',
            'view_mode': 'tree',
            'target': 'current',
            'views': [(self.env.ref('hr_attendance.view_attendance_tree').id, 'tree')],
            'context': {
                'default_employee_id': self.env.user.employee_id.id,
                'search_default_filter': 1
            }
        }



