# -*- coding: utf-8 -*-
# from odoo import http


# class CeCallcenter(http.Controller):
#     @http.route('/ce_callcenter/ce_callcenter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ce_callcenter/ce_callcenter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ce_callcenter.listing', {
#             'root': '/ce_callcenter/ce_callcenter',
#             'objects': http.request.env['ce_callcenter.ce_callcenter'].search([]),
#         })

#     @http.route('/ce_callcenter/ce_callcenter/objects/<model("ce_callcenter.ce_callcenter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ce_callcenter.object', {
#             'object': obj
#         })
