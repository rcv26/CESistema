# -*- coding: utf-8 -*-
# from odoo import http


# class CeBase(http.Controller):
#     @http.route('/ce_base/ce_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ce_base/ce_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ce_base.listing', {
#             'root': '/ce_base/ce_base',
#             'objects': http.request.env['ce_base.ce_base'].search([]),
#         })

#     @http.route('/ce_base/ce_base/objects/<model("ce_base.ce_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ce_base.object', {
#             'object': obj
#         })
