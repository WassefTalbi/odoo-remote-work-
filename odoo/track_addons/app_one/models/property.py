from email.policy import default

from odoo import models, fields,api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class Property(models.Model):
    _name='property'

    name = fields.Char(required=True,default='New house')
    description = fields.Text()
    postcode = fields.Char()
    date_availability=fields.Date()
    expected_selling_date = fields.Date()
    is_late=fields.Boolean()
    expected_price=fields.Float(digits=(0,5))
    selling_price=fields.Float(digits=(0,5))
    diff = fields.Float(compute='_compute_diff',store=0)
    #with the attribut readonly on field diff the diff will be calculated automaticly and the user can update it into the interface (ui)
    #with the attribut diff store on field  the diff the value of the result will be stored into DB
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([
        ('north','NORTH'),
        ('south','SOUTH'),
        ('east','EAST'),
        ('west','WEST')
    ],default='north')

    owner_id = fields.Many2one('owner')
    tag_ids=fields.Many2many('tag')
    state=fields.Selection([
        ('draft','DRAFT'),('pending','PENDING'),('sold','SOLD'),('closed','CLOSED')
    ],default='draft')
    _sql_constraints=[
        ('unique_description','unique("description")','description is exist'),
        ('unique_name', 'unique("name")', 'name is exist'),
    ]


    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms<=0 :
                raise ValidationError("bedrooms numnber can't be negatif or zero")

    # @api.model_create_multi
    # def create(self, vals):
    #     result=super(Property,self).create(vals)
    #     print('print inside create method ')
    #     return result
    # @api.model
    # def search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     result=super(Property,self).search( domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print('print inside search method ')
    #     return result
    #
    # def write(self, vals):
    #     result = super(Property,self).write(vals)
    #     print('print inside update method ')
    #     return result
    #
    # def unlink(self):
    #     result=super(Property,self).unlink()
    #     print('print inside delete method')
    #     return result

    def change_state_draft(self):
        print("print inside draft")
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state='draft'


    def change_state_pending(self):
        print("print inside pending")
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def change_state_sold(self):
        print("print inside sold")
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def change_state_closed(self):
        print("print inside closed")
        for rec in self:
            rec.state = 'closed'

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("print inside onchange_expected_price ")
            return {
                'warning':{'title':'warning','message':'negative value','type':'notification'}
            }

    @api.depends('expected_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("print inside compute diff")
            rec.diff=rec.expected_price-rec.selling_price
    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date<fields.date.today():
                rec.is_late=True

    def create_history_record(self,old_state,new_state):

        for rec in self:
            rec.env['property.history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state': old_state,
                'new_state': new_state,

            })


    def action(self):
        # print(self.env)
        # print(self.env.user)
        # print(self.env.user.login)
        # print(self.env.user.name)
        print(self.env['owner'])

    def redirect_to_related_owner(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id=self.env.ref('app_one.owner_view_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,'form']]
        return action
