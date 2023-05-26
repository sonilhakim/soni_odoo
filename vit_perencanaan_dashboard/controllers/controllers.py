# -*- coding: utf-8 -*-
from odoo import http

# class VitAnggaranDashboard(http.Controller):
#     @http.route('/vit_perencanaan_dashboard/vit_perencanaan_dashboard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_perencanaan_dashboard/vit_perencanaan_dashboard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_perencanaan_dashboard.listing', {
#             'root': '/vit_perencanaan_dashboard/vit_perencanaan_dashboard',
#             'objects': http.request.env['vit_perencanaan_dashboard.vit_perencanaan_dashboard'].search([]),
#         })

#     @http.route('/vit_perencanaan_dashboard/vit_perencanaan_dashboard/objects/<model("vit_perencanaan_dashboard.vit_perencanaan_dashboard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_perencanaan_dashboard.object', {
#             'object': obj
#         })