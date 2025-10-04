# -*- coding: utf-8 -*-
# from odoo import http


# class Rental-service(http.Controller):
#     @http.route('/rental-service/rental-service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rental-service/rental-service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rental-service.listing', {
#             'root': '/rental-service/rental-service',
#             'objects': http.request.env['rental-service.rental-service'].search([]),
#         })

#     @http.route('/rental-service/rental-service/objects/<model("rental-service.rental-service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rental-service.object', {
#             'object': obj
#         })

