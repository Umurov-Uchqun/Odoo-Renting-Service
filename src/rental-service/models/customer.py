from odoo import models, fields, api
from odoo.exceptions import ValidationError



class Customer(models.Model):
    _name = 'service.customer'
    _description = 'Service Customer'

    name = fields.Char('Customer Name', required=True)
    phone = fields.Char('Phone Number', required=True)
    email = fields.Char('Email Address', required=True)
    order_ids = fields.One2many('rental.order', string='Order')


    @api.constrains('phone')
    def _check_phone(self):
        for order in self:
            if not order.phone.isdigit():
                raise ValidationError('Phone number must be entered in the format: +999999999')

    @api.constrains('email')
    def _check_email(self):
        for order in self:
            domain = order.email.split('@')
            if len(domain) != 2 and domain[-1] != 'gmail.com':
                raise ValidationError('Email address must be entered in the format: ')
