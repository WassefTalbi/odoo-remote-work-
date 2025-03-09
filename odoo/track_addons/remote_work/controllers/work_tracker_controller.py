import os
import json
import subprocess
from odoo import http,fields
from odoo.http import request

class WorkTrackerController(http.Controller):
    FOLDER_PATH="PycharmProjects/ScriptDev"
    SCRIPT_PATH = "PycharmProjects/ScriptDev/TrackUserSystemApplications.py"

    def _run_script(self, command):

        try:
            process = subprocess.Popen(
                ['python3', self.SCRIPT_PATH, command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            if error:
                return {"error": error.decode()}
            return json.loads(output.decode()) if output else {}
        except Exception as e:
            return {"error": str(e)}

    @http.route('/work-tracker/start', type="http", auth="public", csrf=False)
    def start_tracking(self, employee_id):

        result = self._run_script("start")
        if "error" not in result:
            request.env['hr.attendance'].sudo().create({
                'employee_id': employee_id,
                'action': 'start',
            })
        return result

    @http.route('/work-tracker/pause', type="http", auth="public", csrf=False)
    def pause_tracking(self, employee_id):

        result = self._run_script("pause")
        if "error" not in result:
            attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id), ('action', '=', 'start')
            ], limit=1, order="check_in desc")
            if attendance:
                attendance.write({'action': 'pause', 'pause_start': fields.Datetime.now()})
        return result

    @http.route('/work-tracker/resume', type="http", auth="public", csrf=False)
    def resume_tracking(self, employee_id):

        result = self._run_script("resume")
        if "error" not in result:
            attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id), ('action', '=', 'pause')
            ], limit=1, order="check_in desc")
            if attendance:
                pause_duration = (fields.Datetime.now() - attendance.pause_start).total_seconds() / 3600.0
                attendance.write({'action': 'resume', 'pause_end': fields.Datetime.now(), 'total_pause_duration': pause_duration})
        return result

    @http.route('/work-tracker/stop', type="http", auth="public", csrf=False)
    def stop_tracking(self, employee_id):

        result = self._run_script("stop")
        if "error" not in result:
            attendance = request.env['hr.attendance'].sudo().search([
                ('employee_id', '=', employee_id), ('action', 'in', ['start', 'resume'])
            ], limit=1, order="check_in desc")
            if attendance:
                attendance.write({'action': 'stop', 'check_out': fields.Datetime.now()})
        return result
