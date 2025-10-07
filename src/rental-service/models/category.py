from odoo import fields, models

class Category(models.Model):
     _name = 'service.category'
     _description = 'Category Model'

     name = fields.Char(string='Name', required=True)
     product_ids = fields.One2many('service.product', string='Product', required=True)