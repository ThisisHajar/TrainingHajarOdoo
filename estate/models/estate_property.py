from email.policy import default
from pickle import FALSE

from docutils.nodes import option

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

from odoo.exceptions import UserError, ValidationError

from odoo import fields, models
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Model"
    # _order = "id desc"

    name = fields.Char(string='Name',required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,default=datetime.today()+timedelta(days=90))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=False, copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades = fields.Integer()
    garage= fields.Boolean()
    garden = fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(selection=[("north", "North"),("south", "South"),("east", "East"),("west", "West"),],)
    active=fields.Boolean(default=True)
    state=fields.Selection(selection=[('new','New'),('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],
                           required=True,
                           copy=False,
                           )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type",options="{'no_create': True, 'no_open': True}")
    salesperson = fields.Many2one("res.users", string="Salesman", default=lambda self:self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer")
    tag_id = fields.Many2many('estate.property.tag',string='Tags')
    offer_id = fields.One2many('estate.property.offer','property_id',string='Offers')
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute='_compute_price', string= 'Best Price')


    _sql_constraints = [('expected_price','CHECK(expected_price >= 0)','The Expected price Must be Positive'),
                        ('selling_price','CHECK(selling_price >= 0)','The Selling price Must be Positive')
                        ]

    @api.constrains ("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError ("The selling price must be greater than the expected price")

    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area + record.garden_area

    @api.depends('offer_id.price')
    def _compute_price(self):
        for record in self:
            if record.offer_id:
                record.best_price = max(record.offer_id.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:

            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = ''

    def sold_property(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
                return True
            else:
                raise UserError("This property is already Canceled")
                return False

    # def sold_function(self):
    #     for record in self:
    #         if record.state == 'canceled':
    #             raise UserError("This property is canceled")
    #         record.state= "sold"
    #

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
                return True
            else:
                raise UserError("This property is already Sold")

    @api.ondelete(at_uninstall=True)
    def _unlink(self):
        if self.state in ('new','canceled'):
            raise UserError(f"you cannot delete property with state {self.state} ")
        # else:
        #     return True

    # def unlink(self):
    #     if self.state not in ('new','canceled'):
    #         raise UserError("you cannot delete property with state {self.state} ")
    #     else:
    #         return True


    # def cancel_function(self):
    #     for record in self:
    #         if record.state == 'sold':
    #             raise UserError("This property is Sold")
    #         record.state= "canceled"






