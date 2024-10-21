from email.policy import default

from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required = True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order types")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [('name', 'UNIQUE(name)', 'Name Must be Unique'),]



