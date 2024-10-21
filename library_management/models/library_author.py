from build.lib.odoo.tools.populate import compute
from odoo import models, fields
from odoo.fields import Many2one


class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "Library Author"


    name = fields.Char(string='Name',required = True)
    birth_date = fields.Date(required = True)
    bid = fields.One2many('library.book','aid',required = True)
    book_ids = fields.Many2many("library.book", string='Book Name',required = True)
    # author_id = fields.Integer()
    # book_author = fields.Many2one("library.book",string='Book Name')
    # author_of_books = fields.One2many('library.book','author_of_book',string='Author for Many Books Relation')
    total_books = fields.Integer(compute='_compute_totalBooks')

    def _compute_totalBooks(self):
        for record in self:
            if len(self.book_ids) == 0:
                record.total_books = 0
            else:
                record.total_books = len(self.book_ids)

                # to access all records and to compute the record I am in (self is record of set)



