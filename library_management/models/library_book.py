from email.policy import default

import datetime
from re import search

from build.lib.odoo.service.server import restart
from odoo import models, fields,api
from odoo.fields import Many2one

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Management Model"

    name = fields.Char(string='Name',required = True)
    isbn = fields.Integer(required = True)
    author_ids = fields.Many2many('library.author',required = True)
    aid = fields.One2many('library.author','book_ids',required = True)
    publication_date = fields.Date(default=datetime.date.today())
    price = fields.Float(required = True)
    book_quantity = fields.Float(required = True)
    total_books_price = fields.Integer(compute='_compute_BooksPrice')
    # author_of_book = fields.Many2one('library.author', string="Book Author")

    _sql_constraints = [
        ('check_isbn','UNIQUE(isbn)','ISBN Must be Unique'),
    ]

    @api.depends('price', 'book_quantity')
    def _compute_BooksPrice(self):
        for record in self:
            record.total_books_price=record.price*record.book_quantity


