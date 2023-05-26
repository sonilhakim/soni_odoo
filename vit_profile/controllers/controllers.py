# -*- coding: utf-8 -*-
from odoo import http

# class VitProfile(http.Controller):
#     @http.route('/vit_profile/vit_profile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_profile/vit_profile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_profile.listing', {
#             'root': '/vit_profile/vit_profile',
#             'objects': http.request.env['vit_profile.vit_profile'].search([]),
#         })

#     @http.route('/vit_profile/vit_profile/objects/<model("vit_profile.vit_profile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_profile.object', {
#             'object': obj
#         })