# -*- coding: utf-8 -*-
from odoo import http

# class VitAssetBmn(http.Controller):
#     @http.route('/vit_asset_bmn/vit_asset_bmn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_asset_bmn/vit_asset_bmn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_asset_bmn.listing', {
#             'root': '/vit_asset_bmn/vit_asset_bmn',
#             'objects': http.request.env['vit_asset_bmn.vit_asset_bmn'].search([]),
#         })

#     @http.route('/vit_asset_bmn/vit_asset_bmn/objects/<model("vit_asset_bmn.vit_asset_bmn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_asset_bmn.object', {
#             'object': obj
#         })