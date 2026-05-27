# -*- coding: utf-8 -*-
# from odoo import http


# class CeCapacitacion(http.Controller):
#     @http.route('/ce_capacitacion/ce_capacitacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ce_capacitacion/ce_capacitacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ce_capacitacion.listing', {
#             'root': '/ce_capacitacion/ce_capacitacion',
#             'objects': http.request.env['ce_capacitacion.ce_capacitacion'].search([]),
#         })

#     @http.route('/ce_capacitacion/ce_capacitacion/objects/<model("ce_capacitacion.ce_capacitacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ce_capacitacion.object', {
#             'object': obj
#         })
