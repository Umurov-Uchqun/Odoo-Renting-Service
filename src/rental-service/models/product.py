from dateutil.utils import today
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = 'service.product'
    _description = 'Product Model'

    name = fields.Char('Product Name', required=True)

    availability = fields.Char('Product Availability', compute='_compute_availability')
    broken = fields.Boolean(default=False)
    future_availability_date = fields.Datetime('Future Availability Date', compute='_compute_future_availability')

    category_id = fields.Many2one("service.category", string="Category")
    rental_price_ids = fields.One2many('product.price', 'product_id')
    orders_ids = fields.One2many('rental.order', 'product_id')

    @api.depends('orders_ids.start_date', 'orders_ids.end_date')
    def _compute_availability(self):
        today = fields.Date.today()
        for record in self:
            orders = self.env['service.product'].search([('product_id', '=', record.id)])
            record.is_available = True
            for order in orders:
                if order.start_date <= today <= order.end_date:
                    record.is_available = False
                    break

    @api.depends('orders_ids')
    def _compute_future_availability(self):
        for order in self:
            if order.orders_status == 'confirmed':
                future_availability_date = order.end_date
            else:
                future_availability_date = order.today()

            order.future_availability_date = future_availability_date


    @api.constrains('broken')
    def _check_broken(self):
        for order in self:
            if order.broken:
                raise ValidationError('Product is not available')
