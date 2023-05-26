# -*- coding: utf-8 -*-
from odoo import http

# class VitAnggaran(http.Controller):
#     @http.route('/vit_anggaran/vit_anggaran/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_anggaran/vit_anggaran/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_anggaran.listing', {
#             'root': '/vit_anggaran/vit_anggaran',
#             'objects': http.request.env['vit_anggaran.vit_anggaran'].search([]),
#         })

#     @http.route('/vit_anggaran/vit_anggaran/objects/<model("vit_anggaran.vit_anggaran"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_anggaran.object', {
#             'object': obj
#         })