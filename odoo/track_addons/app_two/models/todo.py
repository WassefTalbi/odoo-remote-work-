from email.policy import default

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class Todo(models.Model):
    _name='todo'

    name = fields.Char(required=True)





