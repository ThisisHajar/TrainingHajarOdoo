from odoo import models,fields


class SoldWizard (models.TransientModel):
    _name = "sold.wizard"
    _description = "Sold Wizard"

    selling_price = fields.Float(string="Selling Price")


    def action_sold(self):
        active_id = self.env.context.get('active_id')
        # take id of model I am in then get model I am in then the record that I am in then I can edit anything in this record I am in
        active_model = self.env.context.get('active_model')
        record = self.env[active_model].browse(active_id)
         # this wizard I can use anywhere

        record.selling_price = self.selling_price
        record.state = 'sold'