from email.policy import default

from build.lib.odoo.tools.safe_eval import datetime
from odoo import models,fields


class LibraryReservations(models.Model):
    _name = "library.reservations"
    _description = "Library Reservations"


    book_id = fields.Many2one('library.book')
    date_from =fields.Date()
    borrowing_period =fields.Integer()
    return_date =fields.Date(default=datetime.date.today())
    partner_id =fields.Many2one('res.partner')
    price = fields.Float()

