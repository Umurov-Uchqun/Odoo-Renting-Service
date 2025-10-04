from odoo import models, fields, api

class ProductPrice(models.Model):
    _name = "product.price"
    _description = "Product Price"

    product_id = fields.Many2one('service.product', string="Product")
    interval_number = fields.Integer("Interval Number")
    interval_type = fields.Selection(
        [
            ("hour", "Hour"),
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year")
        ], default="hour", required=True)

    hour = fields.Integer(compute="_compute_hour", store=True)

    price = fields.Float(string="Price", digits=0, required=True)

    @api.depends("interval_number", "interval_type")
    def _compute_hour(self):
        for record in self:
            if record.interval_type == "hour":
                hours = 1
            elif record.interval_type == "day":
                hours = 24
            elif record.interval_type == "week":
                hours = 168
            elif record.interval_type == "month":
                hours = 2 * 365
            else:
                hours = 24 * 365

            record.hour = record.interval_number * hours


    @api.model
    def get_min_rental_price(self, product_id, hours):
        rps = self.env["rental.price"].search([("product_id", "=", product_id), ("hour", "<=", hours)],
                                              order="hour asc")

        if not rps:
            return None

        return rps[-1]

    @api.model
    def get_max_rental_price(self, product_id, hours):
        rps = self.env["rental.price"].search([("product_id", "=", product_id), ("hour", ">=", hours)],
                                              order="hour asc")

        if not rps:
            return None

        return rps[0]

    @api.model
    def get_result_price(self, product_id, hours):
        min_rental_price = self.get_min_rental_price(product_id, hours)
        max_rental_price = self.get_max_rental_price(product_id, hours)

        price_by_min = min_rental_price.price * (hours / min_rental_price.hour)
        price_by_max = max_rental_price.price

        return min(price_by_min, price_by_max)

