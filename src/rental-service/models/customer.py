from odoo import models, fields, api


class Customer(models.Model):
    _name = 'service.customer'
    _description = 'Service Customer'

    name = fields.Char('Customer Name', required=True)
    phone = fields.Char('Phone Number', required=True)
    email = fields.Char('Email Address', required=True)
    order_ids = fields.One2many('rental.order', string='Order')