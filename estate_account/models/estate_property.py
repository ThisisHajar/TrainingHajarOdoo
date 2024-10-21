

from odoo import fields, models, api, Command
import logging


from odoo.addons.test_impex.tests.test_load import values


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        result = super().sold_property()
        # sold.propert() we override this function from estate.property models inside estate modules
        logging.error("*******************")
        logging.error("test override")
        #     we override here
        #  create invoice as required (ex in ch 13) sold any property will create new invoice (record = object from class)  in invoicing module
        values = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': 'Property Sale - 0.06%',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'administrative fees',
                    'quantity': 1,
                    'price_unit': 100
                })
            ]
        }
        self.env['account.move'].create(values)

        return result


