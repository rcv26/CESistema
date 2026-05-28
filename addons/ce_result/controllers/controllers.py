# -*- coding: utf-8 -*-
# from odoo import http


# class CeResult(http.Controller):
#     @http.route('/ce_result/ce_result/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ce_result/ce_result/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ce_result.listing', {
#             'root': '/ce_result/ce_result',
#             'objects': http.request.env['ce_result.ce_result'].search([]),
#         })

#     @http.route('/ce_result/ce_result/objects/<model("ce_result.ce_result"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ce_result.object', {
#             'object': obj
#         })
