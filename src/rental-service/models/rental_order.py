from odoo import models, fields, api

class Order(models.Model):
    _name = 'rental.order'
    _description = 'Rental Order'

    name = fields.Char('Order Name', required=True)
    customer_id = fields.Many2one('service.customer', string='Customer')
    product_id = fields.Many2one('service.product', string='Product')
    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    returned_date = fields.Datetime('Returned Date', required=True)
    duration = fields.Integer('Duration',compute = '_compute_duration')
    human_readability = fields.Char('Human Readable Readability', compute='_compute_human_readability')
    total_price = fields.Float('Total Price', compute='_compute_total_price')
    complete_price = fields.Float('Complete Price', compute='_compute_complete_price')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')
    ],default = 'draft')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for order in self:
            if order.start_date < order.end_date:
                order.duration = order.end_date - order.start_date
            else:
                order.duration = 0

    @api.depends('duration')
    def _compute_human_readability(self):
        for record in self:
            years = record.duration // (365*24)
            last_year_duration = record.duration - years * 365 * 24
            months = last_year_duration / (365*2)
            last_month_duration = last_year_duration - months * 365 * 2
            days = last_month_duration / 24
            last_hours = last_month_duration - days * 24

            result = []
            if years > 0:
                result.append(f'{years} years')
            elif months > 0:
                result.append(f'{months} months')
            elif days > 0:
                result.append(f'{days} days')
            else:
                result.append(f'{last_hours} hours')

    @api.depends('start_date', 'end_date', 'product_id')
    def _compute_total_price(self):
        for order in self:
            pass