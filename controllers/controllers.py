# -*- coding: utf-8 -*-
from odoo import http

# class MethodLtdc(http.Controller):
#     @http.route('/method_ltdc/method_ltdc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_ltdc/method_ltdc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_ltdc.listing', {
#             'root': '/method_ltdc/method_ltdc',
#             'objects': http.request.env['method_ltdc.method_ltdc'].search([]),
#         })

#     @http.route('/method_ltdc/method_ltdc/objects/<model("method_ltdc.method_ltdc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_ltdc.object', {
#             'object': obj
#         })