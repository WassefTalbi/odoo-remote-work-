from email.policy import default

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class Tag(models.Model):
    _name='tag'
    property_ids=fields.Many2many('property')
    name = fields.Char(required=True)





