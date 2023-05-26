# -*- coding: utf-8 -*-
from odoo import http

# class VitBilyetGiro(http.Controller):
#     @http.route('/vit_bilyet_giro/vit_bilyet_giro/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_bilyet_giro/vit_bilyet_giro/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_bilyet_giro.listing', {
#             'root': '/vit_bilyet_giro/vit_bilyet_giro',
#             'objects': http.request.env['vit_bilyet_giro.vit_bilyet_giro'].search([]),
#         })

#     @http.route('/vit_bilyet_giro/vit_bilyet_giro/objects/<model("vit_bilyet_giro.vit_bilyet_giro"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_bilyet_giro.object', {
#             'object': obj
#         })