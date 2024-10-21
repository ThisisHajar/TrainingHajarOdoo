# from email.policy import default
# from pkg_resources import require
from build.lib.odoo.tools.view_validation import validate
# from build.lib.odoo.tools.populate import compute
from odoo import models, fields, api, exceptions
from build.lib.odoo.tools.safe_eval import datetime
from odoo import models, fields
from odoo.fields import Many2one
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')])

    partner_id = Many2one("res.partner")
    property_id = Many2one("estate.property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute= '_compute_date_deadline', readonly=False)
    property_type_id = fields.Many2one("estate.property.type", string="property type", related="property_id.property_type_id", store=True)



    _sql_constraints = [('price','CHECK(price >= 0)','The price Must be Positive')]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validity)


    # def _inverse_date_deadline(self):
    #     for record in self:
    #         if record.create_date:
    #         record.validity = (record.date_deadline - record.create_date.date()).days
    #         else:
    #         record.validity = record.date_deadline - datetime.now().date()

    def accepted_action(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("This offer is Refused")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_accepted'


    def refused_action(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("This offer is Accepted")
            record.status = 'refused'


    @api.model
    def create(self,vals):
        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        # define array to add price
        list_price= []
        # check all offers in property and add them in list price array
        # then max price give me higher price
        for i in self.env['estate.property'].browse(vals['property_id']).offer_id:
            list_price.append(i.price)

        max_price = 0
        # >1 if there is no offer on this house it will not ask
        if len(list_price) >= 1:
            max_price = max(list_price)
        # logging to see where is the problem
        logging.error("*************")
        logging.error(max_price)
        logging.error(list_price)
        # if current price that I try to save is > maximum house price raise error
        if self.price < max_price:
                raise ValidationError("you can not add offer less than offers")
        # self.env['estate.property'].browse(vals['property_id']).offer_id

        return super(EstatePropertyOffer, self).create(vals)


    # @api.constrains('price')
    # def _check_price(self):
    #     for record in self:
    #         if record.price <= 0:
    #             raise ValidationError("PRICE cannot be less than 0")
    #



    # @api.constrains ("price")
    # def _check_price(self):
    #     for record in self:
    #         if record.price > 0:
    #             raise ValidationError ("The price must be positive")
