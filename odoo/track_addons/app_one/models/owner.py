from email.policy import default

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class Owner(models.Model):
    _name='owner'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()
    tt=fields.Char()
    property_ids=fields.One2many('property','owner_id')
