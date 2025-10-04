from dateutil.utils import today
from odoo import models, fields, api

class Product(models.Model):
    _name = 'service.product'
    _description = 'Product Model'

    name = fields.Char('Product Name', required=True)
    availability = fields.Char('Product Availability', compute='_compute_availability')
    broken = fields.Boolean(default=False)
    future_availability_date = fields.Datetime('Future Availability Date', compute='_compute_future_availability')
    category_id = fields.Many2one("service.category", string="Category")
    rental_prices_ids = fields.One2many('product.price', 'product_id')
    orders_ids = fields.One2many('rental.order', 'product_id')


    @api.depends('orders_ids')
    def _compute_availability(self):
        for order in self:
            if order.orders_status == 'confirmed':
                availability = 'rented'
            else:
                availability = 'available'

            order.availability = availability

    @api.depends('orders_ids')
    def _compute_future_availability(self):
        for order in self:
            if order.orders_status == 'confirmed':
                future_availability_date = order.end_date
            else:
                future_availability_date = order.today


